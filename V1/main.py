"""
Author:Connor Owens 
Date:Sept/Oct 2023
Project: MAT 267 Honors Enrichment Project
Description: The main simulation file that handles: collision, input, and simulation stuff
"""
from tkinter import *
import random as rand
import time
import classes
import math
import math_functions as mfs
import random
import json
import os

######load the json data with user and player data
file = open(f"{os.getcwd()}/data.json")
data = json.load(file)
file.close()

current_level = "level_"+str(data["max_level"])#this sets the current level to be played as the next level possible for the player
score = data["player_score"]#grabs the stored player_score
cueball = data["level_1"]["cueball"]

#######global variabls
padding = 10 #this is used for spacing in the game section
objs = [] # initialize the global list that will hold the objects
pockets = [] # special objects list of pockets
default_magnitude = "0" # arbitrary number I picked for the initial cue velocity
default_angle = "0"
time_limit = 10 # arbitrary timer number I picked
timer_x = 60 #this is the position for the timer i picked
timer_y = 40
score_counter_x = 60#same thing but the counter
score_counter_y = 60
sim_running = False # used tp control the sim loop
collision_buffer = 2 # I was testing to see if trying to have a collison buffer would stop the bug of when the objects get stuck under each other
default_diameter = 20 # basically how big we make the balls
friction_constant = 0.999999999999 # to be added when the game actually works lol
total_levels = 3 #this is how many levels I've made in the json file
magnitude_cap = 1000

######button functions
def Reset():# this updates the cue balls angle and magnitude given the player input
    global timer
    global score_counter
    global obj
    global pockets
    global score
    global current_level
    if sim_running:#we dont want to edit it when the sim is running
        return
    obj = []
    pockets = []
    score = data["player_score"]
    sim_canvas.delete('all')
    CreateObjectsScene()
    CreatePockets()
    timer = sim_canvas.create_text(timer_x,timer_y, font=("Arial", 18, "normal"), text="Time: "+str(time_limit))
    score_counter = sim_canvas.create_text(score_counter_x,score_counter_y, font=("Arial", 18, "normal"), text="Score: "+str(score))
    cue_ball = objs[0]#the first object in the list is the cue ball
    magnitude = float(cue_ball.tk_info["cue_magnitude_entry"].get())#grabs the mang and angle
    if magnitude > magnitude_cap:
        magnitude = magnitude_cap
        cue_ball.tk_info["cue_magnitude_entry"].delete(0, END)
        cue_ball.tk_info["cue_magnitude_entry"].insert(0, str(magnitude_cap))
    angle = float(cue_ball.tk_info["cue_angle_entry"].get())
    #update the object
    cue_ball.Update(data[current_level]["cueball"], magnitude, angle)#update the mag and angle and reset the coords

    # #reset all of the other objs
    # for i in range(1, len(objs)):#skip the first 0, cuz thats the cue ball
    #     objs[i].Update(coord_sets[i-1], 0, 0)#0 mag and angle and then start location
    #     UpdateCanvas(objs[i]) 

def UpdateCanvas(object): #deletes the old canvas object and draws a new one
    old_canvas_object = object.tk_info["canvas_object"]
    #sim_canvas.move(old_canvas_object, object.coords[0], object.coords[1])
    sim_canvas.delete(old_canvas_object)
    diameter = object.object_diameter
    new_canvas_object = sim_canvas.create_oval(object.coords[0], canvas_height-(object.coords[1]), object.coords[0]+diameter, canvas_height-(object.coords[1]+diameter), fill=object.object_color, width=0)
    object.tk_info["canvas_object"] = new_canvas_object

def UpdateScore():
    global score_counter
    sim_canvas.delete(score_counter)
    score_counter = sim_canvas.create_text(score_counter_x,score_counter_y, font=("Arial", 18, "normal"), text="Score: "+str(score))

