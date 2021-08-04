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

import unicodedata
import jaconv
from dataclasses import dataclass

from ...nn.lang.japanese.kansuji import numeric2kanji
from ...util.dic_index_map import get_dictionary_index_map
from ...util.util import count_lines
from ...util.word_type import WordType
from .yomi.yomieval import YomiEvaluator

IDX_MAP = get_dictionary_index_map("unidic")

# ------------------------------------------------------------------------------------
def normalize_surface(text):
    # 全て全角に統一して処理する。
    text = unicodedata.normalize("NFKC",text)
    text = jaconv.h2z(text, digit=True, ascii=True, kana=True)

    # kansuji
    text = numeric2kanji(text)

    # (株), 株式会社などは無視
    text = text.replace("（株）","株式会社")
    text = text.replace("（有）","有限会社")
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
    y = y.replace("[","").replace("]","") # remove accent marks

    return LineInfo(s, y, pos)

# ------------------------------------------------------------------------------------
def main_(fp_in, fp_out):
    unidic = YomiEvaluator(0, 0)
    c = 0
    L = count_lines(fp_in)

    for line in tqdm(csv.reader(fp_in), total=L):
        if line is None:
            continue
        else:
            info = get_line_info(line)
            dist = unidic.eval(info.surf, info.yomi)
            ratio = float(dist) / float(len(info.yomi))

            # levenshtein distance が 10 以上か、読みの長さの 70% が間違っている場合は除去。
            if dist > 10 or ratio > 0.7:
                pass
            else:
                fp_out.write(",".join(line) + "\n")

    fp_out.write(",".join(line) + "\n")

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
