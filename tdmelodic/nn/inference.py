# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import sys
import os

import numpy as np
from tqdm import tqdm

import chainer
import chainer.functions as F
from chainer.dataset import convert

import re

from .net import Net
from .loader.data_loader import NeologdDictionaryLoader
from .lang.japanese.kana.mora_sep import sep_katakana2mora

# ------------------------------------------------------------------------------
# hyper params
gpu_id = -1 # cpu
bs = 1
embed_dim = 64
_default_path= os.path.dirname(os.path.abspath(__file__)) + "/resource/net_it_2500000"

# ------------------------------------------------------------------------------
class InferAccent(object):
    def __init__(self,
            model_path=_default_path,
            model_dim=embed_dim):
        self.net = self.__load_model(model_path, model_dim)

    def __load_model(self, model_path, model_dim):
        print("[ Loading model ] model_path=\'{}\'".format(model_path))
        net = Net(embed_dim=model_dim)
        chainer.serializers.load_npz(model_path, net)
        return net

    def infer(self, s, y, _):
        with chainer.using_config("debug", False):
            with chainer.using_config("type_check", False):
                with chainer.using_config("train", False):
                    a, _ = self.net(s, y, _)
                    a = F.argmax(a, axis=1).data
                    return a

    def infer_and_get_image(self, s, y, _):
        with chainer.using_config("debug", False):
            with chainer.using_config("type_check", False):
                with chainer.using_config("train", False):
                    a, _ = self.net(s, y, _)
                    return F.argmax(a, axis=1).data, F.softmax(a).data
