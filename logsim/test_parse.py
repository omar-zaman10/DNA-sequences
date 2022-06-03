import pytest
from scanner import Scanner, Symbol
from names import Names


@pytest.fixture
def symbol():
    symbol = Symbol()
    return symbol

@pytest.fixture
def scanner():
    scanner = Scanner()
    return scanner



@pytest.fixture
def test_devices_list(self):
    self.devices_list()
    assert self.symbol.type == self.scanner.KEYWORD or \
            self.in_stopping_symbol is True