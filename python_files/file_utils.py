#!/usr/bin/env python
import os
import re
from os import walk


def create_output_dir_if_needed():
    #   Make output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    return output_dir


def generate_next_file_name(filename_prefix, file_ext):
    output_dir = create_output_dir_if_needed()

    songs = []

    for (dirpath, dirnames, filenames) in walk(output_dir):
        songs.extend(filter(lambda f: f.endswith("." + file_ext), filenames))
        break

    top_num = 0
    for song in songs:
        str_num = ""
        try:
            str_num = re.search(filename_prefix + "(.*)." + file_ext, song, re.IGNORECASE).group(1)
        except:
            str_num = ""
        if str_num == "":
            str_num = "0"
        num = int(str_num)
        if num > top_num:
            top_num = num

    return filename_prefix + str(top_num + 1) + "." + file_ext
