# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import os, sys
import subprocess
import MeCab
import Levenshtein
import numpy as np

def get_mecab_default_path():
    out = subprocess.Popen(['mecab-config', '--dicdir'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout_, stderr_ = out.communicate()
    mecab_default_dir = stdout_.decode('utf-8').strip()
    return mecab_default_dir

mapping=["surface",
    "pron",
    "kana",
    "pos",
    "goshu",
    "acc",
    "concat",
    "cost_uni",
    "cost_bi"] + list(range(100))

class UniDic(object):
    def __init__(self,
                # unidic_path  = "/usr/lib/mecab/dic/unidic", # default setting in our docker image
                unidic_path  = get_mecab_default_path() + "/unidic",
                mecabrc_path = os.path.dirname(os.path.abspath(__file__)) + "/my_mecabrc",
            ):

        self.unidic_path  = unidic_path
        self.mecabrc_path = mecabrc_path
        print("[ MeCab setting ] unidic=\'{}\'".format(self.unidic_path))
        print("[ MeCab setting ] mecabrc=\'{}\'".format(self.mecabrc_path))

        self.__init_mecab()

    def __init_mecab(self):
        self.unidic_acc = MeCab.Tagger(
                "-d {dic} -r {rc} -Oacc" .format(
                        dic=self.unidic_path,   rc=self.mecabrc_path))

    def __parse(self, text, nbest=1, sep1='\t', sep2='\n'):
        parsed = self.unidic_acc.parseNBest(nbest, text)
        nbest = parsed.split("EOS\n")[:-1] # remove the last entry
        ret = [
                [
                    {
                        mapping[i] : c
                        for i, c in enumerate(list(l.split(sep1)))
                    }
                    for l in c.split(sep2)[:-1]
                ]
                for c in nbest
            ]
        return ret

    def get_n_best(self, text, kana_ref, nbest=20):
        '''
        during inference, only the top 1 result is used. see data_loader.py
        '''
        p = self.__parse(text, nbest=nbest)
        kanas = ["".join([e["pron"] for e in p_]) for p_ in p]
        dist = [Levenshtein.distance(k, kana_ref) for k in kanas]

        rank = [i for i, v in sorted(enumerate(dist), key=lambda v: v[1])]

        # rank = rank[0:3] if len(rank) >= 3 else rank # 上位 3 件を返す。
        # rank = rank[0:5] if len(rank) >= 5 else rank # 上位 5 件を返す。
        rank = rank[0:10] if len(rank) >= 10 else rank # 上位 10 件を返す。

        ld = dist[rank[0]]
        return p, rank, ld
