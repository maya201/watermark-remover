# 图片去水印工具 (Image Watermark Remover)

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

## 使用说明
1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行程序：
```bash
python src/main.py
```

3. 使用步骤：
   - 点击"选择文件夹"按钮选择需要处理的图片文件夹
   - 点击"开始处理"按钮
   - 等待处理完成

## 注意事项
- 处理过程中请勿关闭程序
- 建议在处理前备份重要图片

## 水印去除算法说明
- 默认处理图片右下角区域（下方20%，右侧30%的区域）
- 检测颜色范围在 [200,200,200] 到 [250,250,250] 之间的区域作为水印
- 使用 OpenCV 的 TELEA 算法进行图像修复

## 下载和安装
### Windows 用户
1. 下载 `图片去水印工具.exe`
2. 双击运行即可

### Mac 用户
1. 下载 `图片去水印工具.app`
2. 将应用拖入应用程序文件夹
3. 首次运行时右键点击应用图标，选择"打开"

## 开发者说明
如果您想参与开发，可以按照以下步骤设置开发环境：

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
python src/main.py
```