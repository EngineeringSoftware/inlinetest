from inline import itest
import unittest.mock

def __init__(self, file: "IO[str]") -> None:
    handle = GetStdHandle(STDOUT)
    self._handle = handle
    default_text = GetConsoleScreenBufferInfo(handle).wAttributes
    self._default_text = default_text

    self._default_fore = default_text & 7
    self._default_back = (default_text >> 4) & 7
    itest().given(self, unittest.mock.Mock()).given(default_text, 1).check_eq(self._default_back, 0)
    self._default_attrs = self._default_fore | (self._default_back << 4)
    itest().given(self, unittest.mock.Mock()).given(self._default_fore, 1).given(self._default_back, 0).check_eq(self._default_attrs, 1)

    self._file = file
    self.write = file.write
    self.flush = file.flush
