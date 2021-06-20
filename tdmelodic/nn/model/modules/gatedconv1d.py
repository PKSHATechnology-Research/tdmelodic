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

from .dilateconvcausal1d import DilateConvCausal1D

class GatedConv1D(chainer.Chain):
    def __init__(self,
                channel,
                ksize,
                dilate=1,
                dropout_rate = 0.3,
                causal=True):
        self.dropout_rate = dropout_rate
        self.half = channel

        ls = {}
        ls["c"] = DilateConvCausal1D(channel, channel * 2, ksize, dilate=dilate, causal=causal)
        ls["bn"] = L.BatchRenormalization(channel*2, decay=0.9, eps=2e-5)
        super(GatedConv1D, self).__init__(**ls)

    def __call__(self, x):
        h = x
        h = F.dropout(h, ratio=self.dropout_rate)
        h = self.c(h)
        h = self.bn(h)

        h1 = h[:,:self.half,:]
        h2 = h[:,self.half:,:]
        c = F.sigmoid(h2)

        h = F.relu(h1) * c + x * (1 - c)

        return h

if __name__ == '__main__':
    import numpy as np
    x = np.ones((1, 3, 20)).astype(np.float32)
    m = GatedConv1D(3, 5, dilate=2, dropout_rate = 0.1, causal=True)
    y = m(x)
    print(y.shape)
    print(y.data)
