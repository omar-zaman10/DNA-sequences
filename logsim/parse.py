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

        self.switch_input = 0
        self.clock_cycle = 0
        self.no_inputs = 0

        self.devices_symbol_list = []
        self.device_input_dict = {}
        self.device_output_dict = {}
        self.monitored_outputs = []

        self.input_added = False
        self.output_added = False

        self.error_count = 0
        self.syntax_error_count = 0
        self.in_stopping_symbol = False

        self.device_error = False
        self.connection_error = False
        self.monitor_error = False

        self.name_error = False
        self.gate_error = False
        self.input_error = False
        self.output_error = False
        self.section_skipped = False

        self.defining = False
        self.connecting = False
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
            self.device_error = False
            self.connection_error = False
            self.monitor_error = False
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.DEVICES_ID:
                self.defining = True
                self.device_error = False
                self.devices_list()
                self.device_dictionary()
                self.defining = False
                self.devices_instance += 1
                if self.devices_instance > 1:
                    break
            elif (self.symbol.type == self.scanner.KEYWORD
                  and self.symbol.id == self.scanner.CONNECTIONS_ID) \
                    and self.devices_instance == 1:
                self.connecting = True
                self.connection_error = False
                self.connections_list()
                self.connecting = False
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
                self.monitoring = False
                self.monitoring_instance += 1
                if self.monitoring_instance > 1:
                    break
            elif self.symbol.id == self.scanner.HASHTAG:
                self.comment()
            else:
                break

        if (self.devices_instance != 1 or
                self.connections_instance != 1 or
                self.monitoring_instance != 1) and \
                self.section_skipped is False:
            print("Error: Not all sections present")
            self.error_count += 1

        if self.error_count == 0:
            return True
        else:
            print(self.error_count)
            return False

    def error(self, error_type, stopping_symbol):
        self.error_count += 1

        if error_type == "NO_COMMA":
            print("Error: Expected a comma")
            self.syntax_error_count += 1
        elif error_type == "NO_COLON":
            print("Error: Expected a colon")
            self.syntax_error_count += 1
        elif error_type == "NO_DEVICES":
            print("Error: Expected an opening devices statement")
            self.syntax_error_count += 1
        elif error_type == "NO_CONNECTIONS":
            print("Error: Expected an opening connections statement")
            self.syntax_error_count += 1
        elif error_type == "NO_SEMICOLON":
            print("Error: Expected a semicolon")
            self.syntax_error_count += 1
        elif error_type == "NO_MONITOR":
            print("Error: Expected an opening monitor statement")
            self.syntax_error_count += 1
        elif error_type == "NO_IS":
            print("Error: Incorrect devices definition")
            self.syntax_error_count += 1
        elif error_type == "NO_GATE_TYPE":
            print("Error: Gate defined does not exist")
            self.syntax_error_count += 1
        elif error_type == "NO_GATE":
            print("Error: Gate expected")
            self.syntax_error_count += 1
        elif error_type == "NO_SWITCH":
            print("Error: Switch definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_CLOCK":
            print("Error: Clock definition expected")
            self.syntax_error_count += 1
        elif error_type == "SWITCH_INPUT":
            print("Error: Initial switch input of 0 or 1 expected")
            self.syntax_error_count += 1
        elif error_type == "CLOCK":
            print("Error: Clock definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_INTEGER":
            print("Error: Integer expected")
            self.syntax_error_count += 1
        elif error_type == "NO_CYCLE":
            print("Error: Cycle definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_AND":
            print("Error: AND definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_INPUT_NO":
            print("Error: Input number between 1 and 16 expected")
            self.syntax_error_count += 1
        elif error_type == "NO_INPUT":
            print("Error: Input definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_NAND":
            print("Error: NAND definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_OR":
            print("Error: OR definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_NOR":
            print("Error: NOR definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_DTYPE":
            print("Error: DTYPE definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_XOR":
            print("Error: XOR definition expected")
            self.syntax_error_count += 1
        elif error_type == "NO_CONNECTION":
            print("Error: Incorrect connection definition")
            self.syntax_error_count += 1
        elif error_type == "NO_INPUT_TYPE":
            print("Error: Input type does not exist")
            self.syntax_error_count += 1
        elif error_type == "NO_OUTPUT_TYPE":
            print("Error:Output type does not exist")
            self.syntax_error_count += 1
        elif error_type == "NO_CHARACTER":
            print("Error: Alphabetic character expected")
            self.syntax_error_count += 1
        elif error_type == "NO_CHARACTER_DIGIT":
            print("Error: Alphanumeric character expected")
            self.syntax_error_count += 1
        elif error_type == "NO_HASHTAG":
            print("Error: Hashtag expected")
            self.syntax_error_count += 1
        elif error_type == "NO_MONITOR_DEF":
            print("Error: Incorrect monitor definition")
            self.syntax_error_count += 1
        elif error_type == "DEVICE_EXISTS":
            print("Error: Device name already used")
        elif error_type == "NO_DEVICE":
            print("Error: Device has not been defined")
        elif error_type == "INPUT_USED":
            print("Error: Input has already been connected")
        elif error_type == "OUTPUT_MONITORED":
            print("Error: Output is already being monitored")
        elif error_type == "MONITOR_FAILED":
            print("Error: Output not being monitored")
        elif error_type == "CONNECTION_NOT_MADE":
            print("Error: Connection not made")

        error_message = self.scanner.error_location()
        print(error_message[0], "\n", error_message[1], "\n", error_message[2])

        #print(self.names.get_name_string(self.symbol.id))

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
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.PUNCTUATION \
                and self.symbol.id == self.scanner.COLON:
            self.symbol = self.scanner.get_symbol()
            self.device()
            if self.symbol.id == self.scanner.HASHTAG:
                self.comment()
            while self.symbol.id != self.scanner.SEMICOLON:
                if self.device_error is False:
                    if (self.symbol.id == self.scanner.CONNECTIONS_ID
                        or self.symbol.id == self.scanner.MONITOR_ID) \
                            or self.symbol.type == self.scanner.EOF:
                        self.error("NO_SEMICOLON", [(self.scanner.CONNECTIONS_ID, False),
                                                    (self.scanner.MONITOR_ID, False)])
                        break
                    else:
                        self.device()
                        if self.symbol.id == self.scanner.HASHTAG:
                            self.comment()
                else:
                    break
            if self.symbol.id == self.scanner.SEMICOLON:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.id == self.scanner.HASHTAG:
                    self.comment()
        else:
            self.error("NO_COLON", [(self.scanner.CONNECTIONS_ID, False),
                                    (self.scanner.MONITOR_ID, False)])

    # @pytest.fixture
    # def test_devices_list(self):
    #     self.devices_list()
    #     assert self.symbol.type == self.scanner.KEYWORD or \
    #            self.in_stopping_symbol is True

    def connections_list(self):
        """connections= "CONNECTIONS", ":", connection, ";",
        {connection, ";"}, "END CONNECTIONS";"""
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.PUNCTUATION \
                and self.symbol.id == self.scanner.COLON:
            self.symbol = self.scanner.get_symbol()
            self.connection()
            if self.symbol.id == self.scanner.HASHTAG:
                self.comment()
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
                            if self.symbol.id == self.scanner.HASHTAG:
                                self.comment()
                    else:
                        break
                if self.symbol.id == self.scanner.SEMICOLON:
                    self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_COLON", [(self.scanner.MONITOR_ID, False)])

    # @pytest.fixture
    # def test_connections_list(self):
    #     self.connections_list()
    #     assert self.symbol.type == self.scanner.KEYWORD or \
    #            self.in_stopping_symbol is True

    def monitor(self):
        """monitor = "MONITOR", output, {("and"| ",") output}, ";"""""
        self.symbol = self.scanner.get_symbol()
        self.output()
        if self.error_count == 0:
            error_type = self.monitors.make_monitor(self.output_device_id, self.output_id)
            if error_type != self.monitors.NO_ERROR:
                self.error("MONITOR_FAILED", [(self.scanner.EOF, False)])
                self.section_skipped = True
        if self.monitor_error is False:
            if self.symbol.type == self.scanner.NAME:
                self.error("NO_MONITOR_DEF", [(self.scanner.SEMICOLON, True),
                                              (self.scanner.EOF, False)])
            else:
                while self.symbol.id == self.scanner.AND or \
                        self.symbol.type == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    if self.monitor_error is False:
                        self.output()
                        if self.error_count == 0:
                            error_type = self.monitors.make_monitor(self.output_device_id, self.output_id)
                            if error_type != self.monitors.NO_ERROR:
                                self.error("MONITOR_FAILED", [(self.scanner.EOF, False)])
                                self.section_skipped = True
                        if self.symbol.type == self.scanner.EOF:
                            break
                    else:
                        break
                if self.symbol.id == self.scanner.SEMICOLON:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.id == self.scanner.HASHTAG:
                        self.comment()
                else:
                    if self.section_skipped is False:
                        self.error("NO_SEMICOLON", [(self.scanner.EOF, False)])

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
                        self.error("NO_COMMA", [(self.scanner.COMMA, False),
                                                (self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        if self.symbol.id == self.scanner.COMMA:
                            self.symbol = self.scanner.get_symbol()
                            self.device_error = False
                        else:
                            self.section_skipped = True
                            self.device_error = True
                else:
                    if self.name_error:
                        self.name_error = False
                        self.device_error = False
                    elif self.gate_error:
                        self.gate_error = False
                        self.device_error = False
                    elif self.section_skipped:
                        self.device_error = True
            else:
                self.error("NO_IS", [(self.scanner.CONNECTIONS_ID, False),
                                     (self.scanner.MONITOR_ID, False),
                                     (self.scanner.COMMA, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.device_error = False
                else:
                    self.section_skipped = True
                    self.device_error = True
        else:
            if self.name_error:
                self.name_error = False
                self.device_error = False
            elif self.gate_error:
                self.gate_error = False
                self.device_error = False
            elif self.section_skipped:
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
            if self.defining:
                self.error("NO_CHARACTER", [(self.scanner.COMMA, False),
                                            (self.scanner.CONNECTIONS_ID, False),
                                            (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.name_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.device_error = True
            elif self.connecting:
                self.error("NO_CHARACTER", [(self.scanner.COMMA, False),
                                            (self.scanner.CONNECTIONS_ID, False),
                                            (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.name_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.connection_error = True
            elif self.monitoring:
                self.error("NO_CHARACTER", [(self.scanner.SEMICOLON, False),
                                            (self.scanner.MONITOR_ID, False)])
                self.monitor_error = True
            else:
                self.device_error = True
                self.connection_error = True
                self.monitor_error = True

    def connection(self):
        """connection = output, "to", input;"""
        self.output()
        if self.connection_error is False:
            self.symbol = self.scanner.get_symbol()
            self.input()
            if self.connection_error is False:
                if self.syntax_error_count == 0:
                    error_type = self.network.make_connection(self.input_device_id,
                                                              self.input_id,
                                                              self.output_device_id,
                                                              self.output_id)
                    if error_type != self.network.NO_ERROR:
                        self.error("CONNECTION_NOT_MADE", [(self.scanner.EOF, False)])
                        self.connection_error = True
                        self.section_skipped = True
                if self.symbol.type == self.scanner.PUNCTUATION \
                        and self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                elif (self.symbol.type != self.scanner.PUNCTUATION
                      and self.symbol.id != self.scanner.SEMICOLON) \
                        and self.symbol.type != self.scanner.KEYWORD \
                        and self.symbol.type != self.scanner.EOF:
                    self.error("NO_COMMA", [(self.scanner.COMMA, False),
                                            (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.connection_error = False
                    else:
                        self.section_skipped = True
                        self.connection_error = True
            else:
                if self.name_error:
                    self.name_error = False
                    self.connection_error = False
                elif self.gate_error:
                    self.gate_error = False
                    self.connection_error = False
                elif self.section_skipped:
                    self.connection_error = True
                elif self.input_error:
                    self.input_error = False
                    self.connection_error = False
        else:
            if self.name_error:
                self.name_error = False
                self.connection_error = False
            elif self.gate_error:
                self.gate_error = False
                self.connection_error = False
            elif self.section_skipped:
                self.connection_error = True
            elif self.output_error:
                self.output_error = False
                self.connection_error = False

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
                    self.error("NO_INPUT_TYPE", [(self.scanner.COMMA, False),
                                                 (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.input_error = True
                    elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                            self.symbol.id == self.scanner.MONITOR_ID:
                        self.section_skipped = True
                    self.connection_error = True
            else:
                self.error("NO_INPUT_TYPE", [(self.scanner.COMMA, False),
                                             (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.input_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.connection_error = True

    # @pytest.fixture
    # def test_input(self):
    #     assert type(self.input_device_id) == int

    def output(self):
        """output = name, [".", (dtype_output | clock_output)];"""
        self.output_device_id = self.name()
        if self.connection_error is False and \
                self.monitor_error is False:
            if self.symbol.type == self.scanner.PUNCTUATION \
                    and self.symbol.id == self.scanner.FULLSTOP:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.id == self.scanner.Q \
                        or self.symbol.id == \
                        self.scanner.QBAR:
                    self.dtype_output()
                else:
                    self.error("NO_OUTPUT_TYPE", [(self.scanner.COMMA, False),
                                                  (self.scanner.MONITOR_ID, False)])
                    if self.connecting:
                        if self.symbol.id == self.scanner.COMMA:
                            self.symbol = self.scanner.get_symbol()
                            self.output_error = True
                        elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                                self.symbol.id == self.scanner.MONITOR_ID:
                            self.section_skipped = True
                        self.connection_error = True
                    elif self.monitoring:
                        self.monitor_error = True

            elif self.symbol.id != self.scanner.TO and \
                    self.symbol.type != self.scanner.EOF and \
                    self.monitoring is False:
                if self.symbol.type == self.scanner.NAME:
                    self.error("NO_CONNECTION", [(self.scanner.COMMA, False),
                                                 (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.output_error = True
                    elif self.symbol.id == self.scanner.MONITOR_ID:
                        self.section_skipped = True
                    self.connection_error = True
                else:
                    self.error("NO_OUTPUT_TYPE", [(self.scanner.COMMA, False),
                                                  (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.output_error = True
                    elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                            self.symbol.id == self.scanner.MONITOR_ID:
                        self.section_skipped = True
                    self.connection_error = True
            elif self.symbol.id != self.scanner.AND and \
                    self.symbol.id != self.scanner.COMMA and \
                    self.symbol.id != self.scanner.SEMICOLON and \
                    self.symbol.type != self.scanner.EOF and \
                    self.monitoring is True:
                self.error("NO_MONITOR_DEF", [(self.scanner.EOF, False)])
                self.monitor_error = True
            else:
                if self.connecting:
                    self.output_id = None
                    if self.error_count == 0:
                        self.output_added = self.devices.add_output(self.output_device_id,
                                                                    self.output_id)
                        if self.output_added is False:
                            print("Output not added")
                elif self.monitoring:
                    self.output_id = None
                    if (self.output_device_id, self.output_id) in self.monitored_outputs:
                        self.error("OUTPUT_MONITORED", [(self.scanner.EOF, False)])
                        self.section_skipped = True
                        self.monitor_error = True
                    else:
                        self.monitored_outputs.append((self.output_device_id, self.output_id))

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
            elif self.symbol.id == self.scanner.CLOCK_ID:
                self.clock()
            elif self.symbol.id == self.scanner.AND_ID:
                self.and_gate()
            elif self.symbol.id == self.scanner.NAND_ID:
                self.nand_gate()
            elif self.symbol.id == self.scanner.OR_ID:
                self.or_gate()
            elif self.symbol.id == self.scanner.NOR_ID:
                self.nor_gate()
            elif self.symbol.id == self.scanner.DTYPE_ID:
                self.dtype()
            elif self.symbol.id == self.scanner.XOR_ID:
                self.xor()
            elif self.symbol.id == self.scanner.NOT_ID:
                self.not_gate()
            else:
                self.error("NO_GATE_TYPE", [(self.scanner.COMMA, False),
                                            (self.scanner.CONNECTIONS_ID, False),
                                            (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.gate_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.device_error = True
        else:
            self.error("NO_GATE", [(self.scanner.COMMA, False),
                                   (self.scanner.CONNECTIONS_ID, False),
                                   (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.gate_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
            self.device_error = True

    def switch(self):
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
                        self.switch_input = int(self.names.get_name_string(self.symbol.id))
                        if self.device_error is False:
                            self.devices.make_switch(self.device_id, self.switch_input)
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.error("SWITCH_INPUT", [(self.scanner.COMMA, False),
                                                    (self.scanner.CONNECTIONS_ID, False),
                                                    (self.scanner.MONITOR_ID, False)])
                        if self.symbol.id == self.scanner.COMMA:
                            self.symbol = self.scanner.get_symbol()
                            self.gate_error = True
                        elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                                self.symbol.id == self.scanner.MONITOR_ID:
                            self.section_skipped = True
                        self.device_error = True
                else:
                    self.error("NO_SWITCH", [(self.scanner.COMMA, False),
                                             (self.scanner.CONNECTIONS_ID, False),
                                             (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.gate_error = True
                    elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                            self.symbol.id == self.scanner.MONITOR_ID:
                        self.section_skipped = True
                    self.device_error = True
            else:
                self.error("NO_SWITCH", [(self.scanner.COMMA, False),
                                         (self.scanner.CONNECTIONS_ID, False),
                                         (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.gate_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.device_error = True
        else:
            self.error("NO_SWITCH", [(self.scanner.COMMA, False),
                                     (self.scanner.CONNECTIONS_ID, False),
                                     (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.gate_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
            self.device_error = True

    def clock(self):  # FIX ERROR HANDLING FOR IF CONNECTIONS OR MONITOR ARE RETURNED
        """clock = "CLOCK with", digit, "cycle period";"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.CLOCK_ID:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD \
                    and self.symbol.id == self.scanner.WITH:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.INTEGER \
                        or self.symbol.type == self.scanner.INT16:
                    self.clock_cycle = int(self.names.get_name_string(self.symbol.id))
                    self.symbol = self.scanner.get_symbol()
                    while self.symbol.type == self.scanner.INT16:
                        self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and self.symbol.id == self.scanner.CYCLE:
                        self.symbol = self.scanner.get_symbol()
                        if self.symbol.type == self.scanner.KEYWORD \
                                and self.symbol.id == self.scanner.PERIOD:
                            if self.device_error is False:
                                self.devices.make_clock(self.device_id, self.clock_cycle)
                            self.symbol = self.scanner.get_symbol()
                        else:
                            self.error("NO_CYCLE", [(self.scanner.COMMA, False),
                                                    (self.scanner.SEMICOLON, False),
                                                    (self.scanner.CONNECTIONS_ID, False),
                                                    (self.scanner.MONITOR_ID, False)])
                            if self.symbol.id == self.scanner.COMMA:
                                self.symbol = self.scanner.get_symbol()
                                self.gate_error = True
                            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                                    self.symbol.id == self.scanner.MONITOR_ID:
                                self.section_skipped = True
                            self.device_error = True
                    else:
                        self.error("NO_CYCLE", [(self.scanner.COMMA, False),
                                                (self.scanner.SEMICOLON, False),
                                                (self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        if self.symbol.id == self.scanner.COMMA:
                            self.symbol = self.scanner.get_symbol()
                            self.gate_error = True
                        elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                                self.symbol.id == self.scanner.MONITOR_ID:
                            self.section_skipped = True
                        self.device_error = True
                else:
                    self.error("NO_INTEGER", [(self.scanner.COMMA, False),
                                              (self.scanner.SEMICOLON, False),
                                              (self.scanner.CONNECTIONS_ID, False),
                                              (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.gate_error = True
                    elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                            self.symbol.id == self.scanner.MONITOR_ID:
                        self.section_skipped = True
                    self.device_error = True
            else:
                self.error("NO_CLOCK", [(self.scanner.COMMA, False),
                                        (self.scanner.SEMICOLON, False),
                                        (self.scanner.CONNECTIONS_ID, False),
                                        (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.gate_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.device_error = True
        else:
            self.error("NO_CLOCK", [(self.scanner.COMMA, False),
                                    (self.scanner.SEMICOLON, False),
                                    (self.scanner.CONNECTIONS_ID, False),
                                    (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.gate_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
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
                    self.no_inputs = int(self.names.get_name_string(self.symbol.id))
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and (self.symbol.id == self.scanner.INPUT or
                                 self.symbol.id == self.scanner.INPUTS):
                        if self.device_error is False:
                            self.devices.make_gate(self.device_id, self.devices.AND, self.no_inputs)
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.error("NO_INPUT", [(self.scanner.COMMA, False),
                                                (self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        if self.symbol.id == self.scanner.COMMA:
                            self.symbol = self.scanner.get_symbol()
                            self.gate_error = True
                        elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                                self.symbol.id == self.scanner.MONITOR_ID:
                            self.section_skipped = True
                        self.device_error = True
                else:
                    self.error("NO_INPUT_NO", [(self.scanner.COMMA, False),
                                               (self.scanner.CONNECTIONS_ID, False),
                                               (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.gate_error = True
                    elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                            self.symbol.id == self.scanner.MONITOR_ID:
                        self.section_skipped = True
                    self.device_error = True
            else:
                self.error("NO_AND", [(self.scanner.COMMA, False),
                                      (self.scanner.CONNECTIONS_ID, False),
                                      (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.gate_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.device_error = True
        else:
            self.error("NO_AND", [(self.scanner.COMMA, False),
                                  (self.scanner.CONNECTIONS_ID, False),
                                  (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.gate_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
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
                    self.no_inputs = int(self.names.get_name_string(self.symbol.id))
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and (self.symbol.id == self.scanner.INPUT or
                                 self.symbol.id == self.scanner.INPUTS):
                        if self.device_error is False:
                            self.devices.make_gate(self.device_id, self.devices.NAND, self.no_inputs)
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.error("NO_INPUT", [(self.scanner.COMMA, False),
                                                (self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        if self.symbol.id == self.scanner.COMMA:
                            self.symbol = self.scanner.get_symbol()
                            self.gate_error = True
                        elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                                self.symbol.id == self.scanner.MONITOR_ID:
                            self.section_skipped = True
                        self.device_error = True
                else:
                    self.error("NO_INPUT_NO", [(self.scanner.COMMA, False),
                                               (self.scanner.CONNECTIONS_ID, False),
                                               (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.gate_error = True
                    elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                            self.symbol.id == self.scanner.MONITOR_ID:
                        self.section_skipped = True
                    self.device_error = True
            else:
                self.error("NO_NAND", [(self.scanner.COMMA, False),
                                       (self.scanner.CONNECTIONS_ID, False),
                                       (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.gate_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.device_error = True
        else:
            self.error("NO_NAND", [(self.scanner.COMMA, False),
                                   (self.scanner.CONNECTIONS_ID, False),
                                   (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.gate_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
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
                    self.no_inputs = int(self.names.get_name_string(self.symbol.id))
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and (self.symbol.id == self.scanner.INPUT or
                                 self.symbol.id == self.scanner.INPUTS):
                        if self.device_error is False:
                            self.devices.make_gate(self.device_id, self.devices.OR, self.no_inputs)
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.error("NO_INPUT", [(self.scanner.COMMA, False),
                                                (self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        if self.symbol.id == self.scanner.COMMA:
                            self.symbol = self.scanner.get_symbol()
                            self.gate_error = True
                        elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                                self.symbol.id == self.scanner.MONITOR_ID:
                            self.section_skipped = True
                        self.device_error = True
                else:
                    self.error("NO_INPUT_NO", [(self.scanner.COMMA, False),
                                               (self.scanner.CONNECTIONS_ID, False),
                                               (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.gate_error = True
                    elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                            self.symbol.id == self.scanner.MONITOR_ID:
                        self.section_skipped = True
                    self.device_error = True
            else:
                self.error("NO_OR", [(self.scanner.COMMA, False),
                                     (self.scanner.CONNECTIONS_ID, False),
                                     (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.gate_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.device_error = True
        else:
            self.error("NO_OR", [(self.scanner.COMMA, False),
                                 (self.scanner.CONNECTIONS_ID, False),
                                 (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.gate_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
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
                    self.no_inputs = int(self.names.get_name_string(self.symbol.id))
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.KEYWORD \
                            and (self.symbol.id ==
                                 self.scanner.INPUT or
                                 self.symbol.id ==
                                 self.scanner.INPUTS):
                        if self.device_error is False:
                            self.devices.make_gate(self.device_id, self.devices.NOR, self.no_inputs)
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.error("NO_INPUT", [(self.scanner.COMMA, False),
                                                (self.scanner.CONNECTIONS_ID, False),
                                                (self.scanner.MONITOR_ID, False)])
                        if self.symbol.id == self.scanner.COMMA:
                            self.symbol = self.scanner.get_symbol()
                            self.gate_error = True
                        elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                                self.symbol.id == self.scanner.MONITOR_ID:
                            self.section_skipped = True
                        self.device_error = True
                else:
                    self.error("NO_INPUT_NO", [(self.scanner.COMMA, False),
                                               (self.scanner.CONNECTIONS_ID, False),
                                               (self.scanner.MONITOR_ID, False)])
                    if self.symbol.id == self.scanner.COMMA:
                        self.symbol = self.scanner.get_symbol()
                        self.gate_error = True
                    elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                            self.symbol.id == self.scanner.MONITOR_ID:
                        self.section_skipped = True
                    self.device_error = True
            else:
                self.error("NO_NOR", [(self.scanner.COMMA, False),
                                      (self.scanner.CONNECTIONS_ID, False),
                                      (self.scanner.MONITOR_ID, False)])
                if self.symbol.id == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.gate_error = True
                elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                        self.symbol.id == self.scanner.MONITOR_ID:
                    self.section_skipped = True
                self.device_error = True

    def dtype(self):
        """dtype = "DTYPE";"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.DTYPE_ID:
            if self.device_error is False:
                self.devices.make_d_type(self.device_id)
            self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_DTYPE", [(self.scanner.COMMA, False),
                                    (self.scanner.CONNECTIONS_ID, False),
                                    (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.gate_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
            self.device_error = True

    def xor(self):
        """xor = "XOR";"""
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.XOR_ID:
            if self.device_error is False:
                self.devices.make_gate(self.device_id, self.devices.XOR, 2)
            self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_XOR", [(self.scanner.COMMA, False),
                                  (self.scanner.CONNECTIONS_ID, False),
                                  (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.gate_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
            self.device_error = True

    # @pytest.fixture
    # def test_output(self):
    #     assert type(self.output_device_id) == int

    def not_gate(self):
        if self.symbol.type == self.scanner.KEYWORD \
                and self.symbol.id == self.scanner.NOT_ID:
            if self.device_error is False:
                self.devices.make_gate(self.device_id, self.devices.NOT, 1)
            self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_NOT", [(self.scanner.COMMA, False),
                                  (self.scanner.CONNECTIONS_ID, False),
                                  (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.gate_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
            self.device_error = True

    def boolean_input(self):
        """boolean_input = "I", number_inputs;"""
        characters = [c for c in self.scanner.string]
        if 1 <= int(characters[1]) <= 16:
            if self.error_count == 0:
                self.input_id = self.get_input_id(self.input_device_id)
                self.input_added = self.devices.add_input(self.input_device_id,
                                                          self.input_id)
                if self.input_added is False:
                    print("Input not added")
            self.symbol = self.scanner.get_symbol()
        else:
            self.error("NO_INPUT_NO", [(self.scanner.COMMA, False),
                                       (self.scanner.MONITOR_ID, False)])
            if self.symbol.id == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                self.input_error = True
            elif self.symbol.id == self.scanner.CONNECTIONS_ID or \
                    self.symbol.id == self.scanner.MONITOR_ID:
                self.section_skipped = True
            self.connection_error = True

    # @pytest.fixture
    # def test_boolean_input(self):
    #     assert type(self.input_id) == int and self.input_added is True

    def dtype_input(self):
        """dtype_input = ("DATA" | "CLK" | "SET" | "CLEAR");"""
        if self.error_count == 0:
            self.input_id = self.get_input_id(self.input_device_id)
            self.input_added = self.devices.add_input(self.input_device_id,
                                                      self.input_id)
            if self.input_added is False:
                print("Output not added")
        self.symbol = self.scanner.get_symbol()

    # @pytest.fixture
    # def test_dtype_input(self):
    #     assert type(self.input_id) == int and self.input_added is True

    def dtype_output(self):
        """dtype_output = ("Q" | "QBAR");"""
        if self.connecting:
            if self.error_count == 0:
                self.output_id = self.get_output_id(self.output_device_id)
                self.output_added = self.devices.add_output(self.output_device_id,
                                                            self.output_id)
                if self.output_added is False:
                    print("Output not added")
        elif self.monitoring:
            self.output_id = self.get_output_id(self.output_device_id)
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

    def get_id(self, device_name):
        symbol_id = device_name.id
        if self.defining:
            if symbol_id not in self.devices_symbol_list:
                self.devices_symbol_list.append(symbol_id)
                return symbol_id
            else:
                self.error("DEVICE_EXISTS", [(self.scanner.EOF, False)])
                self.section_skipped = True
                self.device_error = True
                return None
        elif self.connecting or self.monitoring:
            if symbol_id in self.devices_symbol_list:
                return symbol_id
            else:
                if self.syntax_error_count == 0:
                    self.error("NO_DEVICE", [(self.scanner.EOF, False)])
                    self.section_skipped = True
                    self.connection_error = True
                return None

    def device_dictionary(self):
        for symbol_id in self.devices_symbol_list:
            self.device_input_dict[symbol_id] = []
            self.device_output_dict[symbol_id] = []

    def get_input_id(self, device_name_id):
        input_numbers = self.device_input_dict[device_name_id]
        if self.symbol.id not in input_numbers:
            self.device_input_dict[device_name_id].append(self.symbol.id)
            return self.symbol.id
        else:
            self.error("INPUT_USED", [(self.scanner.EOF, False)])
            self.section_skipped = True
            self.connection_error = True

    def get_output_id(self, device_name_id):
        output_numbers = self.device_output_dict[device_name_id]
        if self.symbol.id not in output_numbers:
            self.device_output_dict[device_name_id].append(self.symbol.id)
            return self.symbol.id
        else:
            if self.monitoring:
                if (device_name_id, self.symbol.id) in self.monitored_outputs:
                    self.error("OUTPUT_MONITORED", [(self.scanner.EOF, False)])
                    self.section_skipped = True
                    self.monitor_error = True
                else:
                    self.monitored_outputs.append((device_name_id, self.symbol.id))

    def comment(self):
        if self.symbol.type == self.scanner.PUNCTUATION \
                and self.symbol.id == self.scanner.HASHTAG:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.NAME or \
                    self.symbol.type == self.scanner.KEYWORD:
                self.symbol = self.scanner.get_symbol()
                while self.symbol.type == self.scanner.NAME or \
                        self.symbol.type == self.scanner.KEYWORD:
                    self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.PUNCTUATION \
                        and self.symbol.id == self.scanner.HASHTAG:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.EOF:
                        if self.devices_instance == 0 or \
                            self.connections_instance == 0 or \
                                self.monitoring_instance == 0:
                            self.device_error = True
                            self.connection_error = True
                            self.monitor_error = True
                            self.section_skipped = False
                else:
                    self.error("NO_HASHTAG", [(self.scanner.EOF, False)])
                    self.device_error = True
                    self.connection_error = True
                    self.monitor_error = True
                    self.section_skipped = True
            else:
                self.error("NO_CHARACTER_DIGIT", [(self.scanner.HASHTAG, True)])
                self.device_error = True
                self.connection_error = True
                self.monitor_error = True
                self.section_skipped = True
        else:
            self.error("NO_HASHTAG", [(self.scanner.HASHTAG, True)])
            self.device_error = True
            self.connection_error = True
            self.monitor_error = True
            self.section_skipped = True
