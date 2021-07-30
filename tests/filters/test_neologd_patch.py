import unittest
from unittest import TestCase

import argparse
from tdmelodic.filters.neologd_patch import my_add_argument

class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_my_add_argument(self):
        parser = argparse.ArgumentParser()
        my_add_argument(parser, "a", True, "help")
        my_add_argument(parser, "b", True, "help")
        my_add_argument(parser, "c", True, "help")
        my_add_argument(parser, "d", False, "help")
        my_add_argument(parser, "e", False, "help")
        my_add_argument(parser, "f", False, "help")
        args = parser.parse_args(["--a", "--no-b", "--d", "--no-e"])
        assert(args.a is True)
        assert(args.b is False)
        assert(args.c is True)
        assert(args.d is True)
        assert(args.e is False)
        assert(args.f is False)

if __name__ == '__main__':
    unittest.main()