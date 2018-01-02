from InputFileParser import *
from InstructionSimulator import *
import sys
from Tkinter import *
import os
dictreg = dict([("$r%s" % x, 0) for x in range(32)]) 
Mem = dict([(x*4, 0) for x in range(0xffc//4)])
PC = 0x1000
a=""
cycle=0
instrd=0
instre=0
instrm=0
instrw=0
instr_count=0
stall=False
branched=False
dic={}
textBox1=""
textBox=""
textBox2=""
root=Tk()

NOP = InstructionSimulator(None,None,None,None,None,None,None,None,None,None,None)
operations = {'add' : '+', 'addi' : '+', 'sub' : '-', 'subi' : '-', 
                  'and' : '&', 'andi' : '&', 'or'  : '|', 'ori'  : '|'} 
hazardList=[]
instrf=NOP
def Getforwardvalue(regName):
        global instrm, instrw
        if( not instrm.opd=="lw"):
            if (instrm is not Nop 
                    and instrm.res is not None
                    and instrm.dest == regName) :
                        return instrm.res
        elif (instrw is not Nop
                and instrw.dest == regName ):
                    return instrw.res
                
        else :
            return "STALL" 
def fetch():
    global cycle, a, Mem, instr_count, PC, instrf,  NOP
   
    
    if((PC-0x1000)/4<len(a)):        
        k= decode(instrf)
        instr_count=instr_count+1
        instrf=Mem[PC]
    else:
        k=decode(instrf)
        instrf=NOP
        
    PC=PC+4   
    return "F"
            
def decode(l):
    global instrd, NOP, dictreg, PC
    if  cycle==0 :
        k=execute(NOP)
        instrd=l
        
        
    else:
        if(cycle>0):
            if(stall):
                
                d=execute(instrd)
                
            else:
                d=execute(instrd)
                instrd=l
                
            if(instrd.readRegister):
                instrd.srcreg1=dictreg[instrd.source1]
                if (instrd.immd and
                
                 not( instrd.opd == 'bne' or instrd.opd == 'beq' 
                     or instrd.opd =='lw' or instrd.opd =='sw')): 
                    instrd.srcreg2 = int(instrd.immd)
                elif instrd.source2:
                    instrd.srcreg2 = dictreg[instrd.source2]
            if instrd.opd == 'j':
                  tgtval = int(instrd.tgt)
                  PC = tgtval
                  p=fetch(NOP)
            
            
    return "D"
def execute(l):
    global cycle
    global instre
    global NOP
    global progranCounter
    global operations
    global hazardList
    global stall
    global branched
    global instrd
    global instrf
    global PC
    if cycle==0:
        e=memory(NOP)
        instre=l
        
    else:
        if(cycle>0):
            if(stall):
               
                e=memory(NOP)
                stall=False
                
            else:
                e=memory(instre)
                instre=l
            if instre is not Nop and instre.alu_operations:
                if instre.source1 in hazardList :
                    forwardVal = Getforwardvalue(instre.source1)
                    if forwardVal != "STALL":
                        instre.srcreg1 = forwardVal
                    else :
                        stall = True
                        return
                if instre.source2 in hazardList :
                    forwardVal = Getforwardvalue(instre.source2)
                    if forwardVal != "STALL" :
                        instre.srcreg2 = forwardVal
                    else :
                        stall = True
                        return
                
                if instre.writeRegister :
                    hazardList.append(instre.dest)
                if  instre.opd == 'lw':
                    instre.srcreg1 = instre.srcreg1 + int(instre.immd)
                elif  instre.opd == 'sw':
                    instre.srcreg2 = instre.srcreg2 + int(instre.immd)
                elif instre.opd == 'jr':
                    PC = instre.srcreg1                    
                elif instre.opd == 'bne':
                    if instre.srcreg1 != instre.srcreg2:
                        
                        PC = PC + (int(instre.immd) * 4) - 8
                        instrf=NOP
                        instrd=NOP
                        branched = True
                elif instre.opd == 'beq':
                    
                    if instre.srcreg1 == instre.srcreg2:
                        PC = PC + (int(instre.immd) * 4) - 8
                        branched = True
                else :  
                    if (instre.opd =='slt'):
                        val = 1 if instre.srcreg1 < instre.srcreg2 else 0
                        instre.res = val
                    elif (instre.opd == 'nor'):
                        instre.res = ~(instre.srcreg1 | instre.srcreg2)
                    else:
                        instre.res = eval("%d %s %d" % 
                                                            (instre.srcreg1,
                                                            operations[instre.opd],
                                                            instre.srcreg2))
                        
                
    return "E"
        
           

def memory(l):
    global instrm
    global a
    global NOP
    global Mem
    global stall
    if cycle==0:
        
        m=write(NOP)
        instrm=l
        
    else:
        if(cycle>0): 
            
            m=write(instrm)
            instrm=l
            if instrm.Memorywrite:
                 Mem[instrm.srcreg2] = instrm.srcreg1
            elif instrm.Memoryread:
                instrm.res = Mem[instrm.srcreg1]
            
            
    return "M"
       


def write(l):
     
       
            global cycle
            global instrw
            global hazardList
            instrw=l
            if(instrw.writeRegister):
                hazardList.pop(0)
            if instrw.writeRegister:
                if instrw.dest == '$r0':
                    pass
                elif instrw.dest:
                    dictreg[instrw.dest] = instrw.res
                    
            return "W"
       

def reset():
	global dictreg
	global Mem
	global PC
	global a
	global cycle
	global instrd
	global instre
	global instrm
	global instrw
	global instr_count
	global stall
	global branched
	global dic
	global NOP
	global operations
	global hazardList
	global instrf
	dictreg = dict([("$r%s" % x, 0) for x in range(32)]) 
	Mem = dict([(x*4, 0) for x in range(0xffc//4)])
	PC = 0x1000
	a=""
	cycle=0
	instrd=0
	instre=0
	instrm=0
	instrw=0
	instr_count=0
	stall=False
	branched=False
	dic={}

	NOP = InstructionSimulator(None,None,None,None,None,None,None,None,None,None,None)
	operations = {'add' : '+', 'addi' : '+', 'sub' : '-', 'subi' : '-', 
		          'and' : '&', 'andi' : '&', 'or'  : '|', 'ori'  : '|'} 
	hazardList=[]
	instrf=NOP

  

def retrieve_input():
    textBox2.delete('1.0', END)
    global a
    inputValue=textBox.get("1.0","end-1c")
    a=InputFileParser().fileParser(inputValue)
    simulate()
    text = readFile('res.txt')
    textBox2.insert(END, text)

def simulate():
        global textBox1,cycle,Mem, hazardList,stall, PC, stall, branched,dictreg,instrf,instrd,instre, indtrm,instrw, dic,textBox2
        f = open('res.txt', 'w')
        sys.stdout = f
       
        y=0
        for instr in a:
            list1=[]
            dic[instr.__str__()]=list1
            Mem[0x1000 + y] = instr
            y += 4
        
        while not(instrf==NOP and instrd==NOP and instre==NOP and instrm==NOP and instrw==NOP):
            p= fetch()
            
            for x in dic:
                 
                 if x == instrf.__str__():
                     dic[x].append('F ')
                    
                 elif x == instrd.__str__():
                     dic[x].append('D ')
                     
                 elif x == instre.__str__():
                     dic[x].append('E ')
                    
                 elif x == instrm.__str__():
                     dic[x].append('M ')
                     
                 elif x == instrw.__str__():
                     dic[x].append('W ')
                     
                 else:
                     dic[x].append('  ')
            cycle =cycle+1
            if stall or branched:
                PC -= 4 
                branched = False
            
        textBox1.insert(END, "Number of cycles\n\n")
        for x in range(1, cycle):
            
            print("%02d"%x),
        
        print('\n')
        for instr in a:
            textBox1.insert(END,instr.__str__())
            textBox1.insert(END,'\n')
            for x in dic[instr.__str__()]:
                print("%s" %x),
            print
        
        f.close()
def readFile(filename):

    f = open(filename, "r")
    text = f.read()
    return text

def main():
      
    global textBox1,textBox, textBox2
    frame=Frame(root)
    frame.pack()
    root.attributes("-fullscreen",True)
    textBox=Text(root, height=20, width=150)    
    textBox.tag_add("center", "1.0", "end")
    textBox.tag_configure("red", foreground="red")    
    textBox1=Text(root, height=25, width=25)
    textBox1.tag_add("center", "1.0", "end")
    textBox.pack()
    buttonCommit=Button(root, height=1, width=10, text="Simulate", 
                    command= retrieve_input)
    buttonCommit.pack() 
    textBox1.pack(side="left");
    textBox2=Text(root, height=25, width=150)
    textBox2.pack(side="left");
    root.mainloop()
        

            
main()

