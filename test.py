def swap_up(matrix, row, col):
    if row > 0:
        matrix[row][col], matrix[row - 1][col] = matrix[row - 1][col], matrix[row][col]

def swap_down(matrix, row, col):
    if row < len(matrix) - 1:
        matrix[row][col], matrix[row + 1][col] = matrix[row + 1][col], matrix[row][col]

def swap_left(matrix, row, col):
    if col > 0:
        matrix[row][col], matrix[row][col - 1] = matrix[row][col - 1], matrix[row][col]

def swap_right(matrix, row, col):
    if col < len(matrix[0]) - 1:
        matrix[row][col], matrix[row][col + 1] = matrix[row][col + 1], matrix[row][col]

# Example usage:
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Swap the element at (0, 0) with its neighbors
# swap_up(matrix, 0, 0)
swap_down(matrix, 0, 0)
# swap_left(matrix, 1, 1)
# swap_right(matrix, 1, 1)

# Print the modified matrix
for row in matrix:
    print(row)