# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import sys

def count_lines(fp):
    if fp is not sys.stdin:
        for i, l in enumerate(fp):
            pass
        fp.seek(0)
        return i + 1
    else:
        return None
