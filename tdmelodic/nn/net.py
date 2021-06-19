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

import chainer
import chainer.functions as F
from chainer import cuda

from .model.encode_morae import EncodeMorae
from .model.encode_surface import EncodeSurface
from .model.decode_accent import DecodeAccent
from .model.modules.cnn_attention import ConvAttention

class Net(chainer.Chain):
    def __init__(self, embed_dim):
        layers = {}
        layers["enc_surface"]  = EncodeSurface(embed_dim)
        layers["enc_yomigana"] = EncodeMorae(embed_dim)
        layers["att"] = ConvAttention()
        layers["dec"] = DecodeAccent(embed_dim)
        super(Net,self).__init__(**layers)

    def __call__(self, *args, **kwargs):
        input_lst_s, input_lst_y, t_gt = args

        # forward propagation
        h_s = self.enc_surface (input_lst_s)
        h_y = self.enc_yomigana(input_lst_y)
        c, a, a_loss = self.att(h_y, h_s)
        h = self.dec(c)
        # y = F.softmax(h)

        # evaluate loss
        if chainer.config.train:
            loss = F.softmax_cross_entropy(h, t_gt)
        else:
            loss = None

        return h, [loss, a_loss]
