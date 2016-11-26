#This module will evaluate expressions with variables
import function
class Eval:
    def __init__(self,varDict=dict(),fnList=function.fnList,priorityOp=function.priorityOp,operatorList=function.operatorList,functions=function):
        self.varDict=varDict #Variable mapping
        self.fnList=fnList #List of functions to resolve
        self.priorityOp=priorityOp
        self.operatorList=operatorList
        self.functions=functions

    def evaluate(self,exp):
        #Splitting the exp in to a list of operands, operators and functions separate - START
        expL=[]
        buf=[] # Temp variable to store characters temporarily
        for i in exp:
            if i in self.operatorList:
                if len(buf)>0: 
                    expL.append(''.join(buf))
                    buf=[]
                expL.append(i)
            else:
                buf.append(i) # Add to Buf
        if len(buf)>0:
            expL.append(''.join(buf))

        expL=map(lambda x:x.strip(),expL)
        #Splitting the exp in to a list of operands, operators and functions separate - END
        
        operatorStack=[]
        postFix=[]
        flag=1 #To check for negation , 0-operand previously, 1-operator previously
        for i in expL:
            if i not in self.operatorList and i not in self.fnList:
                #Add variables and numbers
                postFix.append(i)
                flag=0
            elif i=='(':
                operatorStack.append(i)
                flag=1
            elif i==')':
                #Pop all elements of operatorStack until opening bracket is encountered
                while len(operatorStack)!=0 and operatorStack[-1]!='(':
                    postFix.append(operatorStack.pop())
                operatorStack.pop() #pop opening bracket
            else:
                #Operator encountered
                if flag==1 and i=='-': #Negation
                    operatorStack.append('neg')
                    continue
                #Pop all operators of higher priority
                while len(operatorStack)!=0 and self.priorityOp(operatorStack[-1])<=self.priorityOp(i):
                    postFix.append(operatorStack.pop())
                #Append current operator
                operatorStack.append(i)
                flag = 1

        #Pop remaining elements
        while len(operatorStack)!=0:
            postFix.append(operatorStack.pop())

        for i in range(len(postFix)):

            if postFix[i] not in self.operatorList and postFix[i] not in self.fnList and postFix[i] in self.varDict:
                #Substitute variable names with value
                postFix[i]=self.varDict[postFix[i]]

            elif postFix[i] not in self.operatorList and postFix[i] not in self.fnList :
                #Convert number in string format to int or float
                num=postFix[i]
                try :
                    num=int(num)
                except Exception:
                    try:
                        num=float(num)
                    except Exception:
                        raise NameError('name '+num+' is not defined')
                postFix[i]=num

        evalStack=[]
        for i in postFix:
            if i not in self.operatorList and i not in self.fnList:
                #Number
                evalStack.append(i)
            else:
                #Checking if its a function - needs only one operand
                if i in self.fnList:
                    op1=evalStack.pop()
                    ans=self.compute(i,op1)

                else:
                    # If its an operator - Needs 2 operands
                    op2=evalStack.pop()
                    op1=evalStack.pop()
                    ans=self.compute(i,op1,op2)

                #Pushing ans back to stack
                evalStack.append(ans)

        # print evalStack
        if len(evalStack) != 1:
            raise Exception('Invalid Syntax')
        return evalStack.pop()

    def compute(self,op,op1,op2=None):
        #If its a function
        if op2==None:
            methodToCall = getattr(self.functions,op)
            return methodToCall(op1)
        #Operator
        if op=='+':
            return op1 + op2
        if op=='*':
            return op1 * op2
        if op=='/':
            return op1 / op2
        if op=='^':
            return op1 ** op2
        if op=='-':
            return op1 - op2
        if op == '%':
            return op1 % op2
        else :raise(str(op)+' is not defined')

#TESTING CODE - START
if __name__=='__main__':
    obj=Eval(varDict=function.varDict)
    while True:
        print obj.evaluate(raw_input())
#TESTING CODE - END