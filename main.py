from tkinter import *
from tkinter import messagebox
import random as rand
import time
import classes
import math
import math_functions as mfs

#######global variabls
padding = 10
objs = [] # initialize the global list that will hold the objects
max_objects = 9 # used to create the ball pyramid
default_magnitude = "40" # arbitrary number I picked for the initial cue velocity
time_limit = 20 # arbitrary timer number I picked
sim_running = False # used tp control the sim loop
collision_buffer = 0 # I was testing to see if trying to have a collison buffer would stop the bug of when the objects get stuck under each other
default_diameter = 20 # basically how big we make the stuff

######button functions
# clear the canvas and create the new objects according to the values for each object and num of objects
def CreateObjects():
    global objs
    for object in objs:#clear any existing objs
        canvas_object = object.tk_info["canvas_object"]
        sim_canvas.delete(canvas_object)
    objs = []

    #print("creating the new num objects for the scene")
    CreateObjectsScene()

def UpdateCue():
    if sim_running:
        return
    cue_ball = objs[0]
    magnitude = float(cue_ball.tk_info["cue_magnitude_entry"].get())
    angle = float(cue_ball.tk_info["cue_angle_entry"].get())
    #update the object
    cue_ball.Update(cue_ball.coords, magnitude, angle)
    #update the canvas
    UpdateCanvas(cue_ball)

        

def UpdateCanvas(object): #deletes the old canvas object and draws a new one
    old_canvas_object = object.tk_info["canvas_object"]
    #sim_canvas.move(old_canvas_object, object.coords[0], object.coords[1])
    sim_canvas.delete(old_canvas_object)
    diameter = object.object_diameter
    new_canvas_object = sim_canvas.create_rectangle(object.coords[0], canvas_height-(object.coords[1]), object.coords[0]+diameter, canvas_height-(object.coords[1]+diameter), fill=object.object_color, width=0)
    object.tk_info["canvas_object"] = new_canvas_object

#starts the simulation
def Run_Sim():
    global timer
    global sim_running
    if sim_running == True: #this will shut off the sim if the sim is running
        sim_running = False
        return
    
    # update the cue ball input stuff
    UpdateCue()
    print("Beginning Simulation")
    sim_running=True#this indicates we are starting the sim
    #make the timer show up
    initial_time = time.time()#this gives us a start time
    run_time = initial_time #this initializes the run_time to be the same as intial time so we can see the change in time
    sim_canvas.delete(timer)#this clears the timer and writes it again
    timer = sim_canvas.create_text(20,20, font=("Arial", 18, "normal"), text=int(time_limit))
    wn.update()# here we update the window so everything is ready to start
    while sim_running:#this si the main sim loop
        if run_time-initial_time >= time_limit:# if we hit the time limit turn off the sim
            sim_running = False
        

        for object in objs:#go throw and move each object every frame
            MoveObj(object, time.time()-run_time)
    
        sim_canvas.delete(timer)#this updates are timer with the new count down time
        timer = sim_canvas.create_text(20,20, font=("Arial", 18, "normal"), text=int(time_limit-(run_time-initial_time)))
        wn.update()#updaets the window so it will display the stuff otherwise it freezes
        run_time = time.time()#updates are run_time
        time.sleep(0.00000000001)#python doesn't like infinitly fast while loops

    print("Ending Simulation")
    # sim_canvas.delete(timer) # we could delete the timer after it ends but idc


def MoveObj(object, change_time):
    #every time this is called we add the velocity and update the objects location, then update the canvas
    #change in distance = V*change in time so velocity times time
    new_x = object.coords[0]+object.velocity_vector.components[0]*change_time
    new_y = object.coords[1]+object.velocity_vector.components[1]*change_time
    #keeping the object inside the canvas, bounds
    if new_x > canvas_width-object.object_diameter:# if its past the right side
        new_x = canvas_width-object.object_diameter
        object.velocity_vector.components[0] *= -1
    elif new_x < 0:# if its past the left side
        new_x = 0
        object.velocity_vector.components[0] *= -1

    if new_y > canvas_height-object.object_diameter: # if its past the top
        new_y = canvas_height-object.object_diameter
        object.velocity_vector.components[1] *= -1
    if new_y < 0: #if its past the bottom
        new_y = 0
        object.velocity_vector.components[1] *= -1

    object.coords = [new_x, new_y]
    UpdateCanvas(object)#this draws the new shape 
    #after we move we want to check for collisions and change the velocities
    CheckForCollisions()

