set -e

FILE=$1
ARGS=$2
PROOF=proof
echo "Running with file: $1, arguments: $ARGS"

rm -f *.pv *.sk *.zkp
time snarky_cli generate-keys $FILE --curve Bn128
time snarky_cli prove $FILE $ARGS
time snarky_cli verify $FILE $ARGS --proof $(ls *.zkp)
