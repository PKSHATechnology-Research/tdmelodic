#!/usr/bin/env bash

# --------------------------------------------------------------------------------------------------------------------
# default values
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
NEOLOGD_DIR=$(    readlink -m ${SCRIPT_DIR}/../../mecab-unidic-neologd)
DIC_PATH=$(       readlink -m ${SCRIPT_DIR}/../../tdmelodic.csv)
UNIDIC_ZIP_PATH=$(readlink -m ${SCRIPT_DIR}/../unidic-mecab_kana-accent-2.1.2_src.zip)
NAME_OF_DIC=tdmelodic

YMD=`ls -ltr \`find ${NEOLOGD_DIR}/seed/mecab-unidic-user-dict-seed.*.csv.xz\` | egrep -o '[0-9]{8}' | tail -1`

INFO=" [ INFO ] "
PREFIX="[ neologd -> ${NAME_OF_DIC} ] "

DIR_FOR_DEBUG=debug
if [ ! -e $DIR_FOR_DEBUG ]; then mkdir $DIR_FOR_DEBUG; fi


# --------------------------------------------------------------------------------------------------------------------
# command line parsing
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -d|--dictionary)
        DIC_PATH=$(readlink -m "$2")
        shift
        shift
    ;;
    -n|--neologd)
        NEOLOGD_DIR=$(readlink -m "$2")
        shift
        shift
    ;;
    -u|--unidic)
        UNIDIC_ZIP_PATH=$(readlink -m "$2")
        shift
        shift
    ;;
    -p|--prefix)
        NAME_OF_DIC=$(readlink -m "$2")
        shift
        shift
    ;;
    -y|--ymd)
        YMD=$(readlink -m "$2")
        shift
        shift
    ;;
    *)
        echo $INFO ignored option ....... "$1"
        shift
    ;;
esac
done

# --------------------------------------------------------------------------------------------------------------------
## show info

echo "==============================================================================================================="
echo "$INFO ${NAME_OF_DIC} dictionary is at ...."
echo "              $DIC_PATH"
echo "$INFO neologd directory is at ......."
echo "              $NEOLOGD_DIR"
echo "$INFO unidic zip file is at ........."
echo "              $UNIDIC_ZIP_PATH"
echo "$INFO dictionary name is $NAME_OF_DIC"
echo "$INFO yyyymmdd is $YMD"
echo "==============================================================================================================="


# --------------------------------------------------------------------------------------------------------------------
## neologd whole installer
IN=${NEOLOGD_DIR}/bin/install-mecab-unidic-neologd
OUT=${NEOLOGD_DIR}/bin/install-${NAME_OF_DIC}
echo "$PREFIX modifying the installation script"
echo "$PREFIX     from .... ${IN}"
echo "$PREFIX     to ...... ${OUT}"
sed -e "s/mecab-unidic-neologd/${NAME_OF_DIC}/g;
        s/make curl sed/make sed/g;
        s/file//g;"\
    ${IN} > ${OUT}
cp ${OUT} ${DIR_FOR_DEBUG}
echo "==============================================================================================================="


# --------------------------------------------------------------------------------------------------------------------
# unidic installer
# * rename unidic-mecab-2.1.2 -> unidic-mecab_kana-accent-2.1.2
# * remove curl and related lined, since we have already downloaded the dictionary file
echo $PREFIX Converting UniDic installer
sed -e "s/unidic-mecab-/unidic-mecab_kana-accent-/g;
         s/cd \${TMP_DIR_PATH}/mv \${MECAB_UNIDIC_FILE_NAME} \${TMP_DIR_PATH}; cd \${TMP_DIR_PATH}/g;
         /^curl/d;
         /^MECAB_UNIDIC_URL/d;" \
    ${NEOLOGD_DIR}/libexec/install-mecab-unidic.sh > ${NEOLOGD_DIR}/libexec/install-mecab-unidic_kana-accent.sh
echo "==============================================================================================================="

