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

#define phi alpha and delta for testing
phi = 303.4 #degrees
alpha = 172.368
delta = 57.65
def dcm_generator (phi, alpha, delta):
    phi_d = math.radians(phi)
    alpha_d = math.radians(alpha)
    delta_d = math.radians(delta)
    c1 = np.array([1,0,0],[0,math.cos(delta),math.sin(delta)],[0,-1*math.sin(delta),math.cos(delta)])
    c3 = np.array([math.cos(phi),math.sin(phi),0],[-1*math.sin(phi),math.cos(phi),0],[0,0,1])
    c3_2 = np.array([math.cos(alpha),math.sin(alpha),0],[-1*math.sin(alpha),math.cos(alpha),0],[0,0,1])

    #multiply 313 sequence in 2 steps 3*1 then (3*1)*3_2
    int = c1.dot(c3)

    c313 = int.dot(c3_2)

    return c313
def quat_generator (c313):
    #math conversion is easier than eigenvalue conversion. Both return the same thing
    Q = c313
    q4 = 0.5*(math.sqrt((1+ Q[0][0] + Q[1][1] + Q[2][2])))
    q1 = (Q[1][2] - Q[2][1])/(4*q4)
    q2 = (Q[2][0] - Q[0][2])/(4*q4)
    q3 = (Q[0][1] - Q[1][0])/(4*q4)

    q = np.array([q1,q2,q3,q4])
    quat = np.transpose(q)
    return quat
