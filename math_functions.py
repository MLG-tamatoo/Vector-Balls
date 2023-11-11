import classes
import math

def DotProduct(vector_a, vector_b):
    #returns a scalar
    #dot product is A1*B1+A2*B2 as well as |A|*|B|*cos(angle btw the vectors)
    return vector_a.components[0]*vector_b.components[0]+vector_a.components[1]*vector_b.components[1]

def ScalarMultiple(scalar, vector):
    #returns a vector
    # c<a,b> = <c*a,c*b>
    new_magnitude = math.sqrt((vector.components[0]*scalar)**2+(vector.components[1]*scalar)**2)
    return classes.Vector(magnitude=new_magnitude, angle=vector.angle)

def ScalarDivison(scalar, vector):
    #returns a vector
    # c<a,b> = <c*a,c*b>, but in this case 1/c
    new_magnitude = math.sqrt((vector.components[0]/scalar)**2+(vector.components[1]/scalar)**2)
    return classes.Vector(magnitude=new_magnitude, angle=vector.angle)

def VectorAddition(vector_a, vector_b):
    #returns a vector
    #<a,b>+<d,e> = <a+d,b+e>
    new_components = [vector_a.components[0]+vector_b.components[0], vector_a.components[1]+vector_b.components[1]]
    new_magnitude = math.sqrt(new_components[0]**2+new_components[1]**2)
    if new_magnitude != 0:
        # r*cos(theta) = x_component -> arccos(x-component/r) = theta
        new_angle = math.acos(new_components[0]/new_magnitude)
    else:
        new_angle = 0
    return classes.Vector(magnitude=new_magnitude, angle=new_angle)

def VectorSubtraction(vector_a, vector_b):
    #returns a vector
    #<a,b>-<d,e> = <a-d,b-e>
    new_components = [vector_a.components[0]-vector_b.components[0], vector_a.components[1]-vector_b.components[1]]
    new_magnitude = math.sqrt(new_components[0]**2+new_components[1]**2)
    if new_magnitude != 0:
        # r*cos(theta) = x_component -> arccos(x-component/r) = theta
        new_angle = math.acos(new_components[0]/new_magnitude)
    else:
        new_angle = 0
    return classes.Vector(magnitude=new_magnitude, angle=new_angle)

# test = DotProduct(classes.Vector([1,0,1]), classes.Vector([2,0,-1]))
# print(test)