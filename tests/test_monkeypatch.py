import os
import pytest

def get_terminal_size():
    terminal_size = os.popen('stty size', 'r').read()
    return terminal_size

def test_get_terminal_size(monkeypatch):
    # The get_terminal_size() function will return a string 'height width\n'
    def mock_size():
        return '10 20\n'

    monkeypatch.setattr(os.popen('stty size', 'r'), 'read', mock_size)

    assert get_terminal_size() == '10 20\n'