def UpdateJson(new_player_score, new_max_level):
    #udpate the json data structure
    data["player_score"] = new_player_score
    data["max_level"] = new_max_level
    #update the stuff in the json
    with open("data.json", "w") as outfile:
        file_text = json.dumps(data, indent=4)
        # json.dump(data, outfile)
        outfile.write(file_text)


#used in run sim - checks to see if the player has one
def CheckForWinCondition():
    global current_level
    if score-data["player_score"] >= len(data[current_level]["balls"]):#if the dif in run score and player score is = to num balls, then all the balls must of hit pockets
        #we won the level
        #do our win animation
        #we need to update the player_score and the max level
        if data["max_level"] != total_levels:# if we arn't at the max level
            UpdateJson(score, data["max_level"]+1)# save our score and move up 1 level
            current_level = "level_"+str(data["max_level"]) # for when we reset to go to the next level
            level_label.config(text=current_level.upper())#updates the current level label
            options_frame.update()
        else:# we are at max level
            UpdateJson(score, data["max_level"])# update score but keep level the same
        Reset() # load the current level, new or old
    else:
        #this run failed to win the level
        print("run failed")

#starts the simulation
def Run_Sim():
    global timer
    global sim_running
    if sim_running == True: #this will shut off the sim if the sim is running
        sim_running = False
        return
    
    # update the cue ball input stuff
    Reset()
    print("Beginning Simulation")
    sim_running=True#this indicates we are starting the sim
    #make the timer show up
    initial_time = time.time()#this gives us a start time
    run_time = initial_time #this initializes the run_time to be the same as intial time so we can see the change in time
    wn.update()# here we update the window so everything is ready to start
    while sim_running:#this si the main sim loop
        if run_time-initial_time >= time_limit:# if we hit the time limit turn off the sim
            sim_running = False

        for object in objs:#go throw and move each object every frame
            MoveObj(object, time.time()-run_time)
        
        #after we move we want to check for collisions and change the velocities, and 
        CheckForCollisions()
    
        sim_canvas.delete(timer)#this updates are timer with the new count down time
        timer = sim_canvas.create_text(timer_x,timer_y, font=("Arial", 18, "normal"), text="Time: "+str(int(time_limit-(run_time-initial_time))))
        wn.update()#updaets the window so it will display the stuff otherwise it freezes
        run_time = time.time()#updates are run_time
        time.sleep(0.0001)#python doesn't like infinitly fast while loops

    print("Ending Simulation")
    #check to see if they beat the level - win condition
    CheckForWinCondition()
    

def MoveObj(object, change_time):
    #every time this is called we add the velocity and update the objects location, then update the canvas
    #change in distance = V*change in time so velocity times time
    new_x = object.coords[0]+object.velocity_vector.components[0]*change_time
    new_y = object.coords[1]+object.velocity_vector.components[1]*change_time
    #keeping the object inside the canvas, bounds
    if new_x > canvas_width-object.object_diameter:# if its past the right side
        new_x = canvas_width-object.object_diameter
        #to flip the angle i came up the formula p = 2*vector.angle + 180complementary 
        new_vector = classes.Vector(magnitude=object.velocity_vector.magnitude, angle=(2*object.velocity_vector.angle+(math.pi-object.velocity_vector.angle))*(180/math.pi)) #if it hits the sides we have to flip the angle to flip the vector
        object.velocity_vector = new_vector
    elif new_x < 0:# if its past the left side
        new_x = 0
        new_vector = classes.Vector(magnitude=object.velocity_vector.magnitude, angle=(2*object.velocity_vector.angle+(math.pi-object.velocity_vector.angle))*(180/math.pi)) #if it hits the sides we have to flip the angle to flip the vector
        object.velocity_vector = new_vector

    if new_y > canvas_height-object.object_diameter: # if its past the top
        new_y = canvas_height-object.object_diameter
        new_vector = classes.Vector(magnitude=object.velocity_vector.magnitude, angle=(2*object.velocity_vector.angle+(math.pi-object.velocity_vector.angle))*(180/math.pi)) #if it hits the sides we have to flip the angle to flip the vector
        object.velocity_vector = new_vector
    if new_y < 0: #if its past the bottom
        new_y = 0
        new_vector = classes.Vector(magnitude=object.velocity_vector.magnitude, angle=(2*object.velocity_vector.angle+(math.pi-object.velocity_vector.angle))*(180/math.pi)) #if it hits the sides we have to flip the angle to flip the vector
        object.velocity_vector = new_vector

    object.coords = [new_x, new_y]
    UpdateCanvas(object)#this draws the new shape 

