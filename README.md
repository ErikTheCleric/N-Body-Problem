# N-Body-Problem
Made by:
Erik Hale

## Description
Having completed the 2 Body Problem Simulation, this code will be a simulation of the 3 Body Problem / N-Body Problem, where there are n amounts of masses that affect each other gavitationally. This could simulate how objects in star systems move or how planets with moons are affected. The idea would be to have a text file to upload information to, so that files could be uploaded with ease.

## Inspiration
I found this article published by Princeton that talks about simulating the N body problem in different ways for a computer where the brute force way is to use the standard equation for accurate results that take a long time (O(n^2): this is becuase we have to go through the data to get the sum of the forces for each mass. I'll implement this version first, as I really meant for this program to only deal with a few masses at a time and not a cluster of masses as the article recommends for a larger amount of masses, though it may be something that I attempt in the future. Link: https://physics.princeton.edu//~fpretori/Nbody/intro.htm

Another Link that I am basing a lot of this work on is: https://blbadger.github.io/3-body-problem.html. It is the basis of this program but scaled up for more masses in a simulation as that was the 3 body problem and this is the N-body problem.

## Updates
10/27/2022: I have begun work on a second more readable and usable implementation of the N-Body-Problem code, setting up classes and other functions that take in and parse files
