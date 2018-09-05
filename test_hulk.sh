#!/bin/bash

SCRIPT=${1:-hulk.py}
WORKSPACE=/tmp/$SCRIPT.$(id -u)
FAILURES=0

error() {
    echo "$@"
    [ -s $WORKSPACE/test ] && (echo ; cat $WORKSPACE/test; echo; rm $WORKSPACE/test)
    FAILURES=$((FAILURES + 1))
}

cleanup() {
    STATUS=${1:-$FAILURES}
    rm -fr $WORKSPACE
    exit $STATUS
}

mkdir $WORKSPACE

trap "cleanup" EXIT
trap "cleanup 1" INT TERM

echo "Testing $SCRIPT ..."

printf " %-40s ... " "$SCRIPT is executable"
if [ ! -x $SCRIPT ]; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT has usage"
if ! ./hulk.py -h 2>&1 | grep -q -i usage > /dev/null; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT doctest"
python3 -m doctest $SCRIPT &> $WORKSPACE/test
if [ $? -ne 0 ]; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT length 1"
if [ $(./$SCRIPT -s hashes.txt -l 1 | wc -l) -ne 36 ]; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT length 2"
if [ $(./$SCRIPT -s hashes.txt -l 2 | wc -l) -ne 3 ]; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT length 3"
if [ $(./$SCRIPT -s hashes.txt -l 3 | wc -l) -ne 232 ]; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT length 2 (CORES: 2)"
if [ $(./$SCRIPT -c 2 -s hashes.txt -l 2 | wc -l) -ne 3 ]; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT length 3 (CORES: 2)"
if [ $(./$SCRIPT -c 2 -s hashes.txt -l 3 | wc -l) -ne 232 ]; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT length 2 (PREFIX: a)"
if [ $(./$SCRIPT -p a -s hashes.txt -l 2 | wc -l) -ne 6 ]; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT length 2 (PREFIX: a, CORES: 2)"
if [ $(./$SCRIPT -c 2 -p a -s hashes.txt -l 2 | wc -l) -ne 6 ]; then
    error "Failure"
else
    echo "Success"
fi

printf " %-40s ... " "$SCRIPT length 3 (PREFIX: a, CORES: 2)"
if [ $(./$SCRIPT -c 2 -p a -s hashes.txt -l 3 | wc -l) -ne 30 ]; then
    error "Failure"
else
    echo "Success"
fi

TESTS=$(($(grep -c Success $0) - 1))
echo "   Score $(echo "scale=2; ($TESTS - $FAILURES) / $TESTS.0 * 7.0" | bc)"
echo