def CheckForCollisions():
    global score
    for o in range(0, len(objs)):
        o_object = objs[o]
        o_four_points = [o_object.coords[0]-collision_buffer, canvas_height-(o_object.coords[1])-collision_buffer, o_object.coords[0]+o_object.object_diameter+collision_buffer, canvas_height-(o_object.coords[1]+o_object.object_diameter+collision_buffer)]
        overlap_list = list(sim_canvas.find_overlapping(o_four_points[0], o_four_points[1], o_four_points[2], o_four_points[3]))
        overlap_list.remove(o_object.tk_info["canvas_object"])#remove o from that overlap list
        if len(overlap_list) != 0:
            for c in range(0, len(objs)):# loop through every object, then we will loop through pockets
                if objs[c].tk_info["canvas_object"] in overlap_list:#if the object is in the overlap list
                    c_object = objs[c]
                    #here is the vector mathstuff
                    initial_vector_o = o_object.velocity_vector
                    initial_vector_c = c_object.velocity_vector
                    if initial_vector_c.magnitude == 0 and initial_vector_o.magnitude == 0:
                        #we dont care if they arnt moving
                        continue
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
                    collision_randomizer = random.uniform(0.9,1.1)# to add a little spice
                    #final_vector_o = ((2*c_object.mass*initial_vector_c)+initial_vector_o(mass_difference))/total_mass
                    final_vector_o = mfs.ScalarDivison(total_mass, mfs.VectorAddition(mfs.ScalarMultiple(2*c_object.mass, initial_vector_c), mfs.ScalarMultiple(mass_difference, initial_vector_o)))
                    #final_vector_c = (2*o_object.mass*initial_vector_o+initial_vector_c(c_object.mass-o_object.mass))/total_mass
                    final_vector_c = mfs.ScalarDivison(total_mass, mfs.VectorAddition(mfs.ScalarMultiple(2*o_object.mass, initial_vector_o), mfs.ScalarMultiple(mass_difference, initial_vector_c)))
                    objs[o].velocity_vector = final_vector_o
                    objs[c].velocity_vector = final_vector_c
                    # print(final_vector_c.components)
                    # print(final_vector_o.components)
                    move_that_b = True
                    while (move_that_b):#after we have changed their velocities we want to move them outside of the range where they will trigger another collision and cause a rebound bug
                        overlap_list = list(sim_canvas.find_overlapping(o_four_points[0], o_four_points[1], o_four_points[2], o_four_points[3]))
                        if c_object.tk_info["canvas_object"] not in overlap_list: # if c isnt empty but c is gone
                            # print("that b is gone")
                            move_that_b = False
                            exit
                        MoveObj(o_object, 0.001)
                        MoveObj(c_object, 0.001)
                        wn.update()
                        time.sleep(0.001)

            for pocket in pockets:#loop through all the pockets to see if they are in the overlap
                if pocket.tk_info["canvas_object"] in overlap_list:# if we collide with a pocket
                    objs.pop(o)# get rid of the ball colliding with the pocket
                    sim_canvas.delete(o_object.tk_info["canvas_object"])# get rid of it on the canvas
                    if o_object.cue == True:#if we scratch
                        score -= 10#idk?
                        UpdateScore()
                    else:
                        score += 1
                        UpdateScore()

