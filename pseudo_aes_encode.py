import utility
from SeparatePrograms.suma_multiplicacion import *
import functools

class Encoder:
    def __init__(self, key):
        self.key = key
        if not self.check_key():
            print("Invalid key")
            exit()

    def check_key(self):
        if(self.key_determinants_nonzero()):
            if(
                add(add(add(self.key[40:44], self.key[44:48]), self.key[48:52]), BitArray(bin = "0b0001")).int != 0
                and
                add(add(add(self.key[52:56], self.key[56:60]), self.key[60:64]), BitArray(bin = "0b0001")).int != 0
            ):
                print("Valid key")
                return True

    def key_determinants_nonzero(self):
        '''
        Matrix determinant using cofactors
        :return:
        '''
        d_1 = self.matrix_determinant(self.key[0:16])
        d_2 = self.matrix_determinant(self.key[20:36])

        if d_1.int != 0 and d_2.int != 0:
            return True

    def matrix_determinant(self, matrix):
        '''
        :param matrix: a 16 bit array
        :return:
        '''
        #Determinant using cofactors and the last  column
        #I am probably taking a transposed version of the matrix, but the determinant is the same
        c_1 = matrix[5:8] + matrix[9:12] + matrix[13:16]
        c_2 = matrix[1:4] + matrix[9:12] + matrix[13:16]
        c_3 = matrix[1:4] + matrix[5:8] + matrix[13:16]
        c_4 = matrix[1:4] + matrix[5:8] + matrix[9:12]

        #print()
        #print(c_1)
        #print(c_2)
        #print(c_3)
        #print(c_4)
        #print()

        irreducible_pol = BitArray(bin="0b10011")


        #print(c_2[2:3],c_2[4:5], c_2[6:7])
        #print(product_in_field(c_2[2:3], product_in_field(c_2[4:5], c_2[6:7], irreducible_pol), irreducible_pol))



        cofactors = [c_1, c_2, c_3, c_4]

        det = BitArray()

        for c in cofactors:
            #print()
            #print(product_in_field(c[0:1], product_in_field(c[4:5], c[8:9], irreducible_pol), irreducible_pol))
            #print(product_in_field(c[3:4], product_in_field(c[7:8], c[2:3], irreducible_pol),irreducible_pol))
            #print(product_in_field(c[1:2], product_in_field(c[5:6], c[6:7], irreducible_pol),irreducible_pol))
            #print(product_in_field(c[2:3], product_in_field(c[4:5], c[6:7], irreducible_pol), irreducible_pol))
            #print(product_in_field(c[1:2], product_in_field(c[3:4], c[8:9], irreducible_pol), irreducible_pol))
            #print(product_in_field(c[0:1], product_in_field(c[5:6], c[7:8], irreducible_pol), irreducible_pol))
            #print()
            det = \
                add(det,
                    add(
                        (add(add(product_in_field(c[0:1], product_in_field(c[4:5], c[8:9], irreducible_pol),
                                                  irreducible_pol),
                                 product_in_field(c[3:4], product_in_field(c[7:8], c[2:3], irreducible_pol),
                                                  irreducible_pol)),
                             product_in_field(c[1:2], product_in_field(c[5:6], c[6:7], irreducible_pol),
                                              irreducible_pol))),

                        (add(add(product_in_field(c[2:3], product_in_field(c[4:5], c[6:7], irreducible_pol),
                                                  irreducible_pol),
                                 product_in_field(c[1:2], product_in_field(c[3:4], c[8:9], irreducible_pol),
                                                  irreducible_pol)),
                             product_in_field(c[0:1], product_in_field(c[5:6], c[7:8], irreducible_pol),
                                              irreducible_pol)))))

        #print("Det:", det)
        return det

    def decode_chunk(self, chunk):
        #Invert the last Mix:
        pass

    def encode_chunk(self, chunk):
        '''
        :param chunk: 16 elements to encode
        :return: The encoded version of the input
        '''
        print(self.key)
        #Taking the necessary matrix for the sub_bytes
        sub_bytes_matrix = BitArray()
        for i in range(4):
            sub_bytes_matrix.append(self.key[0 + i: 0 + i + 1])
            sub_bytes_matrix.append(self.key[4 + i: 4 + i + 1])
            sub_bytes_matrix.append(self.key[8 + i: 8 + i + 1])
            sub_bytes_matrix.append(self.key[12 + i: 12 + i + 1])

        result = BitArray()
        for i in range(16):
            result.append(self.sub_bytes(chunk[i * 4: i * 4 + 4], sub_bytes_matrix, self.key[16:20]))

        print("After sub: ", result)

        #row shift 1
        temp = result[4 * 4:5 * 4]
        result[4 * 4:7 * 4] = result[5 * 4:8 * 4]
        result[7 * 4:8 * 4] = temp

        temp = result[8 * 4:10 * 4]
        result[8 * 4:10 * 4] = result[10 * 4:12 * 4]
        result[10 * 4:12 * 4] = temp

        temp = result[12 * 4:15 * 4]
        result[12 * 4:13 * 4] = result[15 * 4:16 * 4]
        result[13 * 4:16 * 4] = temp

        print("After shift: ", result)

        #Col mix 1
        result = self.row_mix(result, BitArray(bin = "0b0001"), self.key[40:44], self.key[44:48], self.key[48:52])

        print("After mix: ", result)

        #Adding the key
        result = add(result, self.key)

        print("After key sum", result)

        #Sub bytes 2
        # Taking the necessary matrix for the sub_bytes
        sub_bytes_matrix = BitArray()
        for i in range(4):
            sub_bytes_matrix.append(self.key[20 + i: 20 + i + 1])
            sub_bytes_matrix.append(self.key[24 + i: 24 + i + 1])
            sub_bytes_matrix.append(self.key[28 + i: 28 + i + 1])
            sub_bytes_matrix.append(self.key[32 + i: 32 + i + 1])

        result_back = result
        result = BitArray()
        for i in range(16):
            result.append(self.sub_bytes(result_back[i * 4: i * 4 + 4], sub_bytes_matrix, self.key[36:40]))

        print("After sub 2: ", result)

        # row shift 2
        temp = result[4 * 4:5 * 4]
        result[4 * 4:7 * 4] = result[5 * 4:8 * 4]
        result[7 * 4:8 * 4] = temp

        temp = result[8 * 4:10 * 4]
        result[8 * 4:10 * 4] = result[10 * 4:12 * 4]
        result[10 * 4:12 * 4] = temp

        temp = result[12 * 4:15 * 4]
        result[12 * 4:13 * 4] = result[15 * 4:16 * 4]
        result[13 * 4:16 * 4] = temp

        print("After shift 2: ", result)

        # Col mix 2
        result = self.row_mix(result, BitArray(bin="0b0001"), self.key[52:56], self.key[56:60], self.key[60:64])

        print("After mix 2: ", result)

        return result

    def row_mix(self, chunk, k0, k1, k2, k3):
        irreducible_polynomial = BitArray(bin = "0b10001")
        result = BitArray()
        for i in range(4):
            column = chunk[i * 4 * 4: i * 4 * 4 + 16]
            #print("Column:", column)
            for j in range(4):
                products = [product_in_field(column[j * 4: j * 4 + 4], k0, irreducible_polynomial),
                            product_in_field(column[j * 4: j * 4 + 4], k1, irreducible_polynomial),
                            product_in_field(column[j * 4: j * 4 + 4], k2, irreducible_polynomial),
                            product_in_field(column[j * 4: j * 4 + 4], k3, irreducible_polynomial)]
                encoded_column = functools.reduce(lambda a,b : add(a, b), products)
                result.append(encoded_column)
        return result

    def sub_bytes(self, hex_element, key_column, element_to_add):
        '''
        Takes a 4-bit group and performs a substitution multiplying with the
        matrix formed by the bits in key_column and adding element_to_add
        :param hex_element:
        :param key_column:
        :param element_to_add:
        :return:
        '''
        result = BitArray()
        for i in range(4):
            key_element = key_column[i * 4: i * 4 + 4]
            result_element = BitArray(bin = "0b0")

            for j in range(4):
                if key_element[j] and hex_element[j]:
                    result_element = result_element ^ BitArray(bin = "0b1")

            if element_to_add[i]:
                result.append(result_element ^ BitArray(bin = "0b1"))
            else:
                result.append(result_element)
            #print("Result: ", result)

        return result

encoder = Encoder(BitArray(hex="0x94a55ae9b242a648"))

print(encoder.encode_chunk(BitArray(hex = "0x1234123412341234")))

