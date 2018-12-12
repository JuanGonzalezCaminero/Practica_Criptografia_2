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
        if self.key_determinants_nonzero():
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
        c_1 = None
        c_2 = None
        c_3 = None
        c_4 = None
        if matrix[0]:
            c_1 = matrix[5:8] + matrix[9:12] + matrix[13:16]
        if matrix[4]:
            c_2 = matrix[1:4] + matrix[9:12] + matrix[13:16]
        if matrix[8]:
            c_3 = matrix[1:4] + matrix[5:8] + matrix[13:16]
        if matrix[12]:
            c_4 = matrix[1:4] + matrix[5:8] + matrix[9:12]

        cofactors = [c_1, c_2, c_3, c_4]

        irreducible_pol = BitArray(bin="0b10011")

        cofactors = [c for c in cofactors if c != None]

        det = BitArray()

        for c in cofactors:
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

    def extended_euclidean(self, b, a):
        x0, x1, y0, y1 = BitArray(bin="0b1"), \
                         BitArray(bin="0b0"), \
                         BitArray(bin="0b0"), \
                         BitArray(bin="0b1")
        while a.int != 0:
            #print("dividend", b.bin)
            #print("divisor", a.bin)
            temp = a
            q, a = division(b, a)
            # q = BitArray(bin = bin(b.uint // a.uint))
            # a = BitArray(bin = bin(b.uint % a.uint))
            #print("quotient", q.bin)
            #print("rem", a.bin)
            b = temp
            x0, x1 = x1, add(x0, polynomial_product(q, x1))
            y0, y1 = y1, add(y0, polynomial_product(q, y1))
            #print("x0", x0)
            #print("x1", x1)
            #print("y0", y0)
            #print("y1", y1)
            # x0, x1 = x1, x0 - q * x1
            # y0, y1 = y1, y0 - q * y1
        return b, x0, y0

    def cofactor_determinant_f16_for_determinant(self, c, irreducible_pol, element):
        return product_in_field(element, add(
                    add(
                        add(product_in_field(c[0:4], product_in_field(c[16:20], c[32:36], irreducible_pol),
                                              irreducible_pol),
                             product_in_field(c[4:8], product_in_field(c[20:24], c[24:28], irreducible_pol),
                                              irreducible_pol)),

                         product_in_field(c[12:16], product_in_field(c[28:32], c[8:12], irreducible_pol),
                                          irreducible_pol)),

                    add(
                        add(product_in_field(c[24:28], product_in_field(c[16:20], c[8:12], irreducible_pol),
                                              irreducible_pol),
                             product_in_field(c[12:16], product_in_field(c[4:8], c[32:36], irreducible_pol),
                                              irreducible_pol)),

                         product_in_field(c[28:32], product_in_field(c[20:24], c[0:4], irreducible_pol),
                                          irreducible_pol))), irreducible_pol)
    def cofactor_determinant_f16(self, c, irreducible_pol):
        return add(
                    add(
                        add(product_in_field(c[0:4], product_in_field(c[16:20], c[32:36], irreducible_pol),
                                              irreducible_pol),
                             product_in_field(c[4:8], product_in_field(c[20:24], c[24:28], irreducible_pol),
                                              irreducible_pol)),

                         product_in_field(c[12:16], product_in_field(c[28:32], c[8:12], irreducible_pol),
                                          irreducible_pol)),

                    add(
                        add(product_in_field(c[24:28], product_in_field(c[16:20], c[8:12], irreducible_pol),
                                              irreducible_pol),
                             product_in_field(c[12:16], product_in_field(c[4:8], c[32:36], irreducible_pol),
                                              irreducible_pol)),

                         product_in_field(c[28:32], product_in_field(c[20:24], c[0:4], irreducible_pol),
                                          irreducible_pol)))

    def inverse_matrix_f16(self, matrix):
        '''
        Returns the inverse of a matrix formed by 16 F16 elements
        :param matrix:
        :return:
        '''
        #We first need the determinant of the matrix, computed using cofactors with the
        #first column
        det = BitArray(bin = "0b0000")

        c_1 = None
        c_2 = None
        c_3 = None
        c_4 = None
        c_1_first_col_element = matrix[0][0]
        c_2_first_col_element = matrix[1][0]
        c_3_first_col_element = matrix[2][0]
        c_4_first_col_element = matrix[3][0]
        c_1 = matrix[1][1] + matrix[1][2] + matrix[1][3] + \
              matrix[2][1] + matrix[2][2] + matrix[2][3] + \
              matrix[3][1] + matrix[3][2] + matrix[3][3]

        c_2 = matrix[0][1] + matrix[0][2] + matrix[0][3] + \
              matrix[2][1] + matrix[2][2] + matrix[2][3] + \
              matrix[3][1] + matrix[3][2] + matrix[3][3]

        c_3 = matrix[0][1] + matrix[0][2] + matrix[0][3] + \
              matrix[1][1] + matrix[1][2] + matrix[1][3] + \
              matrix[3][1] + matrix[3][2] + matrix[3][3]

        c_4 = matrix[0][1] + matrix[0][2] + matrix[0][3] + \
              matrix[1][1] + matrix[1][2] + matrix[1][3] + \
              matrix[2][1] + matrix[2][2] + matrix[2][3]

        cofactors = [c_1, c_2, c_3, c_4]

        irreducible_pol = BitArray(bin="0b10011")

        first_col_elements = [c_1_first_col_element, c_2_first_col_element, c_3_first_col_element, c_4_first_col_element]

        det = BitArray()

        for i in range(len(cofactors)):
            first_col_element = first_col_elements[i]
            c = cofactors[i]
            det = add(det, self.cofactor_determinant_f16_for_determinant(c, irreducible_pol, first_col_element))
        print("Matrix determinant:", det)

        mcd, x0, y0 = self.extended_euclidean(BitArray(bin = "0b10011"), det)

        print("Determinant inverse:", y0)

        #Now we only have to multiply the determinant inverse with the transposed cofactor matrix
        #Or multiply with the cofactor matrix and transpose the result
        #Cofactor matrix:
        inverse_matrix = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                cofactor = BitArray()
                element = matrix[i][j]
                for i_2 in range(len(matrix)):
                    if i_2 == i:
                        continue
                    for j_2 in range(len(matrix[i])):
                        if j_2 == j:
                            continue
                        cofactor += matrix[i_2][j_2]

                cofactor_det = self.cofactor_determinant_f16(cofactor, irreducible_pol)
                inverse_matrix += product_in_field(cofactor_det, y0, irreducible_pol)

        inverse_matrix = self.transpose_chunk(inverse_matrix)
        print(inverse_matrix)

        #for i in range(len(matrix)):
        #    inverse_matrix.append([])
        #    for element in matrix[i]:
                #print(element, type(element))
                #print(y0, type(y0))
                #print(product_in_field(y0, element, irreducible_pol))
        #        inverse_matrix[i].append(product_in_field(y0, element, irreducible_pol))

        #for row in inverse_matrix:
        #    print(row)

    def sub_bytes_modify(self, sub_bytes_matrix, sub_bytes_add):
        sb0 = sub_bytes_matrix[0:4]
        sb1 = sub_bytes_matrix[4:8]
        sb2 = sub_bytes_matrix[8:12]
        sb3 = sub_bytes_matrix[12:16]
        sb0.reverse()
        sb1.reverse()
        sb2.reverse()
        sb3.reverse()
        sub_bytes_matrix = BitArray(bin="0b" + sb0[0:1].bin + sb1[0:1].bin + sb2[0:1].bin + sb3[0:1].bin) + \
                             BitArray(bin="0b" + sb0[1:2].bin + sb1[1:2].bin + sb2[1:2].bin + sb3[1:2].bin) + \
                             BitArray(bin="0b" + sb0[2:3].bin + sb1[2:3].bin + sb2[2:3].bin + sb3[2:3].bin) + \
                             BitArray(bin="0b" + sb0[3:4].bin + sb1[3:4].bin + sb2[3:4].bin + sb3[3:4].bin)
        sub_bytes_add.reverse()
        return sub_bytes_matrix

    def encode_chunk(self, chunk):
        '''
        :param chunk: 16 elements to encode
        :return: The encoded version of the input
        '''
        encoded_chunk = BitArray()
        print("Key:", self.key)
        print("Chunk to encode:", chunk)
        #Dividing the key parts
        sub_bytes_1_matrix = self.key[0:16]
        sub_bytes_1_add = self.key[16:20]
        sub_bytes_2_matrix = self.key[20:36]
        sub_bytes_2_add = self.key[36:40]
        mix_rows_1_pol = self.key[40:52]
        mix_rows_2_pol = self.key[52:64]
        #Modifying the key for the sub-bytes operations
        sub_bytes_1_matrix = self.sub_bytes_modify(sub_bytes_1_matrix, sub_bytes_1_add)
        sub_bytes_2_matrix = self.sub_bytes_modify(sub_bytes_2_matrix, sub_bytes_2_add)

        #SUB BYTES 1
        for i in range(16):
            to_encode = chunk[i * 4: i * 4 + 4]
            to_encode.reverse()
            result = self.sub_bytes(to_encode, sub_bytes_1_matrix, sub_bytes_1_add)
            result.reverse()
            encoded_chunk += result
        print("After sub bytes 1:", encoded_chunk)

        #SHIFT ROWS 1:
        encoded_chunk = self.shift_rows(encoded_chunk)
        print("After shift rows 1:", encoded_chunk)

        #MIX ROWS 1:
        encoded_chunk = self.row_mix(encoded_chunk, mix_rows_1_pol)
        print("After mix 1:", encoded_chunk)

        #ADD KEY
        encoded_chunk = add(encoded_chunk, self.key)
        print("After key sum:", encoded_chunk)

        # SUB BYTES 2
        temp_result = BitArray()
        for i in range(16):
            to_encode = encoded_chunk[i * 4: i * 4 + 4]
            to_encode.reverse()
            result = self.sub_bytes(to_encode, sub_bytes_2_matrix, sub_bytes_2_add)
            result.reverse()
            temp_result += result
        encoded_chunk = temp_result
        print("After sub bytes 2:", encoded_chunk)

        # SHIFT ROWS 2:
        encoded_chunk = self.shift_rows(encoded_chunk)
        print("After shift rows 2:", encoded_chunk)

        # MIX ROWS 1:
        encoded_chunk = self.row_mix(encoded_chunk, mix_rows_2_pol)
        print("After mix 2:", encoded_chunk)

        return encoded_chunk

        #print(sub_bytes_1_matrix)
        #print(sub_bytes_1_add)
        #print(sub_bytes_2_matrix)
        #print(sub_bytes_2_add)
        #print(mix_rows_1_pol)
        #print(mix_rows_2_pol)

    def decode_chunk(self, chunk):
        #We first need the inverse of the matrices used for the row mix:
        sub_bytes_1_matrix = self.key[0:16]
        sub_bytes_1_add = self.key[16:20]
        sub_bytes_2_matrix = self.key[20:36]
        sub_bytes_2_add = self.key[36:40]
        mix_rows_1_pol = self.key[40:52]
        mix_rows_2_pol = self.key[52:64]
        mix_rows_1_matrix = [[mix_rows_1_pol[8:12], BitArray(bin="0b0001"), mix_rows_1_pol[0:4], mix_rows_1_pol[4:8]],
                             [mix_rows_1_pol[4:8], mix_rows_1_pol[8:12], BitArray(bin="0b0001"), mix_rows_1_pol[0:4]],
                             [mix_rows_1_pol[0:4], mix_rows_1_pol[4:8], mix_rows_1_pol[8:12], BitArray(bin="0b0001")],
                             [BitArray(bin="0b0001"), mix_rows_1_pol[0:4], mix_rows_1_pol[4:8], mix_rows_1_pol[8:12]]]

        mix_rows_2_matrix = [[mix_rows_2_pol[8:12], BitArray(bin="0b0001"), mix_rows_2_pol[0:4], mix_rows_2_pol[4:8]],
                             [mix_rows_2_pol[4:8], mix_rows_2_pol[8:12], BitArray(bin="0b0001"), mix_rows_2_pol[0:4]],
                             [mix_rows_2_pol[0:4], mix_rows_2_pol[4:8], mix_rows_2_pol[8:12], BitArray(bin="0b0001")],
                             [BitArray(bin="0b0001"), mix_rows_2_pol[0:4], mix_rows_2_pol[4:8], mix_rows_2_pol[8:12]]]

        mix_rows_1_matrix = self.inverse_matrix_f16(mix_rows_1_matrix)

        return

    def encode_stream(self, stream):
        if len(stream.hex) % 16 != 0:
            print("El número de caracteres introducido no es múltiplo de 16")
            return
        else:
            result = BitArray()
            for i in range(0, len(stream.hex), 16):
                result += self.encode_chunk(stream[i * 4: i * 4 + 64])
            return result

    def transpose_chunk(self, chunk):
        # Transposing the chunk
        sb0 = chunk[0:16]
        sb1 = chunk[16:32]
        sb2 = chunk[32:48]
        sb3 = chunk[48:64]
        chunk = BitArray(bin="0b" + sb0[0:4].bin + sb1[0:4].bin + sb2[0:4].bin + sb3[0:4].bin) + \
                BitArray(bin="0b" + sb0[4:8].bin + sb1[4:8].bin + sb2[4:8].bin + sb3[4:8].bin) + \
                BitArray(bin="0b" + sb0[8:12].bin + sb1[8:12].bin + sb2[8:12].bin + sb3[8:12].bin) + \
                BitArray(bin="0b" + sb0[12:16].bin + sb1[12:16].bin + sb2[12:16].bin + sb3[12:16].bin)
        return chunk

    def shift_rows(self, chunk):
        chunk = self.transpose_chunk(chunk)

        temp = chunk[4 * 4:5 * 4]
        chunk[4 * 4:7 * 4] = chunk[5 * 4:8 * 4]
        chunk[7 * 4:8 * 4] = temp

        temp = chunk[8 * 4:10 * 4]
        chunk[8 * 4:10 * 4] = chunk[10 * 4:12 * 4]
        chunk[10 * 4:12 * 4] = temp

        temp = chunk[12 * 4:15 * 4]
        chunk[12 * 4:13 * 4] = chunk[15 * 4:16 * 4]
        chunk[13 * 4:16 * 4] = temp

        # Transposing the result
        chunk = self.transpose_chunk(chunk)

        return chunk

    def row_mix(self, chunk, polynomial):
        #Building the matrix
        matrix = [[polynomial[8:12], BitArray(bin = "0b0001"), polynomial[0:4], polynomial[4:8]],
                  [polynomial[4:8], polynomial[8:12], BitArray(bin="0b0001"), polynomial[0:4]],
                  [polynomial[0:4], polynomial[4:8], polynomial[8:12], BitArray(bin="0b0001")],
                  [BitArray(bin="0b0001"), polynomial[0:4], polynomial[4:8], polynomial[8:12]]]

        irreducible_polynomial = BitArray(bin = "0b10011")
        result = BitArray()
        for i in range(4):
            column = chunk[i * 4 * 4: i * 4 * 4 + 16]
            #print("Column:", column)
            for j in range(4):
                #print("---")
                #print(matrix[j][0], matrix[j][1], matrix[j][2], matrix[j][3])
                #print(column[j * 4: j * 4 + 4], column[j * 4: j * 4 + 4], column[j * 4: j * 4 + 4], column[j * 4: j * 4 + 4])
                products = [product_in_field(column[0:4], matrix[j][0], irreducible_polynomial),
                            product_in_field(column[4:8], matrix[j][1], irreducible_polynomial),
                            product_in_field(column[8:12], matrix[j][2], irreducible_polynomial),
                            product_in_field(column[12:16], matrix[j][3], irreducible_polynomial)]
                encoded_column = functools.reduce(lambda a,b : add(a, b), products)
                result.append(encoded_column)
        return result

    def sub_bytes(self, hex_element, matrix, element_to_add):
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
            key_element = matrix[i * 4: i * 4 + 4]
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
#print("Result:", encoder.encode_chunk(BitArray(hex = "0x1234123412341234")))
print("Result:", encoder.decode_chunk(BitArray(hex = "0x1234123412341234")))
#print(encoder.encode_stream(BitArray(hex = "0x12341234123412341234123412341234")))
