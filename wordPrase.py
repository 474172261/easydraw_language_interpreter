
m __future__ import division
import copy
import math
import turtle

TYPE={
    'ORIGIN':'ORIGIN',
    'SCALE':'SCALE',
    'ROT':'ROT',
    'IS':'IS',
    'TO':'TO',
    'STEP':'STEP',
    'DRAW':'DRAW',
    'FOR':'FOR',
    'FROM':'FROM',
    'T':'T',
    'Tan':'Tan',
    'Sqrt':'Sqrt',
    'Sin':'Sin',
    'Exp':'Exp',
    'Ln':'Ln',
    'Cos':'Cos',
    'PI':3.1415926,
    '+':'+',
    '-':'-',
    '*':'*',
    '/':'/',
    '**':'**',
    'Nokey':'Nokey',
    '(':'(',
    ')':')',
    ',':',',
    ';':';'
    }

result=[]

class Line():
    def __init__(self):
        self.point=0
    def Read1Word(self,line):
        len_l=len(line)
        word=line[self.point]
        if word=='\n':
            return 0
        self.point+=1
        return word

def Error():
    print '@@',

def GetType(string):
    if TYPE.has_key(string):
        return TYPE[string]
    return TYPE['Nokey']

def Add2stream(stream,itype):
    global result
    try:
        itype=int(stream)
    except:
        itype=GetType(stream)
    result+=[itype]
 
def WordPrase(line):
    global result
    _line=Line()
    word=_line.Read1Word(line)
    stream=''
    while word:
        if word==' ':
            word=_line.Read1Word(line)
            stream=''
            continue
        if word==0:
            return 0
        #get char
        flag=0
        while word:
            itype=GetType(word)
            if itype=='(' or itype==')' or itype==',':# ( ) ,
                if stream:
                    Add2stream(stream,itype)
                Add2stream(word,itype)
                word=_line.Read1Word(line)
                stream=''
                flag=1
                break
            if itype=='+' or itype=='-':# + -
                if stream:
                    Add2stream(stream,itype)
                Add2stream(word,itype)
                word=_line.Read1Word(line)
                stream=''
                flag=1
                break
            if itype=='/':# /
                s_itype=itype
                t_word=word
                t_itype=itype
                word=_line.Read1Word(line)
                itype=GetType(word)
                if itype=='/':#//
                    return 0
                    word=_line.Read1Word(line)
                    flag=1
                    stream=''
                    break
                if stream:
                    Add2stream(stream,s_itype)
                Add2stream(t_word,t_itype)
                stream=''
                flag=1
                break
            if itype=='*':# *
                if stream:
                    Add2stream(stream,itype)#add
                pword=word
                pitype=itype
                word=_line.Read1Word(line)
                itype=GetType(word)
                if itype=='*':#**
                    Add2stream('**',itype)
                    stream=''
                    word=_line.Read1Word(line)
                    flag=1
                    break
                Add2stream(pword,pitype)
                stream=''
                flag=1
                break
            if itype==';':# ;
                if stream:      #avoid '',0
                    Add2stream(stream,itype)
                Add2stream(word,itype)
                return 0
                word=_line.Read1Word(line)
                stream=''
                #print result
                flag=1
                break
            stream+=word
            word=_line.Read1Word(line)
            if word==' ' or word=='\n' or word=='\r':
                break
        # it's a valid string
        if flag:
            continue
        Add2stream(stream,itype)
        stream=''
        itype=''
        
#FlagrightASMD=1
def ASMD(string, location,result):
    #global FlagrightASMD
    t=string[location]
    # print t,'@'
    if t=='+' or t=='-' or t=='*' or t=='/' or t=='**':
        #print string[location],
        # if FlagrightASMD:
        result.append(string[location])
        return location+1
    else:
        return 0

def IsEnd(string,location,endtype=','):
    t=string[location]
    if t==endtype:
        return location
    return 0

def IsCST(string,location,result):
    #print string[location:]
    if string[location] == 'Cos':
        result.append('Cos')
        if string[location+1] == '(':
            temp=[]
            #print 'cos(ex'
            next_location=Express(string,location+2,temp,',')
            if next_location:
                #print string[next_location],'*'
                result.append(temp)
                return next_location
    elif string[location] == 'Sin':
        result.append('Sin')
        if string[location+1] == '(':
            temp=[]
            next_location=Express(string,location+2,temp,',')
            if next_location:
                #print string[next_location],'*'
                result.append(temp)
                return next_location
    Error()
    return 0


