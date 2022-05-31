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

        self.input_file = open(path, 'r')
        
        self.names = names
        
        self.symbol_type_list = [self.SEMICOLON, self.COLON, self.DOT, self.COMMA, self.HASHTAG, 
                                self.KEYWORD, self.NAME, self.NUMBER, self.EOF] = range(9)
        
        self.keywords_list = ["DEVICES", "CONNECTIONS", "MONITOR", "END" "to", "is", "SWITCH with state", "and", 
                            "CLOCK with", "cycle period", "AND with", "NAND with", "OR with", "NOR with", "DTYPE", 
                            "XOR", "input", "inputs", "I", "DATA", "CLK", "SET", "CLEAR", "Q", "QBAR"]
        
        [self.DEVICES_ID, self.CONNECTIONS_ID, self.MONITOR_ID, self.END_ID, self.TO, self.IS, self.SWITCH_ID, 
        self.AND, self.CLOCK_ID, self.CYCLE_PERIOD, self.AND_ID, self.NAND_ID, self.OR_ID, self.NOR_ID, self.DTYPE_ID, 
        self.XOR_ID, self.INPUT, self.INPUTS, self.I, self.DATA, self.CLK, self.SET, self.CLEAR, self.Q, self.QBAR] = self.names.lookup(self.keywords_list)

        self.current_character = ""
        self.character_number = 1


    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        
        symbol = Symbol() #create instance of the symbol class

        #identify punctuation (semicolon, colon, full stop, comma)
        if self.current_character == ';':
            symbol.type = self.SEMICOLON
            self.nextCharacter()
        
        elif self.current_character == ':':
            symbol.type = self.COLON
            self.nextCharacter()

        elif self.current_character == '.':
            symbol.type = self.DOT
            self.nextCharacter()

        elif self.current_character == ",":
            symbol.type = self.COMMA
            self.nextCharacter()

        #identify end of file
        elif self.current_character == "":
            symbol.type = self.EOF
        
        #identify comments
        elif self.current_character == "#":
            symbol.type = self.HASHTAG
            self.nextCharacter()
            #print('#')
            while self.current_character != '\n':
                #print(self.current_character) #prints comment i.e. characters after '#' until end of line
                symbol.type = self.HASHTAG
                self.nextCharacter()
        
        #identify numbers
        elif self.current_character.isdigit() == True:
            
            self.num = self.getNumber()
            symbol.type = self.NUMBER
            self.nextCharacter()

        #identify alphanumerical sequences as either keywords if in keywords list, or as a name otherwise
        elif self.current_character.isalpha() == True:
            
            self.string = self.getString()

            if self.string in self.keywords_list:
                symbol.type = self.KEYWORD
            else:
                symbol.type = self.NAME
            
            self.nextCharacter()

        return symbol


    def nextCharacter(self):
        """Looks at the next character and increases the character and line counters
        as necessary"""

        self.current_character = self.input_file.read(self.character_number)
        self.character_number += 1 
        
        return self.current_character

    
    def getString(self):
        """Return the next keyword or name string in the input file"""

        string = str(self.current_character)

        while True:
            self.current_character = self.nextCharacter()
            if self.current_character.isalnum():
                string = string + str(self.current_character)
                string = str(string)
            else:
                return string
    
    
    def getNumber(self):
        """Returns the next number in the input file"""

        number = self.current_character
        
        while self.current_character.isdigit():
            self.current_character = self.nextCharacter()
            if self.current_character.isdigit():
                number = str(number) + str(self.current_character)
            else:
                return number
