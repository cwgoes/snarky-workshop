#!/usr/bin/env python2.7

from juby import *
from sagemath.all import *

def pederson_init():
    r = 52435875175126190479447740508185965837690552500527637822603658699938581184513
    Fr = (GF(r))

    # curve parameters
    d = Fr(-(Fr(10240)/Fr(10241)))
    a = Fr(-1)

    # initialize jubjub
    juby = Jubjub(r, d, a)

    # generators for pedersen hash personalization
    G0 = JubPoint(juby, Fr(0x73c016a42ded9578b5ea25de7ec0e3782f0c718f6f0fbadd194e42926f661b51),
                  Fr(0x289e87a2d3521b5779c9166b837edc5ef9472e8bc04e463277bfabd432243cca))
    G1 = JubPoint(juby, Fr(0x15a36d1f0f390d8852a35a8c1908dd87a361ee3fd48fdf77b9819dc82d90607e),
                  Fr(0x015d8c7f5b43fe33f7891142c001d9251f3abeeb98fad3e87b0dc53c4ebf1891))
    G2 = JubPoint(juby, Fr(0x664321a58246e2f6eb69ae39f5c84210bae8e5c46641ae5c76d6f7c2b67fc475),
                  Fr(0x362e1500d24eee9ee000a46c8e8ce8538bb22a7f1784b49880ed502c9793d457))
    G3 = JubPoint(juby, Fr(0x323a6548ce9d9876edc5f4a9cff29fd57d02d50e654b87f24c767804c1c4a2cc),
                  Fr(0x2f7ee40c4b56cad891070acbd8d947b75103afa1a11f6a8584714beca33570e9))
    G4 = JubPoint(juby, Fr(0x3bd2666000b5479689b64b4e03362796efd5931305f2f0bf46809430657f82d1),
                  Fr(0x494bc52103ab9d0a397832381406c9e5b3b9d8095859d14c99968299c3658aef))

    gens = [G0, G1, G2, G3, G4]

    # initialize pedersen hash
    peder = PedersenHash(juby, gens)

    return peder

if __name__ == '__main__':
    pederson = pederson_init()
    print('ok')
