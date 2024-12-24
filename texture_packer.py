# -*- coding: utf-8 -*-

# usage:
# python3 -m venv myenv
# source myenv/bin/activate
# pip3 install PyTexturePacker
# python3 ./texture_packer.py

from PyTexturePacker import Packer

def pack_test():
    # create a MaxRectsBinPacker
    packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffff00)
    # pack texture images under directory "test_case/" and name the output images as "test_case".
    # "%d" in output file name "test_case%d" is a placeholder, which is the atlas index, starting with 0.
    packer.pack("/Users/lichenliu/Documents/temp/png", "test_case%d")


if __name__ == '__main__':
    pack_test()