#create the objects for the canvas
def CreateObjectsScene():
    global objs
    global current_level

    sim_canvas.delete('all')#clear the canvas
    objs = []
    object_colors = ["violet", "teal", "yellow", "red", "blue", "green", "black", "purple", "indigo", "orange"]
    #this will create the canvas scene with all of the objects to be hit and will create their individual information tabs in the otions thingy
    #create the cue ball
    object_color = "grey"
    start_coord = data[current_level]["cueball"]
    diameter = default_diameter
    canvas_object = sim_canvas.create_oval(start_coord[0], canvas_height-(start_coord[1]), start_coord[0]+diameter, canvas_height-(start_coord[1]+diameter), fill=object_color, width=0)

    tk_info = {"cue_frame":cue_frame, "cue_magnitude_entry":cue_magnitude_entry, "canvas_object":canvas_object, "cue_angle_entry":cue_angle_entry}
    
    objs.append(classes.Sim_Object(tk_info, start_coord, object_color, cue=True, magnitude=float(default_magnitude), angle=float(default_angle), object_diameter=diameter))

    for i in range(0, len(data[current_level]["balls"])):# go through and make that many objects
        object_color = rand.choice(object_colors)
        object_colors.remove(object_color)

        #canvas object
        start_coord = data[current_level]["balls"][i]
        diameter = default_diameter
        canvas_object = sim_canvas.create_oval(start_coord[0], canvas_height-(start_coord[1]), start_coord[0]+diameter, canvas_height-(start_coord[1]+diameter), fill=object_color, width=0)

        #create a nice way to store this information
        # tk_info = {"object_frame":object_frame, "object_magnitude_entry":object_magnitude_entry, "canvas_object":canvas_object, "object_angle_entry":object_angle_entry}
        tk_info = {"canvas_object":canvas_object}

        new_object = classes.Sim_Object(tk_info, start_coord, object_color, magnitude=0, angle=0, object_diameter=diameter, mass=1.2)
        objs.append(new_object)


def CreatePockets():
    default_pocket_size = default_diameter
    for i in range(0, len(data[current_level]["pockets"])):
        new_coords = data[current_level]["pockets"][i]
        canvas_object = sim_canvas.create_rectangle(new_coords[0], canvas_height-(new_coords[1]), new_coords[0]+default_pocket_size, canvas_height-(new_coords[1]+default_pocket_size), fill="black")
        new_pocket = classes.Pocket(tk_info={"canvas_object":canvas_object}, coords=[new_coords], color="black")
        pockets.append(new_pocket)


# title screen
def CreateExplination():
    #unpack everything
    #title
    Pack.pack_forget(title_frame)
    #explination
    # Pack.pack_forget(explination_frame)
    #game
    Pack.pack_forget(options_frame)
    Pack.pack_forget(content_frame)

    #pack the wanted section
    explination_frame.pack(expand=True, fill=BOTH)

def CreateTitle():
    #unpack everything
    #title
    # Pack.pack_forget(title_frame)
    #explination
    Pack.pack_forget(explination_frame)
    #game
    Pack.pack_forget(options_frame)
    Pack.pack_forget(content_frame)

    #pack the wanted section
    title_frame.pack(expand=True, fill=BOTH)                    

def CreateGame():
    global canvas_height
    global canvas_width
    #unpack everything
    #title
    Pack.pack_forget(title_frame)
    #explination
    Pack.pack_forget(explination_frame)
    #game
    # Pack.pack_forget(options_frame)
    # Pack.pack_forget(content_frame)

    #pack the wanted section
    options_frame.pack(anchor=W, fill=Y, expand=False, side=LEFT)
    content_frame.pack(anchor=N, fill=BOTH, expand=True, side=LEFT )
    wn.update()
    canvas_height = sim_canvas.winfo_height()
    canvas_width = sim_canvas.winfo_width()
    # print(canvas_width, canvas_height)
    #set up the game scene
    CreateObjectsScene()
    CreatePockets()

