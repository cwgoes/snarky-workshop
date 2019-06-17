set -e

FILE=$1
ARGS=$2
PROOF=proof
echo "Running with file: $1, arguments: $ARGS"

rm -f *.pv *.sk *.zkp
snarky_cli generate-keys $FILE --curve Bn128
snarky_cli prove $FILE $ARGS
snarky_cli verify $FILE $ARGS --proof $(ls *.zkp)
