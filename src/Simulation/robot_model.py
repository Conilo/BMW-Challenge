"""Defines a differential and unicycle 
drive robot and makes it describe a 
simple path"""

from matplotlib import pyplot as plt
import matplotlib.patches as patches
from math import sin, cos

class Robot(object):
    """Defines basic mobile robot properties"""
    def __init__(self):
        self.pos_x  = 0.0
        self.pos_y  = 0.0
        self.angle  = 0.0
        self.plot   = False
        self._delta = 1

    def getDelta(self):
        return self._delta
    def setDelta(self,x):
    	self._delta=x
    	 
    # Movement
    def step(self):
        """ updates the x,y and angle """
        self.deltax()
        self.deltay()
        self.deltaa()

    def move(self, seconds):
        """ Moves the robot for an 's' amount of seconds"""
        for i in range(int(seconds/self._delta)):
            self.step()
            if i % 3 == 0 and self.plot: # plot path every 3 steps
                self.plot_xya()

    def update(self):
        self.step()
        if self.plot:
            self.plot_xya()

    # Printing-and-plotting:
    def print_xya(self):
        """ prints the x,y position and angle """
        print ("x = " + str(self.pos_x) +" "+ "y = " + str(self.pos_y))
        print ("a = " + str(self.angle))

    def plot_robot(self):
        """ plots a representation of the robot """
        plt.arrow(self.pos_x, self.pos_y, 0.001
                  * cos(self.angle), 0.001 * sin(self.angle),
                  head_width=self.length, head_length=self.length,
                  fc='k', ec='k')

    def plot_xya(self):
        """ plots a dot in the position of the robot """
        plt.scatter(self.pos_x, self.pos_y, c='r', edgecolors='r')


class DDRobot(Robot):
    """Defines a differential drive robot"""

    def __init__(self,R,L):
        Robot.__init__(self)
        self.radius = R
        self.length = L

        self.rt_spd_left = 0.0
        self.rt_spd_right = 0.0

    def deltax(self):
        """ update x depending on l and r angular speeds """
        self.pos_x += self._delta * (self.radius*0.5) \
        * (self.rt_spd_right + self.rt_spd_left)*cos(self.angle)

    def deltay(self):
        """ update y depending on l and r angular speeds """
        self.pos_y += self._delta * (self.radius*0.5) \
        * (self.rt_spd_right + self.rt_spd_left)*sin(self.angle)

    def deltaa(self):
        """ update z depending on l and r angular speeds """
        self.angle += self._delta * (self.radius/self.length) \
        * (self.rt_spd_right - self.rt_spd_left)

class Unicycle(Robot):
    """Defines Unicycle robot"""
    def __init__(self):
        Robot.__init__(self)
        self.radius = 0.04
        self.length = 0.1

        self.vel=0
        self.vel_an=0

    def deltax(self):
        """ update x depending on l and r angular speeds """
        self.pos_x += self._delta * (self.vel)*cos(self.angle)

    def deltay(self):
        """ update y depending on l and r angular speeds """
        self.pos_y += self._delta * (self.vel)*sin(self.angle)

    def deltaa(self):
        """ update z depending on l and r angular speeds """
        self.angle += self._delta * self.vel_an

        
def Unicycle_to_Differential(V,Th_dot,L=0.4,R=0.1):
    Vr=V/R+(L*Th_dot)/(2*R)
    Vl=V/R-(L*Th_dot)/(2*R)
    return (Vr,Vl)

def Diff_to_Uni(Vr,Vl,L=0.4,R=0.1):
    V=(R/2.0)*(Vl+Vr)
    Th_dot=(R/L)*(Vr-Vl)
    return(V,Th_dot)
