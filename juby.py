from sage.all import *
# TODO remove all sage code, make it purely python so can use python3

# TODO refactor some of the code


# bits are in little endian in bit format
def bit_unpack(y):
    # 1000 > 945 = 3 * 63 * 5
    for i in range(1000):
        if y < 2**i:
            bit_length = i-1
            break
    bits = []
    for i in range(bit_length):
        if (y & 2**i) == 2**i:
            bits.append(1)
        else:
            bits.append(0)
    return bits


def bit_pack(bits, index):
    result = 0
    for i in range(1, len(bits)):
        result += bits[i-1]*(2**(index*(i-1)))
    return result


def bit_unpack_true(bits):
    tf = []
    for i in bits:
        if i == 1:
            tf.append(True)
        elif i == 0:
            tf.append(False)
    return tf


class Jubjub:

    def __init__(self, r, d, a):
        # TODO refactor global variables into the initialization of jubjub

        self.r = r
        self.d = d
        self.a = a
        self.zero = JubPoint(self, Fr(0), Fr(1))

    # obtain all the points the long way
    def get_points(self):
        points = []
        for x in range(self.r):
            for y in range(self.r):
                if JubPoint(x,y).is_jubjub():
                    print('(x,y) = ', x, y)
                    points.append([x, y])
        return points

    def get_order(self):

        return len(self.get_points())

    def is_jubjub(self, x, y):
        if Fr(self.a * (x**2) + (y**2)) == Fr(1 + self.d * (x**2) * (y**2)):
            return True
        else:
            return False

    # TODO expand implementation by implementing these
    # def group_hash(tag, pers, params):
    #     pass
    #
    # def find_group_hash(m, pers, params):
    #     pass


class PedersenHash:

    def __init__(self, juby, generators):
        if not isinstance(juby, Jubjub):
            raise TypeError('The curve is not a jubjub curve')
        for i in range(len(generators)):
            if not juby.is_jubjub(generators[i].x, generators[i].y):
                raise ValueError('Your points are not generators of jubjub')
        self.juby = juby
        self.gens = generators

    def bit_chunks(self, m):
        bits = bit_unpack(m)
        bit_length = len(bits)
        if bit_length > 946:
            raise ValueError('Your message is too big')
        while (bit_length % 3) != 0:
            bits.append(0)
            bit_length += 1

        chunks = []
        segments = []
        for i in range(5):
            segments.append(bits[i*189:(i+1)*189])
            chunks.append([])
            for j in range(63):
                chunks[i].append(segments[i][j*3:(j+1)*3])

        return chunks

    # compute enc(m_j) as in the documentation
    def encode_chunk(self, chunk):

        if len(chunk) != 3:
            #raise ValueError('The chunk you are encoding is too long: ', chunk)
            return 0
        result = (1 - 2*chunk[2])*(1 + chunk[0] + 2*chunk[1])
        return result

    # compute <M_i> as in the documentation
    def encoding_product(self, chunks):
        # chunks contains 63 chunks of 3 bits each (there are five like these)

        enc = 0

        for index, chunk in enumerate(chunks):
            enc += self.encode_chunk(chunk) * (2**(4*index))
        return enc

    def pedersen_hash_to_point(self, m):

        chunks = self.bit_chunks(m)
        #print('this is the chunks', chunks)
        point = self.juby.zero

        for i in range(5):
            print '> These are the chunks that will be encoded ', chunks[i]
            print '> Computing', i, 'position, for gen (', hex(int(self.gens[i].x)), ',', hex(int(self.gens[i].y)), '),'
            print '> where point is:(', hex(int(point.x)), ',', hex(int(point.y)), ')'
            print ''

            point = point + self.gens[i].scalar_mult(self.encoding_product(chunks[i]) % rj)

        return point

    def pedersen_hash(self, m):

        return self.pedersen_hash_to_point(m).jub_extract()


class JubPoint:

    def __init__(self, juby, x, y):
        if Fr(juby.a * x**2 + y**2) == Fr(1 + juby.d * x**2 * y**2):
            self.x = Fr(x)
            self.y = Fr(y)
            self.juby = juby
        else:
            raise TypeError('The points do not belong to the JubJub curve')

    def __add__(self, other):
        if not isinstance(other, JubPoint):
            raise TypeError('The object you are adding is not a jubjub point', other)

        x3 = Fr(Fr(self.x * other.y + self.y * other.x) / Fr(1 + d * self.x * other.x * self.y * other.y))
        y3 = Fr(Fr(self.y * other.y + self.x * other.x) / Fr(1 - d * self.x * other.x * self.y * other.y))

        return JubPoint(self.juby, x3, y3)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def double(self):

        return self + self

    def scalar_mult(self, s):
        s = s % rj

        # double and add algo
        bits = bit_unpack(s)
        num_ops = len(bits)
        doubling = self
        result = self.juby.zero
        for i in range(num_ops):
            if bits[i] == 1:
                result = result + doubling
            doubling = doubling.double()

        return result

    def jub_extract(self):

        return hex(int(self.x))

    # def order(self):
    #     pass
    #
    # def get_random_point(self):
    #     pass


# test

def test_pedersen_hash(m):
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

    # print bits as array of true or false for rust comparison
    print 'The message,',m,'has the following bit decomposition', bit_unpack_true(bit_unpack(m)),'\n'

    # return pedersen hash
    return peder.pedersen_hash(m)


if __name__ == '__main__':

    #order of underlying field, derived from BLS
    r = 52435875175126190479447740508185965837690552500527637822603658699938581184513
    Fr = (GF(r))

    # curve parameters
    d = Fr(-(Fr(10240)/Fr(10241)))
    a = Fr(-1)

    # curve subgroup order and cofactor
    rj = 6554484396890773809930967563523245729705921265872317281365359162392183254199
    hj = 8

    # trial where expected outcome of pedersen_hash(211111) is
    # 0x17f24895625db0f531472ea0d0ad0d691b4333774b6716693fa5e016dfe80ec2L
    m = 211111
    print 'This is the pedersen hash: '+ test_pedersen_hash(m)

    # test vectors
    #print 'This is the hash of all one bits: '+ test_pedersen_hash(2**946-1)
    #print 'This is the hash of all 0 bits: ' + test_pedersen_hash(0)

