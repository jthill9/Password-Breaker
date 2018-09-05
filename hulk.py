#!/usr/bin/env python3

import functools
import hashlib
import itertools
import multiprocessing
import os
import string
import sys

# Constants

ALPHABET    = string.ascii_lowercase + string.digits
ARGUMENTS   = sys.argv[1:]
CORES       = 1
HASHES      = 'hashes.txt'
LENGTH      = 1
PREFIX      = ''

# Functions

def usage(exit_code=0):
    print('''Usage: {} [-a alphabet -c CORES -l LENGTH -p PREFIX -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file'''.format(os.path.basename(sys.argv[0])))
    sys.exit(exit_code)

def sha1sum(s):
    ''' Generate sha1 digest for given string.

    >>> sha1sum('abc')
    'a9993e364706816aba3e25717850c26c9cd0d89d'

    >>> sha1sum('wake me up inside')
    '5bfb1100e6ef294554c1e99ff35ad11db6d7b67b'

    >>> sha1sum('baby now we got bad blood')
    '9c6d9c069682759c941a6206f08fb013c55a0a6e'
    '''
    # TODO: Implement

    s_encoded = str.encode(s)
    m = hashlib.sha1(s_encoded)

    return m.hexdigest()

def permutations(length, alphabet=ALPHABET):
    ''' Recursively yield all permutations of alphabet up to provided length.

    >>> list(permutations(1, 'ab'))
    ['a', 'b']

    >>> list(permutations(2, 'ab'))
    ['aa', 'ab', 'ba', 'bb']

    >>> list(permutations(1))       # doctest: +ELLIPSIS
    ['a', 'b', ..., '9']

    >>> list(permutations(2))       # doctest: +ELLIPSIS
    ['aa', 'ab', ..., '99']

    >>> import inspect; inspect.isgeneratorfunction(permutations)
    True
    '''
    # TODO: Implement as generator

    # Base case for recursion
    if length == 0:
        yield ''

    # Use recursion to yield each permutation
    else:
        for char in alphabet:
            # Second base case for recursion
            if length == 1:
                yield char
            else:
                for part in permutations(length-1, alphabet):
                    yield (char + part)



def smash(hashes, length, alphabet=ALPHABET, prefix=''):
    ''' Return all password permutations of specified length that are in hashes

    >>> smash([sha1sum('ab')], 2)
    ['ab']

    >>> smash([sha1sum('abc')], 2, prefix='a')
    ['abc']

    >>> smash(map(sha1sum, 'abc'), 1, 'abc')
    ['a', 'b', 'c']
    '''
    # TODO: Implement with list or generator comprehensions

    passwords = [prefix + permutation for permutation in permutations(length, alphabet) if sha1sum(prefix + permutation) in hashes]

    return passwords

# Main Execution

if __name__ == '__main__':
    # Parse command line arguments
    while len(ARGUMENTS) != 0:
        arg = ARGUMENTS.pop(0)
        if arg == '-a':
            ALPHABET = ARGUMENTS.pop(0)
        elif arg == '-c':
            CORES = int(ARGUMENTS.pop(0))
        elif arg == '-l':
            LENGTH = int(ARGUMENTS.pop(0))
        elif arg == '-p':
            PREFIX = ARGUMENTS.pop(0)
        elif arg == '-s':
            HASHES = ARGUMENTS.pop(0)
        elif arg == '-h':
            usage(0)
        else:
            usage(1)

    # Load hashes list
    given_hashes = set()
    for line in open(HASHES):
        line = line.rstrip()
        given_hashes.add(line)

    # Execute smash function
    if LENGTH == 1 or CORES == 1:
        passwords = smash(hashes=given_hashes, length=LENGTH, alphabet=ALPHABET, prefix=PREFIX)
    else:
        prefixes = [PREFIX + a for a in ALPHABET]
        subsmash = functools.partial(smash, given_hashes, LENGTH - 1, ALPHABET)
        pool = multiprocessing.Pool(CORES)
        passwords = itertools.chain.from_iterable(pool.imap(subsmash, prefixes))

    #Pool = multiprocessing.Pool(CORES)

    # Print passwords
    for password in passwords:
        print(password)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
