# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

# -*- coding: utf-8 -*-
import sys
import os
import argparse
import regex as re
import csv
from tqdm import tqdm
import tempfile

from ..util.dic_index_map import get_dictionary_index_map
from ..util.util import count_lines
from .remove_duplicates import main_ as rmdups
from .detect_weird_yomi import main_ as detyom

def main_(fp_in, fp_out):
    if True:
        fp_tmp = tempfile.NamedTemporaryFile("w+")
        print("creating temporary file", fp_tmp.name, file=sys.stderr)
        rmdups(fp_in, fp_tmp)
        fp_tmp.seek(0)
        fp_in.close() # CPython's GC will automatically closes the previous fp_in without doing this
        fp_in = fp_tmp

    if False:
        fp_tmp = tempfile.NamedTemporaryFile("w+")
        print("creating temporary file", fp_tmp.name, file=sys.stderr)
        detyom(fp_in, fp_tmp)
        fp_tmp.seek(0)
        fp_in.close()
        fp_in = fp_tmp

    # output
    for l in fp_tmp:
        fp_out.write(l)
    fp_tmp.close()
    fp_out.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input',
        nargs='?',
        type=argparse.FileType("r"),
        default=sys.stdin,
        help='input CSV file (NEologd dicitionary file) <default=STDIN>')
    parser.add_argument(
        '-o',
        '--output',
        nargs='?',
        type=argparse.FileType("w"),
        default=sys.stdout,
        help='output CSV file <default=STDOUT>')
    args = parser.parse_args()
    if args.input == args.output:
        print("[ Error ] intput and output files should be different.")
    else:
        try:
            main_(args.input, args.output)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()