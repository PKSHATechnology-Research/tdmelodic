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

from tdmelodic.nn.lang.mecab.unidic import UniDic
import Levenshtein
import unicodedata
import romkan
import jaconv
from dataclasses import dataclass

from ...nn.lang.japanese.kansuji import numeric2kanji
from ...util.dic_index_map import get_dictionary_index_map
from ...util.util import count_lines
from ...util.word_type import WordType

IDX_MAP = get_dictionary_index_map("unidic")

class UniDic2(UniDic):
    def __init__(self, **kwargs):
        UniDic.__init__(self, **kwargs)

    def eval(self, *args, **kwargs):
        distance1 = self.eval_normal(*args, **kwargs)
        distance2 = self.eval_force_romaji_to_kana(*args, **kwargs)
        return min(distance1, distance2)

    def eval_normal(self, text, kana_ref, nbest=20):
        '''一番読みが近いものとの距離を評価して返す。順位も考慮に入れる。'''
        text = jaconv.h2z(text, digit=True, ascii=True, kana=True) # zenkaku
        p = self._UniDic__parse(text, nbest=nbest)
        kanas = ["".join([e["pron"] for e in p_]) for p_ in p]
        dist = [Levenshtein.distance(k, kana_ref) for rank, k in enumerate(kanas)]
        rank = [i for i, v in sorted(enumerate(dist), key=lambda v: v[1])]
        ld = dist[rank[0]]
        return ld

    def eval_force_romaji_to_kana(self, text, kana_ref, nbest=20):
        """アルファベットをローマ字読みできそうな箇所を無理やり仮名に変換してからさらにUniDicで分析してより良い読みを探る。"""
        p_ = jaconv.z2h(text, digit=True, ascii=True, kana=False) # hankaku
        p = romkan.to_katakana(p_) # romanize as possible
        if p_ == p: # 変化がないものは以下の処理を行わずに戻る。戻り値は十分大きければなんでも良い。
            return 12345
        return self.eval_normal(p, kana_ref, nbest)

    def eval_force_number_english(self, text, kana_ref, nbest=20):
        """数字を無理やり英語読みする。"""
        # TODO
        pass

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
    unidic = UniDic2()
    c = 0
    L = count_lines(fp_in)
    wt = WordType()

    for line in tqdm(csv.reader(fp_in), total=L):
        if wt.is_hashtag(line) or wt.is_noisy_katakana(line):
            # remove hashtag and noisy katakana
            continue
        elif wt.is_person(line) or wt.is_emoji(line) or wt.is_symbol(line) or wt.is_numeral(line):
            fp_out.write(",".join(line) + "\n")
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
