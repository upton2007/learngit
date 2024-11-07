# -*- coding: utf-8 -*-
import fitz  # PyMuPDF  
import os  
import io  
  
def erase_area_in_pdf(input_folder, output_folder, rect):  
    """  
    遍历输入文件夹中的所有PDF文件，擦除指定区域的内容，并将处理后的PDF保存到输出文件夹。  
  
    :param input_folder: 输入文件夹路径  
    :param output_folder: 输出文件夹路径  
    :param rect: 要擦除的区域，格式为(left, top, right, bottom)  
    """  
    if not os.path.exists(output_folder):  
        os.makedirs(output_folder)  
  
    # 遍历输入文件夹中的所有PDF文件  
    for filename in os.listdir(input_folder):  
        if filename.lower().endswith('.pdf'):  
            input_path = os.path.join(input_folder, filename)  
            output_path = os.path.join(output_folder, filename)  
  
            # 打开PDF文件  
            doc = fitz.open(input_path)  
            # 创建一个新的PDF文档来保存修改后的页面  
            new_doc = fitz.open()  
  
            # 遍历每一页  
            for page_num in range(len(doc)):  
                page = doc.load_page(page_num)  
                new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)  
  
                # 获取页面的Pixmap表示  
                pix = page.get_pixmap(clip=page.rect)  # 使用clip参数确保获取整个页面  
  
                # 创建一个新的Pixmap用于存储修改后的图像  
                new_pix = fitz.Pixmap(fitz.csGRAY, pix.width, pix.height)  
  
                # 遍历每个像素，擦除指定区域  
                for y in range(pix.height):  
                    for x in range(pix.width):  
                        if not (rect[0] <= x < rect[2] and rect[1] <= y < rect[3]):  
                            # 保留不在擦除区域内的像素  
                            gray = pix.get_pixel(x, y)  # 获取灰度值  
                            new_pix.set_pixel(x, y, gray)  
                        else:  
                            # 将擦除区域内的像素设置为白色（灰度值为255）  
                            new_pix.set_pixel(x, y, 255)  
  
                # 将Pixmap保存为内存中的字节流  
                pix_bytes = io.BytesIO()  
                new_pix.save(pix_bytes, format="PNG")  
                pix_bytes.seek(0)  # 重置字节流位置到开头  
  
                # 从内存中的字节流创建图像，并插入到新页面中  
                new_page.insert_image(rect=new_page.rect, stream=pix_bytes, filename=None)  
  
            # 保存修改后的PDF文件  
            new_doc.save(output_path)  
            # 关闭文档  
            new_doc.close()  
            doc.close()  
  
    print(f"Processed all PDF files in {input_folder} and saved them to {output_folder}")  
  
# 使用示例  
input_folder = r"E:\hffg\pdftest"  # 替换为你的输入文件夹路径  
output_folder = r"E:\hffg\pdftest1"  # 替换为你的输出文件夹路径  
# 指定要擦除的区域，格式为(left, top, right, bottom)，单位为点（1/72英寸）  
erase_rect = (100, 100, 200, 200)  
erase_area_in_pdf(input_folder, output_folder, erase_rect)