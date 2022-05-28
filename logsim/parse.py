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

        def connection_list():
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
                    self.nand()
                elif self.symbol.id == self.scanner.OR_GATE:
                    self.or_gate()
                elif self.symbol.id == self.scanner.NOR:
                    self.nor()
                elif self.symbol.id == self.scanner.DTYPE:
                    self.dtype()
                elif self.symbol.id == self.scanner.XOR:
                    self.xor()
                else:
                    self.error()
            else:
                self.error()

        #def switch(self):
            #if self.symbol.type == self.scanner.KEYWORD:



        return True
