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
import copy

from tdmelodic.util.dic_index_map import get_dictionary_index_map
from tdmelodic.util.util import count_lines
from tdmelodic.util.word_type import WordType

from .yomi.basic import modify_longvowel_errors
from .yomi.basic import modify_yomi_of_numerals
from .yomi.particle_yomi import joshi_no_yomi
from .yomi.wrong_yomi_detection import SimpleWrongYomiDetector

class NeologdPatch(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if k != "input" and k != "output":
                self.__setattr__(k, v)
        self.IDX_MAP = get_dictionary_index_map(self.mode)
        self.wt = WordType()
        self.wrong_yomi_detector = SimpleWrongYomiDetector()
        print("[ Info ]")
        print("* Hash tags will" + (" " if self.rm_hashtag else " **NOT** ") + "be removed.", file=sys.stderr)
        print("* Noisy katakana words will" + (" " if self.rm_noisy_katakana else " **NOT** ") + "be removed.", file=sys.stderr)
        print("* Person names will" + (" " if self.rm_person else " **NOT** ") + "be removed.", file=sys.stderr)
        print("* Emojis will" + (" " if self.rm_emoji else " **NOT** ") + "be removed.", file=sys.stderr)
        print("* Symbols will" + (" " if self.rm_symbol else " **NOT** ") + "be removed.", file=sys.stderr)
        print("* Numerals will" + (" " if self.rm_numeral else " **NOT** ") + "be removed.", file=sys.stderr)
        print("* Wrong yomi words will" + (" " if self.rm_wrong_yomi else " **NOT** ") + "be removed.", file=sys.stderr)
        print("* Long vowel errors will" + (" " if self.cor_longvow else " **NOT** ") + "be corrected.", file=sys.stderr)
        print("* Numeral yomi errors will" + (" " if self.cor_yomi_num else " **NOT** ") + "be corrected.", file=sys.stderr)

    def add_accent_column(self, line, idx_accent=None):
        line = line + ['' for i in range(10)]
        line[idx_accent] = '@'
        return line

    def process_single_line(self, line):
        # ----------------------------------------------------------------------
        # remove words by word types
        if self.rm_hashtag:
            if self.wt.is_hashtag(line):
                return None

        if self.rm_noisy_katakana:
            if self.wt.is_noisy_katakana(line):
                return None

        if self.rm_person:
            if self.wt.is_person(line):
                return None

        if self.rm_emoji:
            if self.wt.is_emoji(line):
                return None

        if self.rm_symbol:
            if self.wt.is_symbol(line):
                return None

        if self.rm_numeral:
            if self.wt.is_numeral(line):
                return None

        line = copy.deepcopy(line)

        # ----------------------------------------------------------------------
        # correct yomi
        if self.cor_longvow:
            line = modify_longvowel_errors(line, idx_yomi=self.IDX_MAP["YOMI"])

        if self.cor_yomi_num:
            if self.wt.is_numeral(line):
                line = modify_yomi_of_numerals(line,
                    idx_surface=self.IDX_MAP["SURFACE"], idx_yomi=self.IDX_MAP["YOMI"])

        # 助詞の読みを修正する（TODO）
        line = joshi_no_yomi(line, self.IDX_MAP)

        # ----------------------------------------------------------------------
        # remove words with their yomi
        if self.rm_wrong_yomi:
            line = self.wrong_yomi_detector(line)
            if line is None:
                return None

        # ----------------------------------------------------------------------
        # add additional columns for compatibility with unidic-kana-accent
        line = self.add_accent_column(line, idx_accent=self.IDX_MAP["ACCENT"])

        # ----------------------------------------------------------------------
        return line

    def __call__(self, fp_in, fp_out):
        L = count_lines(fp_in)
        n_removed = 0
        n_corrected= 0
        for line in tqdm(csv.reader(fp_in), total=L):
            line_processed = self.process_single_line(line)
            if line_processed is None:
                n_removed += 1
                continue
            if line_processed[:20] != line[:20]:
                n_corrected += 1
            fp_out.write(','.join(line_processed) + '\n')

        print("[ Complete! ]", file=sys.stderr)
        print("* number of removed entries ", n_removed, file=sys.stderr)
        print("* number of corrected entries ", n_corrected, file=sys.stderr)
        print("[ Done ]", file=sys.stderr)
        return
