"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""
import sys
import pdb

# class Error:
# def __init__(self):
# """Initialise symbol properties."""

# self.type = None
# self.id = None
import pytest


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

        self.symbol = self.scanner.get_symbol()
        self.name_string = ""
        self.device_id = 0
        self.output_id = 0
        self.input_id = 0
        self.input_device_id = 0
        self.output_device_id = 0
        self.devices_symbol_list = []
        self.input_added = False
        self.output_added = False

        self.error_count = 0
        self.in_stopping_symbol = False
        self.device_error = False
        self.connection_error = False
        self.monitor_error = False

        self.monitoring = False

        self.devices_instance = 0
        self.connections_instance = 0
        self.monitoring_instance = 0

    def parse_network(self):
        """Parse the circuit definition file."""

        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        # circuit = devices, connections, monitor

        if self.symbol.type == self.scanner.EOF:
            print("Error: No file content found")
            return False

        while self.symbol.type != self.scanner.EOF:
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.DEVICES_ID:
                self.device_error = False
                self.devices_list()
                self.devices_instance += 1
                if self.devices_instance > 1:
                    break
            elif (self.symbol.type == self.scanner.KEYWORD
                  and self.symbol.id == self.scanner.CONNECTIONS_ID) \
                    and self.devices_instance == 1:
                self.connection_error = False
                self.connections_list()
                self.connections_instance += 1
                if self.connections_instance > 1:
                    break
            elif (self.symbol.type == self.scanner.KEYWORD
                  and self.symbol.id == self.scanner.MONITOR_ID) \
                    and (self.connections_instance == 1
                         and self.devices_instance == 1):
                self.monitoring = True
                self.monitor_error = False
                self.monitor()
                self.monitoring_instance += 1
                if self.monitoring_instance > 1:
                    break
            elif self.symbol.type == self.scanner.PUNCTUATION \
                    and self.symbol.id == self.scanner.HASHTAG:
                self.open_comment()
            else:
                break

        if self.devices_instance != 1 or \
                self.connections_instance != 1 or \
                self.monitoring_instance != 1:
            print("Error: Not all sections present")
            self.error_count += 1

        if self.error_count == 0:
            return True
        else:
            print(self.error_count)
            return False

    def error(self, error_type, stopping_symbol):
        self.error_count += 1

        # if self.error_type.isalpha():
        # self.string = self.getName()

        # if self.string in self.error_types:
        # error.id = self.names.query(self.string)
        # else:
        # print("Error message failed")
        # sys.exit()

        if error_type == "NO_COMMA":
            print("Error: Expected a comma")
        elif error_type == "NO_COLON":
            print("Error: Expected a colon")
        elif error_type == "NO_DEVICES":
            print("Error: Expected an opening devices statement")
        elif error_type == "NO_CONNECTIONS":
            print("Error: Expected an opening connections statement")
        elif error_type == "NO_SEMICOLON":
            print("Error: Expected a semicolon")
        elif error_type == "NO_MONITOR":
            print("Error: Expected an opening monitor statement")
        elif error_type == "NO_IS":
            print("Error: Incorrect devices definition")
        elif error_type == "NO_GATE_TYPE":
            print("Error: Gate defined does not exist")
        elif error_type == "NO_GATE":
            print("Error: Gate expected")
        elif error_type == "NO_SWITCH":
            print("Error: Switch definition expected")
        elif error_type == "NO_CLOCK":
            print("Error: Clock definition expected")
        elif error_type == "SWITCH_INPUT":
            print("Error: Initial switch input of 0 or 1 expected")
        elif error_type == "CLOCK":
            print("Error: Clock definition expected")
        elif error_type == "NO_INTEGER":
            print("Error: Integer expected")
        elif error_type == "NO_CYCLE":
            print("Error: Cycle definition expected")
        elif error_type == "NO_AND":
            print("Error: AND definition expected")
        elif error_type == "NO_INPUT_NO":
            print("Error: Input number between 1 and 16 expected")
        elif error_type == "NO_INPUT":
            print("Error: Input definition expected")
        elif error_type == "NO_NAND":
            print("Error: NAND definition expected")
        elif error_type == "NO_OR":
            print("Error: OR definition expected")
        elif error_type == "NO_NOR":
            print("Error: NOR definition expected")
        elif error_type == "NO_DTYPE":
            print("Error: DTYPE definition expected")
        elif error_type == "NO_XOR":
            print("Error: XOR definition expected")
        elif error_type == "NO_CONNECTION":
            print("Error: Incorrect connection definition")
        elif error_type == "NO_INPUT_TYPE":
            print("Error: Input type does not exist")
        elif error_type == "NO_OUTPUT_TYPE":
            print("Error:Output type does not exist")
        elif error_type == "NO_CHARACTER":
            print("Error: Alphabetic character expected")
        elif error_type == "NO_CHARACTER_DIGIT":
            print("Error: Alphanumeric character expected")
        elif error_type == "NO_HASHTAG":
            print("Error: Hashtag expected")
        elif error_type == "NO_MONITOR_DEF":
            print("Error: Incorrect monitor definition")
        elif error_type == "NO_NEWLINE":
            print("Error: New line expected")

        # error_message = self.scanner.errorPosition()
        # print(error_message[0], "\n", error_message[1])

        print(self.names.get_name_string(self.symbol.id))

        stopping_symbols = []
        go_to_next = []

        for stop in stopping_symbol:
            stopping_symbols.append(stop[0])
            go_to_next.append(stop[1])

        if self.symbol.id in stopping_symbols:
            self.in_stopping_symbol = True
        else:
            self.in_stopping_symbol = False

        while not self.in_stopping_symbol and \
                self.symbol.type != self.scanner.EOF:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.id in stopping_symbols:
                symbol_index = stopping_symbols.index(self.symbol.id)
                print("Returned to parsing", self.names.get_name_string(self.symbol.id))
                if go_to_next[symbol_index]:
                    self.symbol = self.scanner.get_symbol()

                self.in_stopping_symbol = True

    def devices_list(self):
        """devices= "DEVICES", ":", device, ";" ,
        {device, ";"}, "END DEVICES";"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.DEVICES_ID:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.PUNCTUATION \
                    and self.symbol.id == self.scanner.COLON:
                self.symbol = self.scanner.get_symbol()
                self.device()
                while self.symbol.type != self.scanner.PUNCTUATION \
                        and self.symbol.id != self.scanner.SEMICOLON:
                    if self.device_error is False:
                        if (self.symbol.type == self.scanner.KEYWORD and
                            (self.symbol.id == self.scanner.CONNECTIONS_ID
                             or self.symbol.id == self.scanner.MONITOR_ID)) \
                                or self.symbol.type == self.scanner.EOF:
                            self.error("NO_SEMICOLON", [(self.scanner.CONNECTIONS_ID, False),
                                                        (self.scanner.MONITOR_ID, False)])
                            break
                        else:
                            self.device()
                    else:
                        break
                if self.symbol.id == self.scanner.SEMICOLON:
                    self.symbol = self.scanner.get_symbol()
            else:
                self.error("NO_COLON", [(self.scanner.CONNECTIONS_ID, False),
                                        (self.scanner.MONITOR_ID, False)])
        else:
            self.error("NO_DEVICES", [(self.scanner.CONNECTIONS_ID, False),
                                      (self.scanner.MONITOR_ID, False)])

    # @pytest.fixture
    # def test_devices_list(self):
    #     self.devices_list()
    #     assert self.symbol.type == self.scanner.KEYWORD or \
    #            self.in_stopping_symbol is True

    def connections_list(self):
        """connections= "CONNECTIONS", ":", connection, ";",
        {connection, ";"}, "END CONNECTIONS";"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.CONNECTIONS_ID:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.PUNCTUATION \
                    and self.symbol.id == self.scanner.COLON:
                self.symbol = self.scanner.get_symbol()
                self.connection()
                if self.connection_error is False:
                    if self.symbol.id == self.scanner.SEMICOLON:
                        self.symbol = self.scanner.get_symbol()
                    while self.symbol.type != self.scanner.PUNCTUATION \
                            and self.symbol.id != self.scanner.SEMICOLON:
                        if self.connection_error is False:
                            if (self.symbol.type == self.scanner.KEYWORD
                                and self.symbol.id == self.scanner.MONITOR_ID) \
                                    or self.symbol.type == self.scanner.EOF:
                                self.error("NO_SEMICOLON", [(self.scanner.CONNECTIONS_ID, False),
                                                            (self.scanner.MONITOR_ID, False)])
                                break
                            else:
                                self.connection()
                        else:
                            break
                    if self.symbol.id == self.scanner.SEMICOLON:
                        self.symbol = self.scanner.get_symbol()
            else:
                self.error("NO_COLON", [(self.scanner.MONITOR_ID, False)])
        else:
            self.error("NO_CONNECTIONS", [(self.scanner.MONITOR_ID, False)])

    # @pytest.fixture
    # def test_connections_list(self):
    #     self.connections_list()
    #     assert self.symbol.type == self.scanner.KEYWORD or \
    #            self.in_stopping_symbol is True

    def monitor(self):
        """monitor = "MONITOR", output, {("and"| ",") output}, ";"""""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.MONITOR_ID:
            self.symbol = self.scanner.get_symbol()
            self.output()
            if self.monitor_error is False:
                while (self.symbol.type == self.scanner.KEYWORD
                       and self.symbol.id == self.scanner.AND) or \
                        (self.symbol.type == self.scanner.COMMA):
                    self.symbol = self.scanner.get_symbol()
                    if self.monitor_error is False:
                        self.output()
                        if self.symbol.type == self.scanner.EOF:
                            break
                    else:
                        break
                if self.symbol.type == self.scanner.PUNCTUATION \
                        and self.symbol.id == self.scanner.SEMICOLON:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.error("NO_SEMICOLON", [(self.scanner.EOF, False)])
        else:
            self.error("NO_MONITOR", [(self.scanner.SEMICOLON, True)])

    # @pytest.fixture
    # def test_monitor(self):
    #     self.monitor()
    #     assert self.symbol.type == self.scanner.EOF or \
    #            self.in_stopping_symbol is True

    def device(self):
        """device = name, "is", gate, ";";"""
        self.device_id = self.name()
        if self.device_error is False:
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.IS:
                self.symbol = self.scanner.get_symbol()
                self.gate()
                if self.device_error is False:
                    if (self.symbol.type == self.scanner.PUNCTUATION
                            and self.symbol.id == self.scanner.COMMA):
                        self.symbol = self.scanner.get_symbol()
                    elif (self.symbol.type != self.scanner.PUNCTUATION
                          and self.symbol.id != self.scanner.SEMICOLON) \
                            and self.symbol.type != self.scanner.KEYWORD \
                            and self.symbol.type != self.scanner.EOF:
                        self.error("NO_COMMA", [(self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        self.device_error = True
            else:
                self.error("NO_IS", [(self.scanner.CONNECTIONS_ID, False),
                                     (self.scanner.MONITOR_ID, False)])
                self.device_error = True

    # @pytest.fixture
    # def test_device(self):
    #     assert type(self.device_id) == int \
    #            and (self.symbol.type == self.scanner.NAME
    #                 or self.symbol.type == self.scanner.KEYWORD)

    def name(self):
        """name = character, {character|digit};"""
        if self.symbol.type == self.scanner.NAME:
            name_id = self.get_id(self.symbol)
            self.symbol = self.scanner.get_symbol()
            return name_id
        else:
            self.error("NO_CHARACTER", [(self.scanner.CONNECTIONS_ID, False),
                                        (self.scanner.MONITOR_ID, False)])
            self.device_error = True
            self.connection_error = True
            self.monitor_error = True

    def connection(self):
        """connection = output, "to", input;"""
        self.output()
        if self.connection_error is False:
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.TO:
                self.symbol = self.scanner.get_symbol()
                self.input()
                if self.connection_error is False:
                    # error_type = self.network.make_connection(self.output_device_id,
                    #                                           self.output_id,
                    #                                           self.input_device_id,
                    #                                           self.input_id)
                    if self.symbol.type == self.scanner.PUNCTUATION \
                            and self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                    elif (self.symbol.type != self.scanner.PUNCTUATION
                          and self.symbol.id != self.scanner.SEMICOLON) \
                            and self.symbol.type != self.scanner.KEYWORD \
                            and self.symbol.type != self.scanner.EOF:
                        self.error("NO_COMMA", [(self.scanner.MONITOR_ID, False)])
                        self.connection_error = True
            else:
                self.error("NO_CONNECTION", [(self.scanner.MONITOR_ID, False)])
                self.connection_error = True

    def input(self):
        """input = name, ".", (boolean_input | dtype_input);"""
        self.input_device_id = self.name()
        if self.connection_error is False:
            if self.symbol.type == self.scanner.PUNCTUATION \
                    and self.symbol.id == self.scanner.FULLSTOP:
                self.symbol = self.scanner.get_symbol()
                characters = [c for c in self.scanner.string]
                if self.symbol.type == self.scanner.NAME \
                        and characters[0] == "I":
                    self.boolean_input()
                elif self.symbol.type == self.scanner.KEYWORD \
                        and (self.symbol.id == self.scanner.DATA or
                             self.symbol.id == self.scanner.CLK or
                             self.symbol.id == self.scanner.SET or
                             self.symbol.id == self.scanner.CLEAR):
                    self.dtype_input()
                else:
                    self.error("NO_INPUT_TYPE", [(self.scanner.CONNECTIONS_ID, False),
                                                 (self.scanner.MONITOR_ID, False)])
                    self.connection_error = True
            else:
                self.error("NO_INPUT_TYPE", [(self.scanner.CONNECTIONS_ID, False),
                                             (self.scanner.MONITOR_ID, False)])
                self.connection_error = True

    # @pytest.fixture
    # def test_input(self):
    #     assert type(self.input_device_id) == int

    def output(self):
        """output = name, [".", (dtype_output | clock_output)];"""
        self.output_device_id = self.name()
        if self.device_error is False or \
                self.connection_error is False or \
                self.monitor_error is False:
            if self.symbol.type == self.scanner.PUNCTUATION \
                    and self.symbol.id == self.scanner.FULLSTOP:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == \
                        self.scanner.KEYWORD:
                    if self.symbol.id == self.scanner.Q \
                            or self.symbol.id == \
                            self.scanner.QBAR:
                        self.dtype_output()
                    else:
                        self.error("NO_OUTPUT_TYPE", [(self.scanner.CONNECTIONS_ID, False),
                                                      (self.scanner.MONITOR_ID, False)])
                        self.connection_error = True
                        self.monitor_error = True
                else:
                    self.error("NO_OUTPUT_TYPE", [(self.scanner.CONNECTIONS_ID,
                                                   False), (self.scanner.MONITOR_ID, False)])
                    self.connection_error = True
                    self.monitor_error = True

            elif self.symbol.id != self.scanner.TO and \
                    self.symbol.type != self.scanner.EOF and \
                    self.monitoring is False:
                if self.symbol.type == self.scanner.NAME:
                    self.error("NO_CONNECTION", [(self.scanner.MONITOR_ID, False)])
                    self.connection_error = True
                else:
                    self.error("NO_OUTPUT_TYPE", [(self.scanner.CONNECTIONS_ID, False),
                                                  (self.scanner.MONITOR_ID, False)])
                    self.connection_error = True
                    self.monitor_error = True
            elif self.symbol.id != self.scanner.AND and \
                    self.symbol.id != self.scanner.COMMA and \
                    self.symbol.type != self.scanner.EOF and \
                    self.monitoring is True:
                self.error("NO_MONITOR_DEF", [(self.scanner.EOF, False)])
                self.monitor_error = True
            else:
                self.output_id = self.get_id(self.symbol)
                self.output_added = self.devices.add_input(self.input_device_id,
                                                           self.output_id)

    # @pytest.fixture
    # def test_name(self):
    #     name_id = self.name()
    #     assert type(name_id) == int

    def gate(self):
        """gate = switch | clock | and |
        nand | or | nor | dtype | xor;"""
        if self.symbol.type == self.scanner.KEYWORD:
            if self.symbol.id == self.scanner.SWITCH_ID:
                self.switch()
                if self.device_error is False:
                    self.devices.add_device(self.device_id, "SWITCH")
            elif self.symbol.id == self.scanner.CLOCK_ID:
                self.clock()
                if self.device_error is False:
                    self.devices.add_device(self.device_id, "CLOCK")
            elif self.symbol.id == self.scanner.AND_ID:
                self.and_gate()
                if self.device_error is False:
                    self.devices.add_device(self.device_id, "AND")
            elif self.symbol.id == self.scanner.NAND_ID:
                self.nand_gate()
                if self.device_error is False:
                    self.devices.add_device(self.device_id, "NAND")
            elif self.symbol.id == self.scanner.OR_ID:
                self.or_gate()
                if self.device_error is False:
                    self.devices.add_device(self.device_id, "OR")
            elif self.symbol.id == self.scanner.NOR_ID:
                self.nor_gate()
                if self.device_error is False:
                    self.devices.add_device(self.device_id, "NOR")
            elif self.symbol.id == self.scanner.DTYPE_ID:
                self.dtype()
                if self.device_error is False:
                    self.devices.add_device(self.device_id, "DTYPE")
            elif self.symbol.id == self.scanner.XOR_ID:
                self.xor()
                if self.device_error is False:
                    self.devices.add_device(self.device_id, "XOR")
            else:
                self.error("NO_GATE_TYPE", [(self.scanner.CONNECTIONS_ID, False),
                                            (self.scanner.MONITOR_ID, False)])
                self.device_error = True
        else:
            self.error("NO_GATE", [(self.scanner.CONNECTIONS_ID, False),
                                   (self.scanner.MONITOR_ID, False)])
            self.device_error = True

    def switch(self):  # FIX ERRORS
        """switch = "SWITCH with state", inital_switch;"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.SWITCH_ID:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.WITH:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.KEYWORD \
                        and self.symbol.id == self.scanner.STATE:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.INT16 \
                            and (self.symbol.id == self.scanner.ZERO
                                 or self.symbol.id == self.scanner.ONE):
                        self.symbol = self.scanner.get_symbol()

                    else:
                        self.error("SWITCH_INPUT", [(self.scanner.CONNECTIONS_ID, False),
                                                    (self.scanner.MONITOR_ID, False)])
                        self.device_error = True
                else:
                    self.error("NO_SWITCH", [(self.scanner.CONNECTIONS_ID, False),
                                             (self.scanner.MONITOR_ID, False)])
                    self.device_error = True
            else:
                self.error("NO_SWITCH", [(self.scanner.CONNECTIONS_ID, False),
                                         (self.scanner.MONITOR_ID, False)])
                self.device_error = True
        else:
            self.error("NO_SWITCH", [(self.scanner.CONNECTIONS_ID, False),
                                     (self.scanner.MONITOR_ID, False)])
            self.device_error = True

    def clock(self):
        """clock = "CLOCK with", digit, "cycle period";"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.CLOCK_ID:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.WITH:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.INTEGER \
                        or self.symbol.type == self.scanner.INT16:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and self.symbol.id == self.scanner.CYCLE:
                        self.symbol = self.scanner.get_symbol()
                        if self.symbol.type == self.scanner.KEYWORD \
                                and self.symbol.id == self.scanner.PERIOD:
                            self.symbol = self.scanner.get_symbol()
                        else:
                            self.error("NO_CYCLE", [(self.scanner.CONNECTIONS_ID, False),
                                                    (self.scanner.MONITOR_ID, False)])
                            self.device_error = True
                    else:
                        self.error("NO_CYCLE", [(self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        self.device_error = True
                else:
                    self.error("NO_INTEGER", [(self.scanner.CONNECTIONS_ID, False),
                                              (self.scanner.MONITOR_ID, False)])
                    self.device_error = True
            else:
                self.error("NO_CLOCK", [(self.scanner.CONNECTIONS_ID, False),
                                        (self.scanner.MONITOR_ID, False)])
                self.device_error = True
        else:
            self.error("NO_CLOCK", [(self.scanner.CONNECTIONS_ID, False),
                                    (self.scanner.MONITOR_ID, False)])
            self.device_error = True

    def and_gate(self):
        """and = "AND with", number_inputs, ("input"|"inputs");"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.AND_ID:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.WITH:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.INT16 \
                        or self.symbol.type == self.scanner.ONE:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and (self.symbol.id == self.scanner.INPUT or
                                 self.symbol.id == self.scanner.INPUTS):
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.error("NO_INPUT", [(self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        self.device_error = True
                else:
                    self.error("NO_INPUT_NO", [(self.scanner.CONNECTIONS_ID, False),
                                               (self.scanner.MONITOR_ID, False)])
                    self.device_error = True
            else:
                self.error("NO_AND", [(self.scanner.CONNECTIONS_ID, False),
                                      (self.scanner.MONITOR_ID, False)])
                self.device_error = True
        else:
            self.error("NO_AND", [(self.scanner.CONNECTIONS_ID, False),
                                  (self.scanner.MONITOR_ID, False)])
            self.device_error = True

    def nand_gate(self):
        """nand = "NAND with", number_inputs, ("input"|"inputs");"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.NAND_ID:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.WITH:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.INT16 \
                        or self.symbol.type == self.scanner.ONE:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and (self.symbol.id == self.scanner.INPUT or
                                 self.symbol.id == self.scanner.INPUTS):
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.error("NO_INPUT", [(self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        self.device_error = True
                else:
                    self.error("NO_INPUT_NO", [(self.scanner.CONNECTIONS_ID, False),
                                               (self.scanner.MONITOR_ID, False)])
                    self.device_error = True
            else:
                self.error("NO_NAND", [(self.scanner.CONNECTIONS_ID, False),
                                       (self.scanner.MONITOR_ID, False)])
                self.device_error = True
        else:
            self.error("NO_NAND", [(self.scanner.CONNECTIONS_ID, False),
                                   (self.scanner.MONITOR_ID, False)])
            self.device_error = True

    def or_gate(self):
        """or = "OR with", number_inputs, ("input"|"inputs");"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.OR_ID:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.WITH:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.INT16 \
                        or self.symbol.type == self.scanner.ONE:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and (self.symbol.id == self.scanner.INPUT or
                                 self.symbol.id == self.scanner.INPUTS):
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.error("NO_INPUT", [(self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        self.device_error = True
                else:
                    self.error("NO_INPUT_NO", [(self.scanner.CONNECTIONS_ID, False),
                                               (self.scanner.MONITOR_ID, False)])
                    self.device_error = True
            else:
                self.error("NO_OR", [(self.scanner.CONNECTIONS_ID, False),
                                     (self.scanner.MONITOR_ID, False)])
                self.device_error = True
        else:
            self.error("NO_OR", [(self.scanner.CONNECTIONS_ID, False),
                                 (self.scanner.MONITOR_ID, False)])
            self.device_error = True

    def nor_gate(self):
        """nor = "NOR with", number_inputs, ("input"|"inputs");"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.NOR_ID:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.WITH:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.INT16 \
                        or self.symbol.type == \
                        self.scanner.ONE:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and (self.symbol.id ==
                                 self.scanner.INPUT or
                                 self.symbol.id ==
                                 self.scanner.INPUTS):
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.error("NO_INPUT", [(self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        self.device_error = True
                else:
                    self.error("NO_INPUT_NO", [(self.scanner.CONNECTIONS_ID, False),
                                               (self.scanner.MONITOR_ID, False)])
                    self.device_error = True
            else:
                self.error("NO_NOR", [(self.scanner.CONNECTIONS_ID, False),
                                      (self.scanner.MONITOR_ID, False)])
                self.device_error = True

    def dtype(self):
        """dtype = "DTYPE";"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.DTYPE_ID:
            self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_DTYPE", [(self.scanner.CONNECTIONS_ID, False),
                                    (self.scanner.MONITOR_ID, False)])
            self.device_error = True

    def xor(self):
        """xor = "XOR";"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.scanner.id == self.scanner.XOR_ID:
            self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_XOR", [(self.scanner.CONNECTIONS_ID, False),
                                  (self.scanner.MONITOR_ID, False)])
            self.device_error = True

    # @pytest.fixture
    # def test_output(self):
    #     assert type(self.output_device_id) == int

    def boolean_input(self):
        """boolean_input = "I", number_inputs;"""
        characters = [c for c in self.scanner.string]
        if 1 <= int(characters[1]) <= 16:
            self.input_id = self.get_id(self.symbol)
            self.input_added = self.devices.add_input(self.input_device_id,
                                                      self.input_id)
            self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_INPUT_NO", [(self.scanner.CONNECTIONS_ID, False),
                                       (self.scanner.MONITOR_ID, False)])
            self.connection_error = True

    # @pytest.fixture
    # def test_boolean_input(self):
    #     assert type(self.input_id) == int and self.input_added is True

    def dtype_input(self):
        """dtype_input = ("DATA" | "CLK" | "SET" | "CLEAR");"""
        self.input_id = self.get_id(self.symbol)
        self.input_added = self.devices.add_input(self.input_device_id,
                                                  self.input_id)
        self.symbol = self.scanner.get_symbol()

    # @pytest.fixture
    # def test_dtype_input(self):
    #     assert type(self.input_id) == int and self.input_added is True

    def dtype_output(self):
        """dtype_output = ("Q" | "QBAR");"""
        self.output_id = self.get_id(self.symbol)
        self.output_added = self.devices.add_input(self.input_device_id,
                                                   self.output_id)
        self.symbol = self.scanner.get_symbol()

    # @pytest.fixture
    # def test_dtype_output(self):
    #     assert type(self.output_id) == int and self.output_added is True

    def initial_input(self):
        """initial_switch = "0"|"1";"""
        if self.symbol.id == self.scanner.ZERO \
                or self.symbol.id == self.scanner.ONE:
            return True
        else:
            return False

    def open_comment(self):
        if self.symbol.type == self.scanner.PUNCTUATION \
                and self.symbol.id == self.scanner.HASHTAG:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.NAME:
                self.symbol = self.scanner.get_symbol()
                while self.symbol.type == self.scanner.NAME:
                    self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.PUNCTUATION \
                        and self.symbol.id == self.scanner.NEWLINE:
                    self.symbol = self.scanner.get_symbol()
                elif self.symbol.type == self.scanner.EOF:
                    sys.exit()
                else:
                    self.error("NO_NEWLINE", [(self.scanner.EOF, False)])
            else:
                self.error("NO_CHARACTER_DIGIT", [(self.scanner.NEWLINE, True)])
        else:
            self.error("NO_HASHTAG", [(self.scanner.NEWLINE, True)])

    def get_id(self, device_name):

        symbol_id = device_name.id
        if symbol_id not in self.devices_symbol_list:
            self.devices_symbol_list.append(symbol_id)

        device_id = self.devices_symbol_list.index(symbol_id)

        return device_id
