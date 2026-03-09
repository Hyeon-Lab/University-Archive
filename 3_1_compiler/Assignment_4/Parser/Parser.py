from Scanner.SourcePos import *
from Scanner.Token import *
from Scanner.SourcePos import *
from Scanner.Scanner import *
from Parser.SyntaxError import *
from ErrorReporter import *

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

from AstGen.Visitor import *

class Parser:
    def __init__(self, lexer, reporter):
        self.scanner = lexer
        self.errorReporter = reporter
        self.currentToken = 0
        self.previousTokenPosition = 0

    # accept() checks whether the current token matches tokenExpected.
    # If so, it fetches the next token
    # If not, it reports a syntax error.
    def accept(self, tokenExpected):
        if self.currentToken.kind == tokenExpected:
            self.previousTokenPosition = self.currentToken.GetSourcePos()
            self.currentToken = self.scanner.scan()
        else:
            self.syntaxError("% expected here", Token.spell(tokenExpected))
    
    # acceptIt() unconditionally accepts the current token
    # and fetches the next token from the scanner.
    def acceptIt(self):
        self.previousTokenPosition = self.currentToken.GetSourcePos()
        self.currentToken = self.scanner.scan()

    # start records the position of the start of a phrase.
    # This is defined to be the position of the first
    # character of the first token of the phrase.
    def start(self, pos):
        pos.StartCol = self.currentToken.GetSourcePos().StartCol
        pos.StartLine = self.currentToken.GetSourcePos().StartLine

    # finish records the position of the end of a phrase.
    # This is defined to be the position of the last
    # character of the last token of the phrase.  
    def finish(self, pos):
        pos.EndCol = self.previousTokenPosition.EndCol
        pos.EndLine = self.previousTokenPosition.EndLine
    
    def syntaxError(self, messageTemplate, tokenQuoted):
        pos = self.currentToken.GetSourcePos()
        self.errorReporter.reportError(messageTemplate, tokenQuoted, pos)
        raise SyntaxError()
    
    @staticmethod
    def isTypeSpecifier(token):
        if token in (Token.VOID, Token.INT, Token.BOOL, Token.FLOAT):
            return True
        else:
            return False
    
    '''
        parseArrayIndexDecl (Type T):

        Take [INTLITERAL] and generate an ArrayType

    '''
    def parseArrayIndexDecl(self, T):
        self.accept(Token.LEFTBRACKET)
        pos = self.currentToken.GetSourcePos()
        L = IntLiteral(self.currentToken.GetLexeme(), pos)
        self.accept(Token.INTLITERAL)
        self.accept(Token.RIGHTBRACKET)
        IE = IntExpr(L, pos)
        return ArrayType(T, IE, self.previousTokenPosition)
    
    # toplevel parse() routine:

    def parse(self):    # called from the MiniC driver
        ProgramAST = None

        self.previousTokenPosition = SourcePos()
        self.previousTokenPosition.StartLine = 0
        self.previousTokenPosition.StartCol = 0
        self.previousTokenPosition.EndLine = 0
        self.previousTokenPosition.EndCol = 0

        self.currentToken = self.scanner.scan() # get first token from scanner...

        try:
            ProgramAST = self.parseProgram()
            if self.currentToken.kind != Token.EOF:
                self.syntaxError('% not expected after end of program', self.currentToken.GetLexeme())
        except SyntaxError as s:
            return None

        return ProgramAST
    
    '''
        parseProgram():

        program ::= ( (VOID|INT|BOOL|FLOAT) Id ( FunPart | VarPart ) )* ";"

    '''

    # parseProgDecls: recursive helper function to facilitate AST construction.
    def parseProgDecls(self):
        if not Parser.isTypeSpecifier(self.currentToken.kind):
            return EmptyDecl(self.previousTokenPosition)
        pos = SourcePos()
        self.start(pos)
        T = self.parseTypeSpecifier()
        Ident = self.parseID()
        if self.currentToken.kind == Token.LEFTPAREN:
            newD = self.parseFunPart(T, Ident, pos)
            return DeclSequence(newD, self.parseProgDecls(), self.previousTokenPosition)
        else:
            Vars = self.parseVarPart(T, Ident)
            VarsTail = Vars.GetRightmostDeclSequenceNode()
            RemainderDecls = self.parseProgDecls()
            VarsTail.SetRightSubtree(RemainderDecls)
            return Vars
    
    def parseProgram(self):
        pos = SourcePos()
        self.start(pos)
        D = self.parseProgDecls()
        self.finish(pos)
        P = Program(D, pos)
        return P
    
    '''

        parseFunPart():
    
        FunPart ::= ( "(" ParamsList? ")" CompoundStmt )
    
    '''

    def parseFunPart(self, T, Ident, pos):
        # We already know that the current token is "(".
        # Otherwise use accept() !
        self.acceptIt()
        PDecl = self.parseParamsList()  # can also be empty...
        self.accept(Token.RIGHTPAREN)
        CStmt = self.parseCompoundStmt()
        self.finish(pos)
        return FunDecl(T, Ident, PDecl, CStmt, pos)
    
    '''
        parseParamsList():
    
        ParamsList ::= ParameterDecl ( "," ParameterDecl )*
    '''
    def parseParamsList(self):
        if not Parser.isTypeSpecifier(self.currentToken.kind):
            return EmptyFormalParamDecl(self.previousTokenPosition)
        Decl_l = self.parseParameterDecl()
        Decl_r = EmptyFormalParamDecl(self.previousTokenPosition)
        if self.currentToken.kind == Token.COMMA:
            self.acceptIt()
            Decl_r = self.parseParamsList()
            if isinstance(Decl_r, EmptyFormalParamDecl):
                self.syntaxError("Declaration after comma expected", "")
        return FormalParamDeclSequence(Decl_l, Decl_r, self.previousTokenPosition)
    
    '''
        parseParameterDecl():
    
        ParameterDecl ::= (VOID | INT | BOOL | FLOAT) Declarator
    '''
    def parseParameterDecl(self):
        T = None
        D = None

        pos = SourcePos()
        self.start(pos)
        if Parser.isTypeSpecifier(self.currentToken.kind):
            T = self.parseTypeSpecifier()
        else:
            self.syntaxError('Type specifier instead of % expected', Token.spell(self.currentToken.kind))
        D = self.parseDeclarator(T, pos)
        return D
    
    '''
        parseDeclarator():

        Declarator ::= ID ( "[" INTLITERAL "]" )?
    '''
    def parseDeclarator(self, T, pos):
        Ident = self.parseID()
        if self.currentToken.kind == Token.LEFTBRACKET:
            ArrT = self.parseArrayIndexDecl(T)
            self.finish(pos)
            return FormalParamDecl(ArrT, Ident, pos)
        self.finish(pos)
        return FormalParamDecl(T, Ident, pos)
    
    '''
        parseVarPart():
    
        VarPart ::= ( "[" INTLITERAL "]" )? ( "=" initializer ) ? ( "," init_decl )* ";"
    '''
    def parseVarPart(self, T, Ident):
        theType = T
        Seq = None
        E = EmptyExpr(self.previousTokenPosition)
        if self.currentToken.kind == Token.LEFTBRACKET:
            theType = self.parseArrayIndexDecl(T)
        if self.currentToken.kind == Token.ASSIGN:
            self.acceptIt()
            E = self.parseInitializer()

        D = VarDecl(theType, Ident, E, self.previousTokenPosition)
        # You can use the following code after implementation of parseInitDecl()
        if (self.currentToken.kind == Token.COMMA):
            self.acceptIt()
            Seq = DeclSequence(D, self.parseInitDecl(T), self.previousTokenPosition)
        else:
            Seq = DeclSequence(D, EmptyDecl(self.previousTokenPosition), self.previousTokenPosition)
        self.accept(Token.SEMICOLON)
        return Seq
    
    '''
        parseInitDecl():

        init_decl ::= ID ( "[" INTLITERAL "]" )? ("=" initializer)? ("," ID ( "[" INTLITERAL "]" )? ("=" initializer)? )*
    '''

    def parseInitDecl(self, T):
        pos = SourcePos()
        self.start(pos)
        Ident = self.parseID()
        if self.currentToken.kind == Token.LEFTBRACKET:
            T = self.parseArrayIndexDecl(T)
        E = EmptyExpr(pos)

        if self.currentToken.kind == Token.ASSIGN:
            self.acceptIt()
            E = self.parseInitializer()
        D = VarDecl(T, Ident, E, pos)
        if  self.currentToken.kind == Token.COMMA:
            self.acceptIt()
            seq = DeclSequence(D, self.parseInitDecl(T), self.previousTokenPosition)
        else:
            seq = DeclSequence(D, EmptyDecl(self.previousTokenPosition), self.previousTokenPosition)
            self.finish(pos)
        return seq

    '''
        parseVariableDef():

        VariableDef ::= ( void | int | bool | float )  ID ( "[" INTLITERAL "]" )? ("=" initializer) ? ("," ID ( "[" INTLITERAL "]" )? ("=" initializer)? ) * ";"
    '''
    def parseVariableDef(self):
        pos = SourcePos()
        self.start(pos)

        type_spec = self.currentToken.GetLexeme()
        self.acceptIt()

        var_list = []

        while True:
            ident = ID(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.accept(Token.ID)

            array_size = None
            if self.currentToken.kind == Token.LEFTBRACKET:
                self.accept(Token.LEFTBRACKET)
                array_size = int(self.currentToken.GetLexeme())
                self.accept(Token.INTLITERAL)
                self.accept(Token.RIGHTBRACKET)

            initializer = None
            if self.currentToken.kind == Token.ASSIGN:
                self.accept(Token.ASSIGN)
                initializer = self.parseInitializer()

            var_list.append(VarDecl(ident, array_size, initializer))

            if self.currentToken.kind == Token.COMMA:
                self.accept(Token.COMMA)
            else:
                break

        self.accept(Token.SEMICOLON)

        self.finish(pos)
        return VarDecl(type_spec, var_list, pos)

    
    ''' 
        parseInitializer():

        Initializer ::= expr
            | "{" expr ( "," expr ) *  "}"
    '''
    def parseInitSeq(self):
        new = self.parseExpr()
        if self.currentToken.kind == Token.COMMA:
            self.acceptIt()
            return ExprSequence(new, self.parseInitSeq(), self.previousTokenPosition)
        else:
            return ExprSequence(new, EmptyExpr(self.previousTokenPosition), self.previousTokenPosition)

    def parseInitializer(self):
        if self.currentToken.kind == Token.LEFTBRACE:
            pos = SourcePos()
            self.start(pos)
            self.acceptIt()  # '{'
            E = self.parseExpr()
            if self.currentToken.kind == Token.COMMA:
                self.acceptIt()
                E = ExprSequence(E, self.parseInitSeq(), self.previousTokenPosition)
            else:
                E = ExprSequence(E, EmptyExpr(pos), pos)
            self.accept(Token.RIGHTBRACE)
            self.finish(pos)
            return E
        else:
            return self.parseExpr()

    '''
        parseStmt():

        stmt ::= CompoundStmt
                | if "(" expr ")" stmt ( else stmt )?
                | while "(" expr ")" stmt
                | for "(" asgnexpr? ";" expr? ";" asgnexpr? ")" stmt
                | return expr? ";"
                | ID ( "=" expr ";" | "[" expr "]" "=" expr ";" | arglist ";" )
    '''
    def parseStmt(self):
        pos = SourcePos()
        self.start(pos)

        if self.currentToken.kind == Token.LEFTBRACE:
            stmt = self.parseCompoundStmt()
        elif self.currentToken.kind == Token.IF:
            self.acceptIt()
            self.accept(Token.LEFTPAREN)
            cond = self.parseExpr()
            self.accept(Token.RIGHTPAREN)
            then_stmt = self.parseStmt()
            else_stmt = None
            if self.currentToken.kind == Token.ELSE:
                self.acceptIt()
                else_stmt = self.parseStmt()
            stmt = IfStmt(cond, then_stmt, else_stmt, pos)
        elif self.currentToken.kind == Token.WHILE:
            self.acceptIt()
            self.accept(Token.LEFTPAREN)
            cond = self.parseExpr()
            self.accept(Token.RIGHTPAREN)
            body = self.parseStmt()
            stmt = WhileStmt(cond, body, pos)
        elif self.currentToken.kind == Token.FOR:
            self.acceptIt()
            self.accept(Token.LEFTPAREN)
            init = None
            if self.currentToken.kind != Token.SEMICOLON:
                init = self.parseAsgnExpr()
            else:
                init = EmptyExpr(pos)
            self.accept(Token.SEMICOLON)
            cond = None
            if self.currentToken.kind != Token.SEMICOLON:
                cond = self.parseExpr()
            else:
                cond = EmptyExpr(pos)
            self.accept(Token.SEMICOLON)
            step = None
            if self.currentToken.kind != Token.RIGHTPAREN:
                step = self.parseAsgnExpr()
            else:
                step = EmptyExpr(pos)
            self.accept(Token.RIGHTPAREN)
            body = self.parseStmt()
            stmt = ForStmt(init, cond, step, body, pos)
        elif self.currentToken.kind == Token.RETURN:
            self.acceptIt()
            expr = EmptyExpr(pos)
            if self.currentToken.kind != Token.SEMICOLON:
                expr = self.parseExpr()
            self.accept(Token.SEMICOLON)
            stmt = ReturnStmt(expr, pos)
        elif self.currentToken.kind == Token.ID:
            ident = self.parseID()
            if self.currentToken.kind == Token.ASSIGN:
                self.acceptIt()
                expr = self.parseExpr()
                self.accept(Token.SEMICOLON)
                stmt = AssignStmt(VarExpr(ident, pos), expr, pos)
            elif self.currentToken.kind == Token.LEFTBRACKET:
                self.acceptIt()
                index = self.parseExpr()
                self.accept(Token.RIGHTBRACKET)
                self.accept(Token.ASSIGN)
                expr = self.parseExpr()
                self.accept(Token.SEMICOLON)
                stmt = AssignStmt(ArrayExpr(VarExpr(ident, pos), index, pos), expr, pos)
            elif self.currentToken.kind == Token.LEFTPAREN:
                call = self.parseArgList()
                self.accept(Token.SEMICOLON) 
                stmt = CallStmt(CallExpr(ident, call, pos),pos)
            else:
                self.error("unexpected token after identifier")
        else:
            self.error("unexpected token starting statement")

        self.finish(pos)
        return stmt

    '''
        parseExpr():

        expr ::= or-expr
    '''
    def parseExpr(self):
        return self.parseOrExpr()

    '''
        parseOrExpr():

        or-expr ::= and-expr ( "||" and-expr )*
    '''
    def parseOrExpr(self):
        pos = SourcePos()
        self.start(pos)
        expr = self.parseAndExpr()
        while self.currentToken.kind == Token.OR:
            op = Operator(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.acceptIt()
            right = self.parseAndExpr()
            expr = BinaryExpr(expr, op, right, pos)
        self.finish(pos)
        return expr

    '''
        parseAndExpr():

        and-expr ::= relational-expr ( "&&" relational-expr )*
    '''
    def parseAndExpr(self):
        pos = SourcePos()
        self.start(pos)
        expr = self.parseRelationalExpr()
        while self.currentToken.kind == Token.AND:
            op = Operator(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.acceptIt()
            right = self.parseRelationalExpr()
            expr = BinaryExpr(expr, op, right, pos)
        self.finish(pos)
        return expr

    '''
        parseRelationalExpr():

        relational-expr ::= add-expr ( "==" add-expr | "!=" add-expr | "<" add-expr 
                                    | "<=" add-expr | ">" add-expr | ">=" add-expr ) ?
    '''
    def parseRelationalExpr(self):
        pos = SourcePos()
        self.start(pos)
        expr = self.parseAddExpr()
        if self.currentToken.kind in (Token.EQ, Token.NOTEQ, Token.GREATER, Token.GREATEREQ, Token.LESS, Token.LESSEQ):
            op = Operator(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.acceptIt()
            right = self.parseAddExpr()
            expr = BinaryExpr(expr, op, right, pos)
        self.finish(pos)
        return expr

    '''
        parseAddExpr():

        add-expr ::= mult-expr ( "+" mult-expr | "-" mult-expr )*
    '''
    def parseAddExpr(self):
        pos = SourcePos()
        self.start(pos)
        expr = self.parseMultExpr()
        while self.currentToken.kind in (Token.PLUS, Token.MINUS):
            op = Operator(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.acceptIt()
            right = self.parseMultExpr()
            expr = BinaryExpr(expr, op, right, pos)
        self.finish(pos)
        return expr

    '''
        parseMultExpr():

        mult-expr ::= unary-expr ( "*" unary-expr | "/" unary-expr)*
    '''
    def parseMultExpr(self):
        pos = SourcePos()
        self.start(pos)
        expr = self.parseUnaryExpr()

        while self.currentToken.kind in (Token.TIMES, Token.DIV):
            op = Operator(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.acceptIt()
            right = self.parseUnaryExpr()
            expr = BinaryExpr(expr, op, right, pos)

        self.finish(pos)
        return expr

    '''
        parseUnaryExpr():
    
        UnaryExpr ::= ("+"|"-"|"!")* PrimaryExpr
    '''
    def parseUnaryExpr(self):
        if self.currentToken.kind in (Token.PLUS, Token.MINUS, Token.NOT):
            opAST = Operator(self.currentToken.GetLexeme(), self.previousTokenPosition)
            self.acceptIt()
            return UnaryExpr(opAST, self.parseUnaryExpr(), self.previousTokenPosition)
        return self.parsePrimaryExpr()
    
    '''
        parsePrimaryExpr():
        
        PrimaryExpr ::= ID arglist?
                        | ID "[" expr "]"
                        | "(" expr ")"
                        | INTLITERAL | BOOLLITERAL | FLOATLITERAL | STRINGLITERAL
    '''
    def parsePrimaryExpr(self):
        pos = SourcePos()
        self.start(pos)

        if self.currentToken.kind == Token.ID:
            Ident = self.parseID()
            if self.currentToken.kind == Token.LEFTPAREN:
                ArgList = self.parseArgList()
                self.finish(pos)
                return CallExpr(Ident, ArgList, pos)
            elif self.currentToken.kind == Token.LEFTBRACKET:
                self.acceptIt()
                Expr = self.parseExpr()
                self.accept(Token.RIGHTBRACKET)
                self.finish(pos)
                return ArrayExpr(VarExpr(Ident, pos), Expr, pos)
            else:
                self.finish(pos)
                return VarExpr(Ident, pos)

        elif self.currentToken.kind == Token.LEFTPAREN:
            self.acceptIt()
            E = self.parseExpr()
            self.accept(Token.RIGHTPAREN)
            return E

        elif self.currentToken.kind == Token.INTLITERAL:
            L = IntLiteral(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.acceptIt()
            return IntExpr(L, self.previousTokenPosition)

        elif self.currentToken.kind == Token.BOOLLITERAL:
            L = BoolLiteral(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.acceptIt()
            return BoolExpr(L, self.previousTokenPosition)

        elif self.currentToken.kind == Token.FLOATLITERAL:
            L = FloatLiteral(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.acceptIt()
            return FloatExpr(L, self.previousTokenPosition)

        elif self.currentToken.kind == Token.STRINGLITERAL:
            L = StringLiteral(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
            self.acceptIt()
            return StringExpr(L, self.previousTokenPosition)

        else:
            self.syntaxError("Unexpected token in expression", Token.spell(self.currentToken.kind))
            return EmptyExpr(self.currentToken.GetSourcePos())

    '''
        parseAsgnExpr():
    
        asgnexpr ::= ID "=" expr
    '''
    def parseAsgnExpr(self):
        pos = SourcePos()
        self.start(pos)
        Ident = self.parseID()
        self.accept(Token.ASSIGN)
        expr = self.parseExpr()
        expr = AssignExpr(VarExpr(Ident, pos), expr, pos)
        self.finish(pos)
        return expr

    '''
        parseCompoundStmt():

        CompoundStmt ::= "{" VariableDef* Stmt* "}"
    '''
    def parseCompoundDecls(self):
        if not Parser.isTypeSpecifier(self.currentToken.kind):
            return EmptyDecl(self.previousTokenPosition)
        T = self.parseTypeSpecifier()
        Ident = self.parseID()
        Vars = self.parseVarPart(T, Ident)
        VarsTail = Vars.GetRightmostDeclSequenceNode()
        RemainderDecls = self.parseCompoundDecls()
        VarsTail.SetRightSubtree(RemainderDecls)
        return Vars

    def parseCompoundStmts(self):
        if not self.currentToken.kind in (Token.LEFTBRACE, Token.IF, Token.WHILE, Token.FOR, Token.RETURN, Token.ID):
            return EmptyStmt(self.previousTokenPosition)
        S = self.parseStmt()
        return StmtSequence(S, self.parseCompoundStmts(), self.previousTokenPosition)
    
    def parseCompoundStmt(self):
        pos = SourcePos()
        self.start(pos)
        self.accept(Token.LEFTBRACE)
        D = self.parseCompoundDecls()
        S = self.parseCompoundStmts()
        self.accept(Token.RIGHTBRACE)
        self.finish(pos)
        if type(D) is EmptyDecl and type(S) is EmptyStmt:
            return EmptyCompoundStmt(self.previousTokenPosition)
        else:
            return CompoundStmt(D, S, pos)
    
    '''
        parseArgList():
        
        ArgList ::= "(" ( arg ( "," arg )* )? ")"
    '''

    def parseArgs(self):
        if self.currentToken.kind == Token.RIGHTPAREN:
            return EmptyActualParam(self.previousTokenPosition)
        Params = ActualParam(self.parseExpr(), self.previousTokenPosition)
        if self.currentToken.kind == Token.COMMA:
            self.acceptIt()
        return ActualParamSequence(Params, self.parseArgs(), self.previousTokenPosition)
    
    def parseArgList(self):
        self.accept(Token.LEFTPAREN)
        Params = self.parseArgs()
        self.accept(Token.RIGHTPAREN)
        return Params
    
    '''
        parseID():

        ID (terminal)
    '''
    def parseID(self):
        Ident = ID(self.currentToken.GetLexeme(), self.currentToken.GetSourcePos())
        self.accept(Token.ID)
        return Ident

    '''
        parseTypeSpecifier():

        VOID | INT | FLOAT | BOOL (all terminals)
    '''

    def parseTypeSpecifier(self):
        T = None
        match self.currentToken.kind:
            case Token.INT:
                T = IntType(self.currentToken.GetSourcePos())
            case Token.FLOAT:
                T = FloatType(self.currentToken.GetSourcePos())
            case Token.BOOL:
                T = BoolType(self.currentToken.GetSourcePos())
            case Token.VOID:
                T = VoidType(self.currentToken.GetSourcePos())
            case _:
                self.syntaxError("Type specifier expected", "")
        self.acceptIt()
        return T

