import os
import re
import oss2
from flask import Flask, render_template, request, jsonify
from .config_manager import AppConfig

app = Flask(__name__)

# Initialize Config
cfg = AppConfig()

def get_oss_url_pattern():
    return re.compile(
        rf'https://{cfg.get("OSS_DOMAIN")}/{cfg.get("PREFIX")}([^\)\s\?]+)')


def get_oss_bucket():
    auth = oss2.Auth(cfg.get_secret("ACCESS_KEY_ID"), cfg.get_secret("ACCESS_KEY_SECRET"))
    return oss2.Bucket(auth, cfg.get("ENDPOINT"), cfg.get("BUCKET_NAME"))


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
        return f"错误: {str(e)}"


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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
