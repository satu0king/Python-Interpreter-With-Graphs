# This module is a standalone nonGUI Interpreter. This is independent of the graph module
import Evaluation
import sys
#Status Codes
NEWVAR=1
REASSIGNED=2
VALUE=3

class Interpreter:

    def __init__(self,varDict=dict(pi=3.14159265359,e = 2.718281)):
        self.varDict=varDict #Variable Mapping
        self.evaluator=Evaluation.Eval(varDict=varDict) #Evaluator object
        self.evaluate=self.evaluator.evaluate #Evauator Function\
    def getVar(self,varName):
        #Retrieve Variable
        if varName=='x' or varName=='y':
            raise NameError('NameSpace '+varName+' is reserved for Plots')
        return self.varDict.get(varName,None)
    @staticmethod
    def isValidNameSpace(varName):
        #Standard NameSpace rules

        if varName=='x' or varName=='y':
            raise NameError("NameSpace " + varName + " is reserved for Plots")
            return False

        if len(varName)==0:
            return False

        allowed="1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        for i in varName:
            if i not in allowed:
                raise NameError("Invalid Namespace: '"+i+"' Is a special character")
                return False

        if varName[0].isdigit():
            raise NameError('Invalid Namespace: Cannot start with a digit')
            return False

        return True
    def getVarDict(self):
        #Retrieve Mapping
        return self.varDict
    def setVar(self,varName,value):
        if varName=='x' or varName=='y':
            raise NameError('NameSpace '+varName+' is reserved for Plots')
        self.varDict[varName]=value
    @staticmethod
    def removeSpaces(s):
        return "".join(s.split())
    def interpret(self,inp):
        #This function interprets the input

        if inp=='exit()':
            sys.exit()
        #Splits by '='
        inp=[ s.strip () for s in inp.split('=') ]

        #Single Variable or Single expression
        if(len(inp)==1):
            if inp[0] == 'x' or inp[0] == 'y':
                raise NameError('NameSpace ' + inp[0] + ' is reserved for Plots')
            value=self.evaluate(inp[0])
            self.setVar('_',value)
            return VALUE,value

        #Modification of existing variables using shorthand expression
        if(len(inp)==2 and len(inp[0])!=0 and inp[0][-1] in '/-^+%*^'):
            varName=inp[0][:-1]
            if varName not in self.varDict:
                raise NameError('name '+varName+' is not defined')
            value=self.evaluate(str(self.getVar(varName))+inp[0][-1]+inp[1])
            self.setVar(varName, value)
            return REASSIGNED,None

        #Checking if all variables to be assigned have valid names
        for varName in inp[:-1]:
            if not Interpreter.isValidNameSpace(varName):
                raise NameError('Invalid Namespace: '+ varName)

        #Defining Variables and giving value
        value=self.evaluate(inp[-1])
        for varName in inp[:-1]:
            self.setVar(varName,value)
        return NEWVAR,None

#TESTING CODE - START
if __name__=='__main__':

    obj = Interpreter()
    while True:
        try:
            status,output= obj.interpret(raw_input('>>> '))
            if output != None:
                print output
        except NameError as e:
            print e.message
        except SyntaxError:
            print "Variables not Defined or Invalid or wrong Syntax"
        except IndexError:
            print 'Invalid Syntax'
        except Exception as e:
            print e.message
#TESTING CODE - END