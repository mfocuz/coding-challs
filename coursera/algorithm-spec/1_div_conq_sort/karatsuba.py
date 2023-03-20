def karatsuba(val1, val2):
    if val1 < 10 and val2 < 10:
        return int(val1) * int(val2)
    else:
        n = max(len(str(val1)), len(str(val2)))
        n2 = n // 2
        a, b = divmod(val1, 10**n2)
        c, d = divmod(val2, 10**n2)

        ac = karatsuba(a, c)
        bd = karatsuba(b, d)
        abcd = karatsuba(a+b, c+d)
        temp = abcd - ac - bd
        result = ac * 10 ** (n2 * 2) + temp * 10 ** n2 + bd
        return result


if __name__ == '__main__':
    mul1 = 3141592653589793238462643383279502884197169399375105820974944592
    mul2 = 2718281828459045235360287471352662497757247093699959574966967627

    print("python built in multiplying: %d" % (mul1 * mul2))
    karatsuba_result = karatsuba(mul1, mul2)
    print("karatsuba: %d" % karatsuba_result)

