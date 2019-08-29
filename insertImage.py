# -*- coding: utf-8 -*-
from io import BytesIO
import PyPDF2 as pypdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from tkinter import messagebox
import configparser

# 設定ファイルのパスから設定情報を取得
CONF_FILEPATH = "./config/myconf.conf"
config = configparser.ConfigParser()
config.read(CONF_FILEPATH, 'UTF-8')

# Proxy関連
config_val = config['values']
x_pos = config_val['x_pos']
y_pos = config_val['y_pos']
img_name = config_val['img_name']


def gen_pdf(original_file_list):
    for original_file in original_file_list:
        # there are 66 slides (1.jpg, 2.jpg, 3.jpg...)
        path = 'image/'+img_name
        pdf = pypdf.PdfFileWriter()

        # Using ReportLab Canvas to insert image into PDF
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
        # Draw image on Canvas and save PDF in buffer
        # (self, image, x,y,width,height,mask=None)
        #imgDoc.drawImage(path, 10, 10)
        imgDoc.drawImage(path, int(x_pos), int(y_pos))
        # x, y - start position
        # in my case -25, -45 needed
        imgDoc.save()
        # Use PyPDF to merge the image-PDF into the template
        pdf.addPage(pypdf.PdfFileReader(
            BytesIO(imgTemp.getvalue())).getPage(0))

        pdf.write(open("overlay.pdf", "wb"))

        with open("original/"+original_file, "rb") as inFile, open("overlay.pdf", "rb") as overlay:
            original = pypdf.PdfFileReader(inFile)
            print(original.numPages)
            for i in range(original.numPages):
                print(original_file + ":" + str(i)+"page done!")
                background = original.getPage(i)
                foreground = pypdf.PdfFileReader(overlay).getPage(0)
                # merge the first two pages
                background.mergePage(foreground)

            # add all pages to a writer
            writer = pypdf.PdfFileWriter()
            for i in range(original.getNumPages()):
                page = original.getPage(i)
                writer.addPage(page)

            # write everything in the writer to a file
            with open("modified/"+original_file[:-4]+"_modified.pdf", "wb") as outFile:
                writer.write(outFile)


def walk_path(path):
    file_list = []
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            # print(filename)
            file_list.append(filename)
    return file_list


if __name__ == '__main__':
    gen_pdf(walk_path("./original"))
    messagebox.showinfo('完了', '出力が完了しました。')
