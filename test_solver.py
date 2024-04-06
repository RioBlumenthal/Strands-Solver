ROWS = 8
COLS = 6

def convertBinaryToWord(binary_number):
    word = ""
    for i in range(ROWS - 1, -1, -1):
        for j in range(COLS):
            if binary_number & 1:
                word += board[i][j]
            binary_number >>= 1  # Shift right after processing each bit
    return word


board = [['a', 't', 'r', 'i', 'o', 'd'], ['r', 'e', 'm', 'p', 'e', 'r'], ['p', 'o', 'a', 'c', 't', 'y'], ['t', 'h', 't', 'l', 'h', 'l'], ['i', 'm', 'o', 'i', 'p', 'e'], ['e', 'g', 'f', 'a', 'n', 's'], ['r', 'i', 'r', 'h', 'a', 'l'], ['l', 'g', 'h', 't', 's', 'f']]
# Test 1: Binary number with all 1s
binary_number = 0b111111000000000000000000000000000000000000000000
expected_word = "atriod"
print(convertBinaryToWord(binary_number), expected_word)

# Test 2: Binary number with all 0s
binary_number = 0
expected_word = ''
print("all zeros: ", convertBinaryToWord(binary_number), expected_word)

# Test 3: Binary number with alternating 1s and 0s
binary_number = int('101010101010101010101010101010101010101010101010', 2)
expected_word = ''.join([''.join(row) for row in board[::-1] if board[::-1].index(row) % 2 == 0])
print(convertBinaryToWord(binary_number), expected_word)

# Test 4: Binary number with specific pattern
binary_number = int('000000000000000000000000000000000000000000000000', 2)
expected_word = ''
print(convertBinaryToWord(binary_number), expected_word)

# Test 5: Binary number with specific pattern
binary_number = int('111111111111111111111111111111111111111111111111', 2)
expected_word = ''.join([''.join(row) for row in board[::-1]])
print(convertBinaryToWord(binary_number), expected_word)