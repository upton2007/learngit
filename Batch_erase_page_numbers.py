# -*- coding: utf-8 -*-
import os  
from PIL import Image  
  
def erase_region(image_path, output_path, erase_box):  
    """  
    擦除JPG文件中指定区域的内容。  
  
    :param image_path: 输入JPG文件的路径  
    :param output_path: 输出处理后JPG文件的路径  
    :param erase_box: 要擦除的区域，格式为(left, upper, right, lower)  
    """  
    try:  
        # 打开图像  
        with Image.open(image_path) as img:  
            # 获取擦除区域的坐标  
            left, upper, right, lower = erase_box  
            # 创建一个与擦除区域大小相同的白色图像（或其他颜色）  
            erase_color = (255, 255, 255)  # 白色  
            erase_image = Image.new('RGB', (right - left, lower - upper), erase_color)  
            # 将擦除区域覆盖到原图像上  
            img.paste(erase_image, (left, upper))  
            # 保存处理后的图像  
            img.save(output_path)  
            print(f"Processed {image_path} and saved to {output_path}")  
    except Exception as e:  
        print(f"Error processing {image_path}: {e}")  
  
def batch_erase_region(directory, erase_box, output_directory):  
    """  
    批量擦除指定目录中所有JPG文件的指定区域。  
  
    :param directory: 输入JPG文件所在的目录  
    :param erase_box: 要擦除的区域，格式为(left, upper, right, lower)  
    :param output_directory: 输出处理后JPG文件的目录  
    """  
    if not os.path.exists(output_directory):  
        os.makedirs(output_directory)  
  
    for filename in os.listdir(directory):  
        if filename.lower().endswith('.jpg'):  
            image_path = os.path.join(directory, filename)  
            output_path = os.path.join(output_directory, filename)  
            erase_region(image_path, output_path, erase_box)  
  
if __name__ == "__main__":  
    input_directory = r"E:\hffg\hf"  # 使用原始字符串前缀避免转义字符问题  
    output_directory = r"E:\hffg\hf1"  # 使用原始字符串前缀  
    erase_area = (700, 1022, 794, 1122)  # 替换为你要擦除的区域  
  
    batch_erase_region(input_directory, erase_area, output_directory)