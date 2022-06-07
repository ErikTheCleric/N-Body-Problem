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
pX0 = []                                        # the inital positions of the masses
vX0 = []                                        # the inital velocitiies of the masses

pos = []                                      # We note the position for the masses
vel = []                                      # We note the velocities for the masses

for i in masses:
    # For each of the masses, we need to initially fill the pos and vel with zeroes to start
    # ... this will be updated later in the acceleration function and velocity calculations
    pos[i] = np.array([[0.,0.,0.] for j in range(maxTime)])
    vel[i] = np.array([[0.,0.,0.] for j in range(maxTime)])

test = [[10, 5, 8], [0, 0, 0], [7, 8 , 9]]                                                
def organizeInformationFromFile(info):
    # We want to organize the information into different things such as masses, pX0, and vX0
    for i in range(len(info)):
        if i % 3 == 0:
            masses.append(int(info[i]))          # If its the first value, then that is a mass
        if i % 3 == 1:
            print(info[i])
            data = info[i].split(',')
            pX0.append(info[i])                 # for the second val, it is a position val
        if i % 3 == 2:
            data = info[i].split(',')
            vX0.append(data)                 # for the third val, it is the velocity val
    print(pX0)
    print(test)

    
organizeInformationFromFile(lines)              # formulate the data into the diff lists


for i in masses:
    # Now that we have the different masses set with there position values and pos / vel set
    # ... we can update the information that we preset to be zeroes and fill in the initial
    # ... datat that we pulled from the file.
    #n = pX0[i]
    pos[i][0] = int(pX0[i])                          # These are the starting conditions of the 
    vel[i][0] = int(vX0[i])                          # ... simulation (the first values)
#y0 = np.concatenate((pX0, vX0))                 # The starting conditions of the simulation
#print(y0)


# Definition of the n body equation
def accelerationCalc(p):
    # Given a set of objects, find the derivations of x, y, and z
    numberOfObjects = len(masses)

    mNum = masses         # We make a set of masses equal to the number
    planet_dv = list(range(numberOfObjects))    # ... from the file
    # init the planet dev to be 0
    
    for i in mNum:
        for j in mNum:
            if(i != j):                         # We don't run the accel function on itself
                planet_dv[i] += -9.8 * mNum[j] * (p[i] - p[j]) / (np.sqrt((p[i][0] - p[j][0])**2 + (p[i][1] - p[j][1])**2 + (p[i][2] - p[j][2])**2)**3)
    #print(len(mNum))
    return planet_dv


# Running the simulation -------------------------------------------------------------------
for i in range(steps - 1):
    dv = []                                     # The derivations of the different points
    # Find the accelerations
    for j in masses:
        dv[j] = accelerations(range(pos[0][i], pos[-1][i]))         # Go to every pos and access the i location

    # update the next step of the velocity
    for j in masses:
        vel[j][i+1] = vel[j][i] + dv[j] * stepping

    # update the position values for the next step
    for j in masses:
        pos[j][i+1] = pos[j][i] + vel[j][i] * stepping

# Now that we have run the simulation, all the data is stored in pos[][] and vel[][] so now
# ... display these values
for m in masses:
    plt.plot([i[0] for i in pos[m]], [j[0] for j in pos[m]], [k[0] for k in pos[m]])

# Now we just show this to the screen and then close
plt.show()
plt.close()
