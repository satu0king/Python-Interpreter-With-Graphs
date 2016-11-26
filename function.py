# This module has all the functions and operators the Evaluate Module will resolve
from math import *
operatorList=['(',')','^','/','%','*','-','+']
priority={'(':5,')':5,'^':1,'/':2,'*':3,'-':4,'+':4}

def priorityOp(op):
    if op in priority:
        return priority[op]
    elif op in fnList:
        return 0

fnList=['sin','cos','tan','cosec','sec','cot','neg','int','ceil','fact','floor','factorial','abs','fabs','sqrt','log10','log','acos','asin','atan','degrees','radians','cube']
varDict={'a':1,'b':2,'c':3,'pi':3.14159265359}

fact = factorial

def cube(x):
    return x**3

def sec(x):
    return 1.0/cos(x)
def cosec(x):
    return 1.0/sin(x)
def cot(x):
    return 1.0/tan(x)
int=int
abs=abs
def neg(x):
    return -x
