# 3/n body problem 2.0 
# Erik Hale

# Cleaning the code up and making it run smoother

# UPDATES: 
# 1.) The input file now has three parameters at the top of the file: 
# ... (Whether to make an animation or not with 1 or 0 resp), timestep, time
# ... Also, names of the masses have been added to the text file
# 2.) Different classes and objects have been made to make this project scalable

# Having completed the 2 Body Problem Simulation, this code will be a simulation of the
# ... 3 Body Problem / N-Body Problem, where there are n amounts of masses that affect
# ... each other gavitationally. This could simulate how objects in star systems move
# ... or how planets with moons are affected. The idea would be to have a text file to
# ... upload information to, so that files could be uploaded with ease.

# I found this article published by Princeton that talks about simulating the N body
# ... problem in different ways for a computer where the brute force way is to use the
# ... standard equation for accurate results that take a long time (O(n^2): this is
# ... becuase we have to go through the data to get the sum of the forces for each mass.
# ... I'll implement this version first, as I really meant for this program to only deal
# ... with a few masses at a time and not a cluster of masses as the article recommends
# ... for a larger amount of masses, though it may be something that I attempt in the
# ... future. Link: https://physics.princeton.edu//~fpretori/Nbody/intro.htm
# ... Another Link: https://blbadger.github.io/3-body-problem.html

# Now the basic program is done, work can begin on animating the graph and making the
# ... program look good so the data can be better understood. Majorly, I want to update
# ... the program to animate so that you can watch the bodies move, which I think is
# ... much more helpful when trying to understand the motion of some masses in a system

import os
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


class body:
    # The different masses that we will be testing on from the file, in the simulation
    def __init__(self, name, mass, pX0, vX0, color):
        self.name = name
        self.m = mass
        self.p = pX0
        self.v = vX0
        self.c = color
        pass

    def print(self):
        print("Body", self.name, "> m:", self.m, " p:", self.p, " v:", self.v, " c:", self.c)


class n_body_problem:
    def __init__(self, makeAni, stepping, maxTime, bodies):
        self.makeAni = makeAni
        self.stepping = stepping
        self.maxTime = maxTime
        self.bodies = bodies
        pass

    def print(self):
        print("N Body Sim > make animation:", self.makeAni, " stepping:", self.stepping, " maxTime:", self.maxTime, " num Bodies:", self.bodies.len())


def fileReader(filename = "InfoFile.txt"):
    # Read from a file that is either input by the user or just the standard InformationFile.txt
    with open(filename) as f:                       # Open the 
        lines = f.readlines()                       # Read in the file's contents
        fixed_lines = [line[:-1] for line in lines] # Remove the next line character
    return fixed_lines


def parser(data):
    # Takes in file information and then parses it accordingly, creating new bodies 
    num_of_bodies = int((len(data) - 1) / 5) # Remove the first line then there are 5 points of info for each body
    makeAni, stepping, maxTime = data[0].split() # Take the first 3 paramaters 
    # Make animation, the stepping function, and the max Time for program to run

    bodies = []
    for i in range(num_of_bodies):
        n = str(data[(i*5) + 1])      
        m = int(data[(i*5) + 2])
        p = np.array(data[(i*5 + 3)].split(','))
        v = np.array(data[(i*5 + 4)].split(','))
        c = str(data[(i*5 + 5)])

        b = body(n, m, p, v, c)
        bodies.append(b)
    
    return makeAni,stepping,maxTime,bodies

d = fileReader()
nbp = n_body_problem(parser(d))