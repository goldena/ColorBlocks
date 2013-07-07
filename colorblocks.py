#!/usr/bin/env python

from tkinter import *
from tkinter import ttk

import random, time

scores = 0
COLORS = ("red", "green", "yellow", "orange", "violet", "blue")
WIDTH, HEIGHT = 500, 420

root = Tk()
root.title("Color Blocks")
root.minsize(WIDTH, HEIGHT)

root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

mainframe = ttk.Frame(root)
mainframe.grid()

mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)

scoresStr = StringVar()
scoresStr.set("Scores = 0")

game_field = None

def leftClick(event):
    game_field.click(event.x, event.y)

canvas = Canvas(mainframe)
canvas.grid(column = 0, row = 0, sticky = NSEW)
canvas.bind('<Button-1>', leftClick)

ttk.Button(mainframe, text='Quit', command = root.destroy).grid(column = 0, row = 1, sticky = SE)
scoreLabel = ttk.Label(mainframe, textvariable = scoresStr)
scoreLabel.grid(column = 0, row = 1, sticky = SW)
    
def drawRectangle(x1, y1, x2, y2, color):
    canvas.create_rectangle(x1, y1, x2, y2, fill = color, width = 1, tags = "blocks")
        
class Block(object):
    def __init__(self):
        self.color = random.choice(COLORS)

    def __str__(self):
        return(self.color)

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

class Field(object):
    def __init__(self, width_blocks, height_blocks, size):
        self.width = width_blocks
        self.height = height_blocks
        self.size = size
        self.field = []
        self.selected_set = []

        #fill in a 'field' object with 'block' objects
        for i in range(self.width):
            self.field.append([Block() for j in range(self.height)])

    def __str__(self):
        #string representation of a 'field' is used only for a debugging purpose
        res = ""
        
        for i in range(self.width):
            res += "["
            for j in range(self.height):
                res += str(self.field[i][j]) + " "
            res += "] "

        return "<" + res + ">"

    def click(self, x, y):
        if x > self.width * self.size or y > self.height * self.size:
            return
        
        pos = (x // self.size, y // self.size)  #position of a selected 'block'       

        self.selected_set = [pos] 
        self.addSelectedBlocks(pos)
        
        self.updateScores()
        self.deleteSelectedBlocks()
 
        self.drawField()
        canvas.update()

        time.sleep(.3)

        
        self.updateField()
        self.drawField()       

    def compareBlocks(self, pos, new_pos):
        if (0 <= new_pos[0] < self.width) and (0 <= new_pos[1] < self.height):
            if self.field[pos[0]][pos[1]].getColor() == self.field[new_pos[0]][new_pos[1]].getColor():
                return True

        return False
    
    def addSelectedBlocks(self, pos):
        '''
        recursively adds neighbouring blocks of the same color to the initial list
        of positions of 'blocks'
        '''
        new_positions = [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]),
                         (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]        

        for new_pos in new_positions:
            if self.compareBlocks(pos, new_pos):
                if new_pos not in self.selected_set:
                    self.selected_set.append(new_pos)
                    self.addSelectedBlocks(new_pos)

    def updateScores(self):
        global scores
        
        scores += len(self.selected_set) ** 2
        scoresStr.set("Scores = " + str(scores))

    def deleteSelectedBlocks(self):
        '''
        sets the color of a selected group of 'blocks' to 'black'
        for further removal upon updating a 'field'
        '''
        for pos in self.selected_set:
            self.field[pos[0]][pos[1]].setColor("black")

    def updateField(self):
        for i in range(self.width):
            self.field[i] = self.updateColumn(self.field[i])
            
    def updateColumn(self, column):
        updated_column = []

        #remove 'blocks' of the same color that were selected (black)
        for block in column:
            if block.getColor() != "black":
                updated_column.append(block)
       
        while len(updated_column) < len(column):
            updated_column.insert(0, Block())
                    
        return updated_column

    def drawField(self):
        canvas.delete(ALL)
            
        step = self.size
        x_len = len(self.field)
        y_len = len(self.field[0])
        
        for i in range(x_len):
            for j in range(y_len):
                drawRectangle(i * step, j * step, (i + 1) * step, (j + 1) * step, self.field[i][j].getColor())

        scoreLabel["text"] = "Score =" + str(scores)

def main():
    for child in mainframe.winfo_children(): child.grid_configure(padx = 10, pady = 10)
  
    global game_field
    game_field = Field(18, 12, 25)
    game_field.drawField()

    root.mainloop()

if __name__ == '__main__':
    main()
