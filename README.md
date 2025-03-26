# 图片去水印工具 (Image Watermark Remover)

![版本](https://img.shields.io/badge/版本-1.0-blue.svg)

## 项目简介
这是一个基于 Python 开发的跨平台(Mac/Windows)桌面应用程序，用于批量处理图片去除水印。该工具支持文件夹递归处理，界面简洁直观。

## 功能特点
- 跨平台支持 (Mac OS & Windows)
- 图形用户界面 (使用 PyQt6)
- 支持批量处理
- 支持子文件夹递归处理
- 支持多种图片格式 (jpg, png, jpeg, webp)
- 实时处理进度显示
- 保留原始图片的格式和名称
- 去水印后自动替换原始图片

## 技术架构
### 依赖库
- PyQt6: GUI界面开发
- Pillow: 图片处理
- opencv-python: 水印检测和去除
- numpy: 数据处理

### 项目结构
```
watermark-remover/
├── README.md                 # 项目说明文档
├── requirements.txt          # 项目依赖文件
└── src/                     # 源代码目录
    ├── main.py              # 主程序入口
    ├── watermark_remover.spec  # PyInstaller 打包配置
    ├── core/                # 核心功能包
    │   ├── __init__.py
    │   └── remover.py      # 水印去除核心实现
    ├── ui/                  # 用户界面包
    │   ├── __init__.py
    │   ├── main_window.py  # 主窗口界面
    │   └── styles.qss      # 界面样式表
    └── utils/              # 工具函数包
        └── __init__.py
```

## 使用说明
### 方式一：直接运行
1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行程序：
```bash
python src/main.py
```

### 方式二：使用打包版本
#### Windows 用户
1. 下载 `图片去水印工具.exe`
2. 双击运行即可

#### Mac 用户
1. 下载 `图片去水印工具.app`
2. 将应用拖入应用程序文件夹
3. 首次运行时右键点击应用图标，选择"打开"

### 使用步骤
1. 点击"选择文件夹"按钮选择需要处理的图片文件夹
2. 点击"开始处理"按钮
3. 等待处理完成

## 开发者指南
### 获取代码
1. 克隆仓库：
```bash
git clone https://github.com/maya201/watermark-remover.git
```

2. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate    # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行开发版本：
```bash
cd src
python main.py
```

### 打包程序
```bash
cd src
pyinstaller --clean watermark_remover.spec
```

打包后的程序将在 `src/dist` 目录下生成：
- macOS: `dist/图片去水印工具.app`
- Windows: `dist/图片去水印工具.exe`

## 水印去除算法说明
- 默认处理图片右下角区域（下方20%，右侧30%的区域）
- 检测颜色范围在 [200,200,200] 到 [250,250,250] 之间的区域作为水印
- 使用 OpenCV 的 TELEA 算法进行图像修复

## 注意事项
- 处理过程中请勿关闭程序
- 建议在处理前备份重要图片

## 版本历史
### v1.0 (2024-03-21)
- 初始版本发布
- 实现基本的水印去除功能
- 支持批量处理和递归处理
- 提供跨平台支持（Mac/Windows）