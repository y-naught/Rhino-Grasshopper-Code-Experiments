
"""Grasshopper Script"""

### INPUT VARIABLES
# num_iterations - integer that defines the number of steps to take
# seed_random - integer to seed the random number generator
### OUTPUT VARIABLES
# curves - a set of lines (lines are curves in NURBS world) that the walking generated between each step

# Importing rhinoscriptsyntax, which imports the bindings to the RhinoCommon API
# we can use with our python code.
import rhinoscriptsyntax as rs
import random as random

# Setting our random seed value to our input so the random function doesn't automatically
# adjust the seed value between iterations. 
random.seed(int(seed_random))

# Declaring a global variable that stores the last vector path we followed
# so we can not make sure we don't walk back the direction we just came from. 
last_vector = None

# Contains a list of possible direction objects in our 3-dimensional coordinate system
# our random.choice() function will choose a vector from this list. 
dir_options = [
    rs.CreateVector(1,0,0),
    rs.CreateVector(-1,0,0),
    rs.CreateVector(0,1,0),
    rs.CreateVector(0,-1,0),
    rs.CreateVector(0,0,1),
    rs.CreateVector(0,0,-1)
]

# Copy the values into function local variables x,y,z and return a new vector
def CopyVector(in_vector):
    x = in_vector[0]
    y = in_vector[1]
    z = in_vector[2]
    return rs.CreateVector(x,y,z)

# Get's the next random step vector from our list of vectors.
# Restricts the result to make sure we don't step backwards on to our last position
# with a while loop. 
def get_next_step():
    global last_vector
    valid_vector = False
    while not valid_vector:
        next_vector = CopyVector(random.choice(dir_options))
        if(last_vector):
            reversed_last_vector = rs.VectorReverse(last_vector)
            compare = rs.VectorCompare(reversed_last_vector, next_vector)
            if(compare != 0):
                valid_vector = True
                last_vector = CopyVector(next_vector)
                return next_vector
        else:
            last_vector = CopyVector(next_vector)
            return next_vector

# Creates lines between every plotted point in the given list, and 
# returns a new list of lines. 
def create_lines(point_list):
    lines = []
    for i in range(len(point_list) - 1):
        pt1 = point_list[i]
        pt2 = point_list[i+1]
        line = rs.AddLine(pt1, pt2)
        lines.append(line)
    return lines


# Our main function, which isn't required in this circumstance, but 
# offers some structure to our code. It returns the list of lines that 
# we generated with the create_lines function. 
def main():
    points = []
    last_point = rs.CreatePoint(0,0,0)
    points.append(last_point)
    
    for i in range(int(num_iterations)):
        next_vector = get_next_step()
        next_point = rs.CopyObject(last_point, next_vector)
        points.append(next_point)
        last_point = next_point
    
    return create_lines(points)

# assigns the result of the main function to our node output variable. 
curves = main()