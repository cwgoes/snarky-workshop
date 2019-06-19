set -e

FILE=$1
ARGS=$2
CLI=/home/cwgoes/temporary/snarky/_build/install/default/bin/snarky_cli
PROOF=proof
echo "Running with file: $1, arguments: $ARGS"

rm -f *.pv *.sk *.zkp
time $CLI build $FILE --curve Bn128
time $CLI generate-keys $FILE --curve Bn128
time $CLI prove $FILE $ARGS
time $CLI verify $FILE $ARGS --proof $(ls *.zkp)