def Express(string,location,result,endtype=',',Fparent=0):
    #print '\n',Fparent,'#',string[location:],'#'
    presentword=string[location]
    if type(presentword) == int or type(presentword) == float or presentword=='T':#num
        #print string[location],
        result.append(presentword)

        next_location = ASMD(string,location+1,result)
        if next_location:#num + - * / **
            #print '+*',
            next_location = Express(string,location+2,result,endtype,Fparent)
            if next_location:
                #print 'express*'
                return next_location
        elif string[location+1]==')':# num )
            #print ')*',
            Fparent=Fparent-1
            return location+2
        elif IsEnd(string,location+1,endtype):#num , ;
            return location+1
        return 0

    elif presentword=='(':#( express
        Fparent=Fparent+1
        temp=[]
        #print string[location],Fparent
        #result.append('$')
        next_location=Express(string,location+1,temp,endtype,Fparent)#end with )
        if Fparent<0:
            return 0
        if next_location: 
            #print ')end',               
            result.append(temp)
            if IsEnd(string,next_location,endtype):# (), or ();
                #print 'end',
                return next_location
            test_location=ASMD(string, next_location, result)
            if test_location:# () + - * /
                #print '+',string[test_location]
                test_location=Express(string, test_location, result, endtype,Fparent)
                if test_location:
                    #print 'express',
                    return test_location
            elif Fparent-1>-1:
                if string[next_location]==')':
                    return next_location+1
            return 0
    else:
        next_location=IsCST(string, location, result)
        if next_location:#cos() + - * / **
            #print 'cosend',string[next_location]
            test_location=ASMD(string,next_location,result)
            if test_location:#( cos() +-
                #print '+_',
                next_location=Express(string, test_location, result, endtype)
                if next_location:
                    #print 'expr',
                    return next_location
                else:
                    Error()
                    return 0
            elif IsEnd(string,next_location) or IsEnd(string,next_location,endtype=')'):# (), or ();
                #print 'end'
                return next_location
            return 0
    return 0

def Origin(string):
    result=[]
    i=0
    print 'ORIGIN',
    if string[i+1]=='IS':
        print 'IS',
        if string[i+2]=='(':
            print '(',
            i=Express(string,i+3,result,endtype=',')#in next;out , or ;
            if string[i]==',':
                print ',',
                result.append(',')
                i=Express(string,i+1,result,endtype=';')
                result+=','
                if string[i]==';':
                    print ';'
                    return result
    Error()
    return 0
    
def Rot(string):
    result=[]
    i=0
    print 'ROT',
    if string[i+1]=='IS':
        print 'IS',
        i=Express(string,i+2,result,endtype=';')#in next;out , or ;
        result+=','
        if string[i]==';':
            print ';'
            return result
    Error()
    return 0

def Scale(string):
    result=[]
    i=0
    print 'SCALE',
    if string[i+1]=='IS':
        print 'IS',
        if string[i+2]=='(':
            print '(',
            i=Express(string,i+3,result,endtype=',')#in next;out , or ;
            if string[i]==',':
                print ',',
                result.append(',')
                i=Express(string,i+1,result,endtype=';')
                result+=','
                if string[i]==';':
                    print ';'
                    return result
    Error()
    return 0


#FOR T FROM 0 TO 2*PI STEP PI/50 DRAW (Cos(T) ,  Sin(T));
def For(string):
    print 'FOR',
    if string[1]=='T':
        print 'T',
        if string[2] == 'FROM':
            print 'FROM',
            result=[]
            next_location=Express(string,3,result,endtype='TO')
            if next_location:
                result+=','
                print 'TO',
                next_location=Express(string,next_location+1,result,endtype='STEP')
                if next_location:
                    result+=','
                    print 'STEP',
                    next_location=Express(string,next_location+1,result,endtype='DRAW')
                    if next_location:
                        result+=','
                        print 'DRAW',
                        if string[next_location+1] =='(':
                            print '(',
                            #next_location=IsCST(string,next_location+2,result)#cos
                            next_location=Express(string,next_location+2,result,endtype=',')
                            if string[next_location] == ',':#,
                                print ',',
                                result+=','
                                #next_location=IsCST(string,next_location+1,result)
                                next_location=Express(string,next_location+1,result,endtype=';')
                                if next_location:
                                    print ')',
                                    result+=','
                                    if string[next_location+1] ==';':
                                        print ';'
                                        return result
    Error()
    return 0

