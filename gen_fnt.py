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
        ret = ret.replace(":", "=")
        ret = ret.replace("'", '"')
        ret = re.sub(r'[\(\)\{\}]', "", ret)
        return ret

    return wrapper


# fnt configs:
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
            "scaleW": 512,
            "scaleH": 512,
            "pages": 1,
            "packed": 0
        }

        self.pages = {}

    @format_str
    def __str__(self):
        return str(self.info) + '\n' + str(self.common) + '\n'


class CharDef:
    def __init__(self, char, file):
        self.char = char
        self.file = file
        self.param = {
            "id": id,
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "xoffset": 0,
            "yoffset": 0,
            "xadvance": 0,
            "page": 0,
            "chnl": 0
        }

    @format_str
    def __str__(self):
        return str(self.param)

    def update_param(self):
        self.param["id"] = ord(self.char)


class CharSet:
    def __init__(self):
        self.chars = []

    def __str__(self):
        return reduce(lambda char1, char2: str(char1) + str(char2) + "\n", self.chars, "")

    def add_new_char(self, new_char):
        self.chars.append(new_char)

    def update(self):
        for char in self.chars:
            char.update_param()


class TextureMerger(object):
    def __init__(self, config):
        self.config = config
        self.charset = CharSet()

    def get_images(self):
        files = os.listdir('.')
        for filename in files:
            char_name, ext = filename.split('.')
            if ext.lower() == 'png' and len(char_name) == 1:
                new_char = CharDef(char_name, filename)
                self.charset.add_new_char(new_char)

    def gen_texture(self):
        self.get_images()
        texture = Image.new('RGBA', (256, 256), (255, 255, 255, 0))

        x_offset = 0
        for char in self.charset.chars:
            img = Image.open(char.file)
            texture.paste(img, (x_offset, 0))
            x_offset += img.size[0]

        file_name = "output.png"
        try:
            texture.save(file_name, 'PNG')
        except IOError:
            print("IOError: save file failed: " + file_name)
        self.charset.update()


class FntGenerator:
    def __init__(self):
        self.config = FntConfig()
        self.textureMerger = TextureMerger(self.config)

    def gen_texture(self):
        self.textureMerger.gen_texture()

    def gen_fnt(self):
        self.gen_texture()
        fnt_str = ""
        fnt_str += str(self.config)
        fnt_str += str(self.textureMerger.charset)
        print(fnt_str)


if __name__ == '__main__':
    fg = FntGenerator()
    fg.gen_fnt()
