import random
import tkinter as tk
import tkinter.font as font

#💣 bomb
#☹ frowny face
# \U0001F600 happy face

class Gui:
    howManyBombs = 0
    seconds = 0
    gamerunning = False
    columns = 10
    rows = 10
    columnsRowsList = []
    listOfEdgeCases = [0,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,19,29,39,49,59,69,79,89,99,91,92,93,94,95,96,97,98]

    def __init__(self,root):
        self.root = root
        self.createApp()

    def createApp(self):
        #create frame for app header
        self.frame = tk.Frame(master=self.root)
        self.frame.pack()
        #timer button
        self.lbl_counter = tk.Label(master=self.frame,text=self.seconds,width=3,height=2,borderwidth=4,bg="black",fg="red",relief="raised")
        self.lbl_counter.grid(row=0,column=0)
        #custom font for reset button
        self.resetButtonFont = font.Font(size=18)
        #reset button
        self.btn_reset = tk.Button(master=self.frame,text="\U0001F600",width=2,height=1,borderwidth=4,font=self.resetButtonFont)
        self.btn_reset.grid(row=0,column=1,padx=50)
        self.btn_reset.config(command = self.setupResetButton)
        #bombcount button
        self.lbl_bombcount = tk.Label(master=self.frame,text="0",width=3,height=2,borderwidth=4,bg="black",fg="red",relief="raised")
        self.lbl_bombcount.grid(row=0,column=2)
        #frame containing playspace grid
        self.frame1 = tk.Frame(master=self.root,relief="raised")
        self.frame1.pack()
        #setup main grid of buttons
        self.setupNormalButtons()
        self.setupBombButtons()
        
    #creates grid of buttons
    def setupNormalButtons(self):
        counter = 0
        for x in range(self.columns):
            for y in range(self.rows):
                self.columnsRowsList.append(tk.Button(self.frame1, text=" ",height=1,width=2,borderwidth=4,command=lambda m=counter: self.normalClick(index=m)))
                self.columnsRowsList[counter].grid(column=y,row=x)
                
                counter += 1

    #adds "  " which translates to bombs randomly
    #and overwrites normals' button click
    def setupBombButtons(self):
        for x in range(len(self.columnsRowsList)):
            y = random.randint(0,len(self.columnsRowsList)-1)
            trueOrFalse = random.randint(0,10)
            #yields a 1/3 probability of having a bomb
            if trueOrFalse == 2:
                self.bomb(y)
        self.howManyBombs = 0
        for x in range(len(self.columnsRowsList)):
            if self.columnsRowsList[x]["text"] == "  ":
                self.howManyBombs+=1

        self.lbl_bombcount.config(text=self.howManyBombs)

    #assigns a button with text "  " which means there is a bomb there
    #called by setupBombButtons with z being the indexes of the columnsRowsList with bombs
    def bomb(self,z):
        self.columnsRowsList[z].config(text="  ")
        self.columnsRowsList[z].config(command = self.bombClick)

    #logic for when you click a bomb, makes all "  " buttons display a bomb
    def bombClick(self):
        #make gamerunning False so timer() stops counting
        self.gamerunning = False

        for x in range(len(self.columnsRowsList)):
            if self.columnsRowsList[x]['text'] == "  ":
                self.columnsRowsList[x].config(text="💣")
                self.columnsRowsList[x].config(relief="sunken")
        
        self.btn_reset.config(text = "☹")

        #make buttons unclickable
        for x in range(len(self.columnsRowsList)):
                self.columnsRowsList[x]['state'] = 'disabled'

    #if what you click is normal(non bomb) button, execute bombcounter function
    #which calculates how many bombs surround it and displays on button clicked
    def normalClick(self,index):
        #start and reset timer if game hasnt already been started
        if self.gamerunning == False and self.columnsRowsList[index]["text"] != "💣":
            self.seconds = 0
            self.gamerunning = True
            self.timer()
        #if click on "no bomb" button change text to number of bombs around it and make button sunken
        if self.columnsRowsList[index]["text"] == " " and self.columnsRowsList[index]['relief'] == 'raised':
            self.columnsRowsList[index].config(text=str(self.bombcounter(indexOfClicked=index)),relief="sunken")
            #if the button clicked has no bombs surrounding it, cascade
            if self.bombcounter(indexOfClicked=index) == " ":
                self.cascadeEffect(index)


        #check if game won logic
        self.win()

    def win(self):
        c = 0
        for x in range(len(self.columnsRowsList)):
            if self.columnsRowsList[x]["relief"] == "sunken":
                c+=1

        if c == (100 - self.howManyBombs):
            self.gamerunning = False
            self.btn_reset.config(text="!")
            #make buttons unclickable
            for x in range(len(self.columnsRowsList)):
                if self.columnsRowsList[x]['text'] == "  ":
                    self.columnsRowsList[x]['text'] = "💣"
                    self.columnsRowsList[x].config(state = 'disabled')
    


    #timer
    def timer(self):
        
        if self.gamerunning == True and self.seconds <= 999:
            self.lbl_counter.config(text=self.seconds)
            self.seconds+=1
            #debug
            #print(str(seconds) + ":" + str(gamerunning))
            self.root.after(1000,self.timer)

    #checks to see if index of surrounding buttons are in range, if so, and its a bomb, +1 to bombcounter
    def bombcounter(self,indexOfClicked):
        bombcount = 0
        
        
        #check edge cases first, if an edge wasn't clicked, then check middle cases
        if indexOfClicked in self.listOfEdgeCases:
            bombcount += self.outerEdgeCases(indexOfClicked)
        else:
            #middle section logic
            bombcount+=self.innerEdgeCases(indexOfClicked)
        
        
        if bombcount > 0:
            return bombcount
        else:
            return " "

    #checks the middle buttons in relation to the indexOfClicked
    def innerEdgeCases(self,indexOfClicked):
        bombcounter = 0

        if self.columnsRowsList[indexOfClicked - 11]['text'] == "  ":
            bombcounter+=1
          
        if self.columnsRowsList[indexOfClicked - 1]['text'] == "  ":
            bombcounter += 1

        if self.columnsRowsList[indexOfClicked + 9]['text'] == "  ":
            bombcounter += 1

        if self.columnsRowsList[indexOfClicked - 10]['text'] == "  ":
            bombcounter += 1
            
        if self.columnsRowsList[indexOfClicked + 10]['text'] == "  ":
            bombcounter += 1
        
        if self.columnsRowsList[indexOfClicked - 9]['text'] == "  ":
            bombcounter += 1
        
        if self.columnsRowsList[indexOfClicked + 1]['text'] == "  ":
            bombcounter += 1
        
        if self.columnsRowsList[indexOfClicked + 11]['text'] == "  ":
            bombcounter += 1
        

        return bombcounter

    #checks the edge buttons in relation to indexOfClicked
    def outerEdgeCases(self,indexOfClicked):
        bombcount = 0
        #left edge case
        listOfLeftEdgeCases = [10,20,30,40,50,60,70,80]
        if indexOfClicked in listOfLeftEdgeCases:
            if self.columnsRowsList[indexOfClicked - 10]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked - 9]['text'] == "  ":
                bombcount +=1
           
            if self.columnsRowsList[indexOfClicked + 1]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 11]['text'] == "  ":
                bombcount +=1

            if self.columnsRowsList[indexOfClicked + 10]['text'] == "  ":
                bombcount +=1
 
        #right edge case
        listOfRightEdgeCases = [19,29,39,49,59,69,79,89]
        if indexOfClicked in listOfRightEdgeCases:
            if self.columnsRowsList[indexOfClicked - 11]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked - 10]['text'] == "  ":
                bombcount +=1

            if self.columnsRowsList[indexOfClicked - 1]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 9]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 10]['text'] == "  ":
                bombcount +=1

        #corner edge cases
        if indexOfClicked == 0:
            if self.columnsRowsList[indexOfClicked + 1]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 11]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 10]['text'] == "  ":
                bombcount +=1
           
        if indexOfClicked == 9:
            if self.columnsRowsList[indexOfClicked - 1]['text'] == "  ":
                bombcount +=1
           
            if self.columnsRowsList[indexOfClicked + 9]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 10]['text'] == "  ":
                bombcount +=1

        if indexOfClicked == 90:
            if self.columnsRowsList[indexOfClicked - 10]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked - 9]['text'] == "  ":
                bombcount +=1

            if self.columnsRowsList[indexOfClicked + 1]['text'] == "  ":
                bombcount +=1

        if indexOfClicked == 99:
            if self.columnsRowsList[indexOfClicked - 11]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked - 10]['text'] == "  ":
                bombcount +=1

            if self.columnsRowsList[indexOfClicked - 1]['text'] == "  ":
                bombcount +=1
            
        #top edge cases
        listOfTopEdgeCases = [1,2,3,4,5,6,7,8]
        if indexOfClicked in listOfTopEdgeCases:
            if self.columnsRowsList[indexOfClicked - 1]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 1]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 9]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 10]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 11]['text'] == "  ":
                bombcount +=1
            
        #bottom edge cases
        listOfBottomEdgeCases = [91,92,93,94,95,96,97,98]
        if indexOfClicked in listOfBottomEdgeCases:
            if self.columnsRowsList[indexOfClicked - 1]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked + 1]['text'] == "  ":
                bombcount +=1
            
            if self.columnsRowsList[indexOfClicked - 11]['text'] == "  ":
                bombcount +=1
           
            if self.columnsRowsList[indexOfClicked - 10]['text'] == "  ":
                bombcount +=1
           
            if self.columnsRowsList[indexOfClicked - 9]['text'] == "  ":
                bombcount +=1
            
        return bombcount

    #reset button logic
    def setupResetButton(self):
        self.columnsRowsList.clear()
        self.btn_reset.config(text="\U0001F600")
        self.seconds = 0
        self.lbl_counter.config(text=self.seconds)
        self.howManyBombs = 0
        self.gamerunning = False
        for x in range(len(self.columnsRowsList)):
            self.columnsRowsList[x]['state'] = 'normal'
        self.setupNormalButtons()
        self.setupBombButtons()

    #logic for cascade effect
    #after every button is checked, win logic is processed to check if win conditions are met
    def cascadeEffect(self, indexOfClicked):
        #checks the middle buttons in relation to the indexOfClicked
        
        if indexOfClicked not in self.listOfEdgeCases:
            if self.columnsRowsList[indexOfClicked - 11]['text'] != "  ":
                self.columnsRowsList[indexOfClicked - 11].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 11)),relief="sunken")
                self.win()
            if self.columnsRowsList[indexOfClicked - 1]['text'] != "  ":
                self.columnsRowsList[indexOfClicked - 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 1)),relief="sunken")
                self.win()
            if self.columnsRowsList[indexOfClicked + 9]['text'] != "  ":
                self.columnsRowsList[indexOfClicked + 9].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 9)),relief="sunken")
                self.win()
            if self.columnsRowsList[indexOfClicked - 10]['text'] != "  ":
                self.columnsRowsList[indexOfClicked - 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 10)),relief="sunken")
                self.win()
            if self.columnsRowsList[indexOfClicked + 10]['text'] != "  ":
                self.columnsRowsList[indexOfClicked + 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 10)),relief="sunken")
                self.win()    
            if self.columnsRowsList[indexOfClicked - 9]['text'] != "  ":
                self.columnsRowsList[indexOfClicked - 9].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 9)),relief="sunken")
                self.win()             
            if self.columnsRowsList[indexOfClicked + 1]['text'] != "  ":
                self.columnsRowsList[indexOfClicked + 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 1)),relief="sunken")
                self.win() 
            if self.columnsRowsList[indexOfClicked + 11]['text'] != "  ":
                self.columnsRowsList[indexOfClicked + 11].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 11)),relief="sunken")
                self.win()
        #checks edge cases in relation to indexOfClicked
        else:
            listOfLeftEdgeCases = [10,20,30,40,50,60,70,80]
            if indexOfClicked in listOfLeftEdgeCases:
                if self.columnsRowsList[indexOfClicked - 10]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 10)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked - 9]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 9].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 9)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 1)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 11]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 11].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 11)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 10]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 10)),relief="sunken")
                    self.win()
            #right edge case
            listOfRightEdgeCases = [19,29,39,49,59,69,79,89]
            if indexOfClicked in listOfRightEdgeCases:
                if self.columnsRowsList[indexOfClicked - 11]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 11].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 11)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked - 10]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 10)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked - 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 1)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 9]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 9].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 9)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 10]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 10)),relief="sunken")
                    self.win()
            #corner edge cases
            if indexOfClicked == 0:
                if self.columnsRowsList[indexOfClicked + 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 1)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 11]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 11].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 11)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 10]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 10)),relief="sunken")
                    self.win()
            if indexOfClicked == 9:
                if self.columnsRowsList[indexOfClicked - 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 1)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 9]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 9].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 9)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 10]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 10)),relief="sunken")
                    self.win()
            if indexOfClicked == 90:
                if self.columnsRowsList[indexOfClicked - 10]['text'] != "  ":
                   self.columnsRowsList[indexOfClicked - 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 10)),relief="sunken")
                   self.win()
                if self.columnsRowsList[indexOfClicked - 9]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 9].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 9)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 1)),relief="sunken")
                    self.win()
            if indexOfClicked == 99:
                if self.columnsRowsList[indexOfClicked - 11]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 11].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 11)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked - 10]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 10)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked - 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 1)),relief="sunken")
                    self.win()
            #top edge cases
            listOfTopEdgeCases = [1,2,3,4,5,6,7,8]
            if indexOfClicked in listOfTopEdgeCases:
                if self.columnsRowsList[indexOfClicked - 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 1)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 1)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 9]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 9].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 9)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 10]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 10)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 11]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 11].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 11)),relief="sunken")
                    self.win()
            #bottom edge cases
            listOfBottomEdgeCases = [91,92,93,94,95,96,97,98]
            if indexOfClicked in listOfBottomEdgeCases:
                if self.columnsRowsList[indexOfClicked - 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 1)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked + 1]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked + 1].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked + 1)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked - 11]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 11].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 11)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked - 10]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 10].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 10)),relief="sunken")
                    self.win()
                if self.columnsRowsList[indexOfClicked - 9]['text'] != "  ":
                    self.columnsRowsList[indexOfClicked - 9].config(text=str(self.bombcounter(indexOfClicked=indexOfClicked - 9)),relief="sunken")
                    self.win()

                  