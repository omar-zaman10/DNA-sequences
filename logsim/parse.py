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

    def parse_network(self):
        """Parse the circuit definition file."""

        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        return True

    def devices_list(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.DEVICES:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.COLON:
                self.symbol = self.scanner.get_symbol()
                self.device()
                while self.symbol.type != self.scanner.SEMICOLON:
                    self.symbol = self.scanner.get_symbol()
                    self.device()
                if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.ENDDEVICES:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def connection_list(self):
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
                    self.error()
            else:
                self.error()
        else:
            self.error()

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
                self.error()

    def device(self):
        self.name()
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.IS:
            self.symbol = self.scanner.get_symbol()
            self.gate()
            if self.symbol.type == self.scanner.SEMICOLON:
                self.symbol = self.scanner.get_symbol()
            else:
                self.error()
        else:
            self.error()

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
                self.error()
        else:
            self.error()

    def switch(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.SWITCH:
            self.symbol = self.scanner.get_symbol()
            binary = self.initial_input()
            if self.symbol.type == self.scanner.INTEGER and binary is True:
                self.symbol = self.scanner.get_symbol()
            else:
                self.error()
        else:
            self.error()

    def clock(self):
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.CLOCK:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.INTEGER:  # integers or string idk
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.CYCLE:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

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
                    self.error()
            else:
                self.error()
        else:
            self.error()

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
                    self.error()
            else:
                self.error()
        else:
            self.error()

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
                    self.error()
            else:
                self.error()
        else:
            self.error()

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
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def dtype(self):
        if self.symbol.type == self.scanner.KEYWORD and self.scanner.id == self.scanner.DTYPE:
            self.symbol = self.scanner.get_symbol()
        else:
            self.error()

    def xor(self):
        if self.symbol.type == self.scanner.KEYWORD and self.scanner.id == self.scanner.XOR:
            self.symbol = self.scanner.get_symbol()
        else:
            self.error()

    def connection(self):
        self.output()
        if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.TO:
            self.symbol = self.scanner.get_symbol()
            self.input()
        else:
            self.error()

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
                self.error()
        else:
            self.error()

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
                    self.error()
            else:
                self.error()
        else:
            self.symbol = self.scanner.get_symbol()

    def boolean_input(self):
        self.symbol = self.scanner.get_symbol()
        under_16 = self.number_inputs()
        if under_16 is True:
            self.symbol.self.scanner.get_symbol()
        else:
            self.error()

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
            self.error()

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
                    self.error()
            else:
                self.error()
        else:
            self.error()

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
                    self.error()
            else:
                self.error()
        else:
            self.error()


