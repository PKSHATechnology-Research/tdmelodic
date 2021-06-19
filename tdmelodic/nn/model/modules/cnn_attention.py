# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import numpy as np

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import cuda


def attention_loss(a, bs, len_1, len_2):
    xp = cuda.get_array_module(*a.data)

    I, J, sd = len_1, len_2, 15
    def f(bs, i, j):
        return 1 - np.exp(- (i - j)**2/(2 * sd**2)) + 1e-5

    a_soft = np.fromfunction(f, (bs, len_1, len_2), dtype=np.float32)
    a_soft = xp.asarray(a_soft)
    a_loss_tmp = F.sum(a * a_soft)/bs / len_1 /len_2
    a_loss_tmp *= 10
    return a_loss_tmp

class ConvAttention(chainer.Chain):
    def __init__(self):
        layers={}
        super(ConvAttention, self).__init__(**layers)

    def __call__(self, Q, KV):
        bs      = KV.data.shape[0]
        vec_dim = KV.data.shape[1]
        len_KV  = KV.data.shape[2] # key and value : processed surface
        len_Q   = Q. data.shape[2] # query : yomi (morae)

        # key and value are same
        K = KV
        V = KV

        # forward
        KQ = F.batch_matmul(K, Q, transa=True, transb=False)
        KQ /= np.sqrt(vec_dim)
        Attention = F.softmax(KQ, axis=1)
        c = F.batch_matmul(V, Attention)
        c += Q

        if chainer.config.train:
            a_loss = attention_loss(Attention, KQ, bs, len_KV, len_Q) # loss
            a = cuda.to_cpu(Attention.data) # log
        else:
            a, a_loss = None, None

        return c, a, a_loss
