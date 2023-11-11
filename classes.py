#*******************
"""
Author:Connor Owens
Project: MAT 267 Honors Enrichment Project
Description: create all of the custom classes that will be 
used in the project.
"""
#*******************

import math
class Vector:
    #vector class to modulatize/object orient the code better
    def __init__(self, magnitude, angle):
        #goes through the components and adds up their squares, sum of squares
        self.magnitude = magnitude
        self.angle = angle*(math.pi/180)
        self.components = [magnitude*math.cos(angle), magnitude*math.sin(angle)]
        

class Coords:
    def __init__(self, cords_list):
        self.x = cords_list[0]
        self.y = cords_list[1]

class Sim_Object:
    #each object will have its canvas object starting x,y,z coord; z,y, and z velocities

    def __init__(self, tk_info, coords, object_color, magnitude, angle, cue=False, object_diameter=10, mass=1):
        self.mass = mass
        self.tk_info = tk_info
        self.coords = coords
        self.object_color = object_color
        #we will use axial velocities as components and go from there
        #we could do an angle method but that's really complex and I wanna get this going

        self.velocity_vector = Vector(magnitude, angle)

        self.object_diameter = object_diameter

    def Update(self, coords, magnitude, angle):
        self.coords = coords
        self.velocity_vector = Vector(magnitude, angle*(math.pi/180))
