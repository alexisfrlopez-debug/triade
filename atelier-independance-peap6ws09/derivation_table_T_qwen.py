import math

def table_T():
    # Initialize an empty list to store the 64 MD5 constants
    T = []
    
    # Loop through each index i from 0 to 63
    for i in range(64):
        # Calculate the sine of (i + 1) in radians
        sin_value = math.sin(i + 1)
        
        # Compute the integer part of 4294967296 times the absolute value of sin_value
        T.append(int(4294967296 * abs(sin_value)))
    
    # Return the list of 64 MD5 constants
    return T
