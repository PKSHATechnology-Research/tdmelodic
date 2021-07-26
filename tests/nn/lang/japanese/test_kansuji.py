import unittest
from unittest import TestCase
from tdmelodic.nn.lang.japanese.kansuji import num2kansuji as N
from tdmelodic.nn.lang.japanese.kansuji import numeric2kanji as NN

class TestWordType(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(N("123"), "百二十三")
        self.assertEqual(N("100"), "百")
        self.assertEqual(N("103"), "百三")
        self.assertEqual(N("111"), "百十一")
        self.assertEqual(N("123456"), "十二万三千四百五十六")

    def test_float(self):
        self.assertEqual(N("12."), "十二")
        self.assertEqual(N("12.345"), "十二点三四五")
        self.assertEqual(N(".345"), "零点三四五")
        self.assertEqual(N("3.141592"), "三点一四一五九二")
        self.assertEqual(N("0.0001"), "零点零零零一")

    def test_issenman(self):
        self.assertEqual(N("100010001000"), "一千億一千万千")
        self.assertEqual(N("100011001000"), "一千億千百万千")

    def test_zeros(self):
        self.assertEqual(N("1020304050607080"), "千二十兆三千四十億五千六十万七千八十")

    def test_suji_in_text(self):
        self.assertEqual(NN("<BOS>金額は1234567円です<EOS>"),
            "<BOS>金額は百二十三万四千五百六十七円です<EOS>")
        self.assertEqual(NN("１２３４５６は３４.５で、さらに0.１２３４５になります。0.1.2.3.4."),
            "十二万三千四百五十六は三十四点五で、さらに零点一二三四五になります。零点一点二点三点四点")
        self.assertEqual(NN("1000000円、10000000円、100000000円、1000円、100000000000円"),
            "百万円、一千万円、一億円、千円、一千億円")

if False:
    # tests
    print(N("123412341234"))
    print(N("123412341234123400001234"))
    print(N("12345678901234567890123456789012345678901234567890123456789012345678901"))
    print(N("123456789012345678901234567890123456789012345678901234567890123456789012"))
    print(N("1234567890123456789012345678901234567890123456789012345678901234567890123"))

    print( "----------" )
    print(N("100010001000", mode='replace'))
    print(N("100011001000", mode='replace'))
    print(N("1020304050607080", mode='replace'))
    print(N("12345678901234567890123456789012345678901234567890123456789012345678901", mode='replace'))
