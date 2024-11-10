from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from DiceImage import DiceImage
import sqlite3
import os
import sys

root = Tk()
root.title("Dice GUI")

global current_image #the image currently being viewed
global index #the index of the current image, in the image list
index = 0
global image_list #list of all images in database
image_list = []
global index_box
global image_slot
global corrections_box
global path_label
global index_label
global flagged_label
global int_box
global project_root
project_root = os.getcwd() + '/'

# Create a Label for displaying images
image_slot = Label(root)
image_slot.grid(row=2, column=1)  # Span across columns for better positioning

def jump(n):
    #jumps to the nth roll
    
    global current_image
    global image_list
    global index
    #print('index =', index)
    if n not in range(0, len(image_list)):
        return
    
    #print('n =', n)
    index = n
    #print('index =', index)
    current_image = image_list[index]
    #print('photo #' + str(current_image.rollnum))
    
    global index_box
    index_box.delete(0, END)
    index_box.insert(0, str(index+1))
    
    global corections_box
    corrections_box.delete(0, END)
    corrections_box.insert(0, str(current_image.label))
    
    global path_label
    path_label.config(text=project_root + current_image.photo_path[0:len(current_image.photo_path)])
    
    global int_box
    int_box.delete(0, END)
    int_box.insert(0, str(corrections_box.get()))
    
    global flagged_label
    if current_image.flagged:
        flagged_label.config(text='(flagged)', bg='dark red')
    else:
        flagged_label.config(text='', bg=root.cget('bg'))
    
    display_image()
    
    return

def display_image():
    #displays an image, given a path
    
    global image_slot
    global current_image
    
    image_to_display = current_image.load_image()
    image_slot.config(image=image_to_display)
    image_slot.image = image_to_display
    return

def refresh():
    #queries the database to check the latest collection of rolls
    
    global image_list
    global current_image
    global index
    global index_label
    
    image_list.clear()
    if not os.path.exists('dice.db'):
        input("dice.db does not exist.  Exiting.")
        sys.exit()
    conn = sqlite3.connect('dice.db')
    cursor = conn.cursor()
    cursor.execute('select * from rolls ORDER BY rollnum ASC')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    
    if len(rows) <= 0:
        input("No rolls in database.  Exiting.")
        sys.exit()
    
    for row in rows:
        new_pic = DiceImage(row[0], row[1], row[2], row[3], row[4])
        image_list.append(new_pic)
        
    current_image = image_list[index]
        
    for image in image_list:
        print(image.rollnum, image.photo_path)
        
    index_label.config(text='of ' + str(len(image_list)))
    return

def correct():
    #alters information in database in case of incorrect identifications
    
    global current_image
    global corrections_box
    global flagged_label
    flagged_label.config(text='', bg=root.cget('bg'))
    
    conn = sqlite3.connect('dice.db')
    cursor = conn.cursor()
    
    update_query = '''
        UPDATE rolls
        set label = ?,
        flagged = FALSE
        WHERE rollNum = ?
    '''
    
    query_data = (int(corrections_box.get())-1, current_image.rollnum)
    
    cursor.execute(update_query, query_data)
    
    conn.commit()
    conn.close()
    
    refresh()
    
    return

def find_flagged(direction):
    #jumps to the next flagged image
    #stays on current image if no flagged image is found in that direction
    global index
    global image_list
    running_index = index
    running_index += direction #give it a start
    
    while running_index in range(0, len(image_list)):
        if image_list[running_index].flagged:
            jump(running_index)
            return
        running_index += direction
    return

def find_label(direction):
    #jumps to the next roll with specified value
    #stays on current image if no rolls with specified value are found in that direction
    global index
    global image_list
    global int_box
    running_index = index
    running_index += direction
    
    while running_index in range(0, len(image_list)):
        if int(image_list[running_index].label) == int(int_box.get()):
            jump(running_index)
            return
        
        running_index += direction
        
    return

#frames, labels, and entry boxes
index_frame = Frame(root)
index_frame.grid(row=1, column=1)

index_box = Entry(index_frame, width=10)
index_box.insert(0, index+1)
index_box.pack(side=LEFT)

index_label = Label(index_frame, text=('of ' + str(len(image_list))))
index_label.pack(side=RIGHT)

refresh() #refresh needs to be here, or some light refactoring will be necessary

corrections_frame = Frame(root)
corrections_frame.grid(row=4, column=1)

flagged_label = Label(corrections_frame, text='?', fg='white')
flagged_label.pack(side=RIGHT)
if current_image.flagged:
    flagged_label.config(text='(flagged)', bg='dark red')
else:
    flagged_label.config(text='')

corrections_box = Entry(corrections_frame, width=10)
corrections_box.insert(0, str(current_image.label))
corrections_box.pack(side=RIGHT)

corrections_label = Label(corrections_frame, text='Digit Identified:  ')
corrections_label.pack(side=LEFT)

next_of_value_frame = Frame(root)
next_of_value_frame.grid(row=2, column=2)

int_box = Entry(next_of_value_frame, width=5, text='0')
int_box.grid(row=1, column=1, sticky='n')
int_box.insert(0, corrections_box.get())

next_of_value_label = Label(next_of_value_frame, text='Next of Value:')
next_of_value_label.grid(row=0, column=1)


path_label = Label(root, text=project_root + current_image.photo_path[0:len(current_image.photo_path)])
path_label.grid(row=3, column=1)

#buttons
button_prev = Button(root, text='Previous', padx=10, pady=5, command=lambda: jump(index-1))
button_prev.grid(row=0, column=0)

button_jump = Button(root, text='Jump', padx=20, pady=5, command=lambda: jump(int(index_box.get())-1))
button_jump.grid(row=0, column=1)

button_next = Button(root, text='Next', padx=10, pady=5, command=lambda: jump(index+1))
button_next.grid(row=0, column=2)

button_refresh = Button(root, text='Refresh', padx=10, pady=5, command=refresh)
button_refresh.grid(row=2, column=0, sticky='n')

button_correct = Button(root, text='Make Correction', padx=10, pady=5, command=correct)
button_correct.grid(row=5, column=1)

button_next_flagged = Button(root, text='Next Flagged', padx=10, pady=5, command=lambda:find_flagged(1))
button_next_flagged.grid(row=1, column=2)

button_prev_flagged = Button(root, text='Previous Flagged', padx=10, pady=5, command=lambda:find_flagged(-1))
button_prev_flagged.grid(row=1, column=0)

button_next_of_value = Button(next_of_value_frame, text="->", padx=5, pady=2, command=lambda:find_label(1))
button_next_of_value.grid(row=1, column=2, sticky='ne')

button_prev_of_value = Button(next_of_value_frame, text='<-', padx=5, pady=2, command=lambda:find_label(-1))
button_prev_of_value.grid(row=1, column=0, sticky='nw')

# Ensure the grid row and column expand to fill space
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


display_image()
root.mainloop()
