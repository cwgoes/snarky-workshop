#!/usr/bin/env python2.7

import subprocess

def pederson_hash(val):
    print('ext call to hash: {}'.format(val))
    proc = subprocess.Popen(
        ['/home/cwgoes/.opam/snarky/bin/dune', 'exec', 'crypto_util/crypto_util.exe', val],
        cwd = '/home/cwgoes/temporary/snarky',
        stdout = subprocess.PIPE
    )
    output = proc.stdout.read()[:-1]
    return output

def flatten(l):
    return [x for y in l for x in y]

def key_range_base(depth):
    if depth == 1:
        return [[0], [1]]
    recur = key_range_base(depth - 1)
    ret = []
    for k in recur:
        ret += [[0] + k]
        ret += [[1] + k]
    return ret

def key_to_string(key):
    return ''.join(str(s) for s in key)

def key_range(depth):
    return sorted(key_to_string(k) for k in key_range_base(depth))

TRUNCATE = 10

class SparseMerkleTree():

    def __init__(self, depth = 3):
        self.depth = depth
        self.dict = {}
        for k in self.key_range():
            self.set(k, '0')

    def key_range(self):
        return key_range(self.depth)

    def root_hash(self):
        hashes = {}
        for k in self.key_range():
            hashes[k] = pederson_hash(self.get(k))
        for depth in range(1, self.depth)[::-1]:
            for k in key_range(depth):
                hashes[k] = pederson_hash(hashes[k + '0'][:TRUNCATE] + hashes[k + '1'][:TRUNCATE])
        return pederson_hash(hashes['0'][:TRUNCATE] + hashes['1'][:TRUNCATE])
   
    def get(self, key):
        return self.dict[key]

    def set(self, key, value):
        self.dict[key] = value

if __name__ == '__main__':
    t = SparseMerkleTree()
    print('Root hash: {}'.format(t.root_hash()))
