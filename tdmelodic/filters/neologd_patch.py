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

from ..util.dic_index_map import get_dictionary_index_map
from ..util.util import count_lines

from ..util.word_type import WordType
from .modules.yomi_corrector.basic import modify_longvowel_errors
from .modules.yomi_corrector.basic import modify_yomi_of_numerals
from .modules.add_accent_column import add_accent_column


# ------------------------------------------------------------------------------------
def joshi_no_yomi(line, IDX_MAP):
    # TODO
    # neologdの読みは　ワガハイ【ハ】ネコデアル　のように助詞「は」等の読みが適切に処理されていないケースがある。
    return line

# ------------------------------------------------------------------------------------
def main_(fp_in, fp_out, mode):
    IDX_MAP = get_dictionary_index_map(mode)

    wt = WordType()
    L = count_lines(fp_in)

    for line in tqdm(csv.reader(fp_in), total=L):
        line = modify_longvowel_errors(line, idx_yomi=IDX_MAP["YOMI"])

        if wt.is_numeral(line):
            line = modify_yomi_of_numerals(line, idx_surface=IDX_MAP["SURFACE"], idx_yomi=IDX_MAP["YOMI"])

        # 助詞の読みを修正する（TODO）
        # line = joshi_no_yomi(line, IDX_MAP)

        # neologdの末尾に付加的なカラムを追加する（unidic-kana-accentとの互換性のため）
        line = add_accent_column(line, idx_accent=IDX_MAP["ACCENT"])

        # write
        fp_out.write(','.join(line) + '\n')

    print("Complete!", file=sys.stderr)
    return

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
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        help="dictionary format type <default=unidic>",
        choices=["unidic", "ipadic"],
        default="unidic",
    )
    args = parser.parse_args()
    if args.input == args.output:
        print("[ Error ] intput and output files should be different.")
    else:
        try:
            main_(args.input, args.output, args.mode)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()