# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import chainer
import chainer.functions as F
import chainer.links as L

from .modules.stacked_conv import StackedConv


class DecodeAccent(chainer.Chain):
    def __init__(self,embed_dim = 100):
        n_class = 3
        layers = {}
        layers["conv"] = StackedConv(
                        embed_dim,
                        ksizes=[3,3,3,3], dilations=[1,3,1,3],
                        causal=False,
                        dropout_rate=0.5,
                        conditional=False,
                        self_attention=False
                        )
        layers["conv2"] = StackedConv(
                        embed_dim,
                        ksizes=[1,1], dilations=[1,1],
                        causal=False,
                        dropout_rate=0.0,
                        conditional=False,
                        self_attention=False
                        )

        layers["classifier"] = L.ConvolutionND(1, embed_dim, n_class, 1, stride=1, pad=0)
        super(DecodeAccent,self).__init__(**layers)

    def __call__(self, x):
        h = self.conv(x)
        h = self.conv2(h)
        pre_softmax = self.classifier(h)
        return pre_softmax
