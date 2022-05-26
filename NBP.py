# 3/n body problem
# Erik Hale
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


import os
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Reading from a file ----------------------------------------------------------------------
fileName = "InformationFile.txt"                # A file that contains information in the
                                                # format of different orbital bodies, their
                                                # mass, init position, and init velocity
with open(fileName) as f:                       # reading the contents from the entire file
    lines = f.readlines()
    #print(lines)
    for b in range(len(lines) - 1):             # We want to remove the last character which
        temp = lines[b]                         # ... is the '\n' or newline, so that we can
        lines[b] = temp[:-1]                    # ... just set the values later 
    #print(lines)                               # Use the "print()"s to see the differences

# Creating the 3D plot ---------------------------------------------------------------------
# Creation of the grid 
plt.rcParams['axes.grid'] = True
plt.style.use('dark_background')
figure = plt.figure()                           # We want the figure to be created
ax = figure.add_subplot(projection = '3d')      # We want to make this a 3D model
# Making the graph look pretty
ax.w_yaxis.pane.fill = False                    # Makes the pane the same color as the 
ax.w_xaxis.pane.fill = False                    # ... background, so the data can be seen 
ax.w_zaxis.pane.fill = False                    # ... easier.
# Setting the axes properties
ax.set(xlim3d=(0, 6000), xlabel='X')            # We can make the custom dimensions for the    
ax.set(ylim3d=(0, 14000), ylabel='Y')           # ... labels so that the graph shows up.
ax.set(zlim3d=(0, 7000), zlabel='Z')            # We may make the values 

# Constructing the Simulation --------------------------------------------------------------
# Creating the times and constants
G = 6.67359e-20                                 # (km**3/kg/s**2) The Gravity constant
stepping  = 0.5
maxTime = 480
time = np.arange(0,maxTime, stepping)           # The time from 0 to maxTime in stepping
                                                # ... increments

masses = []                                     # The masses of the objects
rX0 = []                                        # the inital positions of the masses
vX0 = []                                        # the inital velocitiies of the masses
                                                
def organizeInformationFromFile(info):
    # We want to organize the information into different things such as masses, rX0, and vX0
    for i in range(len(info)):
        if i % 3 == 0:
            masses.append(info[i])              # If its the first value, then that is a mass
        if i % 3 == 1:
            rX0.append(info[i])                 # for the second val, it is a position val
        if i % 3 == 2:
            vX0.append(info[i])                 # for the third val, it is the velocity val
    #print(masses, rX0, vX0)
    
organizeInformationFromFile(lines)              # formulate the data into the diff lists

y0 = np.concatenate((rX0, vX0))                 # The starting conditions of the simulation
print(y0)

# Definition of the n body equation
def nBodyEquation(stateVec, time, gravity, masses):
    # This will define the n body problem


