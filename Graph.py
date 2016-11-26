from Tkinter import *
import Evaluation
import random
# This Module consists of a standalone graph class. Each object has a functionList and plots the functions.
# The Graph class inherits from canvas class
# The Graph class has helper functions like pane and zoom. This class automatically updates the functions when required.
# Evaluation module is imported to evaluate expressions which are needed for plotting


def drange(start, stop, step):
     r = start
     while r < stop:
         yield r
         r += step
# GRAPH CLASS -START
class Graph_class(Canvas):
    def __init__(self,master,bg,width,height,scale=30.0,varDict=dict()):
        Canvas.__init__(self, master, width=width, height=height, bg=bg)

        self.varDict = varDict # Dictionary of variables
        self.evaluator = Evaluation.Eval(varDict=varDict) # Creation of evaluator object, sending variable dictionary as reference
        self.evaluate = self.evaluator.evaluate # Obtaining the function
        self.fnList=[] # List of functions to be plotted
        self.fnColors={}
        self.xrange=width #Range of x axis
        self.yrange=height #Range of y axis

        # Initializing Origin and Scale
        self.x_offset=width/2.0
        self.y_offset=height/2.0
        self.scale=scale

        # Storing a backup
        self.default_x_offset = self.x_offset
        self.default_y_offset = self.y_offset
        self.default_scale = self.scale

        #Plotting axis
        self.plotAxis()
    def plotAxis(self):

        #Numbers on y Axis
        step=int(max(1,30/self.scale))
        if self.scale>60:
            step = max(0.1,int(10*40 / self.scale)/10.0)

        for i in drange(step,int(self.y_offset/self.scale)+1,step): #Positive
            self.create_text(self.x_offset-10, self.y_offset-i*self.scale, text=str(i),fill='blue')
        for i in drange(step,int((self.yrange-self.y_offset)/self.scale)+1,step):#negative
            self.create_text(self.x_offset+10, self.y_offset+i*self.scale, text=str(-i),fill='blue')

        #Numbers on x axis
        for i in drange(step,int(self.x_offset/self.scale)+1,step):#negative
            self.create_text(self.x_offset-i*self.scale,self.y_offset+12, text=str(-i),fill='blue')
        for i in drange(step,int((self.xrange-self.x_offset)/self.scale)+1,step): #positive
            self.create_text(self.x_offset+i*self.scale, self.y_offset-12, text=str(i),fill='blue')

        #Axis
        self.create_line(self.x_offset,0,self.x_offset,self.yrange,fill='red',width=2)
        self.create_line(0,self.y_offset,self.xrange,self.y_offset,fill='red',width=2)
    def Clear(self):
        self.delete("all")
        self.plotAxis()
    def Pane(self,x):
        if x==1: #Up
            self.setOffsets(y_offset=self.y_offset+1000/self.scale)
        elif x==2: #Right
            self.setOffsets(x_offset=self.x_offset-1000/self.scale)
        elif x==3: #Down
            self.setOffsets(y_offset=self.y_offset-1000/self.scale)
        elif x==4: #Left
            self.setOffsets(x_offset=self.x_offset+1000/self.scale)
    def setOffsets(self,x_offset=None,y_offset=None):
        if x_offset is not None:
            self.x_offset=x_offset
        if y_offset is not None:
            self.y_offset=y_offset
        #Update Plots
        self.Clear()
        self.Plot()
    def Zoom(self,x):
        if x==1:#Zoom in
            self.setScale(self.scale*1.2)
        elif x==-1:#Zoom out
            self.setScale(self.scale /1.2)
    def setScale(self,scale):
        self.scale=scale
        #Update Plot
        self.Clear()
        self.Plot()
    def Plot(self):
        #This fn plots all fns in function List
        self.Clear()
        for fn in self.fnList[::]:
            try:
                self.PlotFn(fn)
            except Exception:
                self.fnList.remove(fn)

    def addFn(self,Fn):
        #Checks if Fn is already present
        if Fn in self.fnList:
            return

        #Checks if fn is plottable
        try:
            color = '#' + str(hex(random.randint(0, int(0xCC))))[2:].rjust(2, '0') + str(hex(random.randint(0, int(0xCC))))[2:].rjust(2, '0') + str(hex(random.randint(0, int(0x99))))[2:].rjust(2, '0')
            self.fnColors[Fn]=color
            self.PlotFn(Fn)
            #adds fn if successful
            self.fnList.append(Fn)
        except Exception as e:
            raise e
    def clearFn(self):
        self.fnList=[]
        self.Clear()
    def Reset(self):
        #Reset to defaults
        self.x_offset=self.default_x_offset
        self.y_offset=self.default_y_offset
        self.scale=self.default_scale
        #Update
        self.Clear()
        self.Plot()
    def PlotFn(self,fn):
        
        x_offset=self.x_offset
        y_offset=self.y_offset
        
        scale=self.scale

        lower_x=-self.x_offset/self.scale #Lower x Limit in Domain
        higher_x=(self.xrange-self.x_offset)/self.scale #Higher x limit in Domain

        delta= .5/self.scale #Precission calculated dynamically based on scale. Smaller = more accurate

        #axis
        self.plotAxis()

        #Start from lower Limit
        x2=lower_x
        y2=0
        x1=lower_x
        self.varDict['x']=x1 #Substitute for x
        y1=self.evaluate(fn) #Find y
        color =self.fnColors[fn]  #'#' + str(hex(random.randint(0, int(0x111111)))[2:]
        #Go until Higher Limit
        while x2<=higher_x:
            x2+=delta
            self.varDict['x'] = x2 #Substitute for x
            y2=-self.evaluate(fn) #Find y
            if abs(y2-y1)/delta>100 and y2*y1<0:
               #If Fn is discontinous Do Nothing
               pass
            else:
                #Join Points

                self.create_line(scale*(x1)+x_offset,scale*(y1)+y_offset,scale*(x2)+x_offset,scale*(y2)+y_offset,fill=color)
            x1=x2
            y1=y2
# GRAPH CLASS -END

def main():

    #Testing code START
    root=Tk()
    root.title("Plotter")
    root.geometry('900x680')
    Graph=Graph_class(root,bg='white',width=900,height=600,scale=30)
    Graph.pack()
    Graph.addFn('1/x')
    Graph.addFn('x*sin(x)')
    entryFn=Entry(root,width=40,font=("Times", "12"))
    label=Label(root,text='Enter Expression:')
    label.pack()
    entryFn.pack()
    root.bind('<Return>',lambda x:Graph.addFn(entryFn.get()))
    root.mainloop()
    #Testing code END

if __name__=="__main__":
    main()    
