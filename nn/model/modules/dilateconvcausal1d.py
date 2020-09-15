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

class DilateConvCausal1D(chainer.Chain):
    ''' dilated convolution (causal) 1D '''
    def __init__(self,
                in_channel,
                out_channel,
                ksize,
                dilate=1,
                causal=True):

        self.in_ch = in_channel
        self.out_ch = out_channel
        self.ksize = ksize
        self.dilate = dilate
        self.causal = causal
        self.conv_size = (self.ksize - 1) * self.dilate + 1

        layers={}
        if self.dilate is None or self.dilate == 1:
            layers["conv"] = L.ConvolutionND(1,
                self.in_ch,
                self.out_ch,
                self.ksize,
                stride=1,
                pad=0)
        else:
            layers["conv"] = L.DilatedConvolution2D( \
                self.in_ch,
                self.out_ch,
                (self.ksize, 1),
                stride=1,
                pad=(0, 0),
                dilate = (self.dilate, 1)
                )

        super(DilateConvCausal1D, self).__init__(**layers)

    def padding(self, h):
        if self.causal:
            h = F.pad(h, (
                        (0, 0), # batch
                        (0, 0), # feature
                        ( (self.ksize - 1 ) * self.dilate, 0) # temporal
                    ), 'constant', constant_values=0)
        else:
            h = F.pad(h, (
                        (0, 0), # batch
                        (0, 0), # feature
                        ( (self.ksize - 1) * self.dilate // 2, (self.ksize - 1) * self.dilate // 2) # temporal
                    ), 'constant', constant_values=0)
        return h

    def __call__(self, x):
        h = x
        h = self.padding(h)
        return self.forward(h)

    def forward(self, x, **kwargs):
        h = x
        if self.dilate == 1:
            h = self.conv(h)
        else:
            h = F.expand_dims(h, axis=3)
            h = self.conv(h)
            h = h[:,:,:,0]

        return h

if __name__ == '__main__':
    import numpy as np
    ''' causal test '''
    x = np.ones((3, 3, 40)).astype(np.float32)
    m = DilateConvCausal1D(3, 2, ksize=5, dilate=3, causal=True)
    y = m(x)
    print(y.shape)
    print(y.data)

    ''' non causal test '''
    x = np.ones((3, 3, 40)).astype(np.float32)
    m = DilateConvCausal1D(3, 2, ksize=5, dilate=3, causal=False)
    y = m(x)
    print(y.shape)
    print(y.data)
