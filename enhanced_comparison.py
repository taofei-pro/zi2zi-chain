#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建增强的比较图像，包括源字体和目标字体
"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse

def create_font_sample(text, font_path, font_size=210, canvas_size=256):
    """
    使用指定字体创建文本图像
    
    Args:
        text: 要渲染的文本
        font_path: 字体路径
        font_size: 字体大小
        canvas_size: 画布大小
    
    Returns:
        PIL Image对象
    """
    # 创建空白图像
    image = Image.new('L', (canvas_size, canvas_size), color=255)
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"无法加载字体: {font_path}")
        return image
    
    # 计算文本位置以居中
    try:
        # 新版PIL API
        text_width = draw.textlength(text, font=font)
        text_bbox = font.getbbox(text)
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        # 旧版PIL API
        text_width, text_height = draw.textsize(text, font=font)
    
    position = ((canvas_size - text_width) // 2, (canvas_size - text_height) // 2)
    
    # 绘制文本
    draw.text(position, text, font=font, fill=0)
    
    return image

def enhanced_comparison(src_font, dst_font, checkpoints, base_dir, output_path, text="你好世界"):
    """
    创建增强的比较图像，包括源字体和目标字体
    
    Args:
        src_font: 源字体路径
        dst_font: 目标字体路径
        checkpoints: 检查点列表
        base_dir: 基础目录
        output_path: 输出路径
        text: 要比较的文本
    """
    # 创建输出目录
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 获取第一个检查点的图像列表
    first_checkpoint_dir = os.path.join(base_dir, f"compare_{checkpoints[0]}/0")
    image_files = sorted([f for f in os.listdir(first_checkpoint_dir) if f.endswith('.png')])
    
    # 确保图像数量与文本长度匹配
    if len(image_files) != len(text):
        print(f"警告: 图像数量 ({len(image_files)}) 与文本长度 ({len(text)}) 不匹配")
    
    # 加载第一张图像以获取尺寸
    first_image = Image.open(os.path.join(first_checkpoint_dir, image_files[0]))
    img_width, img_height = first_image.size
    
    # 创建组合图像
    num_images = len(image_files)
    num_rows = len(checkpoints) + 2  # 源字体 + 目标字体 + 检查点
    
    # 添加标题和间距
    title_height = 40
    padding = 20
    row_label_width = 120
    
    # 计算组合图像的尺寸
    combined_width = row_label_width + num_images * img_width + (num_images + 1) * padding
    combined_height = num_rows * img_height + (num_rows + 1) * padding + title_height
    
    # 创建空白图像
    combined_image = Image.new('RGB', (combined_width, combined_height), color='white')
    draw = ImageDraw.Draw(combined_image)
    
    # 尝试加载字体，如果失败则使用默认字体
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except IOError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 绘制标题
    title_text = f"字体生成比较: {text}"
    title_width = draw.textlength(title_text, font=font)
    draw.text(((combined_width - title_width) // 2, padding), title_text, fill='black', font=font)
    
    # 绘制列标题（字符）
    for i, char in enumerate(text):
        col_title = char
        col_width = draw.textlength(col_title, font=font)
        x = row_label_width + padding + i * (img_width + padding) + (img_width - col_width) // 2
        draw.text((x, title_height + padding), col_title, fill='black', font=font)
    
    # 创建源字体和目标字体的样本
    for i, char in enumerate(text):
        # 源字体
        src_img = create_font_sample(char, src_font)
        x = row_label_width + padding + i * (img_width + padding)
        y = title_height + 2 * padding + img_height
        combined_image.paste(src_img, (x, y))
        
        # 目标字体
        dst_img = create_font_sample(char, dst_font)
        x = row_label_width + padding + i * (img_width + padding)
        y = title_height + 2 * padding + 2 * img_height + padding
        combined_image.paste(dst_img, (x, y))
    
    # 绘制行标题
    draw.text((padding, title_height + padding + img_height // 2), "源字体", fill='black', font=font)
    draw.text((padding, title_height + 2 * padding + img_height + img_height // 2), "目标字体", fill='black', font=font)
    
    # 粘贴生成的图像
    for i, checkpoint in enumerate(checkpoints):
        # 绘制行标题（检查点）
        row_title = f"检查点 {checkpoint}"
        y = title_height + 3 * padding + 2 * img_height + i * (img_height + padding) + img_height // 2
        draw.text((padding, y), row_title, fill='black', font=font)
        
        checkpoint_dir = os.path.join(base_dir, f"compare_{checkpoint}/0")
        
        for j, img_file in enumerate(image_files):
            if j >= len(text):
                break
                
            img_path = os.path.join(checkpoint_dir, img_file)
            if os.path.exists(img_path):
                img = Image.open(img_path)
                x = row_label_width + padding + j * (img_width + padding)
                y = title_height + 3 * padding + 2 * img_height + i * (img_height + padding)
                combined_image.paste(img, (x, y))
    
    # 保存组合图像
    combined_image.save(output_path)
    print(f"增强比较图像已保存到: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='创建增强的字体比较图像')
    parser.add_argument('--src_font', type=str, default='/home/zihun/workspace/zi2zi-chain/fonts/source/T1.ttf', help='源字体路径')
    parser.add_argument('--dst_font', type=str, default='/home/zihun/workspace/zi2zi-chain/fonts/target/M5.ttf', help='目标字体路径')
    parser.add_argument('--text', type=str, default='你好世界', help='要比较的文本')
    parser.add_argument('--output', type=str, default='/home/zihun/workspace/zi2zi-chain/experiment_long/comparison/enhanced_comparison.png', help='输出图像路径')
    
    args = parser.parse_args()
    
    base_dir = "/home/zihun/workspace/zi2zi-chain/experiment_long"
    output_dir = "/home/zihun/workspace/zi2zi-chain/experiment_long/comparison"
    os.makedirs(output_dir, exist_ok=True)
    
    # 检查点列表
    checkpoints = ["1000", "3000", "5000", "5900"]
    
    # 创建增强比较图像
    enhanced_comparison(
        args.src_font,
        args.dst_font,
        checkpoints,
        base_dir,
        args.output,
        args.text
    )
