from AstGen.Program import Program

from AstGen.EmptyDecl import EmptyDecl
from AstGen.FunDecl import FunDecl

from AstGen.VarDecl import VarDecl
from AstGen.FormalParamDecl import FormalParamDecl
from AstGen.FormalParamDeclSequence import FormalParamDeclSequence
from AstGen.EmptyFormalParamDecl import EmptyFormalParamDecl
from AstGen.DeclSequence import DeclSequence

from AstGen.AssignStmt import AssignStmt
from AstGen.IfStmt import IfStmt
from AstGen.WhileStmt import WhileStmt
from AstGen.ForStmt import ForStmt
from AstGen.ReturnStmt import ReturnStmt
from AstGen.CompoundStmt import CompoundStmt
from AstGen.EmptyCompoundStmt import EmptyCompoundStmt
from AstGen.EmptyStmt import EmptyStmt
from AstGen.StmtSequence import StmtSequence
from AstGen.CallStmt import CallStmt

from AstGen.VarExpr import VarExpr
from AstGen.AssignExpr import AssignExpr
from AstGen.IntExpr import IntExpr
from AstGen.FloatExpr import FloatExpr
from AstGen.BoolExpr import BoolExpr
from AstGen.ArrayExpr import ArrayExpr
from AstGen.StringExpr import StringExpr
from AstGen.BinaryExpr import BinaryExpr
from AstGen.UnaryExpr import UnaryExpr
from AstGen.EmptyExpr import EmptyExpr
from AstGen.ActualParam import ActualParam
from AstGen.EmptyActualParam import EmptyActualParam
from AstGen.ActualParamSequence import ActualParamSequence
from AstGen.CallExpr import CallExpr
from AstGen.ExprSequence import ExprSequence
from AstGen.ID import ID
from AstGen.Operator import Operator
from AstGen.IntLiteral import IntLiteral
from AstGen.FloatLiteral import FloatLiteral
from AstGen.BoolLiteral import BoolLiteral
from AstGen.StringLiteral import StringLiteral
from AstGen.IntType import IntType
from AstGen.FloatType import FloatType
from AstGen.BoolType import BoolType
from AstGen.VoidType import VoidType
from AstGen.StringType import StringType
from AstGen.ArrayType import ArrayType
from AstGen.ErrorType import ErrorType
from AstGen.Decl import Decl
from AstGen.AST import AST

from AstGen.Visitor import *

from ErrorReporter import *
from StdEnvironment import *

from CodeGen.JVM import *
from CodeGen.Frame import *

import os

