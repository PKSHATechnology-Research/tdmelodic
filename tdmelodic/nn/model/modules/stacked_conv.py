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

from .gatedconv1d import GatedConv1D

class StackedConv(chainer.Chain):
    def __init__(self,
                channel,
                ksizes=[3,3,3,3],
                dilations=[1,1,1,1],
                causal=False,
                dropout_rate=0.3,
                **kwargs
                ):
        layers = {}
        self.n_layers = len(ksizes)
        self.causal = causal

        for i in range(self.n_layers):
            ksize = ksizes[i]
            dilation = dilations[i]
            layers["l_{}".format(i)] = GatedConv1D(
                    channel,
                    ksize,
                    dilate=dilation,
                    dropout_rate=dropout_rate,
                    causal=causal
                )

        layers["last"] = L.ConvolutionND(1, channel, channel, 1, stride=1, pad=0)

        super(StackedConv,self).__init__(**layers)

    def __call__(self, x, cond=None):
        h = x
        for i in range(self.n_layers):
            l = self.__getattribute__("l_{}".format(i))
            h = l(h)

        h = self.last(h)
        return h
