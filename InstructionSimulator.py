import re 
class InstructionSimulator(object):
    def __init__(self, opd ,dest,source1,source2,immd,tgt,alu_operations,readRegister,writeRegister,Memoryread,Memorywrite):
        self.opd= opd
        self.dest= dest
        self.source1= source1
        self.source2= source2
        self.immd= immd
        self.tgt= tgt
        self.alu_operations= alu_operations
        self.readRegister=readRegister
        self.writeRegister= writeRegister
        self.Memoryread= Memoryread
        self.Memorywrite= Memorywrite	
        self.res = None        
        self.srcreg1 = None 
        self.srcreg2 = None	
        
   
    def __str__(self):
        str ="%s   %s %s %s %s %s" % (self.opd,
                                  self.dest if self.dest else "",
                                  self.source1 if self.source1 else "",
                                  self.source2 if self.source2 else "",
                                  self.immd if self.immd else "",
                                  self.tgt if self.tgt else "")
        return str
        
    def __repr__(self):
	str ="%s alu_operations: %s readRegister: %s writeRegister: %s Memoryread: %s Memorywrite: %s" % (self.opd,
                                  self.alu_operations if self.alu_operations else 0,
                                  self.readRegister if self.readRegister else 0,
                                  self.writeRegister if self.writeRegister else 0,
                                  self.Memoryread if self.Memoryread else 0,
                                  self.Memorywrite if self.Memorywrite else 0)
        return repr(str)
        
class Nop(InstructionSimulator):
    pass
Nop = InstructionSimulator(None,None,None,None,None,None,None,None,None,None,None)


