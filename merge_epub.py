# -*- coding: utf-8 -*-

import os
from Ebooklib import epub

def merge_epubs_in_folder(input_folder, output_filename):
    merged_book = epub.EpubBook()

    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith('.epub'):
                input_filepath = os.path.join(root, filename)

                input_book = epub.read_epub(input_filepath)

                for item in input_book.items:
                    merged_book.add_item(item)

                for key, value in input_book.get_metadata().items():
                    merged_book.add_metadata(key, value)

    epub.write_epub(output_filename, merged_book)

merge_epubs_in_folder('/Users/lichenliu/Documents/temp/cc', 'output.epub')
