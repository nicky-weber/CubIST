""" Convert RA, DEC, and ROLL coordinates to the star camera body frame. 313 euler
    rotation. Return as a quaternion """

# Standard imports:
from pathlib import Path
import logging
import itertools
from time import perf_counter as precision_timestamp
from datetime import datetime

# External imports:
import numpy as np
from numpy.linalg import norm
import math

#----------------- functions --------------------------
#Create the dcm
def dcm_generator (phi, alpha, delta):
    phi = math.radians(phi)
    alpha = math.radians(alpha)
    delta = math.radians(delta)

    c1 = np.array([[1,0,0],[0,math.cos(delta),math.sin(delta)],[0,-1*math.sin(delta),math.cos(delta)]])
    c3 = np.array([[math.cos(phi),math.sin(phi),0],[-1*math.sin(phi),math.cos(phi),0],[0,0,1]])
    c3_2 = np.array([[math.cos(alpha),math.sin(alpha),0],[-1*math.sin(alpha),math.cos(alpha),0],[0,0,1]])

    #multiply 313 sequence in 2 steps 3*1 then (3*1)*3_2
    int = np.matmul(c3_2,c1)

    c313 = np.matmul(int,c3)


    #print(c313)
    return c313

#Return the quaternion
def quat_generator (c313):
    #math conversion is easier than eigenvalue conversion. Both return the same thing
    Q = c313
    q4 = 0.5*(math.sqrt((1+ Q[0][0] + Q[1][1] + Q[2][2])))
    q1 = (Q[1][2] - Q[2][1])/(4*q4)
    q2 = (Q[2][0] - Q[0][2])/(4*q4)
    q3 = (Q[0][1] - Q[1][0])/(4*q4)

    q = np.vstack([q1,q2,q3,q4])
    #quat = np.transpose(q)
    print('Quaternion:')
    print(q)
    return q

#-------------------- main ---------------------------

#define phi alpha and delta for testing
phi = 329 #degrees
alpha = 240.5
delta = 28.9

c313 = dcm_generator (phi, alpha, delta)
kumquat = quat_generator(c313)
