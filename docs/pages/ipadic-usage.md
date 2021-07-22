# Usage of IPADIC-tdmelodic as a MeCab dictionary

## Install IPADIC-tdmelodic
You can install `tdmelodic-ipadic` by replacing all the CSV files with
the generated `*.csv.accent` files, and running the
installation script with appropriate command line options.


```sh
# paths
WORKDIR=/path/to/your/work/dir
NEOLOGD_DIC_DIR=${WORKDIR}/mecab-ipadic-neologd/seed
IPADIC_DIR=${WORKDIR}/mecab-ipadic-2.7.0-XXXX
```

```sh
# copy
for f in `ls ${NEOLOGD_DIC_DIR}/*.csv.accent`
do
    target=`basename $f`
    target=${target%.accent}
    cp $f $IPADIC_DIR/$target
done

for f in `ls ${IPADIC_DIR}/*.csv.accent`
do
    target=`basename $f`
    target=${target%.accent}
    cp $f $IPADIC_DIR/$target
done
```

```sh
# install
cd ${IPADIC_DIR}
./configure --with-dicdir=`mecab-config --dicdir`/tdmelodic-ipadic
make
make install
```


## Use IPADIC-tdmelodic
Here are some examples.

### Example 1

```sh
echo 一昔前は人工知能のプログラミング言語といえばCommon LispやPrologだった。 | \
    mecab -d `mecab-config --dicdir`/tdmelodic-ipadic
```
```
一昔    名詞,一般,*,*,*,*,一昔,ヒトムカシ,ヒ[ト]ムカシ
前      名詞,副詞可能,*,*,*,*,前,マエ,マ]エ
は      助詞,係助詞,*,*,*,*,は,ハ,ワ
人工知能        名詞,固有名詞,一般,*,*,*,人工知能,ジンコウチノウ,ジ[ンコーチ]ノー
の      助詞,連体化,*,*,*,*,の,ノ,ノ
プログラミング言語      名詞,固有名詞,一般,*,*,*,プログラミング言語,プログラミングゲンゴ,プ[ログラミングゲ]ンゴ
と      助詞,格助詞,引用,*,*,*,と,ト,ト]
いえ    動詞,自立,*,*,五段・ワ行促音便,仮定形,いう,イエ,イ[エ]
ば      助詞,接続助詞,*,*,*,*,ば,バ,バ
Common Lisp     名詞,固有名詞,一般,*,*,*,Common Lisp,コモンリスプ,コ[モンリ]スプ
や      助詞,並立助詞,*,*,*,*,や,ヤ,ヤ
Prolog  名詞,固有名詞,一般,*,*,*,Prolog,プロログ,プ[ロログ
だっ    助動詞,*,*,*,特殊・ダ,連用タ接続,だ,ダッ,ダ]ッ
た      助動詞,*,*,*,特殊・タ,基本形,た,タ,タ
。      記号,句点,*,*,*,*,。,。,。
EOS
```

### Example 2

```sh
echo 横浜市中区日本大通 | mecab -d `mecab-config --dicdir`/tdmelodic-ipadic
```
```
横浜市中区日本大通      名詞,固有名詞,地域,一般,*,*,横浜市中区日本大通,ヨコハマシナカクニホンオオドオリ,ヨ[コハマ]シナ[カ]クニ[ホンオード]ーリ
EOS
```

### Example 3

```sh
echo 980hPa | mecab -d `mecab-config --dicdir`/tdmelodic-ipadic
echo 15mm | mecab -d `mecab-config --dicdir`/tdmelodic-ipadic
echo 4月10日 | mecab -d `mecab-config --dicdir`/tdmelodic-ipadic
```
```
980hPa  名詞,固有名詞,一般,*,*,*,980hPa,キュウヒャクハチジュウヘクトパスカル,キュ]ウヒャクハ[チジュウヘクトパ]スカル
EOS
15mm    名詞,固有名詞,一般,*,*,*,15mm,ジュウゴミリメートル,ジュ[ウゴミリメ]ートル
EOS
4月10日 名詞,固有名詞,一般,*,*,*,4月10日,シガツトオカ,シ[ガツトオカ
EOS
```
