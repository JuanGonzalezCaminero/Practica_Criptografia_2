from bitstring import *
import copy

#TODO: Programa Main para poder ejecutar esto de forma cómoda
#NOTA: requiere instalar la biblioteca bitstring (pip install bitstring)

#Recibe 2 elementos de F16 escrito como Z2 /(X^4 + X + 1) y devuelve el resultado
#de la suma y la multiplicación de ambos

#Los elementos de F16 a partir del irreducible X^4 + X + 1 tienen longitud 4, pero
#Con otros polinomios la longitud cambiará
#irreductible_polynomial_degree = 4

#Almaceno los elementos del cuerpo que usemos en objetos "Bits" de la longitud necesaria
#para almacenar cada elemento como una serie de bits, en el caso de F16 con este
#irreducible, cada elemento se almacena como un "Bits" de longitud 4
#
#Nota: me refiero al tipo "Bits" de la biblioteca bitstring, que representa una secuencia inmutable de bits


#Note that both the addition and the product functions defined here only work for finite fields
#constructed from Z2
def add(a, b):
    """
    :param a: A Bits object representing an element of a finite field with p = 2
    :param b: A Bits object representing an element of a finite field with p = 2
    :return: A Bits object containing the sum of a + b
    """
    #In case a and b are of different lenght, add padding zeros to the left of the shorter one
    if len(a) < len(b):
        while(len(a) < len(b)):
            a.prepend('0b0')
    elif len(a) > len(b):
        while (len(a) > len(b)):
            b.prepend('0b0')
    #As we take coefficients from Z2, the sum of two elements is simply the xor between them
    c = a ^ b
    return c

def product_in_field(a, b, irreducible_polynomial):
    """
    The product of two elements from a finite field generated from Z2[X] using
    the irreducible polynomial given
    :param a: A Bits object representing an element of a finite field with p = 2
    :param b: A Bits object representing an element of a finite field with p = 2
    :param irreducible_polynomial: The irreducible polynomial that was used to generate
    the finite field, represented as a Bits object
    :return: A Bits object containing a * b
    """
    # In case a and b are of different lenght, add padding zeros to the left of the shorter one
    if len(a) < len(b):
        while (len(a) < len(b)):
            a.prepend('0b0')
    elif len(a) > len(b):
        while (len(a) > len(b)):
            b.prepend('0b0')

    irreducible_degree = len(irreducible_polynomial) - 1
    # element_length: The length of the elements to be multiplied, the length of either a or b at this point
    element_length = len(a)
    element_max_degree = element_length - 1
    #First multiply both polynomials, the resulting degree will not be higher than
    #2 * the highest possible degree of the elements, + 1 since a polynomial of
    #degree n has n + 1 elements
    result = BitArray(2 * element_max_degree + 1)
    #simple and inefficient multiplication
    for i in range(element_length):
        bit_a = a[i]
        for j in range(element_length):
            bit_b = b[j]
            if bit_a == bit_b == 1:
                #If neither is 0, multiply them, storing a 1 in result
                #in the position of the element that has the degree of the sum
                #of the degrees of bit_a and bit_b (since we index from the left,
                #the lower the degree the higher the index will be and the lower
                #degree the 1 will get in result)
                #Insert it with an xor with the element currently there, since we are
                #taking coeficients from Z2, if we have, for example, X + X = 2X = 0X = 0,
                #if there is already a 1 in the result, its swapped by a 0
                result[i + j] = result[i + j] ^ 1
    #We now have the result of multiplying both polynomials, but have yet to obtain the
    #module with the irreducible polynomial provided, to do this, for each coefficient of
    #degree >= degree of the irreducible polynomial, calculate the remainder and add it
    #to the result
    #First crop the 0 to the left in the result to check the result's degree
    bits_to_crop = 0
    for i in range(len(result) - 1):
        if result[i] == 0:
            bits_to_crop += 1
        else:
            break
    result = result[bits_to_crop:]
    result_degree = len(result) - 1
    #If the degree of the result is smaller than the degree of the irreducible polynomial
    #this will, not be executed.
    if result_degree >= irreducible_degree:
         result = division(result, irreducible_polynomial)[1]

    #If the length of the result is smaller than the degree of the irreducible polynomial
    #(the length of the elements from the field), padding zeros are added to the left
    if len(result) < irreducible_degree:
        while (len(result) < irreducible_degree):
            result.prepend('0b0')
    return result

