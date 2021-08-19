# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

# -*- coding: utf-8 -*-
import sys
import os
import argparse
import tempfile

from .neologd_patch import NeologdPatch
from .neologd_rmdups import rmdups

class Preprocess(object):
    def __init__(self, flag_rmdups, neologd_patch):
        self.flag_rmdups = flag_rmdups
        self.neologd_patch_module = neologd_patch

    def do_rmdups(self, fp_in):
        fp_tmp = tempfile.NamedTemporaryFile("w+")
        print("... creating a temporary file", fp_tmp.name, file=sys.stderr)
        rmdups(fp_in, fp_tmp)
        fp_tmp.seek(0)
        fp_in.close() # CPython's GC will automatically closes the previous fp_in without doing this
        fp_in = fp_tmp
        return fp_in

    def do_neologd_patch(self, fp_in):
        fp_tmp = tempfile.NamedTemporaryFile("w+")
        print("... creating a temporary file", fp_tmp.name, file=sys.stderr)
        self.neologd_patch_module(fp_in, fp_tmp)
        fp_tmp.seek(0)
        fp_in.close() # CPython's GC will automatically closes the previous fp_in without doing this
        fp_in = fp_tmp
        return fp_in

    def copy_temp_to_output(self, fp_in, fp_out):
        # output
        for l in fp_in:
            fp_out.write(l)
        fp_in.close()
        fp_out.close()

    def __call__(self, fp_in, fp_out):
        print("ℹ️  [ Info ]", file=sys.stderr)
        NeologdPatch.message("* {} Duplicate entried will{}be removed.", self.flag_rmdups)
        if self.flag_rmdups:
            fp_in = self.do_rmdups(fp_in)

        fp_in = self.do_neologd_patch(fp_in)

        print("💾  [ Saving ]", file=sys.stderr)
        self.copy_temp_to_output(fp_in, fp_out)
        print("🍺  [ Done ]", file=sys.stderr)

def my_add_argument(parser, option_name, default, help_):
    help_ = help_ + " <default={}>".format(str(default))
    if sys.version_info >= (3, 9):
        parser.add_argument("--" + option_name,
            action=argparse.BooleanOptionalAction,
            default=default,
            help=help_)
    else:
        parser.add_argument("--" + option_name,
            action="store_true",
            default=default,
            help=help_)
        parser.add_argument("--no-" + option_name,
            action="store_false",
            dest=option_name,
            default=default)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        nargs='?',
        type=argparse.FileType("r"),
        default=sys.stdin,
        help='input CSV file (NEologd dicitionary file) <default=STDIN>')
    parser.add_argument(
        '-o', '--output',
        nargs='?',
        type=argparse.FileType("w"),
        default=sys.stdout,
        help='output CSV file <default=STDOUT>')
    parser.add_argument(
        "-m", "--mode",
        type=str,
        choices=["unidic", "ipadic"],
        default="unidic",
        help="dictionary format type <default=unidic>",
    )
    my_add_argument(parser, "rmdups", True, "remove duplicate entries or not")
    my_add_argument(parser, "rm_hashtag", True, "remove hash tags or not")
    my_add_argument(parser, "rm_noisy_katakana", True, "remove noisy katakana words or not")
    my_add_argument(parser, "rm_person", False, "remove person names or not")
    my_add_argument(parser, "rm_emoji", False, "remove emojis or not")
    my_add_argument(parser, "rm_symbol", False, "remove symbols or not")
    my_add_argument(parser, "rm_numeral", False, "remove numerals or not")
    my_add_argument(parser, "rm_wrong_yomi", True, "remove words with possibly wrong yomi or not")
    my_add_argument(parser, "rm_special_particle", True, "remove words with special particles \"は\" or \"へ\"")
    my_add_argument(parser, "cor_longvow", True, "correct long vowel errors or not")
    my_add_argument(parser, "cor_yomi_num", True, "correct the yomi of numerals or not")
    my_add_argument(parser, "normalize", False, "normalize the surface forms by applying "
        "NFKC Unicode normalization, "
        "capitalization of alphabets, "
        "and "
        "hankaku-to-zenkaku converter.")

    args = parser.parse_args()
    if args.input == args.output:
        print("[ Error ] intput and output files should be different.", file=sys.stderr)
        sys.exit(0)
    try:
        preprocess = Preprocess(args.rmdups, NeologdPatch(**vars(args)))
        preprocess(args.input, args.output)
    except Exception as e:
        print(e, file=sys.stderr)

if __name__ == '__main__':
    main()