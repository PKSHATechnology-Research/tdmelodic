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
import unicodedata
import jaconv

from tdmelodic.util.dic_index_map import get_dictionary_index_map
from tdmelodic.util.util import count_lines
from tdmelodic.util.word_type import WordType

from .yomi.basic import modify_longvowel_errors
from .yomi.basic import modify_yomi_of_numerals
from .yomi.particle_yomi import ParticleYomi
from .yomi.wrong_yomi_detection import SimpleWrongYomiDetector

class NeologdPatch(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if k != "input" and k != "output":
                self.__setattr__(k, v)
        self.IDX_MAP = get_dictionary_index_map(self.mode)
        self.wt = WordType()
        self.wrong_yomi_detector = SimpleWrongYomiDetector()
        self.particle_yomi = ParticleYomi()

    def showinfo(self):
        print("[ Info ]", file=sys.stderr)
        self.message("* {} Hash tags will{}be removed.", self.rm_hashtag)
        self.message("* {} Noisy katakana words will{}be removed.", self.rm_noisy_katakana)
        self.message("* {} Person names will{}be removed.", self.rm_person)
        self.message("* {} Emojis will{}be removed.", self.rm_emoji)
        self.message("* {} Symbols will{}be removed.", self.rm_symbol)
        self.message("* {} Numerals will{}be removed.", self.rm_numeral)
        self.message("* {} Wrong yomi words will{}be removed.", self.rm_wrong_yomi)
        self.message("* {} Words with special particles \"は\" and \"へ\" will{}be removed", self.rm_special_particle)
        self.message("* {} Long vowel errors will{}be corrected.", self.cor_longvow)
        self.message("* {} Numeral yomi errors will{}be corrected.", self.cor_yomi_num)
        self.message("* {} Surface forms will{}be normalized.", self.normalize)

    @classmethod
    def message(cls, message, flag):
        if flag:
            message = message.format("✅", " ")
        else:
            message = message.format("❌", " *NOT* ")
        print(message, file=sys.stderr)

    def add_accent_column(self, line, idx_accent=None):
        line = line + ['' for i in range(10)]
        line[idx_accent] = '@'
        return line

    def normalize_surface(self, line, idx_surface=None):
        s = line[idx_surface]
        s = unicodedata.normalize("NFKC", s)
        s = s.upper()
        s = jaconv.normalize(s, "NFKC")
        s = jaconv.h2z(s, digit=True, ascii=True, kana=True)
        s = s.replace("\u00A5", "\uFFE5") # yen symbol
        line[idx_surface] = s
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

        # ----------------------------------------------------------------------
        # 助詞の読みを修正する（TODO）
        if self.rm_special_particle:
            line = self.particle_yomi(line, self.IDX_MAP)
            if line is None:
                return None

        # ----------------------------------------------------------------------
        # normalize surface
        if self.normalize:
            line = self.normalize_surface(line, idx_surface=self.IDX_MAP["SURFACE"])


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
        self.showinfo()
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

        print("🍺  [ Complete! ]", file=sys.stderr)
        print("📊  Number of removed entries ", n_removed, file=sys.stderr)
        print("📊  Number of corrected entries ", n_corrected, file=sys.stderr)
        return
