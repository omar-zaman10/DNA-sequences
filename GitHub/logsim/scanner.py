"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
import names
import numpy as np

class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""

        self.type = None
        self.id = None
        self.position = None
        self.line = None


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""

        try:
            self.input_file = open(path, 'r')
        except:
            raise FileNotFoundError("Error: File doesn't exist in current directory")
            sys.exit()
        

        self.names = names
        
        self.symbol_type_list = [self.SEMICOLON, self.COLON, self.FULLSTOP, self.COMMA, self.HASHTAG, 
                                self.NEWLINE, self.KEYWORD, self.NAME, self.INTEGER, self.INT16, self.EOF] = range(11)
        
        self.keywords_list = ["DEVICES", "CONNECTIONS", "MONITOR", "END" "to", "is", "SWITCH", "with", 
                            "state", "and", "CLOCK", "cycle", "period", "AND", "NAND", "OR", "NOR", "DTYPE", 
                            "XOR", "input", "inputs", "I", "DATA", "CLK", "SET", "CLEAR", "Q", "QBAR"]
        
        [self.DEVICES_ID, self.CONNECTIONS_ID, self.MONITOR_ID, self.END_ID, self.TO, self.IS, self.SWITCH_ID, 
        self.WITH, self.STATE, self.AND, self.CLOCK_ID, self.CYCLE, self.PERIOD, self.AND_ID, self.NAND_ID,
        self.OR_ID, self.NOR_ID, self.DTYPE_ID, self.XOR_ID, self.INPUT, self.INPUTS, self.I, self.DATA, self.CLK,
        self.SET, self.CLEAR, self.Q, self.QBAR] = self.names.lookup(self.keywords_list)


        self.current_character = ""
        self.character_number = 0
        self.line_number = 0
        self.symbol_number = 0
        self.scanner_error_count = 0


    def get_symbol(self):
        """Translate the next sequence of characters into a symbol for the parser"""
        
        symbol = Symbol() #create instance of the symbol class
        self.skipSpace() #ignore whitespace

        #identify punctuation (semicolon, colon, full stop, comma)
        if self.current_character == ';':
            symbol.type = self.SEMICOLON
            self.nextCharacter()
            #print(";")
        
        elif self.current_character == ':':
            symbol.type = self.COLON
            self.nextCharacter()
            #print(":")

        elif self.current_character == '.':
            symbol.type = self.FULLSTOP
            self.nextCharacter()
            #print(".")

        elif self.current_character == ",":
            symbol.type = self.COMMA
            self.nextCharacter()
            #print(",")
        
        #identify new line
        elif self.current_character == '\n':
            symbol.type = self.NEWLINE
            self.nextCharacter()

        #identify comments
        elif self.current_character == "#":
            symbol.type = self.HASHTAG
            #print("#")
            self.nextCharacter()
            while self.current_character != '\n':
                #print(self.current_character) #prints comment i.e. characters after '#' until end of line
                symbol.type = self.HASHTAG
                self.nextCharacter()

        #identify end of file
        elif self.current_character == "":
            symbol.type = self.EOF
        
        #identify integers, in particular 1-16 for gate input allocation
        elif self.current_character.isdigit() == True:
            symbol.id = self.getNumber()
   
            if type(symbol.id) == int:
                symbol.type = self.INTEGER
                if 1 <= symbol.id <= 16:
                    symbol.type = self.INT16
            elif type(symbol.id) == float:
                self.reportErrorLocation()
                raise SyntaxError("Invalid number: only integers allowed")
            
            self.nextCharacter()
            #print(symbol.id)

        #identify alphanumerical sequences as either keywords if in keywords list, or as a name otherwise
        elif self.current_character.isalpha() == True:
            self.string = self.getString()

            if self.string in self.keywords_list:
                symbol.type = self.KEYWORD
                symbol.id = self.names.query(self.string)
            else:
                symbol.type = self.NAME
                symbol.id = self.names.query(self.string)
            
            self.nextCharacter()
            #print(self.string)
        
        else:
            self.reportErrorLocation()
            raise SyntaxError("Error: invalid character")


        symbol.position = self.character_number
        symbol.line = self.line_number
        self.symbol_number += 1
        
        return symbol


    def nextCharacter(self):
        """Looks at the next character and increases the character and line counters
        as necessary"""

        self.character_number += 1 
        self.current_character = self.input_file.read(self.character_number)[-1]
        
        if self.current_character == '\n':
            self.character_number = 0
            self.line_number += 1
        
        return self.current_character


    def skipSpace(self):
        """Skip any whitespace to return the next non-space character"""

        while self.current_character.isspace():
            self.current_character = self.nextCharacter()


    def getString(self):
        """Return the next keyword or name string in the input file"""

        string = str(self.current_character)

        while self.current_character.isalnum():
            self.current_character = self.nextCharacter()
            if self.current_character.isalnum() == True:
                string = str(string) + str(self.current_character)
            else:
                return string
    
    
    def getNumber(self):
        """Returns the next number in the input file"""

        number = self.current_character
        
        while self.current_character.isdigit():
            self.current_character = self.nextCharacter()
            if self.current_character.isdigit() == True:
                number = str(number) + str(self.current_character)
            else:
                return number
    
    def reportErrorLocation(self):
        """For basic error handling: To be called by the parser and in some cases 
        within the scanner in case of an error. Returns the erroneous line and 
        a pointer in the following line pointing to the erroneous character"""

        pointer = ""

        for i in range(self.character_number - 1):
            pointer += " "
        
        pointer += "^"
        self.scanner_error_count += 1

        #Returns the erroneous line to the console, with a pointer in the next line to show poisiton of error
        #print(self.input_file.read()[self.line_number], end = '\n')
        #print(pointer)

        return self.input_file.read()[self.line_number], pointer