# --------------------------------------------------------------------------------------------------------------------
## neologd make script
# * mecab-unidic-neologd -> tdmeldic
# * set YMD
# * curl: do not download unidic*.zip again
# * copy csv instead of unxz.
IN=${NEOLOGD_DIR}/libexec/make-mecab-unidic-neologd.sh
OUT=${NEOLOGD_DIR}/libexec/make-${NAME_OF_DIC}.sh
echo "$PREFIX modifying the make script"
echo "$PREFIX     from .... ${IN}"
echo "$PREFIX     to ...... ${OUT}"
sed -e "s/mecab-unidic-neologd/${NAME_OF_DIC}/g;
        s/unidic-mecab-2.1.2/unidic-mecab_kana-accent-2.1.2/g;
        s/^NEOLOGD_DIC_NAME=.*/TDMELODIC_DIC_NAME=\${ORG_DIC_NAME}-${NAME_OF_DIC}-\${YMD}/g;
        s/NEOLOGD_DIC_DIR/TDMELODIC_DIC_DIR/g;
        s/NEOLOGD_DIC_NAME/TDMELODIC_DIC_NAME/g;
        s/^YMD=.*$/YMD=${YMD}/g;
        s/mecab-unidic-user-dict-seed/${NAME_OF_DIC}/g;
        s/^SEED_FILE_NAME=.*$/SEED_FILE_NAME=${NAME_OF_DIC}.${YMD}.csv/g;
        s/.csv.xz/.csv/g;
        s/^cp.*$/cp \${BASEDIR}\/..\/seed\/\${SEED_FILE_NAME} \${TDMELODIC_DIC_DIR}/g;
        /^unxz/d;
        /^*curl/d" \
    ${IN} > ${OUT}
cp ${OUT} ${DIR_FOR_DEBUG}

## copy dictionary instead of unxz-ing one.
IN=${DIC_PATH}
OUT=$NEOLOGD_DIR/seed/${NAME_OF_DIC}.${YMD}.csv
echo "$PREFIX copying dictionary file"
echo "$PREFIX     from .... ${IN}"
echo "$PREFIX     to ...... ${OUT}"
cp ${IN} ${OUT}
cp ${OUT} ${DIR_FOR_DEBUG}

## copy unidic zip file instead of downloading it
echo "$PREFIX Copying the UniDic zip file to a NEologd directory"
echo "$PREFIX     from ... ${UNIDIC_ZIP_PATH}"
echo "$PREFIX     to ..... ${NEOLOGD_DIR}/build"
if [ ! -e ${NEOLOGD_DIR}/build/ ]; then
    mkdir ${NEOLOGD_DIR}/build/
fi
cp ${UNIDIC_ZIP_PATH} ${NEOLOGD_DIR}/build/
echo "==============================================================================================================="


# --------------------------------------------------------------------------------------------------------------------
## neologd test script
# テストは省略する
OUT=${NEOLOGD_DIR}/libexec/test-${NAME_OF_DIC}.sh
echo "$PREFIX generating test script that does nothing"
echo "$PREFIX     to ...... ${OUT}"

echo "#!/usr/bin/env bash" > ${OUT}
chmod 777 ${OUT}
cp ${OUT} ${DIR_FOR_DEBUG}
echo "==============================================================================================================="

# --------------------------------------------------------------------------------------------------------------------
## neologd install script
# * mecab-unidic-neologd -> tdmeldic
# * set YMD
IN=${NEOLOGD_DIR}/libexec/install-mecab-unidic-neologd.sh
OUT=${NEOLOGD_DIR}/libexec/install-${NAME_OF_DIC}.sh
echo "$PREFIX modifying the installation script"
echo "$PREFIX     from .... ${IN}"
echo "$PREFIX     to ...... ${OUT}"

sed -e "s/mecab-unidic-neologd/${NAME_OF_DIC}/g;
        s/^YMD=.*$/YMD=${YMD}/g;
        s/unidic-mecab-2.1.2/unidic-mecab_kana-accent-2.1.2/g;
        s/2.1.2_src-neologd-/2.1.2_src-${NAME_OF_DIC}-/g;
        s/user-dict/${NAME_OF_DIC}/g" \
    ${IN} > ${OUT}
cp ${OUT} ${DIR_FOR_DEBUG}
echo "==============================================================================================================="
