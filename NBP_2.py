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

# Some other simulations I would like to do:
# > Barnes Hut is a much more optimized version of this brute force method, but done at a 
#   different angle. The problem between this and the other model is that
#   the Barnes Hut algorithm is 2 dimensional while the orgiinal model I created is 3D
#   That means to accurately get the model running time compared to each other, we are going
#   to have to omit a third dimension 

# To run: py NBP_2.py --file_name InfoFile.txt --sim_type mpl

# libraries
from ast import parse
import os
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from argparse import ArgumentParser

# Global constants and variables
GRAV_CONST = 6.67359e-20
THREE_DIM = 3
TWO_DIM = 2
X = 0
Y = 1
Z = 2

# classes and fuctions 
class body:
    # The different masses that we will be testing on from the file, in the simulation
    def __init__(self, name, mass, pX0, vX0, color):
        self.name = name
        self.m = mass
        self.p = np.zeros((1,THREE_DIM))    # position
        self.p[0] = pX0
        self.v = np.zeros((1,THREE_DIM))    # velocity
        self.v[0] = vX0
        self.a = np.zeros((1,THREE_DIM))    # acceleration
        self.c = color
        pass

    def printStats(self):
        print("Body", self.name, "> m:", self.m, " p:", self.p, " v:", self.v, " c:", self.c)

    def resizePosAndVal(self, mt):
        self.p.resize((mt, THREE_DIM))   # The positions for each point (x,y,z)
        self.v.resize((mt, THREE_DIM))   # velocities for each point (x,y,z)

class animation:
    # A class to display a matlibplot graph
    def __init__(self, show_axis_grid, dark_background, proj, panes):
        plt.rcParams['axes.grid'] = show_axis_grid
        if dark_background:
            plt.style.use('dark_background')
        figure = plt.figure()
        ax = plt.axes(projection = proj)

        ax.w_xaxis.pane.fill = panes
        ax.set(xlabel = 'X')
        ax.w_yaxis.pane.fill = panes
        ax.set(ylabel = 'Y')
        if proj == '3d':
            ax.w_zaxis.pane.fill = panes
            ax.set(zlabel = 'Z')
    
    def animate(self, timestep, ptd, bodies):
        self.ax.clear()
        for b in bodies:
            # TODO FILL IN
            self.ax.plot3D()
    
    def display(self, makeAni, steps, bodies):
        if makeAni:
            anim = animation.FuncAnimation(self.figure, self.animate, frames = steps, fargs = (bodies), interval = 1, repeat = True)
        else:
            for b in bodies:
                plt.plot([],[],[], '-', color = bodies.c, lw = 2.0, markersize = 0.1, alpha=1)


class n_body_problem_bf_3d:
    # N body problem brute force 3D
    def __init__(self, makeAni, stepping, maxTime, bodies):
        self.animation = makeAni
        self.stepping = float(stepping)
        self.maxTime = int(maxTime)
        self.bodies = bodies
        self.numsteps = (self.maxTime / self.stepping)
        self.time = np.arange(0, self.maxTime, self.stepping)
        # Resize the bodies pos and velocity vectors to hold the amount of time units to the maxtime
        for b in self.bodies:
            b.resizePosAndVal(self.maxTime)
        pass

    def accelCalc(self, time):
        # Given a set of b (bodies), find the brute force derivation of x, y, and z
        # This gives O(n^2) complexity as we have to compute how each body affects each other
        for body1 in self.bodies:
            for body2 in self.bodies:
                if(body1 != body2):
                    body1.a += -9.8 * body2.m * (body1.p[time] - body2.p[time]) / (np.sqrt((body1.p[time][X] - body2.p[time][X])**2 + (body1.p[time][Y] - body2.p[time][Y])**2 + (body1.p[time][Z] - body2.p[time][Z])**2)**3)
        pass

    def simulation(self):
        # The actual code of the simulation
        for currTimeStep in range(self.maxTime - 1):   
            # Calculate the accelerations
            self.accelCalc(currTimeStep)

            for b in self.bodies:
                # Update the next step of the velocity
                b.v[currTimeStep + 1] = b.v[currTimeStep] + b.a * self.stepping

                # Update the position values for the next step
                b.p[currTimeStep + 1] = b.p[currTimeStep] + b.v[currTimeStep] * self.stepping
        pass

    #def animation(self, num, ptd, numMasses):
        


    def display(self):
        # Show the animation or just the picture
        pass
            
            
    
    def printStats(self):
        print("N Body Sim > make animation:", self.animation, " stepping:", self.stepping, " maxTime:", self.maxTime, " num Bodies:", len(self.bodies))


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
    
    return makeAni, stepping, maxTime, bodies


if __name__ == "__main__":
    # Reading in arguments file name and the type of simulation
    inputFromUser = ArgumentParser()
    inputFromUser.add_argument("--file_name", help = "The file name you want to read")
    inputFromUser.add_argument("--sim_type", help = "which simulation to perform: mpl3, ...")
    args = inputFromUser.parse_args()

    d = fileReader(str(args.file_name))
    mA, step, mT, b = parser(d)
    nbp = n_body_problem_bf_3d(mA, step, mT, b)
    
    
