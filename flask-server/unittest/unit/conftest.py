import pytest
import json
import pathlib



JSON_RESPONSE = pathlib.Path(__file__).parent.parent / "resources" / "json-response"

import app.control as control

@pytest.fixture(scope="session")
def example_control():
    return control.Control()

@pytest.fixture()
def example_json_datalog():
    with open(JSON_RESPONSE / "input.json") as f:
        data = json.load(f)
    return data

@pytest.fixture()
def example_json_filter_out():
    with open(JSON_RESPONSE / "filter-out.json") as f:
        data = json.load(f)
    return data

@pytest.fixture()
def example_json_get_graph():
    with open(JSON_RESPONSE / "get-graph.json") as f:
        data = json.load(f)
    return str(data).replace("\'", "\"")

@pytest.fixture()
def example_json_get_true_graph():
    with open(JSON_RESPONSE / "get-true-graph.json") as f:
        data = json.load(f)
    return str(data).replace("\'", "\"")

@pytest.fixture()
def example_json_remove_behavior():
    with open(JSON_RESPONSE / "remove-behavior.json") as f:
        data = json.load(f)
    return data

@pytest.fixture()
def example_json_get_history_graph():
    with open(JSON_RESPONSE / "get-history-graph.json") as f:
        data = json.load(f)
    return str(data).replace("\'", "\"")

@pytest.fixture()
def example_json_get_event_log():
    with open(JSON_RESPONSE / "get-event-log.json") as f:
        data = json.load(f)
    return str(data).replace("\'", "\"")
