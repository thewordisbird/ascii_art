
import pytest
import m_patch
import os


def test_get_terminal_size(monkeypatch):
    # The get_terminal_size() function will return a string 'height width\n'
    def mock_terminal_size(cmd, **kwargs):
        return '10 20\n'

    monkeypatch.setattr(m_patch, 'Popen' , mock_terminal_size)

    assert m_patch.get_terminal_size() == '10 20\n'

def test_get_path(monkeypatch):
    def mock_abspath(pth):
        return '/mock/path'
    monkeypatch.setattr(m_patch.os.path, 'abspath', mock_abspath)
    assert m_patch.get_path() == '/mock/path'