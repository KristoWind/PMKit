#
# Python file for storing the matrixes of Sense HAT led's
#


# Set colors RGB values
X = [255, 0, 0]  # Red
O = [0, 0, 0]  # White
L = [0, 255, 0]  # Lime
G = [0, 100, 0] # Green

# Matrixes

question_mark = [
    O, O, O, X, X, O, O, O,
    O, O, X, O, O, X, O, O,
    O, O, O, O, O, X, O, O,
    O, O, O, O, X, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, X, O, O, O, O
]

green_checkmark = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, L, O,
    O, O, O, O, O, L, G, O,
    O, O, O, O, O, L, G, O,
    O, G, L, O, L, G, O, O,
    O, O, G, L, G, O, O, O,
    O, O, O, G, O, O, O, O,
    O, O, O, O, O, O, O, O
]
