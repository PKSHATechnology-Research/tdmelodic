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

class EmbedMorae(chainer.Chain):
    def __init__(self,
                embed_dim = 100):
        self.embed_dim = embed_dim
        layers = {}
        layers["emb_v"  ] = L.EmbedID(50,embed_dim)
        layers["emb_c"  ] = L.EmbedID(50,embed_dim)
        super(EmbedMorae,self).__init__(**layers)

    def __call_add_(self, input_lst):
        v, c = input_lst
        emb =  self.emb_v(v)
        emb += self.emb_c(c)

        return emb

    def __call__(self, input_lst):
        r = self.__call_add_(input_lst)
        r = F.transpose(r, axes=(0, 2, 1))

        return r

class EncodeMorae(chainer.Chain):
    def __init__(self,
                embed_dim = 100):
        layers = {}
        layers["emb"] = EmbedMorae(embed_dim = embed_dim)
        layers["conv"] = StackedConv(
                        embed_dim,
                        ksizes=[3,3,3,3], dilations=[1,3,1,3],
                        causal=False,
                        dropout_rate=0.5
                        )

        super(EncodeMorae,self).__init__(**layers)

    def __call__(self, x):
        h = self.emb(x)
        y = self.conv(h)
        return y
