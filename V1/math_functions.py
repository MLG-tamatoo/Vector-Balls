"""
Author:Connor Owens 
Date:Sept/Oct 2023
Project: MAT 267 Honors Enrichment Project
Description: the file that stores the object classes
"""
import classes
import math

debug = False
x_unit_vector = classes.Vector(magnitude=1, angle=0)


def DotProduct(vector_a_components, vector_b_components):
    #returns a scalar
    #dot product is A1*B1+A2*B2 as well as |A|*|B|*cos(angle btw the vectors)
    return vector_a_components[0]*vector_b_components[0]+vector_a_components[1]*vector_b_components[1]

def ScalarMultiple(scalar, vector):
    #returns a vector
    # c<a,b> = <c*a,c*b>
    new_magnitude = math.sqrt((vector.components[0]*scalar)**2+(vector.components[1]*scalar)**2)
    new_vector = classes.Vector(magnitude=new_magnitude, angle=vector.angle*(180/math.pi))
    if debug:
        print(f"scal mult - angle {new_vector.angle*(180/math.pi)} magnitude {new_vector.magnitude}")
    return new_vector

def ScalarDivison(scalar, vector):
    #returns a vector
    # c<a,b> = <c*a,c*b>, but in this case 1/c
    new_magnitude = math.sqrt((vector.components[0]/scalar)**2+(vector.components[1]/scalar)**2)
    new_vector = classes.Vector(magnitude=new_magnitude, angle=vector.angle*(180/math.pi))
    if debug:
        print(f"scal div - angle {new_vector.angle*(180/math.pi)} magnitude {new_vector.magnitude}")
    return new_vector

def HorizontalAngle(vector):
    return math.acos(DotProduct(vector.components, x_unit_vector.components)/(vector.magnitude))

def VectorAddition(vector_a, vector_b):
    #returns a vector
    #<a,b>+<d,e> = <a+d,b+e>
    new_components = [vector_a.components[0]+vector_b.components[0], vector_a.components[1]+vector_b.components[1]]
    new_magnitude = math.sqrt(new_components[0]**2+new_components[1]**2)
    if new_magnitude != 0:
        # r*cos(theta) = x_component -> arccos(x_component/r) = theta
        # new_angle = math.acos(new_components[0]/new_magnitude)#this is the issue
        #dotproduct = maga*magb*cos(theta)
        new_angle = math.acos(DotProduct(new_components, x_unit_vector.components)/(new_magnitude))
        if new_components[1] <= 0: #if the y is negative
            new_angle = math.pi*2-new_angle
            
    else:
        new_angle = 0
    new_vector = classes.Vector(magnitude=new_magnitude, angle=new_angle*(180/math.pi))
    if debug:
        print(f"vect add - angle {new_vector.angle*(180/math.pi)} magnitude {new_vector.magnitude}")
    return new_vector

def VectorSubtraction(vector_a, vector_b):
    #returns a vector
    #<a,b>-<d,e> = <a-d,b-e>
    new_components = [vector_a.components[0]-vector_b.components[0], vector_a.components[1]-vector_b.components[1]]
    new_magnitude = math.sqrt(new_components[0]**2+new_components[1]**2)
    if new_magnitude != 0:
        # r*cos(theta) = x_component -> arccos(x-component/r) = theta
        new_angle = new_angle = math.acos(DotProduct(new_components, x_unit_vector.components)/(new_magnitude))
    else:
        new_angle = 0
    new_vector = classes.Vector(magnitude=new_magnitude, angle=new_angle*(180/math.pi))
    if debug:
        print(f"vect sub - angle {new_vector.angle*(180/math.pi)} magnitude {new_vector.magnitude}")
    return new_vector

# test = DotProduct(classes.Vector([1,0,1]), classes.Vector([2,0,-1]))
# print(test)