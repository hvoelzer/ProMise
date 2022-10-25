import pytest


import app.control as control

@pytest.fixture
def example_control():
    c = control.Control()
    return c
