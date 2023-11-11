"""IGNORE THIS FILE, I THINK IT IS JUST A COPY OF THE ROUGH DRAFT BEFORE CHANGES TO V1"""

"""
Author:Connor Owens 
Date:Sept/Oct 2023
Project: MAT 267 Honors Enrichment Project
Description: The main simulation file that handles: collision, input, and simulation stuff
"""


from tkinter import *
from tkinter import ttk
import classes

#######global variabls
xpadding = 10
ypadding = 10
objs = []
max_objects = 6

######button functions
# clear the canvas and create the new objects according to the values for each object and num of objects
def CreateObjects():
    global objs
    #print("clearing the objects from the window")
    for object in objs:
        object_frame = object.tk_info["object_frame"]
        canvas_object = object.tk_info["canvas_object"]
        object_frame.destroy()
        sim_canvas.delete(canvas_object)
    objs = []

    #print("creating the new num objects for the scene")
    CreateObjectsScene()

def UpdateObjs():
    for object in objs:
        x_velocity = int(object.tk_info["object_x_velocity_entry"].get())
        y_velocity = int(object.tk_info["object_y_velocity_entry"].get())
        z_velocity = int(object.tk_info["object_z_velocity_entry"].get())
        coords = object.tk_info["object_coords_entry"].get().split(",")
        coords = [int(coords[0]), int(coords[1]), int(coords[2])]
        #update the object
        object.Update(coords, x_velocity, y_velocity, z_velocity)
        #update the canvas
        UpdateCanvas(object)
  

def UpdateCanvas(object):
    old_canvas_object = object.tk_info["canvas_object"]
    sim_canvas.delete(old_canvas_object)
    diameter = object.object_diameter
    new_canvas_object = sim_canvas.create_oval(object.coords[0], wn_height-object.coords[1], object.coords[0]+diameter, wn_height-object.coords[1]+diameter)
    object.tk_info["canvas_object"] = new_canvas_object
#starts the simulation
def Run_Sim():
    print("read all of the object entries and update their velocities to whats in the entries")
    UpdateObjs()
    print("Beginning Simulation")

    print("we do something")

    print("Ending Simulation")


#make tkinter world
wn = Tk() # creates the tkinter window
wn.title("MAT 267")
wn_height = 700
wn_width = 1000
wn.geometry(f"{wn_width}x{wn_height}")
wn.resizable(False, False) # sets the major characteristics of the window

s = ttk.Style()#this lets us edit the style of stuff

options_frame = ttk.Frame(wn, width=wn_width/3, height=wn_height, )#creates the window for user input on the left
s.configure("options_frame", background="green")
options_frame.grid(row=0, column=0, rowspan=max_objects*9, columnspan=3)# nine objects, 
#propogate button reads the num of objects and creates the associated labels and propogates the canvas with the num of objects
propogate_button = ttk.Button(options_frame, text="Propogate Sim", command=CreateObjects, width=20)
##_*style stuff necesary for it
propogate_button.grid(row=0, column=0, pady=ypadding)
# #update button
# update_button = Button(options_frame, text="Update Objs", activebackground="grey", bg="yellow", command=UpdateObjs, width=20)
# update_button.grid(row=0, column =1, pady=ypadding)
# # run button runs the simulation
# run_button = Button(options_frame, text="Run Sim", activebackground="grey", bg="orange", command=Run_Sim, width=20)
# run_button.grid(row=0, column=2, pady=ypadding)

# num_objects_label = Label(options_frame, text="Num Objs")#this is the number of stationary objects in the window, for now only 1
# num_objects_label.grid(row=1, column=1)#the .grid is what makes things show up
# num_objects_entry = Entry(options_frame)# the user input
# num_objects_entry.insert(0, "1")#sets the default user input to 1
# num_objects_entry.grid(row=2, column=1)


# content_frame = Frame(wn, bg="orange")
# content_frame.grid(row=0, column=4, columnspan=30, rowspan=30)# no span because its only the canvas
# sim_canvas_width = wn_width/2
# sim_canvas_height = wn_height/2
# sim_canvas = Canvas(content_frame, width=sim_canvas_width, height=sim_canvas_height, bg="blue")
# coord_sets = [[100,100],[100,150], [200,200], [300,300], [400,400]]
# sim_canvas.grid(row=0, column=4, columnspan=30, rowspan=30)

# #create the objects for the canvas
# def CreateObjectsScene():
#     global objs
#     #this will create the canvas scene with all of the objects to be hit and will create their individual information tabs in the otions thingy
#     num_objects_input = num_objects_entry.get()#this gets the user input for reading
#     for i in range(0, int(num_objects_input)):# go through and make that many objects
#         print("Creating Object "+ str(i+1))

#         if i < max_objects/2:
#             object_column_count = 0
#         else:
#             object_column_count = 2
#         object_row_count = i%(max_objects//2)+3
    

#         #create the tkinter user input for the object
#         object_frame = Frame(options_frame, width=wn_width/3, height=wn_height/6)
#         object_frame.grid(row=object_row_count, column=object_column_count)
#         object_label = Label(object_frame, text=f"Object {i+1}")
#         object_label.grid(row=object_row_count, column=object_column_count, padx=xpadding)
#         #x velocity
#         object_x_velocity_label = Label(object_frame, text="x-velocity")
#         object_x_velocity_label.grid(row=object_row_count+1, column=object_column_count, padx=xpadding)
#         object_x_velocity_entry = Entry(object_frame)
#         object_x_velocity_entry.insert(0, "0")
#         object_x_velocity_entry.grid(row=object_row_count+2, column=object_column_count, padx=xpadding)
#         #y velocity
#         object_y_velocity_label = Label(object_frame, text="y-velocity")
#         object_y_velocity_label.grid(row=object_row_count+3, column=object_column_count, padx=xpadding)
#         object_y_velocity_entry = Entry(object_frame)
#         object_y_velocity_entry.insert(0, "0")
#         object_y_velocity_entry.grid(row=object_row_count+4, column=object_column_count, padx=xpadding)
#         #z velocity
#         object_z_velocity_label = Label(object_frame, text="z-velocity")
#         object_z_velocity_label.grid(row=object_row_count+5, column=object_column_count, padx=xpadding)
#         object_z_velocity_entry = Entry(object_frame)
#         object_z_velocity_entry.insert(0, "0")
#         object_z_velocity_entry.grid(row=object_row_count+6, column=object_column_count, padx=xpadding)
#         #coords input
#         start_coord = coord_sets[i]
#         object_coords_label = Label(object_frame, text="x-velocity")
#         object_coords_label.grid(row=object_row_count+7, column=object_column_count, padx=xpadding)
#         object_coords_entry = Entry(object_frame)
#         object_coords_entry.insert(0, f"{start_coord[0]},{start_coord[1]},0")
#         object_coords_entry.grid(row=object_row_count+8, column=object_column_count, padx=xpadding)
#         #canvas object
#         diameter = 20
#         canvas_object = sim_canvas.create_oval(start_coord[0], wn_height-start_coord[1], start_coord[0]+diameter, wn_height-start_coord[1]+diameter)

#         #create a nice way to store this information
#         tk_info = {"object_frame":object_frame, "object_x_velocity_entry":object_x_velocity_entry, "object_y_velocity_entry":object_y_velocity_entry, "object_z_velocity_entry":object_z_velocity_entry, "canvas_object":canvas_object, "object_coords_entry":object_coords_entry}

#         new_object = classes.Sim_Object(tk_info, start_coord, object_diameter=diameter)
#         objs.append(new_object)


# CreateObjects()
wn.mainloop()
