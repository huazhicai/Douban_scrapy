import os

import pymysql
import pytesseract
import tesserocr
from pprint import pprint
from PIL import Image, ImageFilter, ImageEnhance


class OperateImage(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host="localhost",
            user="root",
            passwd="654321",
            db="test",
            port=3306,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def read_text(self, image):
        # im = Image.open(image)
        text = pytesseract.image_to_string(image)
        return text

    def resize_image(self, image):
        image = image.convert('L')
        w, h = image.size
        resize = image.resize((2 * w, 2 * h))
        threshold = 150
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = resize.point(table, '1')
        return image

    def image_filter(self, image):
        im_detail = image.filter(ImageFilter.DETAIL)
        im_sharpen = image.filter(ImageFilter.SHARPEN)
        return im_detail, im_sharpen

    def enhance_sharpen(self, image):
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(2.0)

    def enhance_brightness(self, image):
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(2.0)

    def do_insert(self, *args):
        sql = """insert into image_text(im, resize, im_detail, im_sharpen, en_brightness, 
                    shap_bright, bright_shap) values(%s, %s,%s,%s,%s, %s,%s,%s)"""
        try:
            self.cursor.execute(sql, args)
            self.cursor.connection.commit()
        except pymysql.Error as err:
            print("****** Insert Database failure:", err)

    def close_db(self):
        self.cursor.close()
        self.connect.close(0)


def main(operate_image):
    image_list = os.listdir('./images')
    for image in image_list:
        im = Image.open('./images/{}'.format(image))
        resize = operate_image.resize_image(im)
        im_detail = resize.filter(ImageFilter.DETAIL)
        im_sharpen = resize.filter(ImageFilter.SHARPEN)
        # en_sharpen = operate_image.enhance_sharpen(resize)
        # en_brightness = operate_image.enhance_brightness(resize)
        # shap_bright = operate_image.enhance_brightness(en_sharpen)
        # bright_shap = operate_image.enhance_sharpen(en_brightness)
        yield (operate_image.read_text(im),
               operate_image.read_text(resize),
               operate_image.read_text(im_detail),
               operate_image.read_text(im_sharpen),
               # operate_image.read_text(en_sharpen),
               # operate_image.read_text(en_brightness),
               # operate_image.read_text(shap_bright),
               # operate_image.read_text(bright_shap),
               )


if __name__ == "__main__":
    operate_image = OperateImage()
    for val in main(operate_image):
        print(val)
        # operate_image.do_insert(*val)
    operate_image.close_db()