def polynomial_product(a, b):
    """
    The product of two polynomials from Z2[X]
    :param a: A Bits object representing an element of a finite field with p = 2
    :param b: A Bits object representing an element of a finite field with p = 2
    :return: A Bits object containing a * b
    """
    # In case a and b are of different lenght, add padding zeros to the left of the shorter one
    if len(a) < len(b):
        while (len(a) < len(b)):
            a.prepend('0b0')
    elif len(a) > len(b):
        while (len(a) > len(b)):
            b.prepend('0b0')

    # element_length: The length of the elements to be multiplied, the length of either a or b at this point
    element_length = len(a)
    element_max_degree = element_length - 1
    #First multiply both polynomials, the resulting degree will not be higher than
    #2 * the highest possible degree of the elements, + 1 since a polynomial of
    #degree n has n + 1 elements
    result = BitArray(2 * element_max_degree + 1)
    #simple and inefficient multiplication
    for i in range(element_length):
        bit_a = a[i]
        for j in range(element_length):
            bit_b = b[j]
            if bit_a == bit_b == 1:
                #If neither is 0, multiply them, storing a 1 in result
                #in the position of the element that has the degree of the sum
                #of the degrees of bit_a and bit_b (since we index from the left,
                #the lower the degree the higher the index will be and the lower
                #degree the 1 will get in result)
                #Insert it with an xor with the element currently there, since we are
                #taking coeficients from Z2, if we have, for example, X + X = 2X = 0X = 0,
                #if there is already a 1 in the result, its swapped by a 0
                result[i + j] = result[i + j] ^ 1
    #We now have the result of multiplying both polynomials, but have yet to obtain the
    #module with the irreducible polynomial provided, to do this, for each coefficient of
    #degree >= degree of the irreducible polynomial, calculate the remainder and add it
    #to the result
    #First crop the 0 to the left in the result to check the result's degree
    bits_to_crop = 0
    for i in range(len(result) - 1):
        if result[i] == 0:
            bits_to_crop += 1
        else:
            break
    result = result[bits_to_crop:]

    return result

def division(dividend, divisor):
    """
    :param dividend: A Bits object representing a polynomial to be divided by d, coefficients from Z2
    :param divisor: A Bits object representing a polynomial to act as the divisor, coefficients from Z2
    :param irreducible_polynomial: The irreducible polynomial that was used to generate
    the finite field, represented as a Bits object
    :return: A tuple containing a Bits object with the quotient and a Bits object
    with the remainder
    """
    divisor = copy.copy(divisor)
    #Crop both dividend and divisor so there are no 0 to the left
    for i in range(len(dividend)):
        if dividend[i] == 0:
            dividend = dividend[1:]
        else:
            break
    for i in range(len(divisor)):
        if divisor[i] == 0:
            divisor = divisor[1:]
        else:
            break

    dividend_degree = len(dividend) - 1
    divisor_degree = len(divisor) - 1
    remainder_degree = dividend_degree
    #The degrees of the quotient and remainder will not be higher than the degree of
    #the dividend, + 1 since a polynomial of degree n has n + 1 elements
    quotient = BitArray(dividend_degree + 1)
    remainder = dividend
    while remainder.int != 0 and remainder_degree >= divisor_degree:
        #t -> result of the division of the higher-degree terms, in this case,
        #this is a polynomial with a single coefficient with degree the difference
        #of the degrees of the dividend (stored in the remainder) and the divisor
        #If the difference is 0, this means that remainder and dividend are equal
        #and the result is the constant polynomial 1
        degree_difference = remainder_degree - divisor_degree
        #print("Degree difference: ", degree_difference)
        t = BitArray(degree_difference + 1)
        t[0] = 1
        quotient = add(quotient, t)
        #print("Remainder: ", remainder)
        #print("T: ", t)
        #print("Divisor: ", divisor)
        #print("T * Divisor: ", polynomial_product(t, divisor))
        #Since we are in Z2, substraction is the same as addition
        remainder = add(remainder, polynomial_product(t, divisor))
        #print("Remainder + T * Divisor: ", remainder)
        #Getting the new degree of the remainder
        bits_to_crop = 0
        for i in range(len(remainder) - 1):
            if remainder[i] == 0:
                bits_to_crop += 1
            else:
                break
        remainder = remainder[bits_to_crop:]
        #print(remainder.bin)
        remainder_degree = len(remainder) - 1
        #print(remainder_degree)
    return quotient, remainder

    #function
    #n / d:
    #require
    #d ≠ 0
    #q ← 0
    #r ← n  # At each step n = d × q + r
    #while r ≠ 0 AND degree(r) ≥ degree(d):
    #    t ← lead(r) / lead(d)  # Divide the leading terms
    #    q ← q + t
    #    r ← r − t * d























