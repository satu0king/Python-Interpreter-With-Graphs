# Combines Modules and sets up the GUI for interpreter with graphs
from Tkinter import *
from Graph import Graph_class
from interpreter import Interpreter
import ScrolledText
from multiListBox import MultiListbox as multiListbox

#Fn to combine functions , returns a single function which acts as a combined function
def combine_funcs(*funcs):
    def combined_func():
        for f in funcs:
            f()
    return combined_func

class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        # Create Interpteret object
        self.interpreter = Interpreter()

        # Create Graph Object and Initialize
        self.Graph=Graph_class(self,bg='white',width=900,height=600,varDict=self.interpreter.getVarDict())
        self.Graph.place(x=10,y=10)
        self.Graph.config(highlightbackground='black')

        # Adding Variable
        self.interpreter.interpret('graphScale='+str(self.Graph.scale))

        # Setting up input box
        self.entry=Entry(self,width=42,font=("Times", "12"))
        self.entry.place(x=920,y=550)
        self.entry.focus_set()

        # Setting up terminal window
        self.inputList = []
        self.inputIndex = 0
        self.textPad = ScrolledText.ScrolledText(self, width=42, height=14,font=("Times","12"))
        self.textPad.place(x=920,y=277)

        # Binding events to functions
        self.bind('<Return>',lambda x:self.interpret())
        self.bind('<Up>', lambda x: self.prevInp())
        self.bind('<Down>', lambda x: self.nextInp())

        # Setting up GUI
        self.setupButtons()
        self.setupListBox()

    def prevInp(self):
        # This fn will Retrieve the prev command
        if self.inputIndex>0:
            self.inputIndex-=1
        self.entry.delete(0,END)
        self.entry.insert(END,self.inputList[self.inputIndex])

    def nextInp(self):
        # This fn will retrieve the next command
        if self.inputIndex<len(self.inputList)-1:
            self.inputIndex+=1
        elif(self.inputIndex>=len(self.inputList)-1):
            self.inputIndex=len(self.inputList)
            self.entry.delete(0, END)
            return
        self.entry.delete(0,END)
        self.entry.insert(END,self.inputList[self.inputIndex])

    def nonGUI(self):
        # nonGUI Mode - Temporarily close the GUI, sets up the interpreter in terminal without Graphing features
        self.withdraw()
        print 'non GUI mode: graphing commands and features are disabled\n'
        while True:
            try:
                inp=raw_input('>>> ')
                if inp!='':
                    self.inputList.append(inp)
                if inp=='graphMode':
                    # Return back to Graphing mode
                    self.deiconify()
                    return
                status, output = self.interpreter.interpret(inp)
                if output != None:
                    print output
            except NameError as e:
                print e.message
            except SyntaxError:
                print "Variables not Defined or Invalid or wrong Syntax"
            except IndexError:
                print "Invalid Syntax"
            except Exception as e:
                print e.message

    def interpret(self):
        # This function will use the interpreter object to resolve commands.
        # This function will Resolve Graphing commands and extra commands separately
        inp=self.entry.get()
        if inp=='':
            return

        # Add Command into Interpreter window and history
        self.inputList.append(inp)
        self.inputIndex=len(self.inputList)
        self.textPad.insert(END, '>>> '+inp + '\n')
        self.entry.delete(0, END)
        self.textPad.see(END)

        # Commands
        if inp=='nonGUI':
            self.nonGUI()
            self.updateListBox()
            return
        if inp=='reset':
            self.Graph.Reset()
            return
        if inp[:10]=='graphScale':
            # Change the Scale of graph
            if inp=='graphScale':
                self.textPad.insert(END, str(self.Graph.scale)+'\n')
                self.textPad.see(END)
                return
            self.interpreter.interpret('graphScale=' + str(self.Graph.scale))
            try:
                self.interpreter.interpret(inp)
                self.Graph.setScale(self.interpreter.interpret('graphScale')[1])
            except Exception as e:
                print e.message
                self.textPad.insert(END,'Invalid Syntax\n')
                self.textPad.see(END)
            self.updateListBox()
            return
        if inp[:4]=='Pane':
            # Shifts Origin of Graph
            inp=inp.split()

            try:
                if(len(inp)==3):

                    if inp[1]=='x':
                        print inp[1]
                        if inp[2][-2:]=='px':
                            self.Graph.setOffsets(x_offset=Graph.x_offset-float(inp[2][:-2]))
                        else:
                            self.Graph.setOffsets(x_offset=self.Graph.x_offset - float(inp[2])*self.Graph.scale)
                    elif inp[1]=='y':
                        if inp[2][-2:]=='px':
                            self.Graph.setOffsets(y_offset=self.Graph.y_offset+float(inp[2][:-2]))
                        else:
                            self.Graph.setOffsets(y_offset=self.Graph.y_offset + float(inp[2])*self.Graph.scale)
                    else:
                        raise Exception()
                elif(len(inp)==5):

                    if inp[1]=='x':
                        if inp[2][-2:]=='px':
                            self.Graph.setOffsets(x_offset=self.Graph.x_offset-float(inp[2][:-2]))
                        else:
                            self.Graph.setOffsets(x_offset=self.Graph.x_offset - float(inp[2])*self.Graph.scale)
                    elif inp[1]=='y':
                        if inp[2][-2:]=='px':
                            self.Graph.setOffsets(y_offset=self.Graph.y_offset+float(inp[2][:-2]))
                        else:
                            self.Graph.setOffsets(y_offset=self.Graph.y_offset+float(inp[2])*self.Graph.scale)
                    else:
                        raise Exception()

                    if inp[3]=='x':
                        if inp[4][-2:]=='px':
                            self.Graph.setOffsets(x_offset=self.Graph.x_offset-float(inp[4][:-2]))
                        else:
                            self.Graph.setOffsets(x_offset=self.Graph.x_offset - float(inp[4])*self.Graph.scale)
                    elif inp[3]=='y':
                        if inp[4][-2:]=='px':
                            self.Graph.setOffsets(y_offset=self.Graph.y_offset+float(inp[4][:-2]))
                        else:
                            self.Graph.setOffsets(y_offset=self.Graph.y_offset + float(inp[4])*self.Graph.scale)
                    else:
                        raise Exception()
                else:
                    raise Exception()

            except Exception as e:
                print e.message
                self.textPad.insert(END,'Invalid Syntax\n')
                self.textPad.see(END)
            return
        if inp=='clear':
            self.inputIndex=0
            self.textPad.delete(1.0,END)
            return
        if inp=='clear_all':
            self.inputIndex = 0
            self.Graph.clearFn()
            self.Graph.Clear()
            self.textPad.delete(1.0, END)
            self.interpreter.varDict.clear()
            self.interpreter.setVar('pi',3.14159265359)
            self.interpreter.setVar('e',2.718281)
            self.interpreter.setVar('graphScale',self.Graph.scale)
            self.updateListBox()
            return
        if inp=='clear_fns':
            self.Graph.clearFn()
            self.Graph.Clear()
            self.updateListBox()
            return

        # Plot function Command
        if len(inp)>7 and inp[:7]=='Plot y=':

            try:
                self.Graph.addFn(inp[inp.find('y=')+2:])
                self.updateListBox()
            except Exception as e:
                self.textPad.insert(END,e.message+'\n')
                self.textPad.see(END)
            return
        elif len(inp) > 8 and inp[:8] == 'Plot y =':
            try:
                self.Graph.addFn(inp[inp.find('y =') + 3:])
                self.updateListBox()
            except Exception as e:
                self.textPad.insert(END,e.message+'\n')
                self.textPad.see(END)
            return

        # Normal Interpreter Command
        try:
            status,output=self.interpreter.interpret(inp)
            if output!=None:
                self.textPad.insert(END,str(output)+'\n')
        except NameError as e:
            self.textPad.insert(END, e.message + '\n')
        except SyntaxError:
            self.textPad.insert(END, "Variables not Defined or Invalid or wrong Syntax" + '\n')
        except IndexError:
            self.textPad.insert(END, 'Invalid Syntax' + '\n')
        except Exception as e:
            self.textPad.insert(END, e.message + '\n')
        self.updateListBox()

    def setupButtons(self):

        self.TextModeB = Button(self, text=">>", height=1, width=2, command=self.nonGUI)
        self.TextModeB.place(x=1260, y=547)

        self.PlotB=Button(self,text="Update Plots",height=3,width=10,command=self.Graph.Plot)
        self.PlotB.place(x=930,y=20)

        self.ClearB=Button(self,text="Clear Fns",height=3,width=10,command=combine_funcs(self.Graph.clearFn,self.updateListBox))
        self.ClearB.place(x=1010,y=20)

        self.Zoom_in_B=Button(self,text="+",height=1,width=2,command=lambda :self.Graph.Zoom(1),font=("Times","10"))
        self.Zoom_in_B.place(x=1100,y=20)

        self.Zoom_out_B=Button(self,text="-",height=1,width=2,command=lambda :self.Graph.Zoom(-1),font=("Times","10"))
        self.Zoom_out_B.place(x=1100,y=50)

        self.reset_B=Button(self,text="*",height=1,width=2,command=self.Graph.Reset,font=("Times","10"))
        self.reset_B.place(x=1200, y=40)

        self.Right_B=Button(self,text=">",height=1,width=2,command=lambda :self.Graph.Pane(2),font=("Times","10"))
        self.Right_B.place(x=1225,y=40)

        self.Left_B=Button(self,text="<",height=1,width=2,command=lambda :self.Graph.Pane(4),font=("Times","10"))
        self.Left_B.place(x=1175,y=40)

        self.Up_B=Button(self,text="^",height=1,width=2,command=lambda :self.Graph.Pane(1),font=("Times","10"))
        self.Up_B.place(x=1200,y=15)

        self.Down_B=Button(self,text="v",height=1,width=2,command=lambda :self.Graph.Pane(3),font=("Times","10"))
        self.Down_B.place(x=1200,y=65)

    def setupListBox(self):

        self.varBox=multiListbox(self,(('varName',12),('Value',15)))
        self.varBox.place(x=920,y=93)

        self.fnBox = multiListbox(self, (('Fn', 2),('Expression',15)))
        self.fnBox.place(x=1140, y=93)
        self.updateListBox()

    def updateListBox(self):
        self.varBox.delete(0,END)
        self.fnBox.delete(0,END)
        for varName in sorted(self.interpreter.varDict.keys(),key=len,reverse=True):
            try:
                self.varBox.insert(END, (('%s='%varName).rjust(12,' '), self.interpreter.getVar(varName)))
            except Exception:
                pass
        self.varBox.see(END)
        for fn in self.Graph.fnList:
            self.fnBox.insert(END, ( 'y=', fn))
        self.fnBox.see(END)

# TESTING CODE - START
if __name__=='__main__':
    root=App()
    root.title("Interpreter")
    root.geometry('1330x700')
    root.mainloop()
# TESTING CODE - END