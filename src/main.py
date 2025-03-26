#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@description: 图片去水印工具主程序
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
from ui.main_window import MainWindow

def load_stylesheet(app):
    """
    加载 QSS 样式表
    """
    style_file = QFile(os.path.join(os.path.dirname(__file__), 'ui/styles.qss'))
    if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(style_file)
        app.setStyleSheet(stream.readAll())
        style_file.close()

def main():
    """
    主程序入口
    """
    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 