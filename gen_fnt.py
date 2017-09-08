# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gen_fnt (https://github.com/aillieo/bitmap-font-generator)
Fast and easy way to generate bitmap font with images
Created by Aillieo on 2017-09-06
With Python 3.5
"""

from functools import reduce
from PIL import Image
import os
import re


def format_str(func):
    def wrapper(*args, **kw):
        ret = func(*args, **kw)
        ret = re.sub(r'[\(\)\{\}]', "", ret)
        ret = re.sub(r'\'(?P<name>\w+)\': ', "\g<name>=", ret)
        ret = re.sub(r', (?P<name>\w+)=', " \g<name>=", ret)
        ret = ret.replace("'", '"')
        return ret

    return wrapper


class FntConfig:
    def __init__(self):
        self.info = {
            "face": "Arial",
            "size": 16,
            "bold": 0,
            "italic": 0,
            "charset": "",
            "unicode": 0,
            "stretchH": 100,
            "smooth": 1,
            "aa": 1,
            "padding": (0, 0, 0, 0),
            "spacing": (1, 1),
        }

        self.common = {
            "lineHeight": 19,
            "base": 26,
            "scaleW": 256,
            "scaleH": 256,
            "pages": 1,
            "packed": 0
        }

        self.pages = {}

    @format_str
    def __str__(self):
        return 'info ' + str(self.info) + '\ncommon ' + str(self.common) + '\n'


class CharDef:
    def __init__(self, file):
        self.file = file
        self.param = {
            "id": 0,
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "xoffset": 0,
            "yoffset": 0,
            "xadvance": 0,
            "page": 0,
            "chnl": 15
        }
        char_name = self.file.split('.')[0]
        self.param["id"] = ord(char_name)
        img = Image.open(self.file)
        self.set_texture_size(img.size)

    @format_str
    def __str__(self):
        return 'char ' + str(self.param)

    def set_texture_size(self, size):
        self.param["width"], self.param["height"] = size
        self.param["xadvance"] = size[0]

    def set_texture_position(self, position):
        self.param["x"], self.param["y"] = position


class CharSet:
    def __init__(self):
        self.chars = []

    def __str__(self):
        ret = 'chars count=' + str(len(self.chars)) + '\n'
        ret += reduce(lambda char1, char2: str(char1) + str(char2) + "\n", self.chars, "")
        return ret

    def add_new_char(self, new_char):
        self.chars.append(new_char)

    def sort_for_texture(self):
        self.chars.sort(key=lambda char: char.param["width"], reverse=True)
        self.chars.sort(key=lambda char: char.param["height"], reverse=True)


class PageDef:
    def __init__(self, pid, file):
        self.param = {
            "id": pid,
            "file": file
        }

    @format_str
    def __str__(self):
        return 'page ' + str(self.param)


class TextureMerger:
    def __init__(self, config):
        self.config = config
        self.charset = CharSet()
        self.pages = []

    def get_images(self):
        files = os.listdir('.')
        for filename in files:
            name, ext = filename.split('.')
            if ext.lower() == 'png' and len(name) == 1:
                new_char = CharDef(filename)
                self.charset.add_new_char(new_char)
        self.charset.sort_for_texture()

    def gen_texture(self):
        self.get_images()
        texture_w, texture_h = self.config.common["scaleW"], self.config.common["scaleH"]
        texture = Image.new('RGBA', (texture_w, texture_h), (0, 0, 0, 0))

        pos_x, pos_y, row_h = 0, 0, 0
        for char in self.charset.chars:
            img = Image.open(char.file)
            if row_h == 0:
                row_h = img.size[1]
            if texture_w - pos_x >= img.size[0]:
                char.set_texture_position((pos_x, pos_y))
                texture.paste(img, (pos_x, pos_y))
                pos_x += img.size[0]
            else:
                pos_y += row_h
                row_h = img.size[1]
                char.set_texture_position((0, pos_y))
                texture.paste(img, (0, pos_y))
                pos_x = img.size[0]

        file_name = "output.png"
        try:
            texture.save(file_name, 'PNG')
            self.pages.append(PageDef(0, file_name))
        except IOError:
            print("IOError: save file failed: " + file_name)

    def pages_to_str(self):
        return reduce(lambda page1, page2: str(page1) + str(page2) + "\n", self.pages, "")


class FntGenerator:
    def __init__(self):
        self.config = FntConfig()
        self.textureMerger = TextureMerger(self.config)

    def gen_fnt(self):
        self.textureMerger.gen_texture()
        with open('output.fnt', 'w', encoding='utf8') as fnt:
            fnt.write(str(self.config))
            fnt.write(self.textureMerger.pages_to_str())
            fnt.write(str(self.textureMerger.charset))
        fnt.close()


if __name__ == '__main__':
    fg = FntGenerator()
    fg.gen_fnt()