class Emitter(Visitor):
    def __init__(self, infile, reporter):
        self.reporter = None
        self.out = None
        self.ClassName = ""
        self.indent = 0
        self.INDENT_LEVEL = 3   #amount of indentation per level
        self.frame = None
        self.MaxOperandStackSize = 150
        # Upper bound for the maximum operand stack height for a MiniC function
        # The actual stack height can be determined by interpreting the function's
        # bytecode.
        self.LabelIndent = 0
        self.isMain = False         # true if we are generating code for "main"
        self.GlobalScope = False    # true if we are in the outermost "global" scope.

        try:
            self.isMain = False
            self.GlobalScope = True
            self.reporter = reporter
            self.LabelIndent = 1

            # Create output file name:
            f = open(infile, 'r')
            namepart = os.path.basename(infile)
            l = len(namepart)
            if namepart[l-3] == '.' and namepart[l-2] == 'm' and namepart[l-1] == 'c':
                self.ClassName = namepart[:l-3]
                outfile = namepart[:l-2]
                outfile = outfile + "j"
            else:
                self.ClassName = namepart
                outfile = namepart
                outfile = outfile + "j"
            # Create output file:
            self.out = open(outfile, 'w')
            self.indent = 0
        except Exception as e:
            # Catch exception if any:
            print("Error:", e)
            exit(1)
    
    # top-level routine, called by the compiler driver:
    def genCode(self, progAST: Program):
        self.visit(progAST)
        try:
            self.out.close()
        except Exception as e:
            # Catch exception if any:
            print("Error:", e)
            exit(1)
    
    # Emit a single string, but do not indent.
    def emitNoIndent(self, s):
        try:
            self.out.write(s + "\n")
        except Exception as e:
            print("Error:", e)
            exit(1)
    
    '''
        emit* routines output Jasmin assembly code of various sorts.
    '''
    def emit(self, *args):  #s, value
        if len(args) == 1:
            s = args[0]
            value = None
        else:
            s, value = args
        if value is None:
            # Emit a single string using indentation:
            try:
                for i in range(1, self.indent*self.INDENT_LEVEL+1):
                    self.out.write(" ")
                self.out.write(s + "\n")
            except Exception as e:
                print("Error:", e)
                exit(1)
        else:
            if type(value) == int:
                self.emit(s + " " + str(value))
            elif type(value) == float:
                self.emit(s + " " + str(value))
    
    # For a given label nr, return the string representation
    # of that label:
    def getLabelString(self, label):
        return "Label" + str(label)
    
    # Emit the defining occurrence of a label:
    def emitLabel(self, label):
        assert label >= 0
        Ind = ' '
        for i in range(1, self.LabelIndent+1):
            Ind = Ind + ' '
        self.emitNoIndent(Ind + "Label" + str(label) + ":")
    
    # Emit an integer constant:
    def emitICONST(self, value):
        if value == -1:
            self.emit(JVM.ICONST_M1)
        elif value >= 0 and value <= 5:
            self.emit(JVM.ICONST + "_" + str(value))
        elif value >= -128 and value <= 127:
            self.emit(JVM.BIPUSH, value)
        elif value >= -32768 and value <= 32767:
            self.emit(JVM.SIPUSH, value)
        else:
            self.emit(JVM.LDC, value)
    
    # Emit a floating point constant:
    def emitFCONST(self, value):
        if value == 0.0:
            self.emit(JVM.FCONST_0)
        elif value == 1.0:
            self.emit(JVM.FCONST_1)
        elif value == 2.0:
            self.emit(JVM.FCONST_2)
        else:
            self.emit(JVM.LDC, value)
    
    # Emit a boolean constant:
    def emitBCONST(self, value):
        if value:
            self.emit(JVM.ICONST_1) # true = 1 with the JVM
        else:
            self.emit(JVM.ICONST_0)
    
    # Emit an integer load instruction:
    def emitILOAD(self, LocalVarIndex):
        if LocalVarIndex == 0:
            self.emit(JVM.ILOAD_0)
        elif LocalVarIndex == 1:
            self.emit(JVM.ILOAD_1)
        elif LocalVarIndex == 2:
            self.emit(JVM.ILOAD_2)
        elif LocalVarIndex == 3:
            self.emit(JVM.ILOAD_3)
        else:
            self.emit(JVM.ILOAD, LocalVarIndex)
    
    # Emit an integer store instruction:
    def emitISTORE(self, LocalVarIndex):
        if LocalVarIndex == 0:
            self.emit(JVM.ISTORE_0)
        elif LocalVarIndex == 1:
            self.emit(JVM.ISTORE_1)
        elif LocalVarIndex == 2:
            self.emit(JVM.ISTORE_2)
        elif LocalVarIndex == 3:
            self.emit(JVM.ISTORE_3)
        else:
            self.emit(JVM.ISTORE, LocalVarIndex)
    
    # Emit a floating point load instruction:
    def emitFLOAD(self, LocalVarIndex):
        if LocalVarIndex == 0:
            self.emit(JVM.FLOAD_0)
        elif LocalVarIndex == 1:
            self.emit(JVM.FLOAD_1)
        elif LocalVarIndex == 2:
            self.emit(JVM.FLOAD_2)
        elif LocalVarIndex == 3:
            self.emit(JVM.FLOAD_3)
        else:
            self.emit(JVM.FLOAD, LocalVarIndex)
    
    # Emit a floating point store instruction:
    def emitFSTORE(self, LocalVarIndex):
        if LocalVarIndex == 0:
            self.emit(JVM.FSTORE_0)
        elif LocalVarIndex == 1:
            self.emit(JVM.FSTORE_1)
        elif LocalVarIndex == 2:
            self.emit(JVM.FSTORE_2)
        elif LocalVarIndex == 3:
            self.emit(JVM.FSTORE_3)
        else:
            self.emit(JVM.FSTORE, LocalVarIndex)
    
    # Emit a return statement of a given type:
    def emitRETURN(self, T: Type):
        if T.Tequal(StdEnvironment.intType) or T.Tequal(StdEnvironment.boolType):
            self.emit(JVM.IRETURN)
        elif T.Tequal(StdEnvironment.floatType):
            self.emit(JVM.FRETURN)
        elif T.Tequal(StdEnvironment.voidType):
            self.emit(JVM.RETURN)
    
    # Emit the constructor for the class of our MiniC program:
    def emitConstructor(self):
        self.emit("\n.method public <init>()V")
        self.indent+=1
        self.emit(".limit stack 1")
        self.emit(".limit locals 1")
        self.emit(".var 0 is this L" + self.ClassName + "; from Label0 to Label1\n")
        self.emitLabel(0)
        self.emit("aload_0")
        self.emit("invokespecial java/lang/Object/<init>()V")
        self.emitLabel(1)
        self.emit("return")
        self.indent-=1
        self.emit(".end method")
    
    # Emit declarations for the static class variables. Static class variables
    # correspont to MiniC global variables.
    # This function recursively traverses the declarations in the global
    # block of the program.
    def emitStaticClassVariableDeclaration(self, d: Decl):
        assert d != None
        if isinstance(d, DeclSequence):
            SD = d
            self.emitStaticClassVariableDeclaration(SD.D1)
            self.emitStaticClassVariableDeclaration(SD.D2)
        elif isinstance(d, VarDecl):
            D = d
            T = self.typeOfDecl(D)
            self.emit(".field static " + D.idAST.Lexeme + " " + self.getTypeDescriptorLabel(T))
    
    # Emit initializers for the static class variables.
    # This function recursively traverses the declarations in the global
    # block of the program.
    def emitInitializer(self, d: Decl):
        assert d is not None
        if isinstance(d, DeclSequence):
            SD = d
            self.emitInitializer(SD.D1)
            self.emitInitializer(SD.D2)
        elif isinstance(d, VarDecl):
            VD = d
            T = self.typeOfDecl(VD)
            Init_Expr = VD.eAST
            if isinstance(Init_Expr, EmptyExpr):
                # Programmer did not provide initializer for global variable.
                # Initialize to something safe:
                if T.Tequal(StdEnvironment.intType) or T.Tequal(StdEnvironment.boolType):
                    self.emit(JVM.ICONST_0)
                elif T.Tequal(StdEnvironment.floatType):
                    self.emit(JVM.FCONST_0)
                else:
                    # Type not supported for global variable initalizer:
                    assert False
            else:
                # Programmer provided initializer expression, emit it:
                Init_Expr.accept(self)
            self.emitStaticVariableReference(VD.idAST, VD.tAST, True)
    
    # Emit a class initializer method for the global MiniC variables.
    # Global MiniC variables correspond to static Java class variables
    # in our code generation model. Our MiniC assembly code needs one
    # class initializer where all class variables are initialized. 
    def emitClassInitializer(self, d: Decl):
        self.emit("\n.method static <clinit>()V")
        self.indent+=1
        self.emit(".limit stack 1")
        self.emit(".limit locals 0")
        self.emitInitializer(d)
        self.emit(JVM.RETURN)
        self.indent -= 1
        self.emit(".end method")
    
    # Get the JVM type descriptor for a given MiniC type:
    def getTypeDescriptorLabel(self, t: Type):
        l = ""
        assert (t is not None) and not isinstance(t, ErrorType)
        if t.Tequal(StdEnvironment.intType):
            l = "I"
        elif t.Tequal(StdEnvironment.boolType):
            l = "Z"
        elif t.Tequal(StdEnvironment.floatType):
            l = "F"
        elif t.Tequal(StdEnvironment.stringType):
            l = "Ljava/lang/String;"
        elif t.Tequal(StdEnvironment.voidType):
            l = "V"
        else:
            assert False
        return l
    
    # Get the type of a given declaration:
    def typeOfDecl(self, d: AST):
        assert d is not None
        assert isinstance(d, FunDecl) or isinstance(d, VarDecl) or isinstance(d, FormalParamDecl)
        if isinstance(d, FunDecl) or isinstance(d, VarDecl):
            T = d.tAST
        else:
            T = d.astType
        if isinstance(T, ArrayType):
            self.reporter.reportError("Arrays not implemented", "", d.pos)
            retType = T.astType
        else:
            retType = T
        return retType
    
    # Global MiniC variables become static variables in the Jasmine assembly code.
    # Regerences to those variables are generated using this function.
    # The boolean "write" value determines between read access (write=false) and
    # write access (write=true).
    def emitStaticVariableReference(self, Ident, T, write):
        if write:
            ref = JVM.PUTSTATIC
        else:
            ref = JVM.GETSTATIC
        ref = ref + " " + self.ClassName + "." + Ident + " " + self.getTypeDescriptorLabel(T)
        self.emit(ref)
    
    # Returns true if the function declaration passed as parameter must become a static
    # method (aka class method) in the generated Jasmine assembly code.
    # The methods belonging to this category are:
    #  - all functions from the StdEnvironment
    #  - main()
    def isStaticMethod(self, f):
        N = f.idAST.Lexeme
        if N in (StdEnvironment.getInt.idAST.Lexeme, StdEnvironment.putInt.idAST.Lexeme, 
                 StdEnvironment.getBool.idAST.Lexeme, StdEnvironment.putBool.idAST.Lexeme,
                 StdEnvironment.getFloat.idAST.Lexeme, StdEnvironment.putFloat.idAST.Lexeme,
                 StdEnvironment.getString.idAST.Lexeme, StdEnvironment.putString.idAST.Lexeme, 
                 StdEnvironment.putLn.idAST.Lexeme, "main"):
            return True
        else:
            return False
    
    # Given a function declaration FunDecl, this method returns the number
    # of formal parameters. E.g., for the following function
    #
    #    void foo (int a, bool b){}
    #
    # the return value will be 2.
    # Note: this function assumes the AST tree layout from Assignment 3.
    def GetNrOfFormalParams(self, f):
        NrArgs = 0
        D = f.paramsAST
        assert isinstance(D, EmptyFormalParamDecl) or isinstance(D, FormalParamDeclSequence)
        if isinstance(D, EmptyFormalParamDecl):
            return 0
        while isinstance(D, FormalParamDeclSequence):
            NrArgs+=1
            D = D.rAST
            assert isinstance(D, EmptyFormalParamDecl) or isinstance(D, FormalParamDeclSequence)
        return NrArgs
    
    # Given a function declaration FunDecl, this method returns the AST for 
    # the formal parameter nr (nr is the number of the parameter).
    # E.g., for the following function and nr=2,
    #
    #    void foo (int a, bool b){}
    #
    # the AST returned will be "bool b".
    # Note: this function assumes the AST tree layout from Assignment 3.
    def GetFormalParam(self, f, nr):
        fArgs = self.GetNrOfFormalParams(f)
        assert fArgs >= 0
        assert nr <= fArgs
        S = f.paramsAST
        for i in range(1, nr):
            assert isinstance(S.rAST, FormalParamDeclSequence)
            S = S.rAST
        assert isinstance(S.lAST, FormalParamDecl)
        return S.lAST
    
    # Construct the descriptor for a given function declaration.
    def getDescriptor(self, f):
        ret = "("
        for arg in range(1, self.GetNrOfFormalParams(f)+1):
            D = self.GetFormalParam(f, arg)
            ret = ret + self.getTypeDescriptorLabel(self.typeOfDecl(D))
        ret = ret + ")"
        ret = ret + self.getTypeDescriptorLabel(f.tAST)
        return ret
    
    #
    # Here the Visitor methods for our code generator start:
    #

    @singledispatchmethod
    def visit(self, x):
        return super().visit(x)

    @visit.register
    def _(self, x: Program):
        self.emit("; Jassmin assembly code")
        self.emit("; MiniC v. 1.0")
        self.emit(".class public " + self.ClassName)
        self.emit('.super java/lang/Object')
        if isinstance(x.D, VarDecl):
            x.D.setGlobal()
        self.emitStaticClassVariableDeclaration(x.D)
        self.emitClassInitializer(x.D)
        self.emitConstructor()
        x.D.accept(self)

    @visit.register
    def _(self, x: EmptyDecl):
        # self.emit('; EmptyDecl')
        pass

    @visit.register
    def _(self, x: FunDecl):
        self.GlobalScope = False
        # Allocate a frame for this function:
        self.isMain = (x.idAST.Lexeme == "main")
        if self.isMain:
            self.frame = Frame(True)
            self.emit("\n.method public static main([Ljava/lang/String;)V")
            # .var for main's "this" pointer:
            # emit(".var 0 is this L" + ClassName + "; from Label0 to Label1")
            # .var for main's String[] argument:
            # emit(".var 1 is arg0 [Ljava/lang/String; from Label0 to Label1")
        else:
            self.frame = Frame(False)
            self.emit("\n.method public " + x.idAST.Lexeme + self.getDescriptor(x))
            x.paramsAST.accept(self) # process formal parameters to adjust the
            # local variable count.
        self.indent+=1
        L0 = self.frame.getNewLabel()
        L1 = self.frame.getNewLabel()
        self.emitLabel(L0)
        if self.isMain:
            self.emit("new " + self.ClassName)
            self.emit("dup")
            self.emit("invokespecial " + self.ClassName + "/<init>()V")
            self.emit("astore_1")
        x.stmtAST.accept(self)
        self.emitLabel(L1)
        if self.isMain:
            self.emit(JVM.RETURN)
        self.emit(".limit locals " + str(self.frame.getNewLocalVarIndex()))
        self.emit(".limit stack " + str(self.MaxOperandStackSize))
        self.indent-=1
        self.emit(".end method")
        self.GlobalScope = True
        self.isMain = False
    
    @visit.register
    def _(self, x: TypeDecl):
        assert False    # Can only occur in the StdEnvironment AST!
    
    @visit.register
    def _(self, x: FormalParamDecl):
        # self.emit("; FormalParamDecl")
        # TBD: here you need to allocate a new local variable index to the formal parameter.
        #      Relevant: x.index, self.frame.getNewLocalVarIndex()
        x.index = self.frame.getNewLocalVarIndex()
    
    @visit.register
    def _(self, x: FormalParamDeclSequence):
        # self.emit("; FormalParamDeclSequence")
        x.lAST.accept(self)
        x.rAST.accept(self)
    
    @visit.register
    def _(self, x: EmptyFormalParamDecl):
        # self.emit("; EmptyFormalParamDecl")
        pass

    @visit.register
    def _(self, x: StmtSequence):
        x.s1AST.accept(self)
        x.s2AST.accept(self)
    
    @visit.register
    def _(self, x: AssignStmt):
        self.emit("; AssignStmt, line " + str(x.pos.StartLine))
        #x.lAST.accept(self)
        x.rAST.accept(self)
        if isinstance(x.lAST, VarExpr):
            V = x.lAST
            D = V.Ident.declAST
            T = self.typeOfDecl(D)
            #TBD: here you have to distinguish between local and global MiniC variables.
            #     Local variables are kept in the JVM's local variable array.
            #     Global variables are kept as static JVM class variables.
            #     The code for the right-hand side of the assignment statement has already
            #     been generated by the x.rAST.accept(). Now the result of the right-hand side
            #     of the expression needs to be written back from the stack to the left-hand
            #     side variable.
            #
            #     Relevant functions: isGlobal()
            #                         emitStaticVariableReference()
            #                         emitISTORE()
            #                         emitFSTORE()
            #
            if D.isGlobal():
                self.emitStaticVariableReference(V.Ident, T, True)
            else:
                if T.Tequal(StdEnvironment.intType) or T.Tequal(StdEnvironment.boolType):
                    self.emitISTORE(D.index)
                elif T.Tequal(StdEnvironment.floatType):
                    self.emitFSTORE(D.index)
                else:
                    assert False
        else:
            assert False    # Arrays not implemented.
    
    @visit.register
    def _(self, x: IfStmt):
        self.emit("; IfStmt, line " + str(x.pos.StartLine))
        # The following code evaluates the condition of the if statement.
        # After execution of this code, the stack will contain 0 if the condition
        # evaluated to false, and 1 if the condition evaluated to true.
        # You should apply the template for if statements from the lecture slides.
        x.eAST.accept(self)
        # Allocate 2 new labels for this if statement.

        L1 = self.frame.getNewLabel()
        L2 = self.frame.getNewLabel()
        # TBD: your code goes here...
        self.emit(JVM.IFEQ + " " + self.getLabelString(L1))

        x.thenAST.accept(self)
        # TBD: your code goes here...
        self.emit(JVM.GOTO + " " + self.getLabelString(L2))
        self.emitLabel(L1)

        if x.elseAST:
            x.elseAST.accept(self)
        # TBD: your code goes here...
        self.emitLabel(L2)
    
    @visit.register
    def _(self, x: WhileStmt):
        self.emit("; WhileStmt, line " + str(x.pos.StartLine))
        # You should apply the template for while loops from the lecture slides.
        # TBD:
        Lbegin = self.frame.getNewLabel()
        Lend = self.frame.getNewLabel()
        self.emitLabel(Lbegin)
        x.eAST.accept(self)
        self.emit(JVM.IFEQ + " " + self.getLabelString(Lend))
        x.stmtAST.accept(self)
        self.emit(JVM.GOTO + " " + self.getLabelString(Lbegin))
        self.emitLabel(Lend)
    
    @visit.register
    def _(self, x: ForStmt):
        self.emit("; ForStmt, line " + str(x.pos.StartLine))
        # No template was given for "for" loops, but you can find out by compiling
        # a Java "for" loop to bytecode, use "classfileanalyzer" and look how it
        # is done there.  Using the classfileanalyzer is described in the
        # Assignment 5 spec.
        # TBD:
        Lcond = self.frame.getNewLabel()
        Lend = self.frame.getNewLabel()
        x.e1AST.accept(self)
        self.emitLabel(Lcond)
        x.e2AST.accept(self)
        self.emit(JVM.IFEQ + " " + self.getLabelString(Lend))
        x.stmtAST.accept(self)
        x.e3AST.accept(self)
        self.emit(JVM.GOTO + " " + self.getLabelString(Lcond))
        self.emitLabel(Lend)
    
    @visit.register
    def _(self, x: ReturnStmt):
        self.emit("; ReturnStmt, line " + str(x.pos.StartLine))
        x.eAST.accept(self) # visit even in "main", for possible side-effects
        if self.isMain or isinstance(x.eAST, EmptyExpr):
            self.emitRETURN(StdEnvironment.voidType)
        else:
            self.emitRETURN(x.eAST.type)
    
    @visit.register
    def _(self, x: CompoundStmt):
        x.astDecl.accept(self)
        x.astStmt.accept(self)
    
    @visit.register
    def _(self, x: EmptyStmt):
        pass

    @visit.register
    def _(self, x: EmptyCompoundStmt):
        pass

    @visit.register
    def _(self, x: CallStmt):
        self.emit("; CallStmt, line " + str(x.pos.StartLine))
        x.eAST.accept(self)
    
    @visit.register
    def _(self, x: VarDecl):
        if x.isGlobal():
            # Global variables have been treated already in the static
            # variable initializer clinit:
            return
        #TBD: if this variable declaration declares a local variable, then
        #     you have to allocate a new local variable index from "frame"
        #     and assign it to x.index.
        #     Relevant functions:
        #                        frame.getNewLocalVarIndex
        #                        x.tAST.accept(this);
        #                        x.idAST.accept(this);
        #                        x.eAST.accept(this);
        x.index = self.frame.getNewLocalVarIndex()
        x.tAST.accept(self)
        x.idAST.accept(self)

        if not isinstance(x.eAST, EmptyExpr):
            x.eAST.accept(self)

            T = self.typeOfDecl(x)
            if T.Tequal(StdEnvironment.intType) or T.Tequal(StdEnvironment.boolType):
                self.emitISTORE(x.index)
            elif T.Tequal(StdEnvironment.floatType):
                self.emitFSTORE(x.index)
            else:
                assert False
    
    @visit.register
    def _(self, x: DeclSequence):
        if isinstance(x.D1, VarDecl) and self.GlobalScope:
            x.D1.setGlobal()
        if isinstance(x.D2, VarDecl) and self.GlobalScope:
            x.D2.setGlobal()
        x.D1.accept(self)
        x.D2.accept(self)
    
    @visit.register
    def _(self, x: VarExpr):
        #Here we are dealing with read-accesses of applied occurrences of variables.
        #Why only read-access? Basically, no left-hand side of an assignment statement
        #will occur here, because we do not invoke accept() on left-hand sides of
        #assignment statements. This means that left-hand sides of assignments are not
        #traversed; they are handled right at the visit method for AssignStmt.
        #
        # Example1: a = b + 1
        # The left-hand side of the assignment won't be traversed ("a"). But the
        # right-hand side ("b+1") will.
        #
        # Example2: foo(247+x)
        # "x" will be another VarExpr, again a read-access.
        #
        #What you should do:
        # - if x is global, emit a static variable access to push the static
        #   variable onto the stack.
        # - if x is a local variable, you need to emit an ILOAD or an FLOAD,
        #   depending on the type of variable (ILOAD for int and bool).
        #     Relevant functions: isGlobal()
        #                         emitStaticVariableReference()
        #                         emitILOAD(), emitFLOAD()
        D = x.Ident.declAST
        T = self.typeOfDecl(D)
        # TBD: your code goes here...
        if D.isGlobal():
            self.emitStaticVariableReference(x.Ident, T, False)
        else:
            if T.Tequal(StdEnvironment.intType) or T.Tequal(StdEnvironment.boolType):
                self.emitILOAD(D.index)
            elif T.Tequal(StdEnvironment.floatType):
                self.emitFLOAD(D.index)
            else:
                assert False

    
    @visit.register
    def _(self, x: AssignExpr):
        self.emit("; AssignExpr")
        x.rAST.accept(self)
        if isinstance(x.lAST, VarExpr):
            V = x.lAST
            D = V.Ident.declAST
            T = self.typeOfDecl(D)
            if D.isGlobal():
                self.emitStaticVariableReference(V.Ident, self.typeOfDecl(V.Ident.declAST), True)
            else:
                if T.Tequal(StdEnvironment.intType) or T.Tequal(StdEnvironment.boolType):
                    self.emitISTORE(D.index)
                elif T.Tequal(StdEnvironment.floatType):
                    self.emitFSTORE(D.index)
                else:
                    assert False
        else:
            assert False    # Arrays not implemented.
    
    @visit.register
    def _(self, x: IntExpr):
        x.astIL.accept(self)
    
    @visit.register
    def _(self, x: FloatExpr):
        x.astFL.accept(self)
    
    @visit.register
    def _(self, x: BoolExpr):
        x.astBL.accept(self)
    
    @visit.register
    def _(self, x: StringExpr):
        x.astSL.accept(self)
    
    @visit.register
    def _(self, x: ArrayExpr):
        self.emit("; ArrayExpr)")
        x.idAST.accept(self)
        x.indexAST.accept(self)
    
    @visit.register
    def _(self, x: BinaryExpr):
        # self.emit("; BinaryExpr")
        Op = x.oAST.Lexeme
        if Op == "&&":
            L1 = self.frame.getNewLabel()
            L2 = self.frame.getNewLabel()
            #TBD: implement the code template for && short circuit evaluation
            #     from the lecture slides.
            x.lAST.accept(self)
            self.emit(JVM.IFEQ + " " + self.getLabelString(L1))
            x.rAST.accept(self)
            self.emit(JVM.IFEQ + " " + self.getLabelString(L1))
            self.emit(JVM.ICONST_1)
            self.emit(JVM.GOTO + " " + self.getLabelString(L2))
            self.emitLabel(L1)
            self.emit(JVM.ICONST_0)
            self.emitLabel(L2)

            return
        
        if Op == "||":
            #TBD: implement || short circuit evaluation.
            #     Similar to &&, you may use a Java example to figure it out..
            L1 = self.frame.getNewLabel()
            L2 = self.frame.getNewLabel()
            x.lAST.accept(self)
            self.emit(JVM.IFNE + " " + self.getLabelString(L1))
            x.rAST.accept(self)
            self.emit(JVM.IFNE + " " + self.getLabelString(L1))
            self.emit(JVM.ICONST_0)
            self.emit(JVM.GOTO + " " + self.getLabelString(L2))
            self.emitLabel(L1)
            self.emit(JVM.ICONST_1)
            self.emitLabel(L2)
            return
        '''
            Here we treat +, -, *, / >, >=, <, <=, ==, !=
            See the code templates in the lecture slides. Remaining cases are
            similar, you can check how the javac compiler does it.
        '''
        x.lAST.accept(self)
        x.rAST.accept(self)
        # TBD:
        if Op == "+":
            self.emit(JVM.IADD)
        elif Op == "-":
            self.emit(JVM.ISUB)
        elif Op == "*":
            self.emit(JVM.IMUL)
        elif Op == "/":
            self.emit(JVM.IDIV)

        elif Op in ("==", "!=", "<", "<=", ">", ">="):
            L1 = self.frame.getNewLabel()
            L2 = self.frame.getNewLabel()

            if Op == "==":
                self.emit(JVM.IF_ICMPEQ + " " + self.getLabelString(L1))
            elif Op == "!=":
                self.emit(JVM.IF_ICMPNE + " " + self.getLabelString(L1))
            elif Op == "<":
                self.emit(JVM.IF_ICMPLT + " " + self.getLabelString(L1))
            elif Op == "<=":
                self.emit(JVM.IF_ICMPLE + " " + self.getLabelString(L1))
            elif Op == ">":
                self.emit(JVM.IF_ICMPGT + " " + self.getLabelString(L1))
            elif Op == ">=":
                self.emit(JVM.IF_ICMPGE + " " + self.getLabelString(L1))
            self.emit(JVM.ICONST_0)
            self.emit(JVM.GOTO + " " + self.getLabelString(L2))
            self.emitLabel(L1)
            self.emit(JVM.ICONST_1)
            self.emitLabel(L2)

    @visit.register
    def _(self, x: UnaryExpr):
        # self.emit("; UnaryExpr")
        Op = x.oAST.Lexeme
        x.eAST.accept(self)
        # Here we treat the following cases:
        #   unary "-": emit JVM.INEG for integers
        #   unary "+": do nothing
        #   "i2f": emit JVM.I2F instruction
        #   "!": you can use the following code template:
        #
        #    !E  =>    [[E]]
        #              ifne Label1
        #              iconst_1
        #              goto Label2
        #           Label1:
        #              iconst_0
        #           Label2:
        # TBD:
        if Op == "-":
            self.emit(JVM.INEG)
        elif Op == "+":
            pass
        elif Op == "i2f":
            self.emit(JVM.I2F)
        elif Op == "!":
            L1 = self.frame.getNewLabel()
            L2 = self.frame.getNewLabel()
            self.emit(JVM.IFNE + " " + self.getLabelString(L1))
            self.emit(JVM.ICONST_1)
            self.emit(JVM.GOTO + " " + self.getLabelString(L2))
            self.emitLabel(L1)
            self.emit(JVM.ICONST_0)
            self.emitLabel(L2)
        else:
            assert False
    
    @visit.register
    def _(self, x: EmptyExpr):
        pass

    @visit.register
    def _(self, x: ActualParam):
        self.emit("; ActualParam")
        x.pAST.accept(self)
    
    @visit.register
    def _(self, x: EmptyActualParam):
        pass

    @visit.register
    def _(self, x: ActualParamSequence):
        x.lAST.accept(self)
        x.rAST.accept(self)
    
    @visit.register
    def _(self, x: CallExpr):
        self.emit("; CallExpr")
        assert isinstance(x.idAST.declAST, FunDecl)
        F = x.idAST.declAST
        if not self.isStaticMethod(F):
            self.emit('; "this"-pointer is the first ActualParam with instance methods:')
            if self.isMain:
                self.emit(JVM.ALOAD_1)
            else:
                self.emit(JVM.ALOAD_0)
        x.paramAST.accept(self)
        if self.isStaticMethod(F):
            self.emit(JVM.INVOKESTATIC + " lang/System/" + x.idAST.Lexeme + self.getDescriptor(F))
        else:
            #TBD: in case of an instance method, you need emit an JVM.INVOKEVIRTUAL instruction.
            #     the name of the function consists of <ClassName>/<functionname><functiondescriptor>.
            #      Relevant variables/functions: see above for static methods.
            self.emit(JVM.INVOKEVIRTUAL + " " + self.ClassName + "/" + x.idAST.Lexeme + self.getDescriptor(F))
    
    @visit.register
    def _(self, x: ExprSequence):
        x.lAST.accept(self)
        x.rAST.accept(self)
    
    @visit.register
    def _(self, x: ID):
        pass

    @visit.register
    def _(self, x: Operator):
        pass

    @visit.register
    def _(self, x: IntLiteral):
        #emit("; IntLiteral: " + x.Lexeme + "\n");
        #TBD: here you have to emit an ICONST instruction to load the integer literal
        #     onto the JVM stack. (see emitICONST).
        self.emitICONST(x.value)

    @visit.register
    def _(self, x: FloatLiteral):
        #emit("; FloatLiteral: " + x.Lexeme + "\n");
        #TBD: same for float
        self.emitFCONST(float(x.Lexeme))
    
    @visit.register
    def _(self, x: BoolLiteral):
        #emit("; BoolLiteral: " + x.Lexeme + "\n");
        #TBD: and bool...
        self.emitBCONST(x.Lexeme == "true")

    @visit.register
    def _(self, x: StringLiteral):
        #self.emit("; StringLiteral: " + x.Lexeme)
        self.emit(JVM.LDC + ' "' + x.Lexeme + '"')
    
    @visit.register
    def _(self, x: IntType):
        pass

    @visit.register
    def _(self, x: FloatType):
        pass

    @visit.register
    def _(self, x: BoolType):
        pass

    @visit.register
    def _(self, x: StringType):
        pass

    @visit.register
    def _(self, x: VoidType):
        pass

    @visit.register
    def _(self, x: ArrayType):
        pass

    @visit.register
    def _(self, x: ErrorType):
        self.emit('; ErrorType')
        assert False
    
