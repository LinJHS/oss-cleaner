<div align="center">

<img src="img/logo.jpg" width="80%" alt="oss-cleaner">

<br>

[![PyPI version](https://img.shields.io/pypi/v/oss-cleaner.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/oss-cleaner/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/oss-cleaner.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/oss-cleaner/)
[![Build Status](https://github.com/LinJHS/oss-cleaner/actions/workflows/publish.yml/badge.svg)](https://github.com/LinJHS/oss-cleaner/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/oss-cleaner.svg?style=flat-square&logo=python&logoColor=white)](https://pypi.org/project/oss-cleaner/)
[![License](https://img.shields.io/github/license/LinJHS/oss-cleaner.svg?style=flat-square)](https://github.com/LinJHS/oss-cleaner/blob/main/LICENSE)

**A tool for managing and cleaning "orphan" images in Aliyun OSS, designed for Markdown note users.**

[Chinese Version](README.md) | [Features](#-key-features) • [Installation](#-installation--run) • [Usage](#-quick-start-pip-users)

</div>

It scans your local Markdown folder, analyzes all referenced image links, and compares them with files in your Aliyun OSS bucket. Any OSS images not used in your local Markdown files are identified as "orphaned." You can easily view and batch delete them via a Web UI, saving storage space and costs.

## ✨ Key Features

*   **Smart Scanning**: Automatically recursively scans all `.md` files in a specified directory.
*   **Precise Matching**: Extracts OSS image links from Markdown and compares them with cloud data.
*   **Visual Management**: Provides an intuitive Web UI to display the list of orphaned images.
*   **Batch Cleaning**: Supports one-click batch deletion of unused images.
*   **Easy Configuration**: Supports easy path configuration via Web UI or folder selector.

## 📦 Installation & Run

### Method 1: Download Executable (Recommended)

No Python environment required. Simply download and run the executable for your OS.

1.  Go to [Releases Page](https://github.com/LinJHS/oss-cleaner/releases) and download the latest version:
    *   **Windows**: Download `oss-cleaner-win.exe`
    *   **macOS**: Download `oss-cleaner-mac`
    *   **Linux**: Download `oss-cleaner-linux`
2.  **Run the application**:
    *   **Windows**: Double-click `oss-cleaner-win.exe`.
    *   **macOS/Linux**: Grant execution permission and run in terminal:
        ```bash
        chmod +x oss-cleaner-mac  # or oss-cleaner-linux
        ./oss-cleaner-mac
        ```
    *   The browser will automatically open [http://localhost:6900](http://localhost:6900) after startup.

### Method 2: Install via pip

If you have Python installed:

```bash
pip install oss-cleaner
```

Or install from source (development mode):

```bash
git clone https://github.com/LinJHS/oss-cleaner.git
cd oss-cleaner
pip install -e .
```

## 🚀 Quick Start (pip users)

1.  **Start the Service**

    After installation, run the following command in your terminal to start the Web service (browser opens automatically by default):

    ```bash
    python -m oss_cleaner
    ```

    **Command Line Arguments:**

    *   `--port <port>`: Specify the port to run on (default: 6900)
    *   `--no-browser`: Do not open the browser automatically
    *   `--debug`: Run in debug mode

    Example:
    ```bash
    python -m oss_cleaner --port 8080 --no-browser
    ```

2.  **Access the UI**

    Open your browser and visit [http://localhost:6900](http://localhost:6900).

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

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
