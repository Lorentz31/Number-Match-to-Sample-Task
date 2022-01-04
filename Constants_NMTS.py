'''
Constants Numbers_Match-to-Sample_Task.1.1.py
'''

n_max = 10 # Number of max numerosity
n_rep = 2 # Number of repetions of the whole sequence

a = 20 # Create random coordinates for the dots sets, in a way they don't overlap
b = 50
c = 65
d = 85
A = [b, d]
B = [-d, -b]
C = [-d, b]
D = [d, -b]
E = [b, b]
F = [-b, -b]
G = [b, -b]
H = [-b, b]
J = [a, c]
K = [-a, -c]
positions_array_from_constants = [A, B, C, D, E, F, G, H, J, K]

s_min = 15 # Create minimum and maximum for radius
s_max = 27

# ATTENTION: Modifying size/coordinates of dots sets could make dots overlap

DISPSIZE = (1920, 1080) # Display sizes
fullscr = True # Set to TRUE if fullscreen
