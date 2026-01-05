# oss-cleaner

[中文](./README.md)

![PyPI - Version](https://img.shields.io/pypi/v/oss-cleaner)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oss-cleaner)
![License](https://img.shields.io/github/license/yourusername/oss-cleaner)

**oss-cleaner** is a tool designed for Markdown users to manage and clean orphaned images stored in Aliyun OSS.

It scans your local Markdown folder, analyzes all referenced image links, and compares them with files in your Aliyun OSS bucket. Any OSS images not used in your local Markdown files are identified as "orphaned." You can easily view and batch delete them via a Web UI, saving storage space and costs.

## ✨ Key Features

*   **Smart Scanning**: Automatically recursively scans all `.md` files in a specified directory.
*   **Precise Matching**: Extracts OSS image links from Markdown and compares them with cloud data.
*   **Visual Management**: Provides an intuitive Web UI to display the list of orphaned images.
*   **Batch Cleaning**: Supports one-click batch deletion of unused images.
*   **Easy Configuration**: Supports easy path configuration via Web UI or folder selector.

## 📦 Installation

Install via `pip`:

```bash
pip install oss-cleaner
```

Or install from source (development mode):

```bash
git clone https://github.com/yourusername/oss-cleaner.git
cd oss-cleaner
pip install -e .
```

## 🚀 Quick Start

1.  **Start the Service**

    After installation, run the following command in your terminal to start the Web service:

    ```bash
    python -m oss_cleaner
    ```

2.  **Access the UI**

    Open your browser and visit [http://localhost:5000](http://localhost:5000).

3.  **Configuration**

    On the first run, you need to configure the following information (can be set via the configuration button on the UI):
    *   **OSS Domain**: Your OSS custom domain or default domain (e.g., `oss-cn-hangzhou.aliyuncs.com`).
    *   **Prefix**: The directory prefix for image storage (e.g., `images/`).
    *   **Access Key ID & Secret**: Aliyun Access Keys.
    *   **Endpoint**: OSS Region Endpoint (e.g., `oss-cn-hangzhou.aliyuncs.com`).
    *   **Bucket Name**: The name of your bucket.
    *   **Markdown Path**: The root directory of your local Markdown notes.

4.  **Clean Images**

    After configuration, refresh the home page. The system will list all unreferenced images. Select the images you want to delete and click the "Delete" button.

## ⚙️ Configuration

The configuration file is stored by default in `.config/oss-cleaner/settings.json` (Linux/macOS) or `AppData/Roaming/oss-cleaner/settings.json` (Windows) under your user directory.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
