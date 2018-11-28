import sys
import os
import utility
from bitstring import *

#transformation_matrix = [[BitArray("0b0010"), BitArray("0b0011"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000")],
#                   [BitArray("0b0110"), BitArray("0b0111"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000")],
#                   [BitArray("0b1111"), BitArray("0b1110"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000")],
#                   [BitArray("0b1110"), BitArray("0b1111"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001")]]
#control_matrix = [[BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001")],
#                    [BitArray("0b0001"), BitArray("0b0011"), BitArray("0b0111"), BitArray("0b1111"), BitArray("0b1110"), BitArray("0b1100")]]
#irreducible_polynomial = BitArray("0b10011")



############################ MAIN ############################
FICHERO_CODIFICADO_BINARIO = "EncodedTextBin"
FICHERO_CODIFICADO_ASCII = "EncodedText.txt"
FICHERO_CORREGIDO_BINARIO = "CorrectedBin"
FICHERO_CORREGIDO_ASCII = "Corrected.txt"
FICHERO_TEMPORAL = "TempBin"
FICHERO_DECODIFICADO = "DecodedText.txt"
FICHERO_DECODIFICADO_SIN_CORRECCION = "DecodedTextNotCorrected.txt"
FICHERO_MATRIZ_GENERATRIZ = "Matriz_gen.txt"
FICHERO_MATRIZ_CONTROL = "Matriz_contr.txt"
GENERATE_BINARY_FILES = 0

fichero_entrada = ""
sum_mult = 0
encode = 0
correct = 0
decode = 0
errors = 0

transformation_matrix = []
control_matrix = []

try:
    #Read transformation matrix
    file = open(sys.path[0] + "\\" + FICHERO_MATRIZ_GENERATRIZ, 'r')
    for line in file:
        transformation_matrix.append([])
        element_list = line.split(",")
        for element in element_list:
            transformation_matrix[-1].append(BitArray(bin = "0b" + element))
    file.close()
    #Read control matrix
    file = open(sys.path[0] + "\\" + FICHERO_MATRIZ_CONTROL, 'r')
    for line in file:
        control_matrix.append([])
        element_list = line.split(",")
        for element in element_list:
            control_matrix[-1].append(BitArray(bin = "0b" + element))
    file.close()
except FileNotFoundError:
    print("Este programa utiliza las matrices definidas en los ficheros \"Matriz_gen.txt\" y  \"Matriz_contr.txt\"que tienen "
             "que estar en el mismo directorio que este fichero")

irreducible_str = input("Introduce el polinomio irreducible a usar, usando unos y ceros:\n")
irreducible_polynomial = BitArray(bin = "0b" + irreducible_str)

while True:
    sum_mult = 0
    encode = 0
    correct = 0
    decode = 0
    errors = 0

    action = int(input("¿Qué quieres hacer?:"
                      "\n0: Salir"
                      "\n1: Sumar/Multiplicar"
                      "\n2: Codificar un fichero"
                      "\n3: Corregir errores en el fichero"
                      "\n4: Decodificar el fichero"
                      "\n5: Introducir errores\n"))
    if action == 0:
        break
    elif action == 1:
        sum_mult = 1
    elif action == 2:
        encode = 1
    elif action == 3:
        correct = 1
    elif action == 4:
        decode = 1
    elif action == 5:
        errors = 1

    if sum_mult:
        utility.sum_mult()

    if encode:
        #Encode

        fichero_entrada = input("Introduce el nombre del fichero a cofificar:\n")

        encoded = utility.encode("\\" + fichero_entrada, transformation_matrix, irreducible_polynomial)

        if GENERATE_BINARY_FILES:
            file = open(sys.path[0] + "\\" + FICHERO_CODIFICADO_BINARIO, 'wb+')
            file.write(bytes.fromhex(encoded.hex))

        file = open(sys.path[0] + "\\" + FICHERO_CODIFICADO_ASCII, 'w+')
        file.write(encoded.bin)

        file.flush()
        os.fsync(file.fileno())
        file.close()

    if correct:
        # If the data is read from an text file containing "1" and "0",
        # it is transformed to a bit sequence, which is subsequently saved
        # in a temporal binary file, used as the stream passed to the decoder
        try:
            utility.generate_temp_binary_file(FICHERO_CODIFICADO_ASCII, FICHERO_TEMPORAL)

            corrected = utility.correct("\\" + FICHERO_TEMPORAL, transformation_matrix, control_matrix, irreducible_polynomial)

            os.remove(sys.path[0] + "\\" + FICHERO_TEMPORAL)
        except FileNotFoundError:
            print("No se ha encontrado el fichero codificado")
            continue
        # Save the results
        if GENERATE_BINARY_FILES:
            file = open(sys.path[0] + "\\" + FICHERO_CORREGIDO_BINARIO, 'bw+')
            file.write(bytes.fromhex(corrected.hex))

        file = open(sys.path[0] + "\\" + FICHERO_CORREGIDO_ASCII, 'w+')
        file.write(corrected.bin)

        file.flush()
        os.fsync(file.fileno())
        file.close()

    if decode:
        #Decode
        #If the data is read from an text file containing "1" and "0",
        #it is transformed to a bit sequence, which is subsequently saved
        #in a temporal binary file, used as the stream passed to the decoder

        try:
            utility.generate_temp_binary_file(FICHERO_CODIFICADO_ASCII, FICHERO_TEMPORAL)
            decoded_without_correction = utility.decode("\\" + FICHERO_TEMPORAL, transformation_matrix, irreducible_polynomial)

            os.remove(sys.path[0] + "\\" + FICHERO_TEMPORAL)

            # Save the results
            file = open(sys.path[0] + "\\" + FICHERO_DECODIFICADO_SIN_CORRECCION, 'bw+')
            file.write(bytes.fromhex(decoded_without_correction.hex))
            file.close()
        except FileNotFoundError:
            print("No se ha encontrado el fichero codificado")
            continue

        try:
            utility.generate_temp_binary_file(FICHERO_CORREGIDO_ASCII, FICHERO_TEMPORAL)
            decoded = utility.decode("\\" + FICHERO_TEMPORAL, transformation_matrix, irreducible_polynomial)

            os.remove(sys.path[0] + "\\" + FICHERO_TEMPORAL)

            # Save the results
            file = open(sys.path[0] + "\\" + FICHERO_DECODIFICADO, 'bw+')
            file.write(bytes.fromhex(decoded.hex))
            file.close()
        except FileNotFoundError:
            print("No se ha encontrado el fichero corregido, se decodificará sólo el fichero codificado original")

    if errors:
        error_frequency = int(input("¿Cada cuántos bits quieres introducir un error?\n"))
        try:
            utility.generate_temp_binary_file(FICHERO_CODIFICADO_ASCII, FICHERO_TEMPORAL)

            encoded_with_errors = utility.introduce_errors("\\" + FICHERO_TEMPORAL, error_frequency)

            os.remove(sys.path[0] + "\\" + FICHERO_TEMPORAL)
        except FileNotFoundError:
            print("No se ha encontrado el fichero codificado")
            continue

        #Overwriting the encoded file
        file = open(sys.path[0] + "\\" + FICHERO_CODIFICADO_ASCII, 'w+')
        file.write(encoded_with_errors.bin)

        file.flush()
        os.fsync(file.fileno())
        file.close()


