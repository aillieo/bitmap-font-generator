# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gen_fnt (https://github.com/aillieo/bitmap-font-generator)
Fast and easy way to generate bitmap font with images
Created by Aillieo on 2017-09-06
With Python 3.5
"""

from PIL import Image
import os
import re


def dict_to_str(dict):
    ret = str(dict)
    ret = ret.replace(":", "=")
    ret = ret.replace("'", '"')
    ret = re.sub(r'[\(\)\{\}]', "", ret)

    return ret


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

    def __str__(self):
        return dict_to_str(self.info) + '\n' + dict_to_str(self.common)


class CharDef:
    def __init__(self):
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
            "chnl": 0
        }

    def __str__(self):
        return ""


class CharSet:
    def __init__(self):
        self.chars = []

    def __str__(self):
        ret = ""
        for char in self.chars:
            ret += str(char)
        return ret


class TextureMerger(object):
    def __init__(self, config, charset):
        self.config = config
        self.charset = charset

    def get_images(self):
        files = os.listdir('.')
        print(files)

    def gen_texture(self):
        texture = Image.new('RGBA', (100, 100), (255, 255, 255))
        print(texture)


class FntGenerator:
    def __init__(self):
        self.config = FntConfig()
        self.charset = CharSet()

    def gen_texture(self):
        texture_merger = TextureMerger(self.config, self.charset)
        texture_merger.gen_texture()

    def gen_fnt(self):
        fnt_str = ""
        fnt_str += str(self.config)
        fnt_str += str(self.charset)
        print(fnt_str)


if __name__ == '__main__':
    fg = FntGenerator()
    fg.gen_texture()
    fg.gen_fnt()
