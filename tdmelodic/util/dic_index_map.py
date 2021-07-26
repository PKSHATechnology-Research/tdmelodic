# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

unidic_index_map = {
    # see also mecabrc
    "SURFACE": 0,
    "COST": 3,
    "POS1": 4,  # f[0]:   pos1
    "POS2": 5,  # f[1]:   pos2
    "POS3": 6,  # f[2]:   pos3
    "POS4": 7,  # f[3]:   pos4
    "YOMI": 13,  # f[9]:   pron
    "GOSHU": 16,  # f[12]:  goshu
    "ACCENT": 27,  # f[23]:  aType
}

ipadic_index_map = {
    # see also mecabrc
    "SURFACE": 0,
    "COST": 3,
    "POS1": 4,
    "POS2": 5,
    "POS3": 6,
    "POS4": 7,
    "YOMI": 12,
    "GOSHU": 0,  # Not used. Dummy value for now.
    "ACCENT": 0,  # Not used. Dummy value for now.
}

def get_dictionary_index_map(mode):
    if mode == "unidic":
        IDX_MAP = unidic_index_map
    elif mode == "ipadic":
        IDX_MAP = ipadic_index_map
    else:
        IDX_MAP = unidic_index_map
    return IDX_MAP