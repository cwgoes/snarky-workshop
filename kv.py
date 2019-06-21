#!/usr/bin/env python2.7

import subprocess

def cache(func):
    d = {}
    def wrapper(val):
        if val in d:
            return d[val]
        res = func(val)
        d[val] = res
        return res
    return wrapper

def pedersen_hash(val):
    proc = subprocess.Popen(
        ['/home/cwgoes/.opam/snarky/bin/dune', 'exec', '--', 'crypto_util/crypto_util.exe', 'pedersen', val, '-padded-length', '256'],
        cwd = '/home/cwgoes/temporary/snarky',
        stdout = subprocess.PIPE
    )
    output = proc.stdout.read()[:-1]
    print('ext call to hash: {} return {}'.format(val, output))
    return output

pedersen_hash = cache(pedersen_hash)

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

    def calc_all(self):
        hashes = {}
        for k in self.key_range():
            hashes[k] = pedersen_hash(self.get(k))
        for depth in range(1, self.depth)[::-1]:
            for k in key_range(depth):
                hashes[k] = pedersen_hash(hashes[k + '0'][:TRUNCATE] + hashes[k + '1'][:TRUNCATE])
        hashes['root'] = pedersen_hash(hashes['0'][:TRUNCATE] + hashes['1'][:TRUNCATE])
        return hashes

    def root_hash(self):
        return self.calc_all()['root']

    def merkle_path(self, key):
        hashes = self.calc_all()
        path = []
        for depth in range(0, self.depth)[::-1]:
            mod = [x for x in key][:depth + 1]
            mod[depth] = '0' if key[depth] == '1' else '1'
            mod = ''.join(mod)
            path.append(hashes[mod])
        return (path, hashes['root'], hashes[key])
   
    def get(self, key):
        return self.dict[key]

    def set(self, key, value):
        self.dict[key] = value

if __name__ == '__main__':
    t = SparseMerkleTree()
    print('Root hash: {}'.format(t.root_hash()))
    key = '000'
    value = '123'
    print('Setting {} to {}'.format(key, value))
    t.set(key, value)
    print('Merkle path and root and val-hash: {}'.format(t.merkle_path(key)))