def CheckForCollisions():
    for o in range(0, len(objs)):
        o_object = objs[o]
        o_four_points = [o_object.coords[0]-collision_buffer, canvas_height-(o_object.coords[1])-collision_buffer, o_object.coords[0]+o_object.object_diameter+collision_buffer, canvas_height-(o_object.coords[1]+o_object.object_diameter+collision_buffer)]
        overlap_list = list(sim_canvas.find_overlapping(o_four_points[0], o_four_points[1], o_four_points[2], o_four_points[3]))
        overlap_list.remove(o_object.tk_info["canvas_object"])
        if len(overlap_list) != 0:
            colliding_objects = []
            for possible_object in objs:
                if possible_object.tk_info["canvas_object"] in overlap_list:#if its the object we dont care
                    colliding_objects.append(possible_object)
            for c in range(0, len(colliding_objects)):
                c_object = objs[c]
                #here is the vector mathstuff
                initial_vector_o = o_object.velocity_vector
                initial_vector_c = c_object.velocity_vector
                # #first I want to calculate the angle between the vectors |a|*|b|*cos(theta)=dot_product
                # #dot_product = a1*b1+a2*b2+a3*b3
                # dot_product = mfs.DotProduct(vector_o, vector_c)
                # theta = math.arccos(dot_product/(vector_o.magnitude*vector_c.magnitude))
                # # momentum = m*v
                # u is initial and v is final
                #https://unacademy.com/content/jee/study-material/physics/velocities-of-colliding-bodies-after-collision-in-1-dimension/#:~:text=Colliding%20Bodies%20Velocity%20Meaning,and%20v2%20%3D%20u1.
                #m1*u1+m2*u2 = m1*v1+m2*v2'
                #as well we are gonna have elatic collisions
                #this means kinetic eneryg is conserved
                #1/2*m1*u1^2+1/2*m2*u2^2 = 1/2*m1*v1^2+1/2*m2*v2^2
                #therefore m1(u1^2-v1^2) = m2(v2^2-u2^2)
                #and m1(u1-v1) = m2(v2-u2)
                #divide m1(u1^2-v1^2) = m2(v2^2-u2^2) by m1(u1-v1) = m2(v2-u2)
                #u1+v1=u2+v2
                #v1=v2+u2-u1
                #plug this into the convervation of momentum
                #v2=[2m1u1+u2(m2-m1)]/(m1+m2)
                #put this back into the v1
                #v1=[2m2u2+u1(m2-m1)]/[m1+m2]
                #vector=(scalar*vector+vector*scalar)/scalar = vector/scalar = vector
                total_mass = (c_object.mass+o_object.mass)
                mass_difference = (c_object.mass-o_object.mass)
                #final_vector_o = ((2*c_object.mass*initial_vector_c)+initial_vector_o(mass_difference))/total_mass
                final_vector_o = mfs.ScalarDivison(total_mass, mfs.VectorAddition(mfs.ScalarMultiple(2*c_object.mass, initial_vector_c), mfs.ScalarMultiple(mass_difference, initial_vector_o)))
                #final_vector_c = (2*o_object.mass*initial_vector_o+initial_vector_c(c_object.mass-o_object.mass))/total_mass
                final_vector_c = mfs.ScalarDivison(total_mass, mfs.VectorAddition(mfs.ScalarMultiple(2*o_object.mass, initial_vector_o), mfs.ScalarMultiple(mass_difference, initial_vector_c)))
                objs[o].velocity_vector = final_vector_o
                objs[c].velocity_vector = final_vector_c
                    


#make tkinter world
wn = Tk() # creates the tkinter window
wn.title("MAT 267")
wn_height = 600
wn_width = 1000
wn.geometry(f"{wn_width}x{wn_height}")
wn.resizable(False, False) # sets the major characteristics of the window

options_frame = Frame(wn, bg="green", width=wn_width/3)#creates the window for user input on the left
options_frame.pack(anchor=W, fill=Y, expand=False, side=LEFT)
#update button
update_button = Button(options_frame, text="Update Objs", activebackground="grey", bg="yellow", command=UpdateCue)
update_button.pack(anchor=N, side=TOP, pady=padding, padx=padding)
#run button runs the simulation
run_button = Button(options_frame, text="Run/Stop Sim", activebackground="grey", bg="orange", command=Run_Sim)
run_button.pack(anchor=N, side=TOP, pady=padding, padx=padding)


