# -*- coding: utf-8 -*-
from io import BytesIO
import PyPDF2 as pypdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import configparser

# 設定ファイルのパスから設定情報を取得
CONF_FILEPATH = "./config/myconf.conf"
config = configparser.ConfigParser()
config.read(CONF_FILEPATH, 'UTF-8')

config_val = config['values']
x_pos = config_val['x_pos']
y_pos = config_val['y_pos']
img_name = config_val['img_name']


# pdfマージシステム利用
def gen_pdf(original_file_list):
    for original_file in original_file_list:
        path = 'image/'+img_name
        pdf = pypdf.PdfFileWriter()

        # reportlabのキャンバスを利用する
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=A4)

        # イメージを挿入したpdfを作成する
        # x_posとy_posが画像の挿入位置
        imgDoc.drawImage(path, int(x_pos), int(y_pos))
        imgDoc.save()

        # 画像付きpdfを生成 → overlay.pdf
        pdf.addPage(pypdf.PdfFileReader(
            BytesIO(imgTemp.getvalue())).getPage(0))
        pdf.write(open("overlay.pdf", "wb"))

        # 作成したpdfと、画像を貼り付けたいpdfとをマージしていく
        with open("original/"+original_file, "rb") as inFile, open("overlay.pdf", "rb") as overlay:
            original = pypdf.PdfFileReader(inFile)
            print(original.numPages)
            for i in range(original.numPages):
                print(original_file + ":" + str(i)+"page done!")
                background = original.getPage(i)
                foreground = pypdf.PdfFileReader(overlay).getPage(0)
                background.mergePage(foreground)

            # 各ページに書き込み処理を行う
            writer = pypdf.PdfFileWriter()
            for i in range(original.getNumPages()):
                page = original.getPage(i)
                writer.addPage(page)

            # ファイル化
            with open("modified/"+original_file[:-4]+"_modified.pdf", "wb") as outFile:
                writer.write(outFile)


# Python本より利用 フォルダを渡り歩いてファイル名のリストを得る
def walk_path(path):
    file_list = []
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            # print(filename)
            file_list.append(filename)
    return file_list


if __name__ == '__main__':
    gen_pdf(walk_path("./original"))
    print("処理が完了しました")