#make tkinter world
wn = Tk() # creates the tkinter window
wn.title("MAT 267")
wn_height = 500
wn_width = 1000
wn.geometry(f"{wn_width}x{wn_height}")
wn.resizable(False, False) # sets the major characteristics of the window

options_frame = Frame(wn, bg="green", width=wn_width/3)#creates the window for user input on the left
# options_frame.pack(anchor=W, fill=Y, expand=False, side=LEFT) # we do this in menu frame
level_label = Label(options_frame, text=current_level.upper())
level_label.pack(anchor=N, pady=padding, padx=padding)
#update button
reset_button = Button(options_frame, text="Reset Objs", activebackground="grey", bg="yellow", command=Reset)
reset_button.pack(anchor=N, side=TOP, pady=padding, padx=padding)
#run button runs the simulation
run_button = Button(options_frame, text="Run/Stop Sim", activebackground="grey", bg="orange", command=Run_Sim)
run_button.pack(anchor=N, side=TOP, pady=padding, padx=padding)

#create the cue ball
cue_frame = Frame(options_frame, width=wn_width/3, height=wn_height/6)
cue_frame.pack(side=TOP)
cue_label = Label(cue_frame, text="Cue Ball")
cue_label.pack(side=LEFT)
#velocity magnitude
cue_magnitude_label = Label(cue_frame, text="velocity magnitude")
cue_magnitude_label.pack()
cue_magnitude_entry = Entry(cue_frame)
cue_magnitude_entry.insert(0, default_magnitude)
cue_magnitude_entry.pack()
#angle input
cue_angle_label = Label(cue_frame, text="Angle")
cue_angle_label.pack()
cue_angle_entry = Entry(cue_frame)
cue_angle_entry.insert(0, default_angle)
cue_angle_entry.pack()

content_frame = Frame(wn, bg="orange")
# content_frame.pack(anchor=N, fill=BOTH, expand=True, side=LEFT ) #we do this in menu frame
sim_canvas = Canvas(content_frame)
sim_canvas.pack(anchor=W, fill=BOTH, expand=True, side=TOP, padx=padding, pady=padding)
timer = sim_canvas.create_text(timer_x,timer_y, font=("Arial", 18, "normal"), text="Time: "+str(time_limit))
score_counter = sim_canvas.create_text(score_counter_x,score_counter_y, font=("Arial", 18, "normal"), text="Score: "+str(score))
wn.update()
content_frame.update()
canvas_height = sim_canvas.winfo_height()
canvas_width = sim_canvas.winfo_width()
# coord_sets = [[canvas_width//2,default_diameter*7+ball_spacer], [canvas_width//2-default_diameter*0.5-ball_spacer,default_diameter*9+ball_spacer], [canvas_width//2+default_diameter*0.5+ball_spacer,default_diameter*9+ball_spacer], [canvas_width//2-default_diameter*1-ball_spacer,default_diameter*11+ball_spacer], [canvas_width//2,default_diameter*11+ball_spacer], [canvas_width//2+default_diameter*1+ball_spacer,default_diameter*11+ball_spacer], [canvas_width//2-default_diameter*1.75-ball_spacer,default_diameter*13+ball_spacer], [canvas_width//2-default_diameter*0.5-ball_spacer,default_diameter*13+ball_spacer], [canvas_width//2+default_diameter*0.5+ball_spacer,default_diameter*13+ball_spacer], [canvas_width//2+default_diameter*1.75+ball_spacer,default_diameter*13+ball_spacer]]


#title frame that will have access to explination frames and then the game frames
title_color = "green"
num_of_widgets = 3
title_spacer = wn_height/(num_of_widgets*4)
title_frame = Frame(wn, bg=title_color)
title_frame.pack(expand=True, fill=BOTH)

title_label = Label(title_frame, font=("Arial", 22, "normal"), text="Vector Calculus 8-Ball", bg=title_color)
title_label.pack(anchor=N, side=TOP, pady=title_spacer)

play_button = Button(title_frame, font=("Arial", 18, "normal"), text="PLAY", command=CreateGame)
play_button.pack(anchor=N, side=TOP, pady=title_spacer)

