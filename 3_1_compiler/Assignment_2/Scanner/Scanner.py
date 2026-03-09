from Scanner.Token import *
from Scanner.SourceFile import *
from Scanner.SourcePos import *

class Scanner:
    @staticmethod
    def isDigit(c):
        return (c >= '0' and c <= '9')

    @staticmethod
    def isLetter(c):
        return ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_')
    
    def __init__(self, source):
        self.sourceFile = source
        self.currentChar = self.sourceFile.readChar()
        self.verbose = False
        self.currentLineNr = 1
        self.currentColNr = 1

        self.currentLexeme = ''
        self.currentlyScanningToken = False
        
        self.buffer = []
        self.replacedByBuffer = ''

    def enableDebugging(self):
        self.verbose = True

    def takeIt(self):
        if(len(self.buffer) == 0):
            if self.currentlyScanningToken:
                self.currentLexeme += self.currentChar
            if self.currentChar == '\n':
                self.currentLineNr += 1
                self.currentColNr = 1
            else:
                self.currentColNr += 1
            self.currentChar = self.sourceFile.readChar()
        else:
            self.buffer = self.buffer[1:]
            self.currentLexeme += self.currentChar
            if(len(self.buffer) == 0):
                self.currentChar = self.replacedByBuffer
            else:   
                self.currentChar = self.buffer[0]           

    def scanToken(self):
        match self.currentChar:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                self.takeIt()
                while self.isDigit(self.currentChar): #d+
                    self.takeIt()
                if(self.currentChar == '.'): #d+.
                    self.takeIt()
                    if(self.isDigit(self.currentChar)): #d+.d
                        self.takeIt()
                        while (self.isDigit(self.currentChar)): #d+.d+
                            self.takeIt()
                        if(self.currentChar == 'e' or self.currentChar == 'E'): #d+.d+(e|E)
                            self.takeIt()
                            if(self.currentChar == '+' or self.currentChar == '-'): #d+.d+(e|E)(+|-)
                                self.takeIt()
                                if(self.isDigit(self.currentChar)): #d+.d+(e|E)(+|-)d+
                                    self.takeIt()
                                    while self.isDigit(self.currentChar):
                                        self.takeIt()
                                    return Token.FLOATLITERAL
                                else: #d+.d+(e|E)(+|-)x
                                    #buffer로 d+.d+ -> float
                                    self.replacedByBuffer = self.currentChar
                                    self.buffer = self.currentLexeme
                                    self.currentLexeme = ""
                                    self.currentChar = self.buffer[0]
                                    if(self.isDigit(self.currentChar)):
                                        self.takeIt()
                                        while(self.isDigit(self.currentChar)):
                                            self.takeIt()
                                        if(self.currentChar == '.'):
                                            self.takeIt()
                                            if(self.isDigit(self.currentChar)):
                                                self.takeIt()
                                                while(self.isDigit(self.currentChar)):
                                                    self.takeIt()
                                                return Token.FLOATLITERAL
                            elif(self.isDigit(self.currentChar)): #d+.d+(e|E)d+
                                self.takeIt()
                                while self.isDigit(self.currentChar):
                                    self.takeIt()
                                return Token.FLOATLITERAL
                            else: #d+.d+(e|E)x
                                #buffer로 d+.d+ -> float
                                self.replacedByBuffer = self.currentChar
                                self.buffer = self.currentLexeme
                                self.currentLexeme = ""
                                self.currentChar = self.buffer[0]
                                if(self.isDigit(self.currentChar)):
                                    self.takeIt()
                                    while(self.isDigit(self.currentChar)):
                                        self.takeIt()
                                    if(self.currentChar == '.'):
                                        self.takeIt()
                                        if(self.isDigit(self.currentChar)):
                                            self.takeIt()
                                            while(self.isDigit(self.currentChar)):
                                                self.takeIt()
                                            return Token.FLOATLITERAL
                        else: #d+.d+x
                            return Token.FLOATLITERAL
                    elif(self.currentChar == 'e' or self.currentChar == 'E'): #d+.(e|E)
                        self.takeIt()
                        if(self.currentChar == '+' or self.currentChar == '-'): #d+.(e|E)(+|-)
                            self.takeIt()
                            if(self.isDigit(self.currentChar)): #d+.(e|E)(+|-)d+
                                self.takeIt()
                                while self.isDigit(self.currentChar):
                                    self.takeIt()
                                return Token.FLOATLITERAL
                            else: #d+.(e|E)(+|-)x
                                #buffer로 d+. -> float
                                self.replacedByBuffer = self.currentChar
                                self.buffer = self.currentLexeme
                                self.currentLexeme = ""
                                self.currentChar = self.buffer[0]
                                if(self.isDigit(self.currentChar)):
                                    self.takeIt()
                                    while(self.isDigit(self.currentChar)):
                                        self.takeIt()
                                    if(self.currentChar == '.'):
                                        self.takeIt()
                                        return Token.FLOATLITERAL
                        elif(self.isDigit(self.currentChar)): #d+.(e|E)d+
                            self.takeIt()
                            while self.isDigit(self.currentChar):
                                self.takeIt()
                            return Token.FLOATLITERAL
                        else: #d+.(e|E)x
                            #buffer로 d+. -> float
                            self.replacedByBuffer = self.currentChar
                            self.buffer = self.currentLexeme
                            self.currentLexeme = ""
                            self.currentChar = self.buffer[0]
                            if(self.isDigit(self.currentChar)):
                                self.takeIt()
                                while(self.isDigit(self.currentChar)):
                                    self.takeIt()
                                if(self.currentChar == '.'):
                                    self.takeIt()
                                    return Token.FLOATLITERAL
                    else: #d+.x
                        return Token.FLOATLITERAL
                elif(self.currentChar == 'e' or self.currentChar == 'E'): #d+(e|E)
                    self.takeIt()
                    if(self.currentChar == '+' or self.currentChar == '-'): #d+(e|E)(+|-)
                        self.takeIt()
                        if(self.isDigit(self.currentChar)): #d+(e|E)(+|-)d+
                            self.takeIt()
                            while self.isDigit(self.currentChar):
                                self.takeIt()
                            return Token.FLOATLITERAL
                        else: #d+(e|E)(+|-)x
                            #buffer로 d+ -> int
                            self.replacedByBuffer = self.currentChar
                            self.buffer = self.currentLexeme
                            self.currentLexeme = ""
                            self.currentChar = self.buffer[0]
                            if(self.isDigit(self.currentChar)):
                                self.takeIt()
                                while(self.isDigit(self.currentChar)):
                                    self.takeIt()
                                return Token.INTLITERAL
                    elif(self.isDigit(self.currentChar)): #d+(e|E)d+
                        self.takeIt()
                        while self.isDigit(self.currentChar):
                            self.takeIt()
                        return Token.FLOATLITERAL
                    else: #d+(e|E)x
                        #buffer로 d+ -> int
                        self.replacedByBuffer = self.currentChar
                        self.buffer = self.currentLexeme
                        self.currentLexeme = ""
                        self.currentChar = self.buffer[0]
                        if(self.isDigit(self.currentChar)):
                            self.takeIt()
                            while(self.isDigit(self.currentChar)):
                                self.takeIt()
                            return Token.INTLITERAL
                else:
                    return Token.INTLITERAL
            case '.':
                self.takeIt() #.
                if(self.isDigit(self.currentChar)):
                    self.takeIt() #.d
                    while(self.isDigit(self.currentChar)):
                        self.takeIt() #.d+
                    if(self.currentChar == 'e' or self.currentChar == 'E'):
                        self.takeIt() #.d+(e|E)
                        if(self.currentChar == '+' or self.currentChar == '-'):
                            self.takeIt() #.d+(e|E)(+|-)
                            if(self.isDigit(self.currentChar)):
                                self.takeIt() #.d+(e|E)(+|-)d
                                while self.isDigit(self.currentChar):
                                    self.takeIt() #.d+(e|E)(+|-)d+
                                return Token.FLOATLITERAL
                            else:
                                #.d+(e|E)(+|-)x
                                #buffer로 .d+ -> float 
                                self.replacedByBuffer = self.currentChar
                                self.buffer = self.currentLexeme
                                self.currentLexeme = ""
                                self.currentChar = self.buffer[0]
                                if(self.currentChar == '.'):
                                    self.takeIt()
                                    if(self.isDigit(self.currentChar)):
                                        self.takeIt()
                                        while(self.isDigit(self.currentChar)):
                                            self.takeIt()
                                        return Token.FLOATLITERAL
                        elif(self.isDigit(self.currentChar)):
                            self.takeIt() #.d+(e|E)d
                            while(self.isDigit(self.currentChar)):
                                self.takeIt() #.d+(e|E)d+
                            return Token.FLOATLITERAL
                        else:
                            #.d+(e|E)x
                            #buffer로 .d+ -> float
                            self.replacedByBuffer = self.currentChar
                            self.buffer = self.currentLexeme
                            self.currentLexeme = ""
                            self.currentChar = self.buffer[0]
                            if(self.currentChar == '.'):
                                self.takeIt()
                                if(self.isDigit(self.currentChar)):
                                    self.takeIt()
                                    while(self.isDigit(self.currentChar)):
                                        self.takeIt()
                                    return Token.FLOATLITERAL
                    else:
                        #.d+
                        return Token.FLOATLITERAL
                else: #.
                    return Token.ERROR        
            case 'a'|'b'|'c'|'d'|'e'|'f'|'g'|'h'|'i'|'j'|'k'|'l'|'m'|'n'|'o'|'p'|'q'|'r'|'s'|'t'|'u'|'v'|'w'|'x'|'y'|'z'|'A'|'B'|'C'|'D'|'E'|'F'|'G'|'H'|'I'|'J'|'K'|'L'|'M'|'N'|'O'|'P'|'Q'|'R'|'S'|'T'|'U'|'V'|'W'|'X'|'Y'|'Z'|'_':
                if(self.currentChar == 'b'):
                    self.takeIt()
                    if(self.currentChar == 'o'):
                        self.takeIt()
                        if(self.currentChar == 'o'):
                            self.takeIt()
                            if(self.currentChar == 'l'):
                                self.takeIt()
                                if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                    return Token.BOOL
                elif(self.currentChar == 'e'):
                    self.takeIt()
                    if(self.currentChar == 'l'):
                        self.takeIt()
                        if(self.currentChar == 's'):
                            self.takeIt()
                            if(self.currentChar == 'e'):
                                self.takeIt()
                                if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                    return Token.ELSE
                elif(self.currentChar == 'f'):
                    self.takeIt()
                    if(self.currentChar == 'a'):
                        self.takeIt()
                        if(self.currentChar == 'l'):
                            self.takeIt()
                            if(self.currentChar == 's'):
                                self.takeIt()
                                if(self.currentChar == 'e'):
                                    self.takeIt()
                                    if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                        return Token.BOOLLITERAL
                    elif(self.currentChar == 'l'):
                        self.takeIt()
                        if(self.currentChar == 'o'):
                            self.takeIt()
                            if(self.currentChar == 'a'):
                                self.takeIt()
                                if(self.currentChar == 't'):
                                    self.takeIt()
                                    if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                        return Token.FLOAT
                    elif(self.currentChar == 'o'):
                        self.takeIt()
                        if(self.currentChar == 'r'):
                            self.takeIt()
                            if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                return Token.FOR
                elif(self.currentChar == 'i'):
                        self.takeIt()
                        if(self.currentChar == 'f'):
                            self.takeIt()
                            if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                return Token.IF
                        elif (self.currentChar == 'n'):
                            self.takeIt()
                            if(self.currentChar == 't'):
                                    self.takeIt()
                                    if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                        return Token.INT
                elif(self.currentChar == 'r'):
                    self.takeIt()
                    if(self.currentChar == 'e'):
                        self.takeIt()
                        if(self.currentChar == 't'):
                            self.takeIt()
                            if(self.currentChar == 'u'):
                                self.takeIt()
                                if(self.currentChar == 'r'):
                                    self.takeIt()
                                    if(self.currentChar == 'n'):
                                        self.takeIt()
                                        if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                            return Token.RETURN
                elif(self.currentChar == 't'):
                        self.takeIt()
                        if(self.currentChar == 'r'):
                            self.takeIt()
                            if(self.currentChar == 'u'):
                                self.takeIt()
                                if(self.currentChar == 'e'):
                                    self.takeIt()
                                    if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                        return Token.BOOLLITERAL
                elif(self.currentChar == 'v'):
                        self.takeIt()
                        if(self.currentChar == 'o'):
                            self.takeIt()
                            if(self.currentChar == 'i'):
                                self.takeIt()
                                if(self.currentChar == 'd'):
                                    self.takeIt()
                                    if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                        return Token.VOID
                elif(self.currentChar == 'w'):
                    self.takeIt()
                    if(self.currentChar == 'h'):
                        self.takeIt()
                        if(self.currentChar == 'i'):
                            self.takeIt()
                            if(self.currentChar == 'l'):
                                self.takeIt()
                                if(self.currentChar == 'e'):
                                    self.takeIt()
                                    if((self.isLetter(self.currentChar) == 0 and self.isDigit(self.currentChar) == 0)):
                                        return Token.WHILE
                if (self.isLetter(self.currentChar) or self.isDigit(self.currentChar)):
                    self.takeIt()
                while (self.isLetter(self.currentChar) or self.isDigit(self.currentChar)):
                    self.takeIt()
                return Token.ID

            case '"':
                self.takeIt()
                while self.currentChar != '"' and self.currentChar != SourceFile.EOF and self.currentChar != '\n':
                    if (self.currentChar == '\\'):
                        self.takeIt()
                        if(self.currentChar != 'n'):
                            print("ERROR: illegal escape sequence")
                    self.takeIt()
                if self.currentChar == '"':
                    self.takeIt()
                    self.currentLexeme = self.currentLexeme[1:-1]
                    return Token.STRINGLITERAL
                else:
                    print("ERROR: unterminated string literal")
                    self.currentLexeme = self.currentLexeme[1:]
                    return Token.STRINGLITERAL
            case '=':
                self.takeIt()
                if(self.currentChar == '='):
                    self.takeIt()
                    return Token.EQ
                else:
                    return Token.ASSIGN
            case '|':
                self.takeIt()
                if(self.currentChar == '|'):
                    self.takeIt()
                    return Token.OR
                else:
                    return Token.ERROR
            case '&':
                self.takeIt()
                if(self.currentChar == '&'):
                    self.takeIt()
                    return Token.AND
                else:
                    return Token.ERROR
            case '!':
                self.takeIt()
                if(self.currentChar == '='):
                    self.takeIt()
                    return Token.NOTEQ
                else:
                    return Token.NOT
            case '<':
                self.takeIt()
                if(self.currentChar == '='):
                    self.takeIt()
                    return Token.LESSEQ
                else:
                    return Token.LESS
            case '>':
                self.takeIt()
                if(self.currentChar == '='):
                    self.takeIt()
                    return Token.GREATEREQ
                else:
                    return Token.GREATER
            case '+':
                self.takeIt()
                return Token.PLUS
            case '-':
                self.takeIt()
                return Token.MINUS
            case '*':
                self.takeIt()
                return Token.TIMES
            case '/':
                self.takeIt()
                if(self.currentChar == '/'):
                    self.takeIt()
                    while(self.currentChar != '\n'):
                        self.takeIt()
                    return None
                elif(self.currentChar == '*'):
                    self.takeIt()
                    while(self.currentChar != SourceFile.EOF):
                        if(self.currentChar == '*'):
                            self.takeIt()
                            if(self.currentChar == '/'):
                                self.takeIt()
                                return None
                        else:
                            self.takeIt()
                    if(self.currentChar == SourceFile.EOF):
                        print("ERROR: unterminated multi-line comment.")
                        return None
                else:
                    return Token.DIV
            case '{':
                self.takeIt()
                return Token.LEFTBRACE
            case '}':
                self.takeIt()
                return Token.RIGHTBRACE
            case '[':
                self.takeIt()
                return Token.LEFTBRACKET
            case ']':
                self.takeIt()
                return Token.RIGHTBRACKET
            case '(':
                self.takeIt()
                return Token.LEFTPAREN
            case ')':
                self.takeIt()
                return Token.RIGHTPAREN
            case ',':
                self.takeIt()
                return Token.COMMA
            case ';':
                self.takeIt()
                return Token.SEMICOLON
            case SourceFile.EOF:
                self.currentLexeme += '$'
                return Token.EOF
            case _:
                self.takeIt()
                return Token.ERROR

    def scan(self):

        if(len(self.buffer) == 0):
            # 공백 문자 건너뛰기
            self.currentlyScanningToken = False
            while self.currentChar in (' ', '\f', '\n', '\r', '\t'):
                self.takeIt()
            self.currentlyScanningToken = True

        self.currentLexeme = ""
    
        # 시작 위치 저장
        pos = SourcePos()
        pos.StartLine = self.currentLineNr
        pos.StartCol = self.currentColNr - len(self.buffer)

        kind = self.scanToken()
        if (kind == None):
            return self.scan()

        # 끝 위치 저장
        pos.EndLine = self.currentLineNr
        pos.EndCol = self.currentColNr - 1 - len(self.buffer) if self.currentColNr > 1 else 1

        currentToken = Token(kind, self.currentLexeme, pos)

        if self.verbose:
            print(currentToken)

        return currentToken