"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
import names
import dataclasses
import pdb
import sys
import parse
import os 


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
        self.line = None
        self.position = None


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

    def __init__(self, path, names, test_string=False):
        """Open specified file and initialise reserved words and IDs."""
        if test_string:
            if os.path.exists("test_file.txt"):
                os.remove("test_file.txt")
            f = open("test_file.txt", "a")
            f.write(path)
            f.close()
            self.input_file = open("test_file.txt", "r")
        else:
            try:
                self.input_file = open(path, 'r')
            except FileNotFoundError:
                raise FileNotFoundError(
                    "Error: File doesn't exist in current directory"
                )

        self.names = names

        self.symbol_type_list = [self.PUNCTUATION, self.KEYWORD,
                                 self.NAME, self.INTEGER, self.INT16,
                                 self.EOF, self.SPECIAL] = range(7)

        self.punctuation_list = [";", ":", ".", ",", "#", "\n", ""]

        [self.SEMICOLON, self.COLON, self.FULLSTOP,
         self.COMMA, self.HASHTAG, self.NEWLINE, self.EOF_ID] = \
            self.names.lookup(self.punctuation_list)

        self.numbers_list = ['0', '1', '2', '3', '4', '5', '6',
                             '7', '8', '9', '10', '11', '12',
                             '13', '14', '15', '16']

        [self.ZERO, self.ONE, self.TWO, self.THREE, self.FOUR,
         self.FIVE, self.SIX, self.SEVEN, self.EIGHT, self.NINE,
         self.TEN, self.ELEVEN, self.TWELVE, self.THIRTEEN,
         self.FOURTEEN, self.FIFTEEN, self.SIXTEEN] = \
            self.names.lookup(self.numbers_list)

        self.keywords_list = ["DEVICES", "CONNECTIONS", "MONITOR",
                              "END", "to", "is", "SWITCH", "with",
                              "state", "and", "CLOCK", "cycle",
                              "period", "AND", "NAND", "OR", "NOR",
                              "DTYPE", "XOR", "NOT", "input", "inputs",
                              "I", "DATA", "CLK", "SET", "CLEAR", "Q", "QBAR"]

        [self.DEVICES_ID, self.CONNECTIONS_ID, self.MONITOR_ID,
         self.END_ID, self.TO, self.IS, self.SWITCH_ID,
         self.WITH, self.STATE, self.AND, self.CLOCK_ID, self.CYCLE,
         self.PERIOD, self.AND_ID, self.NAND_ID, self.OR_ID,
         self.NOR_ID, self.DTYPE_ID, self.XOR_ID, self.NOT_ID, self.INPUT,
         self.INPUTS, self.I, self.DATA, self.CLK, self.SET,
         self.CLEAR, self.Q, self.QBAR] = \
            self.names.lookup(self.keywords_list)


        self.current_character = " "
        self.character_number = 0
        self.line_number = 0
        self.symbol_number = 0
        self.scanner_error_count = 0
        self.string = ""
        self.address = path

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol.
        Symbols to be passed requested by the parser
        """
        symbol = Symbol()  # create instance of the symbol class
        self.skip_spaces()  # current character is now now whitespace

        # check for punctuation (semicolon, colon, full stop, comma)
        if self.current_character == ';':
            symbol.type = self.PUNCTUATION
            symbol.id = self.names.query(self.current_character)
            self.advance()
            # print(";")

        elif self.current_character == ':':
            symbol.type = self.PUNCTUATION
            symbol.id = self.names.query(self.current_character)
            self.advance()
            # print(":")

        elif self.current_character == '.':
            symbol.type = self.PUNCTUATION
            symbol.id = self.names.query(self.current_character)
            self.advance()
            # print(".")

        elif self.current_character == ",":
            symbol.type = self.PUNCTUATION
            symbol.id = self.names.query(self.current_character)
            self.advance()
            # print(",")

        # check for new line
        elif self.current_character == '\n':
            symbol.type = self.PUNCTUATION
            symbol.id = self.names.query(self.current_character)
            self.advance()

        # check for comments
        elif self.current_character == "#":
            symbol.type = self.PUNCTUATION
            symbol.id = self.names.query(self.current_character)
            # print("#")
            self.advance()
            while self.current_character != '\n':
                # print(self.current_character)
                symbol.type = self.PUNCTUATION
                self.advance()

        # check for end of line
        elif self.current_character == "":
            symbol.type = self.EOF
            symbol.id = self.EOF_ID
            self.string = ""

        # check for integers, in particular 1-16 for gate input allocation
        elif self.current_character.isdigit():
            number = self.get_number()
            if type(number) == int:
                if 0 <= number <= 16:
                    symbol.type = self.INT16
                    if number == 0:
                        symbol.id = self.ZERO
                    elif number == 1:
                        symbol.id = self.ONE
                    elif number == 2:
                        symbol.id = self.TWO
                    elif number == 3:
                        symbol.id = self.THREE
                    elif number == 4:
                        symbol.id = self.FOUR
                    elif number == 5:
                        symbol.id = self.FIVE
                    elif number == 6:
                        symbol.id = self.SIX
                    elif number == 7:
                        symbol.id = self.SEVEN
                    elif number == 8:
                        symbol.id = self.EIGHT
                    elif number == 9:
                        symbol.id = self.NINE
                    elif number == 10:
                        symbol.id = self.TEN
                    elif number == 11:
                        symbol.id = self.ELEVEN
                    elif number == 12:
                        symbol.id = self.TWELVE
                    elif number == 13:
                        symbol.id = self.THIRTEEN
                    elif number == 14:
                        symbol.id = self.FOURTEEN
                    elif number == 15:
                        symbol.id = self.FIFTEEN
                    elif number == 16:
                        symbol.id = self.SIXTEEN
                else:
                    symbol.type = self.INTEGER

                    symbol.id = number
            elif type(number) == float:
                self.error_location()
                
                raise SyntaxError("Invalid number: only integers allowed")
            self.advance()

        # identify alphanumerical sequences as either keywords if in keywords
        # list, or as a name otherwise
        elif self.current_character.isalpha():
            self.get_name()

            if self.string in self.keywords_list:
                symbol.type = self.KEYWORD
                symbol.id = self.names.query(self.string)
            else:
                symbol.type = self.NAME
                symbol.id = self.names.lookup(self.string)
                symbol.id = symbol.id[0]
            # print(self.string)

        else:
            symbol.type = self.SPECIAL
            symbol.id = self.names.lookup(self.string)
            # self.error_location()
            # raise SyntaxError("Error: invalid symbol")

        # try:
        #     print(self.names.get_name_string(symbol.id))
        # except Exception:
        #     print(self.string)
        
        symbol.position = self.character_number
        symbol.line = self.line_number
        self.symbol_number += 1

        return symbol

    def advance(self):
        """Look at the next character.

        Increase the character and line counters as necessary
        """
        self.current_character = self.input_file.read(1)
        self.character_number += 1

        if self.current_character == '\n':
            self.line_number += 1
            self.character_number = self.symbol_number = 0

    def skip_spaces(self):
        """Skip any whitespace to return the next non-space character."""
        while self.current_character.isspace():
            self.advance()

    def get_name(self):
        """Return the next keyword or name string in the input file."""
        name = ""

        while self.current_character.isalnum():
            name = name + self.current_character
            self.advance()
        self.string = name

    def get_number(self):
        """Return the next number in the input file."""
        number = ""
        current_position = self.input_file.tell()

        while self.current_character.isdigit():
            number = number + self.current_character
            current_position = self.input_file.tell()
            self.nextCharacter()

        self.input_file.seek(current_position)
        return int(number)

    def error_location(self):
        """For basic error handling.

        To be called by the parser and in some cases within the scanner
        in case of an error. Returns the erroneous line and a pointer
        in the following line pointing to the erroneous character
        """
        current_position = self.input_file.tell()
        pointer = ""
        for i in range(self.character_number-2):
            pointer += " "
        pointer += "^"

        f = open(self.address, 'r')
        error_message = "Line {line}:".format(line=str(self.line_number+1)), f.readlines()[self.line_number], pointer
        
        self.input_file.seek(current_position)
                
        self.scanner_error_count += 1

        return error_message
