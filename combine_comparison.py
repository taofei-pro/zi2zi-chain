#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
组合不同检查点生成的图像进行比较
"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def combine_images(checkpoints, base_dir, output_path):
    """
    将不同检查点生成的图像组合在一起进行比较
    
    Args:
        checkpoints: 检查点列表
        base_dir: 基础目录
        output_path: 输出路径
    """
    # 创建输出目录
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 获取第一个检查点的图像列表
    first_checkpoint_dir = os.path.join(base_dir, f"compare_{checkpoints[0]}/0")
    image_files = sorted([f for f in os.listdir(first_checkpoint_dir) if f.endswith('.png')])
    
    # 加载第一张图像以获取尺寸
    first_image = Image.open(os.path.join(first_checkpoint_dir, image_files[0]))
    img_width, img_height = first_image.size
    
    # 创建组合图像
    num_images = len(image_files)
    num_checkpoints = len(checkpoints)
    
    # 添加标题和间距
    title_height = 30
    padding = 10
    
    # 计算组合图像的尺寸
    combined_width = num_images * img_width + (num_images + 1) * padding
    combined_height = num_checkpoints * img_height + (num_checkpoints + 1) * padding + title_height
    
    # 创建空白图像
    combined_image = Image.new('RGB', (combined_width, combined_height), color='white')
    draw = ImageDraw.Draw(combined_image)
    
    # 尝试加载字体，如果失败则使用默认字体
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    # 绘制标题
    title_text = "字体生成比较：不同检查点的效果"
    title_width = draw.textlength(title_text, font=font)
    draw.text(((combined_width - title_width) // 2, padding), title_text, fill='black', font=font)
    
    # 绘制列标题（图像编号）
    for i, img_file in enumerate(image_files):
        col_title = f"图像 {i+1}"
        col_width = draw.textlength(col_title, font=font)
        x = padding + i * (img_width + padding) + (img_width - col_width) // 2
        draw.text((x, title_height), col_title, fill='black', font=font)
    
    # 粘贴图像
    for i, checkpoint in enumerate(checkpoints):
        # 绘制行标题（检查点）
        row_title = f"检查点 {checkpoint}"
        row_width = draw.textlength(row_title, font=font)
        y = title_height + padding + i * (img_height + padding) + img_height // 2
        draw.text((padding, y), row_title, fill='black', font=font)
        
        checkpoint_dir = os.path.join(base_dir, f"compare_{checkpoint}/0")
        
        for j, img_file in enumerate(image_files):
            img_path = os.path.join(checkpoint_dir, img_file)
            if os.path.exists(img_path):
                img = Image.open(img_path)
                x = padding + (j + 1) * padding + j * img_width
                y = title_height + padding + (i + 1) * padding + i * img_height
                combined_image.paste(img, (x, y))
    
    # 保存组合图像
    combined_image.save(output_path)
    print(f"组合图像已保存到: {output_path}")

if __name__ == "__main__":
    base_dir = "/home/zihun/workspace/zi2zi-chain/experiment_long"
    output_dir = "/home/zihun/workspace/zi2zi-chain/experiment_long/comparison"
    os.makedirs(output_dir, exist_ok=True)
    
    # 检查点列表
    checkpoints = ["1000", "3000", "5000", "5900"]
    
    # 组合图像
    output_path = os.path.join(output_dir, "comparison_nihao.png")
    combine_images(checkpoints, base_dir, output_path)
