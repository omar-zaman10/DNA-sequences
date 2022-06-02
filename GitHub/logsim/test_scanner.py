"""Pytest file to test out the scanner.py module"""

import pytest
import os
from scanner import Scanner, Symbol
from names import Names 

"""Functions to test:
get_symbol()
advance()
skip_spaces()
get_name()
get_number()
reportErrorLocation()"""

@pytest.fixture
def names():
    names = Names()
    return names

@pytest.fixture
def symbol():
    symbol = Symbol()
    return symbol

@pytest.fixture
def scanner():
    scanner = Scanner()
    return scanner

@pytest.fixture
def scanner_with_string():
    string = "    is AND with 10 inputs"
    names = Names()
    scanner = Scanner(string, names, test_string=True)
    return scanner

@pytest.fixture
def random_string():
    string = "SW3 is SWITCH with state 1;"
    return string


def test_scanner_with_non_existing_file(names):
    """Test error when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        Scanner("i_dont_exist.txt", names, test_string=False)

def test_skip_spaces(scanner_with_string, expected_out="i"):
    while scanner_with_string.current_character.isspace():
        scanner_with_string.skip_spaces()
    assert scanner_with_string.current_character == expected_out 

@pytest.mark.parametrize("steps,expected", [
    (0, "S"),
    (8, "W"),
    (12, "H"),
    (15, "i"),
    (25, "1"),
    (26, ";"),
])

def test_advance(steps, expected, random_string, names):

    if os.path.exists("random_string.txt"):
        os.remove("random_string.txt")
    f = open("random_string.txt", "a")
    f.write(random_string)
    f.close()
    
    scanner = Scanner("random_string.txt", names, test_string=False)
    
    i=0
    while i<=steps:
        scanner.advance()
        i+=1
    
    assert scanner.current_character == expected

def test_get_name(scanner_with_string):
    while scanner_with_string.current_character.isspace():
        scanner_with_string.skip_spaces()
    scanner_with_string.get_name()
    assert scanner_with_string.string == "is"
    
    while scanner_with_string.current_character.isspace():
        scanner_with_string.skip_spaces()
    scanner_with_string.get_name()
    assert scanner_with_string.string == "AND"
    
    while scanner_with_string.current_character.isspace():
        scanner_with_string.skip_spaces()
    scanner_with_string.get_name()
    assert scanner_with_string.string == "with"

def test_get_number(scanner_with_string):
    while scanner_with_string.current_character.isdigit() == False:
        scanner_with_string.advance()
    number = scanner_with_string.get_number()
    assert number == 10

@pytest.mark.parametrize("data, expected_symbol_type", [
    ("AND", 1),
    ("SWITCH", 1),
    ("CLOCK", 1),
    ("G5", 2),
    ("S10", 2),
    ("is", 1),
    ("with", 1),
    ("cycle", 1),
    ("period", 1),
    ("09", 4),
    ("16", 4),
    ("17", 3),
    ("75", 3),
    (";", 0),
    (".", 0),
    ("", 5)
])

def test_get_symbol(data, expected_symbol_type, symbol, names):
    symbol = Scanner(data, names, test_string=True).get_symbol()
    assert symbol.type == expected_symbol_type

def test_non_valid_characters(names):
    with pytest.raises(SyntaxError):
        Scanner("!+$", names, test_string=True).get_symbol()

def test_comments(symbol, names):
    scanner = Scanner("#this is a comment \n", names, test_string=True)
    symbol = scanner.get_symbol()

    assert symbol.type == 0
    assert scanner.current_character == '\n'

