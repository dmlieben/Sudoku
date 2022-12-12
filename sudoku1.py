from tkinter import *
import numpy as np
root = Tk()
root.geometry('800x800')
#cd users/dmlie/personal/code stuff/sudoku2
#python gameboard.py

#creates all the global variables we'll need
sudokuboard = np.zeros([9, 9], dtype = int)
possiblities = np.zeros([9,9], dtype = object)
highlight = [9,9]
textcolor = 'black'

#draws sudoku board (this could DEFINTIELY be shorter)
def gameboard():
    #bold lines
    my_canvas.create_line(40, 40, 40, 760, width=2, fill = 'blue') #38 and 762 bc pixel gaps
    my_canvas.create_line(760, 40, 760, 760, width=2, fill = 'blue')
    my_canvas.create_line(40, 40, 760, 40, width=2, fill = 'blue')
    my_canvas.create_line(40, 760, 760, 760, width=2, fill = 'blue')
    my_canvas.create_line(280, 40, 280, 760, width=2, fill = 'blue')
    my_canvas.create_line(520, 40, 520, 760, width=2, fill = 'blue')
    my_canvas.create_line(40, 280, 760, 280, width=2, fill = 'blue')
    my_canvas.create_line(40, 520, 760, 520, width=2, fill = 'gray')
    #non bold lines
    my_canvas.create_line(120, 40, 120, 760, width=2, fill = 'gray')
    my_canvas.create_line(200, 40, 200, 760, width=2, fill = 'gray')
    my_canvas.create_line(360, 40, 360, 760, width=2, fill = 'gray')
    my_canvas.create_line(440, 40, 440, 760, width=2, fill = 'gray')
    my_canvas.create_line(600, 40, 600, 760, width=2, fill = 'gray')
    my_canvas.create_line(680, 40, 680, 760, width=2, fill = 'gray')
    my_canvas.create_line(40, 120, 760, 120, width=2, fill = 'gray')
    my_canvas.create_line(40, 200, 760, 200, width=2, fill = 'gray')
    my_canvas.create_line(40, 360, 760, 360, width=2, fill = 'gray')
    my_canvas.create_line(40, 440, 760, 440, width=2, fill = 'gray')
    my_canvas.create_line(40, 600, 760, 600, width=2, fill = 'gray')
    my_canvas.create_line(40, 680, 760, 680, width=2, fill = 'gray')

#takes the coordinates from click and returns matrix coords
def centercoords(num):
    if 38 <= num < 120:
        newnum = 0
    elif 120 <= num < 200:
        newnum = 1
    elif 200 <= num < 280:
        newnum = 2
    elif 280 <= num < 360:
        newnum = 3
    elif 360 <= num < 440:
        newnum = 4
    elif 440 <= num < 520:
        newnum = 5
    elif 520 <= num < 600:
        newnum = 6
    elif 600 <= num < 680:
        newnum = 7
    elif 680 <= num <= 762:
        newnum = 8
    else:
        newnum = 9
    return newnum

#prints the back end matrix onto the GUI
def printmatrix(sudokuboard):
    my_canvas.delete('guimatrix')
    for i in range (0,9):
        for j in range (0,9):
            i2 = i*80+80
            j2 = j*80+80
            if sudokuboard[i][j] != 0:
                my_canvas.create_text(j2,i2, text = str(sudokuboard[i][j]), tag = 'guimatrix', font = ('Comic Sans', 30))
                #figure out how to change font


#i got this from the internet, that third for loop is way too clever for me to have thought of
def possible(row,column,n):
    global sudokuboard
    for i in range (0,9):
        if sudokuboard[row][i] == n:
            return False
    for j in range (0,9):
        if sudokuboard[j][column] == n:
            return False
    x0 = (column//3)*3
    y0 = (row//3)*3
    for i in range  (0,3):
        for j in range (0,3):
            if sudokuboard [y0+i][x0+j] == n:
                return False
    return True

#remakes the possibility matrix each time the function is called
def create_possibilitymatrix():
    #if its possible for a number to go in the square, add it to the list
    #cycle thru numbers then cycle thru all the places
    #deletes old possibility matrix
    for i in range (9):
        for j in range (9):
            possiblities[i][j] = []
    for n in range (1,10):
        for row in range (9):
            for column in range (9):
                if possible(row,column,n):
                    if sudokuboard[row][column] == 0:
                        possiblities[row][column].append(n)

def only_number_left():
    for row in range (9):
        for column in range (9):
            if len(possiblities[row][column]) == 1:
                if possible(row,column,possiblities[row][column][0]):
                    sudokuboard [row][column] = possiblities[row][column][0]
                    del possiblities[row][column][0]
                    printmatrix(sudokuboard)
                    print(sudokuboard)
                    only_number_left()

#binded to click
def highlightcell(event):
    my_canvas.delete('graybox')
    global x1,y1
    global xmatrix,ymatrix
    x1 = event.x
    y1 = event.y
    xmatrix = centercoords(x1)
    ymatrix = centercoords(y1)
    if (xmatrix != 9) and (ymatrix != 9):
        highlight[0] = ymatrix
        highlight[1] = xmatrix
        x2 = xmatrix*80+80
        y2 = ymatrix*80+80
        my_canvas.create_rectangle((x2-39), (y2-39), (x2+39), (y2+39), fill = '#cce7e8' ,tag = 'graybox')
        print(highlight)

#binded to keyboard, inputs number
#NOTE: make it so highlighting doesnt cover up the number
def inputnumber(event):
    my_canvas.delete('graybox')
    number = event.char
    rowcoord = highlight[0]
    columncoord = highlight[1]
    if number in '0123456789':
        sudokuboard[rowcoord][columncoord] = int(number)
        printmatrix(sudokuboard)
        create_possibilitymatrix()
        only_number_left()
    elif number == 'w':
        highlight[0] = highlight[0] - 1
        print(highlight)
        x2x = highlight[1] * 80 + 80
        y2x = highlight[0] * 80 + 80
        my_canvas.create_rectangle((x2x - 39), (y2x - 39), (x2x + 39), (y2x + 39), fill='#cce7e8', tag='graybox')
    elif number == 'a':
        highlight[1] = highlight[1] - 1
        print(highlight)
        x2x = highlight[1] * 80 + 80
        y2x = highlight[0] * 80 + 80
        my_canvas.create_rectangle((x2x - 39), (y2x - 39), (x2x + 39), (y2x + 39), fill='#cce7e8', tag='graybox')
    elif number == 's':
        highlight[0] = highlight[0] + 1
        print(highlight)
        x2x = highlight[1] * 80 + 80
        y2x = highlight[0] * 80 + 80
        my_canvas.create_rectangle((x2x - 39), (y2x - 39), (x2x + 39), (y2x + 39), fill='#cce7e8', tag='graybox')
    elif number == 'd':
        highlight[1] = highlight[1] + 1
        print(highlight)
        x2x = highlight[1] * 80 + 80
        y2x = highlight[0] * 80 + 80
        my_canvas.create_rectangle((x2x - 39), (y2x - 39), (x2x + 39), (y2x + 39), fill='#cce7e8', tag='graybox')

my_canvas = Canvas(root, width=800, height=800)
my_canvas.grid(row=0,column=0)
my_canvas.bind('<Button-1>', highlightcell)
root.bind('<Key>', inputnumber)
gameboard()

root.mainloop()