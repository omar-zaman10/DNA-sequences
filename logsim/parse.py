"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""


class Parser:
    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """

    def __init__(self, names, devices, network, monitors, scanner):
        """Initialise constants."""

        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner

        self.error_types = ["NO_END_DEVICES", "NO_COLON", "NO_DEVICES", "NO_END_CONNECTIONS", "NO_CONNECTIONS",
                            "NO_SEMICOLON", "NO_MONITOR", "NO_IS", "NO_GATE_TYPE", "NO_GATE", "NO_SWITCH",
                            "SWITCH_INPUT", "CLOCK", "INTEGER", "NO_CYCLE", "NO_AND", "NO_INPUT_NO", "NO_INPUT",
                            "NO_NAND", "NO_OR", "NO_NOR", "NO_DTYPE", "NO_XOR", "NO_CONNECTION", "NO_INPUT_TYPE",
                            "NO_FULLSTOP", "NO_OUTPUT_TYPE", "NO_CHARACTER", "NO_CHARACTER_DIGIT", "NO_HASHTAG",
                            "NO_NEWLINE"]
        [self.NO_END_DEVICES, self.NO_COLON, self.NO_DEVICES, self.NO_END_CONNECTIONS, self.NO_CONNECTIONS,
         self.NO_SEMICOLON, self.NO_MONITOR, self.NO_IS, self.NO_GATE_TYPE, self.NO_GATE, self.NO_SWITCH,
         self.SWITCH_INPUT, self.CLOCK, self.INTEGER, self.NO_CYCLE, self.NO_AND, self.NO_INPUT_NO, self.NO_INPUT,
         self.NO_NAND, self.NO_OR, self.NO_NOR, self.NO_DTYPE, self.NO_XOR, self.NO_CONNECTION, self.NO_INPUT_TYPE,
         self.NO_FULLSTOP, self.NO_OUTPUT_TYPE, self.NO_CHARACTER, self.NO_CHARACTER_DIGIT, self.NO_HASHTAG,
         self.NO_NEWLINE] = self.names.lookup(self.error_types)

        self.error_count = 0
        self.symbol = self.scanner.get_symbol()

    def parse_network(self):
        """Parse the circuit definition file."""

        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        self.devices_list()
        self.connections_list()
        self.monitor()

        return True

    def error(self, error_type, stopping_symbol):
        self.error_count += 1

        if error_type == self.NO_END_DEVICES:
            print("Error: Expected a closing devices statement")
        elif error_type == self.NO_COLON:
            print("Error: Expected a colon")
        elif error_type == self.NO_DEVICES:
            print("Error: Expected an opening devices statement")
        elif error_type == self.NO_END_CONNECTIONS:
            print("Error: Expected a closing connections statement")
        elif error_type == self.NO_CONNECTIONS:
            print("Error: Expected an opening connections statement")
        elif error_type == self.NO_SEMICOLON:
            print("Error: Expected a semicolon")
        elif error_type == self.NO_MONITOR:
            print("Error: Expected an opening monitor statement")
        elif error_type == self.NO_IS:
            print("Error: Incorrect devices definition")
        elif error_type == self.NO_GATE_TYPE:
            print("Error: Gate defined does not exist")
        elif error_type == self.NO_GATE:
            print("Error: Gate expected")
        elif error_type == self.NO_SWITCH:
            print("Error: Switch definition expected")
        elif error_type == self.SWITCH_INPUT:
            print("Error: Initial switch input of 0 or 1 expected")
        elif error_type == self.CLOCK:
            print("Error: Clock definition expected")
        elif error_type == self.INTEGER:
            print("Error: Integer expected")
        elif error_type == self.NO_CYCLE:
            print("Error: Cycle definition expected")
        elif error_type == self.NO_AND:
            print("Error: AND definition expected")
        elif error_type == self.NO_INPUT_NO:
            print("Error: Input number between 1 and 16 expected")
        elif error_type == self.NO_INPUT:
            print("Error:Input definition expected")
        elif error_type == self.NO_NAND:
            print("Error: NAND definition expected")
        elif error_type == self.NO_OR:
            print("Error: OR definition expected")
        elif error_type == self.NO_NOR:
            print("Error: NOR definition expected")
        elif error_type == self.NO_DTYPE:
            print("Error: DTYPE definition expected")
        elif error_type == self.NO_XOR:
            print("Error: XOR definition expected")
        elif error_type == self.NO_CONNECTION:
            print("Error: Incorrect connection definition")
        elif error_type == self.NO_INPUT_TYPE:
            print("Error: Input type does not exist")
        elif error_type == self.NO_FULLSTOP:
            print("Error: Full stop expected")
        elif error_type == self.NO_OUTPUT_TYPE:
            print("Error:Output type does not exist")
        elif error_type == self.NO_CHARACTER:
            print("Error: Alphabetic character expected")
        elif error_type == self.NO_CHARACTER_DIGIT:
            print("Error: Alphanumeric character expected")
        elif error_type == self.NO_HASHTAG:
            print("Error: Hashtag expected")
        elif error_type == self.NO_NEWLINE:
            print("Error: New line expected")

        #while self.symbol.type != stopping_symbol and self.symbol.type != self.scanner.EOF:
            #self.symbol = self.scanner.get_symbol()

    def devices_list(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.DEVICES:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.COLON:
                self.symbol = self.scanner.get_symbol()
                self.device()
                while self.symbol.type != self.scanner.SEMICOLON:
                    self.device()
                    self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.ENDDEVICES:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_END_DEVICES", self.scanner.)
            else:
                self.error("NO_COLON")
        else:
            self.error("NO_DEVICES")

    def connections_list(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.CONNECTIONS:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.COLON:
                self.symbol = self.scanner.get_symbol()
                self.connection()
                while self.symbol.type != self.scanner.KEYWORD:
                    self.symbol = self.scanner.get_symbol()
                    self.connection()
                if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.ENDCONNECTIONS:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_END_CONNECTIONS")
            else:
                self.error("NO_COLON")
        else:
            self.error("NO_CONNECTIONS")

    def monitor(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.MONITOR:
            self.symbol = self.scanner.get_symbol()
            self.output()
            while (self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.AND) or \
                    (self.symbol.type == self.scanner.COMMA):
                self.symbol = self.scanner.get_symbol()
                self.output()
            if self.symbol.type == self.scanner.SEMICOLON:
                self.symbol = self.scanner.get_symbol()
            else:
                self.error("NO_SEMICOLON")
        else:
            self.error("NO_MONITOR")

    def device(self):
        self.name()
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.IS:
            self.symbol = self.scanner.get_symbol()
            self.gate()
            if self.symbol.type == self.scanner.SEMICOLON:
                self.symbol = self.scanner.get_symbol()
            else:
                self.error("NO_SEMICOLON")
        else:
            self.error("NO_IS")

    def gate(self):
        if self.symbol.type == self.scanner.KEYWORD:
            if self.symbol.id == self.scanner.SWITCH:
                self.switch()
            elif self.symbol.id == self.scanner.CLOCK:
                self.clock()
            elif self.symbol.id == self.scanner.AND_GATE:
                self.and_gate()
            elif self.symbol.id == self.scanner.NAND:
                self.nand_gate()
            elif self.symbol.id == self.scanner.OR_GATE:
                self.or_gate()
            elif self.symbol.id == self.scanner.NOR:
                self.nor_gate()
            elif self.symbol.id == self.scanner.DTYPE:
                self.dtype()
            elif self.symbol.id == self.scanner.XOR:
                self.xor()
            else:
                self.error("NO_GATE_TYPE")
        else:
            self.error("NO_GATE")

    def switch(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.SWITCH:
            self.symbol = self.scanner.get_symbol()
            binary = self.initial_input()
            if self.symbol.type == self.scanner.INTEGER and binary is True:
                self.symbol = self.scanner.get_symbol()
            else:
                self.error("SWITCH_INPUT")
        else:
            self.error("NO_SWITCH")

    def clock(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.CLOCK:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.INTEGER:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.CYCLE:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_CYCLE")
            else:
                self.error("NO_INTEGER")
        else:
            self.error("NO_CLOCK")

    def and_gate(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.AND_GATE:
            self.symbol = self.scanner.get_symbol()
            under_16 = self.number_inputs()
            if self.symbol.type == self.scanner.INTEGER and under_16 is True:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.KEYWORD and (self.symbol.id == self.scanner.INPUT or
                                                                 self.symbol.id == self.scanner.INPUTS):
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_INPUT")
            else:
                self.error("NO_INPUT_NO")
        else:
            self.error("NO_AND")

    def nand_gate(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.NAND:
            self.symbol = self.scanner.get_symbol()
            under_16 = self.number_inputs()
            if self.symbol.type == self.scanner.INTEGER and under_16 is True:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.KEYWORD and (self.symbol.id == self.scanner.INPUT or
                                                                 self.symbol.id == self.scanner.INPUTS):
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_INPUT")
            else:
                self.error("NO_INPUT_NO")
        else:
            self.error("NO_NAND")

    def or_gate(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.OR_GATE:
            self.symbol = self.scanner.get_symbol()
            under_16 = self.number_inputs()
            if self.symbol.type == self.scanner.INTEGER and under_16 is True:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.KEYWORD and (self.symbol.id == self.scanner.INPUT or
                                                                 self.symbol.id == self.scanner.INPUTS):
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_INPUT")
            else:
                self.error("NO_INPUT_NO")
        else:
            self.error("NO_OR")

    def nor_gate(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.NOR:
            self.symbol = self.scanner.get_symbol()
            under_16 = self.number_inputs()
            if self.symbol.type == self.scanner.INTEGER and under_16 is True:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.KEYWORD and (self.symbol.id == self.scanner.INPUT or
                                                                 self.symbol.id == self.scanner.INPUTS):
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_INPUT")
            else:
                self.error("NO_INPUT_NO")
        else:
            self.error("NO_NOR")

    def dtype(self):
        if self.symbol.type == self.scanner.KEYWORD and self.scanner.id == self.scanner.DTYPE:
            self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_DTYPE")

    def xor(self):
        if self.symbol.type == self.scanner.KEYWORD and self.scanner.id == self.scanner.XOR:
            self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_XOR")

    def connection(self):
        self.output()
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.TO:
            self.symbol = self.scanner.get_symbol()
            self.input()
        else:
            self.error("NO_CONNECTION")

    def input(self):
        self.name()
        if self.symbol.type == self.scanner.FULLSTOP:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.I:
                self.boolean_input()
            elif self.symbol.type == self.scanner.KEYWORD and (self.symbol.id == self.scanner.DATA or
                                                               self.symbol.id == self.scanner.CLK or
                                                               self.symbol.id == self.scanner.SET or
                                                               self.symbol.id == self.scanner.CLEAR):
                self.dtype_input()
            else:
                self.error("NO_INPUT_TYPE")
        else:
            self.error("NO_FULLSTOP")

    def output(self):
        self.name()
        if self.symbol.type == self.scanner.FULLSTOP:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD:
                if self.symbol.id == self.scanner.Q or self.symbol.id == self.scanner.QBAR:
                    self.dtype_output()
                elif self.symbol.id == self.scanner.CLOCK:
                    self.clock_output()
                else:
                    self.error("NO_OUTPUT_TYPE")
            else:
                self.error("NO_OUTPUT_TYPE")
        else:
            self.symbol = self.scanner.get_symbol()

    def boolean_input(self):
        self.symbol = self.scanner.get_symbol()
        under_16 = self.number_inputs()
        if under_16 is True:
            self.symbol.self.scanner.get_symbol()
        else:
            self.error("NO_INPUT_NO")

    def dtype_input(self):
        self.symbol = self.scanner.get_symbol()

    def dtype_output(self):
        self.symbol = self.scanner.get_symbol()

    def clock_output(self):
        self.symbol = self.scanner.get_symbol()

    def initial_input(self):
        if self.symbol.type == self.scanner.INTEGER and (self.symbol.id == self.scanner.ZERO or
                                                         self.symbol.id == self.scanner.ONE):
            return True
        else:
            return False

    def number_inputs(self):
        if self.symbol.type == self.scanner.INTEGER:
            if self.symbol.id == self.scanner.ONE or self.symbol.id == self.scanner.TWO \
                    or self.symbol.id == self.scanner.THREE or self.symbol.id == self.scanner.FOUR \
                    or self.symbol.id == self.scanner.FIVE or self.symbol.id == self.scanner.SIX \
                    or self.symbol.id == self.scanner.SEVEN or self.symbol.id == self.scanner.EIGHT \
                    or self.symbol.id == self.scanner.NINE or self.symbol.id == self.scanner.TEN \
                    or self.symbol.id == self.scanner.ELEVEN or self.symbol.id == self.scanner.TWELVE \
                    or self.symbol.id == self.scanner.THIRTEEN or self.symbol.id == self.scanner.FOURTEEN \
                    or self.symbol.id == self.scanner.FIFTEEN or self.symbol.id == self.scanner.SIXTEEN:
                return True
            else:
                return False

    def name(self):
        if self.symbol.type == self.scanner.CHARACTER:
            self.symbol = self.scanner.get_symbol()
            while self.symbol.type == self.scanner.CHARACTER or self.symbol.type == self.scanner.INTEGER:
                self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_CHARACTER")

    def closed_comment(self):
        if self.symbol.type == self.scanner.HASHTAG:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.CHARACTER or self.symbol.type == self.scanner.INTEGER:
                self.symbol = self.scanner.get_symbol()
                while self.symbol.type == self.scanner.CHARACTER or self.symbol.type == self.scanner.INTEGER:
                    self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.HASHTAG:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_HASHTAG")
            else:
                self.error("NO_CHARACTER_DIGIT")
        else:
            self.error("NO_HASHTAG")

    def open_comment(self):
        if self.symbol.type == self.scanner.HASHTAG:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.CHARACTER or self.symbol.type == self.scanner.INTEGER:
                self.symbol = self.scanner.get_symbol()
                while self.symbol.type == self.scanner.CHARACTER or self.symbol.type == self.scanner.INTEGER:
                    self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.NEWLINE:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_NEWLINE")
            else:
                self.error("NO_CHARACTER_DIGIT")
        else:
            self.error("NO_HASHTAG")