content_frame = Frame(wn, bg="orange")
content_frame.pack(anchor=N, fill=BOTH, expand=True, side=LEFT )
sim_canvas = Canvas(content_frame)
sim_canvas.pack(anchor=W, fill=BOTH, expand=True, side=RIGHT, padx=padding, pady=padding)
timer = sim_canvas.create_text(20,20, font=("Arial", 18, "normal"), text=int(time_limit))
wn.update()
content_frame.update()
canvas_height = sim_canvas.winfo_height()
canvas_width = sim_canvas.winfo_width()
coord_sets = [[canvas_width//2,default_diameter*4], [canvas_width//2-default_diameter*1,default_diameter*5], [canvas_width//2+default_diameter*1,default_diameter*5], [canvas_width//2-default_diameter*1.5,default_diameter*6], [canvas_width//2,default_diameter*6], [canvas_width//2+default_diameter*1.5,default_diameter*6], [canvas_width//2-default_diameter*2,default_diameter*7], [canvas_width//2+default_diameter*1,default_diameter*7], [canvas_width//2+default_diameter*1,default_diameter*5], [canvas_width//2+default_diameter*2,default_diameter*5]]
# for i in range(0, int(math.sqrt(max_objects))):
#     for j in range(0, i):
#         coord_sets.append([canvas_width//2, canvas_height//(max_objects-i+0.5)])
#coord_sets = [[canvas_width//2,canvas_height//6],[canvas_width//2,canvas_height//4], [canvas_width//2,canvas_height//3], [canvas_width//2,canvas_height//2]]

#create the objects for the canvas
def CreateObjectsScene():
    global objs
    object_colors = ["grey", "violet", "teal", "yellow", "grey", "red", "blue", "green", "black", "purple"]
    #this will create the canvas scene with all of the objects to be hit and will create their individual information tabs in the otions thingy
    #create the cue ball
    object_color = object_colors[0]
    object_colors.remove(object_color)
    # #create the tkinter user input for the object
    cue_frame = Frame(options_frame, width=wn_width/3, height=wn_height/6)
    cue_frame.pack(side=TOP)
    cue_label = Label(cue_frame, text="Cue Ball", bg=object_color)
    cue_label.pack(side=LEFT)
    #velocity magnitude
    cue_magnitude_label = Label(cue_frame, text="velocity magnitude", bg=object_color)
    cue_magnitude_label.pack()
    cue_magnitude_entry = Entry(cue_frame)
    cue_magnitude_entry.insert(0, default_magnitude)
    cue_magnitude_entry.pack()
    #angle input
    cue_angle_label = Label(cue_frame, text="coords", bg=object_color)
    cue_angle_label.pack()
    cue_angle_entry = Entry(cue_frame)
    cue_angle_entry.insert(0, f"90")
    cue_angle_entry.pack()


    start_coord = [canvas_width//2,default_diameter*2]

    diameter = default_diameter
    canvas_object = sim_canvas.create_rectangle(start_coord[0], canvas_height-(start_coord[1]), start_coord[0]+diameter, canvas_height-(start_coord[1]+diameter), fill=object_color, width=0)

    tk_info = {"cue_frame":cue_frame, "cue_magnitude_entry":cue_magnitude_entry, "canvas_object":canvas_object, "cue_angle_entry":cue_angle_entry}
    
    objs.append(classes.Sim_Object(tk_info, start_coord, object_color, cue=True, magnitude=0, angle=0, object_diameter=diameter))


    num_objects = max_objects#this gets the number of balls to hit
    for i in range(0, int(num_objects)):# go through and make that many objects
        object_color = rand.choice(object_colors)
        object_colors.remove(object_color)

        #canvas object
        start_coord = coord_sets[i]
        diameter = default_diameter
        canvas_object = sim_canvas.create_rectangle(start_coord[0], canvas_height-(start_coord[1]), start_coord[0]+diameter, canvas_height-(start_coord[1]+diameter), fill=object_color, width=0)

        #create a nice way to store this information
        # tk_info = {"object_frame":object_frame, "object_magnitude_entry":object_magnitude_entry, "canvas_object":canvas_object, "object_angle_entry":object_angle_entry}
        tk_info = {"canvas_object":canvas_object}

        new_object = classes.Sim_Object(tk_info, start_coord, object_color, magnitude=0, angle=0, object_diameter=diameter)
        objs.append(new_object)

CreateObjects()
wn.mainloop()
