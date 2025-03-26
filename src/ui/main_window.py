#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@description: 主窗口界面
"""

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                           QLineEdit, QProgressBar, QLabel, QFileDialog,
                           QMessageBox, QTextEdit, QScrollBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from core.remover import WatermarkRemover

class WorkerThread(QThread):
    """
    工作线程，用于处理图片去水印
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    log = pyqtSignal(str)  # 新增日志信号

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.remover = WatermarkRemover()

    def run(self):
        try:
            total_files = 0
            processed_files = 0
            
            # 统计需要处理的文件总数
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        total_files += 1
            
            if total_files == 0:
                self.error.emit("所选文件夹中没有找到图片文件！")
                return

            self.log.emit(f"找到 {total_files} 个图片文件待处理")
            
            # 处理图片
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        file_path = os.path.join(root, file)
                        try:
                            self.log.emit(f"正在处理: {file}")
                            self.remover.process_image(file_path)
                            processed_files += 1
                            progress = int((processed_files / total_files) * 100)
                            self.progress.emit(progress)
                            self.log.emit(f"处理完成: {file}")
                        except Exception as e:
                            self.log.emit(f"处理失败: {file}, 错误: {str(e)}")
            
            self.progress.emit(100)  # 确保进度条到达100%
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        初始化用户界面
        """
        self.setWindowTitle('图片去水印工具')
        self.setMinimumSize(800, 600)  # 增加窗口大小以适应日志区域

        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # 创建文件夹选择相关控件
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText('请选择需要处理的图片文件夹...')
        self.path_input.setReadOnly(True)

        select_button = QPushButton('选择文件夹')
        select_button.clicked.connect(self.select_folder)

        # 创建进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建状态标签
        self.status_label = QLabel('准备就绪')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建日志显示区域
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMinimumHeight(300)
        self.log_display.setStyleSheet("background-color: #f8f8f8; font-family: monospace;")

        # 创建开始按钮
        self.start_button = QPushButton('开始处理')
        self.start_button.clicked.connect(self.start_processing)
        self.start_button.setEnabled(False)

        # 添加控件到布局
        layout.addWidget(self.path_input)
        layout.addWidget(select_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        layout.addWidget(QLabel('处理日志:'))  # 日志区域标题
        layout.addWidget(self.log_display)
        layout.addWidget(self.start_button)

        # 初始化工作线程
        self.worker = None

    def add_log(self, message):
        """
        添加日志信息
        """
        self.log_display.append(message)
        # 滚动到底部
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def select_folder(self):
        """
        选择文件夹
        """
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if folder_path:
            self.path_input.setText(folder_path)
            self.start_button.setEnabled(True)
            self.add_log(f"已选择文件夹: {folder_path}")

    def start_processing(self):
        """
        开始处理图片
        """
        folder_path = self.path_input.text()
        if not folder_path:
            QMessageBox.warning(self, '警告', '请先选择文件夹！')
            return

        self.start_button.setEnabled(False)
        self.status_label.setText('正在处理...')
        self.progress_bar.setValue(0)
        self.log_display.clear()
        self.add_log("开始处理图片...")

        # 创建并启动工作线程
        self.worker = WorkerThread(folder_path)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.process_finished)
        self.worker.error.connect(self.process_error)
        self.worker.log.connect(self.add_log)  # 连接日志信号
        self.worker.start()

    def update_progress(self, value):
        """
        更新进度条
        """
        self.progress_bar.setValue(value)

    def process_finished(self):
        """
        处理完成
        """
        self.progress_bar.setValue(100)  # 确保进度条到达100%
        self.status_label.setText('处理完成！')
        self.start_button.setEnabled(True)
        self.add_log("所有图片处理完成！")
        QMessageBox.information(self, '完成', '所有图片处理完成！')

    def process_error(self, error_message):
        """
        处理错误
        """
        self.status_label.setText('处理出错')
        self.start_button.setEnabled(True)
        self.add_log(f"错误: {error_message}")
        QMessageBox.critical(self, '错误', f'处理过程中出错：{error_message}')