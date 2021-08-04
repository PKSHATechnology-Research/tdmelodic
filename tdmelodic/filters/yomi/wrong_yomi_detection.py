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

from tdmelodic.nn.lang.japanese.kansuji import numeric2kanji
from tdmelodic.util.dic_index_map import get_dictionary_index_map
from tdmelodic.util.util import count_lines
from tdmelodic.util.word_type import WordType
from .yomieval import YomiEvaluator


@dataclass
class LineInfo(object):
    surf: str
    yomi: str
    pos: str

class WrongYomiDetector(object):
    def __init__(self, distance_threshold=10, ratio_threshold=0.7):
        """
If the Levenshtein distance between the provided yomi and the predicted yomi from the surface form
is greater than the given thresholds, the entry will be removed.
        """
        self.distance_threshold = distance_threshold
        self.ratio_threshold = ratio_threshold

        self.yomieval = YomiEvaluator(rank_weight=0, romaji_priority=0, nbest=10)
        self.IDX_MAP = get_dictionary_index_map("unidic")
        self.wt = WordType()

    def __call__(self, line):
        if line is None:
            return None

        elif not self.is_target(line):
            return line

        else:
            info = self.get_line_info(line, self.IDX_MAP)
            dist = self.yomieval.eval(info.surf, info.yomi)
            ratio = float(dist) / float(len(info.yomi))

            if dist > self.distance_threshold or ratio > self.ratio_threshold:
                return None
            else:
                return line

    def is_target(self, line):
        not_target = self.wt.is_person(line) or \
                self.wt.is_emoji(line) or \
                self.wt.is_symbol(line) or \
                self.wt.is_numeral(line)
        return not not_target


    def get_line_info(self, line, IDX_MAP):
        s = line[IDX_MAP["SURFACE"]]
        y = line[IDX_MAP["YOMI"]]
        pos = "-".join([line[i] for i in [IDX_MAP["POS1"], IDX_MAP["POS2"], IDX_MAP["POS3"]]])
        s = self.normalize_surface(s)
        y = y.replace("[","").replace("]","") # remove accent marks

        return LineInfo(s, y, pos)

    def normalize_surface(self, text):
        # 全て全角に統一して処理する。
        text = unicodedata.normalize("NFKC",text)
        text = jaconv.h2z(text, digit=True, ascii=True, kana=True)

        # kansuji
        text = numeric2kanji(text)

        # (株), 株式会社などは無視
        text = text.replace("（株）","株式会社")
        text = text.replace("（有）","有限会社")
        return text
