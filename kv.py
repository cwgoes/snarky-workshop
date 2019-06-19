#!/usr/bin/env python2.7

import subprocess

def pederson_hash(val):
    proc = subprocess.Popen(
        ['/home/cwgoes/.opam/snarky/bin/dune', 'exec', 'crypto_util/crypto_util.exe', val],
        cwd = '/home/cwgoes/temporary/snarky',
        stdout = subprocess.PIPE
    )
    output = proc.stdout.read()[:-1]
    return output

def flatten(l):
    return [x for y in l for x in y]

def key_range(depth):
    if depth == 1:
        return [[0], [1]]
    recur = key_range(depth - 1)
    ret = []
    for k in recur:
        ret += [[0] + k]
        ret += [[1] + k]
    return ret

class SparseMerkleTree():

    def __init__(self, depth = 3):
        self.depth = depth
        self.dict = {}

    def root_hash(self):
        ## todo cache me
        return 0
   
    def get(key):
        return ''

    def set(key, value):
        return

if __name__ == '__main__':
    print(key_range(3))
    print(pederson_hash('hello world'))