explination_button = Button(title_frame, font=("Arial", 18, "normal"), text="Explination", command=CreateExplination)
explination_button.pack(anchor=N, side=TOP, pady=title_spacer)

#explination frame - explains the project
explination_frame = Frame(wn, bg=title_color)
explination_text = Text(explination_frame, width=80, height=20, wrap=WORD)

explination_text_text = "HOW TO PLAY\nThis game is about a using vectors to play a game. Knock the balls into the holes to score points, but don't scratch. Put the magnitude of the velocity vector in terms of coords/sec and the angle of the velocity vector in degrees from 0-360. There are three levels can you beat them all?\n\nRead more below for how the game works. \n\nWHY\n\n\nI made this project for my Calc 3 for Engineers, MAT 267, class. The game uses simple vector calculation techniques and principles to create a 2D collision simulation based on user input. The user input is the cueball's velocity vector magnitude and angle from 0-360 degrees. By implementing varying magnitudes, the user can easily identify how an object's velocity vector's magnitude relates to its movement. The game uses a variety of vector calulation methods such as Dot Product and Vector Addition. These concepts and their implementations are explained in more detail below\n\n\nCOLLISION PHYSICS\n\n\nThe physics for 2 objects colliding was taken from __ website by __. Using algebra, equations for the final vectors of each object were found. Becuase vectors are used in the equations, I had to use vector calculus ideas to implement vector addition and subraction and scalar mulitlication and division. Their formulas and implementations are explained below.\n\n\nMATHEMATICS/CALCULUS\n\n\nDot Product=d: Used to get angle between vector and x-axis\nv1=vector 1 v2 = vector 2 theta = angle between vectors 1 and 2\nd=|v1|*|v2|*cos(theta) & d=v1x+v2x+v1y+v2y\nDot Product was used to caclulate the angle between the horizontal vector <1,0> and velocity vectors. This angle was used to detmine the vecotor components with the magnitude.\n\n X and Y components: Used to update the objects locations X*frame_time = change in X\nX=|v|*cos(vector angle) & Y=|v|*sin(vector angle)\n\nFinal Velocity of 2 colliding objects: The two physics equations used for collisions. *o and c don't matter but what is labled o must be of o and same for c.\nFinal_o=((2*c_object.mass*initial_vector_c)+initial_vector_o(mass_difference))/total_mass\nFinal_c=(2*o_object.mass*initial_vector_o+initial_vector_c(c_object.mass-o_object.mass))/total_mass\n\nVector Addition: Used in physics equations\n<a,b>+<d,e> = <a+d,b+e>\n\nVector Subtraction: Used in physics equations\n<a,b>-<d,e> = <a-d,b-e>\n\nScalar Divison: Used in physics equations\nc<a,b> = <c*a,c*b>\n\nScalar Multiple: Used in physics equations\nc<a,b> = <c*a,c*b>\n\n\nFURTHER CONTRIBUTIONS\n\n\n"

explination_text.insert(END, explination_text_text)
explination_text.config(state=DISABLED)
explination_text.pack(anchor=N, side=TOP, pady=title_spacer)
return_button = Button(explination_frame, text="Return to Title", command=CreateTitle)
return_button.pack(anchor=N, side=TOP)

# def load_special

#to allow people to nagivate back to the title and other sections
menubar = Menu(wn)
menubar.add_command(label="Title", command=CreateTitle)
# menubar.add_command(label="Game", command=CreateGame)
menubar.add_command(label="Explination", command=CreateExplination)
game_menu = Menu(menubar, tearoff=0)
game_menu.add_command(label="Play Current", command=CreateGame)
for i in range(1, total_levels):# the idea here is to allow players to go back and play previous levels
    game_menu.add_command(label=f"Level {i}", command=0)
menubar.add_cascade(label="Game", menu=game_menu)

wn.config(menu=menubar)
wn.mainloop()
