import os
import re
import oss2
from flask import Flask, render_template, request, jsonify
from .config_manager import AppConfig

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

app = Flask(__name__)

# Inject version into all templates
@app.context_processor
def inject_version():
    return dict(version=__version__)

# Initialize Config
cfg = AppConfig()

def get_oss_url_pattern():
    domain = cfg.get("OSS_DOMAIN")
    prefix = cfg.get("PREFIX")
    if not domain or not prefix:
        raise ValueError("请先配置 OSS_DOMAIN 和 PREFIX")
    return re.compile(
        rf'https://{domain}/{prefix}([^\)\s\?]+)')


def get_oss_bucket():
    ak_id = cfg.get_secret("ACCESS_KEY_ID")
    ak_secret = cfg.get_secret("ACCESS_KEY_SECRET")
    endpoint = cfg.get("ENDPOINT")
    bucket_name = cfg.get("BUCKET_NAME")

    if not all([ak_id, ak_secret, endpoint, bucket_name]):
        raise ValueError("请先在配置页面设置 OSS 相关信息 (Access Key, Endpoint, Bucket)")

    auth = oss2.Auth(ak_id, ak_secret)
    return oss2.Bucket(auth, endpoint, bucket_name)


def get_local_used_images():
    used_images = set()
    markdown_path = cfg.get("MARKDOWN_PATH")
    if not markdown_path or not os.path.exists(markdown_path):
        return set()
        
    for root, dirs, files in os.walk(markdown_path):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = get_oss_url_pattern().findall(content)
                    for m in matches:
                        used_images.add(m)
    return used_images


def get_oss_images():
    bucket = get_oss_bucket()
    oss_files = []
    prefix = cfg.get("PREFIX")
    oss_domain = cfg.get("OSS_DOMAIN")
    
    if not prefix:
        raise ValueError("请先配置 PREFIX")
    if not oss_domain:
        raise ValueError("请先配置 OSS_DOMAIN")

    for obj in oss2.ObjectIterator(bucket, prefix=prefix):
        if obj.key != prefix:
            filename = obj.key.replace(prefix, "")
            if filename:
                # 在后端直接组装完整的 URL，避免前端拼接出错
                full_url = f"https://{oss_domain}/{obj.key}"
                oss_files.append({
                    "name": filename,
                    "key": obj.key,
                    "url": full_url,  # 这里的 URL 将用于前端展示
                    "size": f"{obj.size / 1024:.2f} KB"
                })
    return oss_files


@app.route('/')
def index():
    try:
        used_set = get_local_used_images()
        all_oss_files = get_oss_images()
        orphans = [f for f in all_oss_files if f['name'] not in used_set]
        return render_template('index.html', orphans=orphans, count=len(orphans))
    except Exception as e:
        # 如果发生错误（如配置缺失），仍然渲染页面，但显示错误信息
        return render_template('index.html', orphans=[], count=0, error=str(e))


@app.route('/delete', methods=['POST'])
def delete_images():
    keys_to_delete = request.json.get('keys', [])
    if not keys_to_delete:
        return jsonify({"status": "error", "message": "未选择文件"})

    try:
        bucket = get_oss_bucket()
        # 阿里云支持批量删除
        result = bucket.batch_delete_objects(keys_to_delete)

        # 属性名从 deleted_objects 改为 deleted_keys
        return jsonify({"status": "success", "deleted": result.deleted_keys})

    except Exception as e:
        # 增加一个异常捕获，防止服务端报错导致前端没反应
        return jsonify({"status": "error", "message": str(e)})


@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        data = request.json
        # Update secrets
        if 'ACCESS_KEY_ID' in data:
            cfg.set_secret('ACCESS_KEY_ID', data['ACCESS_KEY_ID'])
        if 'ACCESS_KEY_SECRET' in data:
            cfg.set_secret('ACCESS_KEY_SECRET', data['ACCESS_KEY_SECRET'])
        
        # Update standard settings
        for key in ['ENDPOINT', 'BUCKET_NAME', 'OSS_DOMAIN', 'MARKDOWN_PATH', 'PREFIX']:
            if key in data:
                cfg.set(key, data[key])
        
        return jsonify({"status": "success"})
    
    # GET request - return current config
    return jsonify({
        "ACCESS_KEY_ID": cfg.get_secret("ACCESS_KEY_ID"),
        "ACCESS_KEY_SECRET": cfg.get_secret("ACCESS_KEY_SECRET"),
        "ENDPOINT": cfg.get("ENDPOINT"),
        "BUCKET_NAME": cfg.get("BUCKET_NAME"),
        "OSS_DOMAIN": cfg.get("OSS_DOMAIN"),
        "MARKDOWN_PATH": cfg.get("MARKDOWN_PATH"),
        "PREFIX": cfg.get("PREFIX")
    })


@app.route('/test-connection', methods=['POST'])
def test_connection():
    data = request.json
    ak_id = data.get('ACCESS_KEY_ID')
    ak_secret = data.get('ACCESS_KEY_SECRET')
    endpoint = data.get('ENDPOINT')
    bucket_name = data.get('BUCKET_NAME')

    if not all([ak_id, ak_secret, endpoint, bucket_name]):
        return jsonify({"status": "error", "message": "请填写完整的 OSS 配置信息"})

    try:
        auth = oss2.Auth(ak_id, ak_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        # 尝试获取 Bucket 信息来验证连接和权限
        bucket.get_bucket_info()
        return jsonify({"status": "success", "message": "连接成功！配置有效。"})
    except oss2.exceptions.OssError as e:
        return jsonify({"status": "error", "message": f"OSS 错误: {e.message} (Code: {e.code})"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"连接失败: {str(e)}"})


@app.route('/select-folder')
def select_folder():
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Create a hidden root window
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        # Open directory selection dialog
        folder_path = filedialog.askdirectory()
        
        # Destroy the root window
        root.destroy()
        
        if folder_path:
            # Normalize path separators
            folder_path = os.path.normpath(folder_path)
            return jsonify({"status": "success", "path": folder_path})
        else:
            return jsonify({"status": "cancelled"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=6900)
