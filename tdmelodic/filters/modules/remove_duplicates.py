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

import jaconv
import unicodedata
from dataclasses import dataclass

from ...nn.lang.japanese.kansuji import numeric2kanji
from ...util.dic_index_map import get_dictionary_index_map
from ...util.util import count_lines
from ...util.word_type import WordType
from .yomi.yomieval import YomiEvaluator

IDX_MAP = get_dictionary_index_map("unidic")

# ------------------------------------------------------------------------------------
def normalize_surface(text):
    # hankaku
    text = unicodedata.normalize("NFKC",text)
    text = jaconv.h2z(text, digit=True, ascii=True, kana=False)

    # kansuji
    text = numeric2kanji(text)

    # (株), 株式会社など
    text = text.replace("（株）","・カブシキガイシャ・")
    text = text.replace("（有）","・ユウゲンガイシャ・")
    text = text.replace("＆","・アンド・")
    return text

# ------------------------------------------------------------------------------------
@dataclass
class LineInfo(object):
    surf: str
    yomi: str
    pos: str

def get_line_info(line):
    s = line[IDX_MAP["SURFACE"]]
    y = line[IDX_MAP["YOMI"]]
    pos = "-".join([line[i] for i in [IDX_MAP["POS1"], IDX_MAP["POS2"], IDX_MAP["POS3"]]])
    s = normalize_surface(s)

    return LineInfo(s, y, pos)

# ------------------------------------------------------------------------------------
def main_(fp_in, fp_out):
    yomieval = YomiEvaluator()
    prev_line = [""] * 100
    c = 0
    L = count_lines(fp_in)
    wt = WordType()

    for i, curr_line in enumerate(tqdm(csv.reader(fp_in), total=L)):
        prev = get_line_info(prev_line)
        curr = get_line_info(curr_line)

        if prev.surf == curr.surf and prev.pos == curr.pos and \
            not wt.is_person(prev_line) and not wt.is_placename(prev_line):
            # if the surface form and pos are the same
            distance_p = yomieval.eval(prev.surf, prev.yomi)
            distance_c = yomieval.eval(curr.surf, curr.yomi)
        else:
            distance_p = 0
            distance_c = 100

        if distance_p > distance_c:
            c += 1
            if c % 100 == 0:
                print(c, curr.surf, "| deleted: ", prev.yomi, distance_p, " | left: ", curr.yomi, distance_c, file=sys.stderr)
        else:
            if i != 0:
                fp_out.write(",".join(prev_line) + "\n")

        prev_line = curr_line
        continue

    fp_out.write(",".join(prev_line) + "\n")

# ------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="""
        Remove duplicate entries from the base dictionary.
        Duplicate entries are removed based on the correctness of their yomis.
        """
    )
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
