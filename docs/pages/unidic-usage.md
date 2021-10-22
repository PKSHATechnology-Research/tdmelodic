# Usage of UniDic-tdmelodic as a MeCab dictionary

## Install UniDic-tdmelodic

You can install `tdmelodic` (`tdmelodic-unidic`) by copying the content of `tdmelodic.csv` we have just created
to the UniDic default dictionary (`lex.csv`), and running the
installation script with appropriate command line options.

Firstly, specify the file paths.
```sh
WORKDIR=/path/to/your/work/dir
UNIDIC_ZIP_PATH=/path/to/your/unidic/file/unidic-mecab_kana-accent-2.1.2_src.zip
TDMELODIC_CSV=${WORKDIR}/tdmelodic.csv
```

Then unzip the UniDic file.
```sh
cd ${WORKDIR}
cp ${UNIDIC_ZIP_PATH} .
unzip unidic-mecab_kana-accent-2.1.2_src.zip
```

Concatenate the dictionaries.
```sh
cd ${WORKDIR}/unidic-mecab_kana-accent-2.1.2_src
cp lex.csv lex_bak.csv # backup
cat ${TDMELODIC_CSV} >> lex.csv
```

Finally, install `tdmelodic`.
```sh
./configure --with-dicdir=`mecab-config --dicdir`/tdmelodic
make
make install
```

## Use UniDic-tdmelodic
Here are some examples.

### Example 1

```sh
echo 一昔前は人工知能のプログラミング言語といえばCommon LispやPrologだった。 | \
    mecab -d `mecab-config --dicdir`/tdmelodic/
```
```
一昔	ヒトムカシ	ヒトムカシ	一昔	名詞-普通名詞-一般			2,3
前	マエ	マエ	前	名詞-普通名詞-副詞可能			1
は	ワ	ハ	は	助詞-係助詞
人工知能	ジ[ンコーチ]ノー	ジンコウチノウ	人工知能	名詞-固有名詞-一般			@
の	ノ	ノ	の	助詞-格助詞
プログラミング言語	プ[ログラミングゲ]ンゴ	プログラミングゲンゴ	プログラミング言語	名詞-固有名詞-一般			@
と	ト	ト	と	助詞-格助詞
いえ	イエ	イウ	言う	動詞-一般	五段-ワア行	仮定形-一般	0
ば	バ	バ	ば	助詞-接続助詞
Common Lisp	コ[モンリ]スプ	コモンリスプ	Common Lisp	名詞-固有名詞-一般			@
や	ヤ	ヤ	や	助詞-副助詞
Prolog	プ[ロログ	プロログ	Prolog	名詞-固有名詞-一般			@
だっ	ダッ	ダ	だ	助動詞	助動詞-ダ	連用形-促音便
た	タ	タ	た	助動詞	助動詞-タ	終止形-一般
。			。	補助記号-句点
EOS
```
Cf.

```sh
echo 一昔前は人工知能のプログラミング言語といえばCommon LispやPrologだった。 | \
    mecab -d `mecab-config --dicdir`/unidic/
```
```
一昔	ヒトムカシ	ヒトムカシ	一昔	名詞-普通名詞-一般			2,3
前	マエ	マエ	前	名詞-普通名詞-副詞可能			1
は	ワ	ハ	は	助詞-係助詞
人工	ジンコー	ジンコウ	人工	名詞-普通名詞-一般			0
知能	チノー	チノウ	知能	名詞-普通名詞-一般			1
の	ノ	ノ	の	助詞-格助詞
プログラミング	プログラミング	プログラミング	プログラミング-programming	名詞-普通名詞-サ変可能			4
言語	ゲンゴ	ゲンゴ	言語	名詞-普通名詞-一般			1
と	ト	ト	と	助詞-格助詞
いえ	イエ	イウ	言う	動詞-一般	五段-ワア行	仮定形-一般	0
ば	バ	バ	ば	助詞-接続助詞
Common	Common	Common	Common	名詞-普通名詞-一般			0
Lisp	Lisp	Lisp	Lisp	名詞-普通名詞-一般			0
や	ヤ	ヤ	や	助詞-副助詞
Prolog	Prolog	Prolog	Prolog	名詞-普通名詞-一般			0
だっ	ダッ	ダ	だ	助動詞	助動詞-ダ	連用形-促音便
た	タ	タ	た	助動詞	助動詞-タ	終止形-一般
。			。	補助記号-句点
EOS
```

### Example 2

```sh
echo 横浜市中区日本大通 | mecab -d `mecab-config --dicdir`/tdmelodic
```
```
横浜市中区日本大通	ヨ[コハマ]シナ[カ]クニ[ホンオオド]オリ	ヨコハマシナカクニホンオオドオリ	横浜市中区日本大通	名詞-固有名詞-地名-一般			@
EOS
```

```sh
echo 横浜市中区日本大通 | mecab -d `mecab-config --dicdir`/unidic
```
```
横浜	ヨコハマ	ヨコハマ	ヨコハマ	名詞-固有名詞-地名-一般			0
市中	シチュー	シチュウ	市中	名詞-普通名詞-一般			0,2
区	ク	ク	区	名詞-普通名詞-一般			1
日本	ニッポン	ニッポン	日本	名詞-固有名詞-地名-国			3
大通	ダイツー	ダイツウ	大通	名詞-普通名詞-一般			3,0
EOS
```

### Example 3

```sh
echo 980hPa | mecab -d `mecab-config --dicdir`/tdmelodic/
echo 15mm | mecab -d `mecab-config --dicdir`/tdmelodic/
echo 4月10日 | mecab -d `mecab-config --dicdir`/tdmelodic/
```
```
980hPa	キュ]ーヒャクハ[チジュウヘクトパ]スカル	キュウヒャクハチジュウヘクトパスカル	980hPa	名詞-固有名詞-一般			@
EOS
15mm	ジュ[ウゴミリメ]ートル	ジュウゴミリメートル	15mm	名詞-固有名詞-一般			@
EOS
4月10日	シ[ガツトオカ	シガツトオカ	4月10日	名詞-固有名詞-一般			@
EOS
```
