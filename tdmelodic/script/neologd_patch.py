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

# ------------------------------------------------------------------------------------
# see also mecabrc
IDX_SURFACE= 0
IDX_COST   = 3
IDX_POS1   = 4 +  0 # f[0]:   pos1
IDX_POS2   = 4 +  1 # f[1]:   pos2
IDX_POS3   = 4 +  2 # f[2]:   pos3
IDX_YOMI   = 4 +  9 # f[9]:   pron
IDX_GOSHU  = 4 + 12 # f[12]:  goshu
IDX_ACCENT = 4 + 23 # f[23]:  aType

# ------------------------------------------------------------------------------------
def count_lines(fname):
    with open(fname, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# ------------------------------------------------------------------------------------
def modify_katakana_errors(line):
    # katakana regex
    line[IDX_YOMI] = line[IDX_YOMI]\
                    .replace("ーィ","ウィ")\
                    .replace("ーェ","ウェ")\
                    .replace("ーォ","ウォ")
    return line

# ------------------------------------------------------------------------------------
def modify_yomi_of_numerals(line):
    """
    数値の読みを簡易的に修正する（完全なものではない）
    """

    surface = line[IDX_SURFACE]
    # 1文字目が数字で2文字以上の長さがあるもの
    num=[str(i) for i in range(10)] + ['１','２','３','４','５','６','７','８','９','０']
    if (surface[0] in num) and len(line[1]) >= 2:
        pass
    else:
        # otherwise do nothing
        return line

    filters=[
                (r"ニ(テン\p{Katakana}+)", r"ニー\1" ),
                (r"ゴ(テン\p{Katakana}+)", r"ゴー\1" ),
                (r"ニ(イチ|ニ|サン|ヨン|ゴ|ロク|ナナ|ハチ|キュウ|キュー|レー|レイ|ゼロ)", r"ニー\1" ),
                (r"ゴ(イチ|ゴ|サン|ヨン|ゴ|ロク|ナナ|ハチ|キュウ|キュー|レー|レイ|ゼロ)", r"ゴー\1" ),
                (r"イチ(サ^ン|シ|ス|セ|ソ|タ|チ|ツ|テ|ト|カ|キ^ュ|ケ|コ|パ|ピ|プ|ペ|ポ)", r"イッ\1" ),
                (r"ハチ(サ^ン|シ|ス|セ|ソ|タ|チ|ツ|テ|ト|カ|キ^ュ|ケ|コ|パ|ピ|プ|ペ|ポ)", r"ハッ\1" ),
                (r"ジュウ(サ^ン|シ^チ|ス|セ|ソ|タ|チ|ツ|テ|ト|カ|キ^ュ|ケ|コ|パ|ピ|プ|ペ|ポ)", r"ジュッ\1" ),
#                (r"ンエ", r"ンイェ" ), # 「万円」などを en -> yen
                (r"ヨンニチ", r"ヨッカ" ),
                (r"ニーニチ", r"ニニチ" ), # 12日など
                (r"ゴーニチ", r"ゴニチ" ) # 15日など
            ]
    yomi = line[IDX_YOMI]

    for regex1, regex2 in filters:
        prev_yomi = ''
        while prev_yomi != yomi: # 変化しなくなるまでループ
            prev_yomi = yomi
            if re.search(regex1, yomi):
                yomi = re.sub(regex1, regex2, yomi)

    line[IDX_YOMI] = yomi

    return line

# ------------------------------------------------------------------------------------
def joshi_no_yomi(line):
    # TODO
    # neologdの読みは　ワガハイ【ハ】ネコデアル　のように助詞「は」等の読みが適切に処理されていないケースがある。
    return line

# ------------------------------------------------------------------------------------
def main_(neologd_csv, output_csv):
    L = count_lines(neologd_csv)
    fp_in = csv.reader(open(neologd_csv, 'r'))

    with open(output_csv, mode='w') as fp_out:
        for line in tqdm(fp_in, total=L):
            # 「スーェーデン」「ノルーェー」のようなエラーを修正する
            line = modify_katakana_errors(line)

            # 数値表現の読みを変更する
            line = modify_yomi_of_numerals(line)

            # 助詞の読みを修正する（TODO）
            line = joshi_no_yomi(line)

            # neologdの末尾に付加的なカラムを追加する（unidic-kana-accentとの互換性のため）
            line = line + ['' for i in range(10)]
            line[IDX_ACCENT] = '@'

            # 出力
            line = ','.join(line) + '\n'
            fp_out.write(line)

    print("Complete! Saved the converted file as ... ", output_csv)
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
                        help='input csv (neologd dicitionary file)')
    parser.add_argument('-o', '--output', type=str,
                        help='output csv')
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