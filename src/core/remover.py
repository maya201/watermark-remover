#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@description: 水印去除核心功能
"""

import cv2
import numpy as np
from PIL import Image
import os

class WatermarkRemover:
    """
    水印去除器类
    """
    def __init__(self):
        """
        初始化水印去除器
        """
        # 水印检测的颜色范围
        self.lower_bound = np.array([200, 200, 200])
        self.upper_bound = np.array([250, 250, 250])
        
        # 膨胀操作的核大小
        self.kernel_size = (3, 3)
        self.kernel = np.ones(self.kernel_size, np.uint8)
        
        # 修复算法的参数
        self.inpaint_radius = 5

    def process_image(self, image_path):
        """
        处理单个图片
        
        Args:
            image_path: 图片路径
        """
        # 读取图片
        img = cv2.imread(image_path, 1)
        if img is None:
            raise Exception(f"无法读取图片：{image_path}")

        height, width = img.shape[:2]
        
        # 处理右下角区域（假设水印在右下角）
        roi_height = int(height * 0.2)  # 下方20%
        roi_width = int(width * 0.3)    # 右侧30%
        
        # 提取感兴趣区域(ROI)
        roi = img[height-roi_height:height, width-roi_width:width]
        
        # 在ROI中检测水印
        mask = cv2.inRange(roi, self.lower_bound, self.upper_bound)
        
        # 如果没有检测到水印（白色像素），直接返回
        if cv2.countNonZero(mask) == 0:
            return
        
        # 扩展待修复区域
        mask = cv2.dilate(mask, self.kernel, iterations=10)
        
        # 使用修复算法
        result = cv2.inpaint(roi, mask, self.inpaint_radius, cv2.INPAINT_TELEA)
        
        # 将处理后的区域放回原图
        img[height-roi_height:height, width-roi_width:width] = result
        
        # 保存处理后的图片
        cv2.imwrite(image_path, img)

    def _create_backup(self, image_path):
        """
        创建图片备份
        
        Args:
            image_path: 原图片路径
        Returns:
            backup_path: 备份文件路径
        """
        backup_dir = os.path.join(os.path.dirname(image_path), 'backup')
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_path = os.path.join(backup_dir, os.path.basename(image_path))
        if not os.path.exists(backup_path):
            with open(image_path, 'rb') as src, open(backup_path, 'wb') as dst:
                dst.write(src.read())
        
        return backup_path