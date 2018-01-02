import re 
from InstructionSimulator import *
import sys
instl=0
instructionList=[]
class InputParser:

  def fileParser(self,ins):  
        for line in ins.splitlines():
            global instructionList
            instructionList.append(self.parse(line.replace(',','')));
            instl=len(instructionList)
            
        return instructionList


  def parse(self,s):
        s = s.split()
        instr = s[0]
        if instr in ['lw', 'sw', 'bne', 'beq', 'addi', 'subi', 'ori']:
            memread = s[0] == "lw" 
       	    memwrite = s[0] == "sw"
            if (memread or memwrite):
            	regex = re.compile("(\d+)\((\$r\d+)\)")
            	match = regex.match(s[2])            
            	immd = match.group(1) 
            	sval = match.group(2)
            	if s[0] == "lw" :
                    return InstructionSimulator(s[0],s[1],sval,None,immd,None,1,1,1,1,None)
            	else :
                	return InstructionSimulator(s[0],None,s[1],sval,immd,None,1,1,None,None,1)

            if ( s[0] == 'bne' or s[0] == 'beq') :
                  return InstructionSimulator(s[0],None, s[1] , s[2],s[3], None, 1, 1, None, None, None)			            
            return InstructionSimulator(s[0],s[1],s[2],None,s[3], None,1,1,1, None,None) 

        elif instr  in ['add', 'sub', 'and', 'or', 'jr', 'nor', 'slt']:
            if s[0] == "jr":
                return InstructionSimulator(s[0],None,s[1],None,None,None,1,1, None,None,None)        
            return InstructionSimulator(s[0],s[1],s[2],s[3],None,None,1,1,1,None,None)
       
        elif instr in ['j']:
            return InstructionSimulator(s[0],None,None,None,None,s[1],None,None,None,None,None)

        else:
            print('Invald instruction, exiting program')
            
            sys.exit