def Calc(result,T=0):
    while 1:
        try:
            result[result.index('T')]=T
        except:
            break
    #print result,T,'~'
    #raw_input('>>')
    if len(result)==1 or result[1]==',':
        return result[0]
    try:
        iscos=result.index('Cos')
        cosvalue=Cos(result[iscos+1],T)
        result[iscos]=cosvalue
        #print result,'cos('
        result.pop(iscos+1)
        #print result,'cos)'
    except:
        pass
    try:
        issin=result.index('Sin')
        sinvalue=Sin(result[issin+1],T)
        result[issin]=sinvalue
        result.pop(issin+1)
        #print result,'sin'
    except:
        pass
    if len(result)==1 or result[1]==',':
        return result[0]
    a=result[0]
    m=result[1]
    b=result[2]
    #print result,'"""'
    if m=='*' or m=='/':
        if type(b)==list:
            if m=='/':
                sum=a/CalcResult(b,T)
            else:
                sum=a*CalcResult(b,T)
            #print result,'('
            result[0]=sum
            result.pop(1)
            result.pop(1)
            #print result,')'
            return result
        else:
            if len(result)>4:
                if result[3]=='**':# 3*3**3
                    if m=='/':
                        sum=a/Calc(b,T)
                    else:
                        sum=a*Calc(b,T)
                    result[0]=sum
                    #print result,'['
                    result.pop(1)
                    result.pop(1)
                    result.pop(1)
                    result.pop(1)
                    #print result,']'
                    return result
                if m=='*':
                    sum=a*b
                else:
                    sum=a/b     #a*b+c
                result[0]=sum
                #print result
                result.pop(1)
                result.pop(1)
                #print result
                return result
            else:
                if m=='*':
                    return a*b
                else:
                    return a/b 
    if result[1]=='**':
        if type(result[2])==list:
            sum=a**CalcResult(b,T)
            #print result,'&'
            result[0]=sum
            result.pop(1)
            result.pop(1)
            #print result,'&'
            return result
        else:
            sum=a**b
            #print result,'%'
            result[0]=sum
            result.pop(1)
            result.pop(1)
            #print result,'%'
            return result
    if m=='+' or m=='-':
        if type(b)==list:
            if m=='+':
                sum=a+CalcResult(b,T)
            else:
                sum=a-CalcResult(b,T)
            #print result,'^'
            result[0]=sum
            result.pop(1)
            result.pop(1)
            #print result,'^'
            return result
        else:
            if len(result)>4:
                if m=='+':
                    sum=a+CalcResult(result[2:],T)  
                else:
                    sum=a-CalcResult(result[2:],T)
                result[0]=sum
                return result[:1]
            else:
                if m=='+':
                    return a+b
                else:
                    return a-b     


def CalcResult(result,T=0):
    #print result,'#'
    answer=0
    while True:
        #raw_input('>')
        if type(result[0])==list:
            CalcResult(result[0],T)
            continue
        else:
            while 1:
                temp=Calc(result,T)
                #print 'temp',temp,'result',result
                #raw_input('>>')
                if type(temp)==int or type(temp)==float:
                    return temp
                if len(temp)==1 or temp[1]==',':
                    return temp[0]

def Cos(express,T=0):
    #print T,'cos'
    get=CalcResult(express,T)
    return math.cos(get)

def Sin(express,T=0):
    get=CalcResult(express,T)
    return math.sin(get)

def Divid(result,dividetype=';'):#将表达式分开
    new_result=[]
    line=[]
    for i in result:
        line.append(i)
        try:
            if i==dividetype:
                new_result.append(line)
                line=[]
        except:
            continue
    return new_result

def printlist(list):#打印结果
    print '\n***********************'
    for i in list:
        print i,
    print '\n',

def pot(getresult):#绘点
    start=CalcResult(getresult[0])
    end=CalcResult(getresult[1])
    step=CalcResult(getresult[2])
    T=start
    a=copy.deepcopy(getresult[3])
    b=copy.deepcopy(getresult[4])
    print a,'\n',b
    print 'start      end        step'
    print start,' '*4,end,' '*4,step
    t=turtle.Pen()
    upx=0
    upy=0
    while T<=end:
        T+=step
        x=CalcResult(a,T)
        y=CalcResult(b,T)
        _x=x-upx
        _y=y-upy
        #print drawLeft,drawRight
        a=copy.deepcopy(getresult[3])
        b=copy.deepcopy(getresult[4])
        t.up()
        if _x>0:
            t.forward(_x*20)
            t.left(90)
        else:
            t.backward(-_x*20)
            t.left(90)
        if _y>0:
            t.forward(_y*20)
            t.right(90)
        else:
            t.backward(-_y*20)
            t.right(90)
        t.down()
        t.dot()
        # t.up()
        # t.goto(0,0)
        # t.down()
        upx=x
        upy=y
    #raw_input('>')

def AnalyzeWord(result):
    getresult=[]
    for each in result:
        printlist(each)
        if each[0]=='ORIGIN':
            getresult=Origin(each)
            #print getresult
            getresult=Divid(getresult,',')
            for each in getresult:
                print CalcResult(each)
        elif each[0]=='ROT':
            getresult=Rot(each)
            #print getresult
            getresult=Divid(getresult,',')
            for each in getresult:
                print CalcResult(each)
        elif each[0]=='SCALE':
            getresult=Scale(each)
            #print getresult
            getresult=Divid(getresult,',')
            for each in getresult:
                print CalcResult(each)
        elif each[0]=='FOR':
            getresult=For(each)
            #print getresult,'*'
            getresult=Divid(getresult,',')
            pot(getresult)

if __name__=='__main__':
    #fpath=raw_input('input file:')
    fpath='1.txt'
    fp=open(fpath,'r+')
    line=fp.readline()
    while line:
        WordPrase(line)
        line=fp.readline()
    fp.close()
    #print result
    result=Divid(result)
    #print result
    #raw_input('end')
    AnalyzeWord(result)
    exit(1)

