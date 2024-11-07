# -*- coding: utf-8 -*-
import os  
from PIL import Image, ImageDraw, ImageFont  
  
def add_page_numbers_to_images(input_folder, output_folder, start_number=1, font_path=None, font_size=36, margin=20):  
    # 如果输出文件夹不存在，则创建它  
    if not os.path.exists(output_folder):  
        os.makedirs(output_folder)  
  
    # 加载字体（可选，如果未指定则使用默认字体）  
    if font_path:  
        font = ImageFont.truetype(font_path, font_size)  
    else:  
        # 注意：默认字体可能不支持中文，如果需要支持中文请指定一个支持中文的字体文件  
        font = ImageFont.load_default()  
  
    # 获取输入文件夹中的所有JPG文件  
    jpg_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.jpg')]  
    jpg_files.sort()  # 按文件名排序（这通常意味着按升序，但取决于文件名的命名规则）  
  
    # 遍历JPG文件并添加页码  
    for idx, filename in enumerate(jpg_files, start=start_number):  
        # 构建完整的文件路径  
        input_path = os.path.join(input_folder, filename)  
        output_path = os.path.join(output_folder, f"page_{idx}.jpg")  
  
        # 打开图像  
        with Image.open(input_path) as img:  
            # 创建一个可以在图像上绘制的对象  
            draw = ImageDraw.Draw(img)  
  
            # 获取图像的尺寸  
            img_width, img_height = img.size  
  
            # 使用 draw.textsize 方法来获取文本大小  
            text_size = draw.textsize(str(idx), font=font)  
  
            # 计算页码文本的位置（右下角），并预留指定的边距  
            text_position = (img_width - margin - text_size[0], img_height - margin - text_size[1])  
  
            # 在图像上绘制页码文本  
            draw.text(text_position, str(idx), fill=(0, 0, 0), font=font)  # 黑色文本  
  
            # 保存处理后的图像  
            img.save(output_path)  
  
    print(f"Processed {len(jpg_files)} images and saved them to {output_folder}")  
  
# 使用示例  
input_folder = r"E:\hffg\test"  # 替换为你的输入文件夹路径  
output_folder = r"E:\hffg\test1"  # 替换为你的输出文件夹路径  
# 可选：指定字体路径和大小（如果需要支持中文，请确保字体文件支持中文）  
# font_path = r"C:\Windows\Fonts\msyh.ttc"  # Windows系统上的微软雅黑字体路径示例（支持中文）  
# add_page_numbers_to_images(input_folder, output_folder, start_number=1, font_path=font_path, font_size=36)  
# 如果不指定字体路径，则使用默认字体（可能不支持中文）  
add_page_numbers_to_images(input_folder, output_folder)