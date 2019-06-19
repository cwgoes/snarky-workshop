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

if __name__ == '__main__':
    print(pederson_hash('hello world'))
