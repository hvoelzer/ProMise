import pytest


import app.control as control

@pytest.fixture(scope="session")
def example_control():
    c = control.Control()
    return c
