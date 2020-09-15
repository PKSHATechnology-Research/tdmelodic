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
import re
import numpy as np

from functools import reduce

import chainer
from chainer import dataset
from chainer import datasets
from chainer import iterators


class DataLoaderBase(dataset.DatasetMixin):
    def __init__(self):
        self.memo = {} # メモ化

    def _load_word_list(self, text_file):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def _get_example_core(self, i):
        raise NotImplementedError

    if False:
        # 2epoch以降はロードなどの処理を省略する。
        def _get_example_memoized(self, i):
            if i not in self.memo.keys():
                self.memo[i] = self._get_example_core(i)
            return self.memo[i]
    else:
        # ロードや前処理を毎回実行する。
        # 毎回違う分析結果が欲しい（毎回MeCabを実行したい）ので今回はこっちを使う。
        def _get_example_memoized(self, i):
            return self._get_example_core(i)

    def get_example(self, i):
        dat_tuple = self._get_example_memoized(i)
        return dat_tuple
