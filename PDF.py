# -*- coding: utf-8 -*-
import fitz  # PyMuPDF  
import os  
  
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
  
                # 复制页面的内容，但排除指定区域  
                pix = page.get_pixmap()  
                new_pix = fitz.Pixmap(fitz.csGRAY, pix.width, pix.height)  
                for y in range(pix.height):  
                    for x in range(pix.width):  
                        if not (rect[0] <= x < rect[2] and rect[1] <= y < rect[3]):  
                            # 保留不在擦除区域内的像素  
                            new_pix.set_pixel(x, y, pix.get_pixel(x, y))  
                        else:  
                            # 将擦除区域内的像素设置为白色（或透明，如果支持）  
                            # 注意：PyMuPDF的Pixmap默认是灰度图，所以白色是255  
                            # 如果是彩色图或需要透明处理，则需要更复杂的逻辑  
                            new_pix.set_pixel(x, y, 255)  # 设置为白色  
  
                # 将处理后的Pixmap插入到新页面中（这里简单处理为灰度图，可能需要转为RGB或其他格式）  
                # 注意：PyMuPDF的Pixmap转换为PDF页面时可能需要额外的处理，因为Pixmap默认是图像数据  
                # 这里我们采用一个简单的方法：将Pixmap保存为临时图像文件，然后从该图像文件创建PDF页面  
                # 这不是最高效的方法，但可以避免一些复杂的图像处理问题  
                temp_image_path = "temp_image.png"  
                new_pix.save(temp_image_path, format="PNG")  
                new_doc.insert_image(new_doc.page_count - 1, filename=temp_image_path)  
  
                # 删除临时图像文件  
                os.remove(temp_image_path)  
  
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