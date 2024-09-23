def get_bit_at_index(num, index):
    return (num >> index) & 1

def get_num_bits(num):
    return num.bit_length()

def multiply_uint128(a, b):
    return a * b

def add_uint128(a, b):
    return a + b

def subtract_uint128(a, b):
    return a - b

def greater_than_or_equal_uint128(a, b):
    return a >= b

def bitshift_uint128_right(num, shift):
    return num >> shift

def montgomery_multiplication(X, Y, M):
    T = 0
    Y0 = get_bit_at_index(Y, 0)

    M_num_bits = get_num_bits(M)
    X_num_bits = get_num_bits(X)
    Y_num_bits = get_num_bits(Y)

    num_bits = max(M_num_bits, X_num_bits, Y_num_bits)

    R = 1 << M_num_bits  # R = 2^k
    R_inv = pow(R, -1, M)  # Calculate R^-1 mod M

    for i in range(num_bits):
        T0 = get_bit_at_index(T, 0)
        Xi = get_bit_at_index(X, i)
        Xi_and_Y0 = Xi & Y0
        n = T0 ^ Xi_and_Y0
        
        Xi_times_Y = multiply_uint128(Xi, Y)
        n_times_M = multiply_uint128(n, M)

        T = bitshift_uint128_right(add_uint128(add_uint128(T, Xi_times_Y), n_times_M), 1)

    if greater_than_or_equal_uint128(T, M):
        T = subtract_uint128(T, M)


    # Final multiplication by R_inv if needed (this is context-dependent)
    #T = multiply_uint128(T, R_inv) % M

    return T


def print_uint128_test_result(result, expected, test_name):
    if result == expected:
        print(f"{test_name}: Passed")
    else:
        print(f"{test_name}: Failed. Expected {expected}, but got {result}")

# Define the test values
x_test = (0xc6beec7602f3b06, 0x5bb2ac322c1f95e1)
y_test = (0xf665ffaa6dd4204, 0xb29c6ad048eb9fb1)
m_test = (0xfb10458be6c5468, 0xe0b603ea54d107ed)

# Convert the test values to a single integer
x_test_int = (x_test[0] << 64) | x_test[1]
y_test_int = (y_test[0] << 64) | y_test[1]
m_test_int = (m_test[0] << 64) | m_test[1]

# Run the Montgomery multiplication
mont_result = montgomery_multiplication(x_test_int, y_test_int, m_test_int)

# Print the result in the desired format
print(f"Montgomery Result: {{{mont_result >> 64:#018x}, {mont_result & 0xffffffffffffffff:#018x}}}")

# Define the expected result
mont_expected = (0x0f8dcdc8e57bc403, 0xf1e937f6a7d35a5a)
mont_expected_int = (mont_expected[0] << 64) | mont_expected[1]

# Print the test result
print_uint128_test_result(mont_result, mont_expected_int, "High Montgomery multiplication test")


