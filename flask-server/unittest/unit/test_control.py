
def test_loadRawfile(example_control, example_json_datalog):
    example_control.loadRawfile(example_json_datalog)
    
    assert example_control.graph is not None
    assert len(example_control.graph.nodes) == 1
    eventlog = example_control.graph.nodes[0].eventLog
    assert len(eventlog.traces) == 2
    trie = example_control.graph.trie
    assert trie.child["#"] == 0

def test_filterout(example_control, example_json_filter_out):
    example_control.applyFilter(example_json_filter_out)
    
    assert example_control.graph is not None
    assert len(example_control.graph.nodes) == 2
    eventlog = example_control.graph.nodes[0].eventLog
    assert len(eventlog.traces) == 2
    eventlog = example_control.graph.nodes[1].eventLog
    assert len(eventlog.traces) == 0
    trie = example_control.graph.trie
    filter = list(trie.child.keys())[1]
    assert filter.getName() == 'filterOut H F'
    assert trie.child[filter]["#"] == 1

def test_changeLastNode(example_control):
    example_control.changeLastNode({'id': 0})
    
    assert example_control.graph is not None
    assert len(example_control.graph.nodes) == 2
    eventlog = example_control.graph.nodes[0].eventLog
    assert len(eventlog.traces) == 2
    eventlog = example_control.graph.nodes[1].eventLog
    assert len(eventlog.traces) == 0
    trie = example_control.graph.trie
    filter = list(trie.child.keys())[1]
    assert filter.getName() == 'filterOut H F'
    assert trie.child[filter]["#"] == 1

def test_removeBehavior(example_control, example_json_remove_behavior):
    example_control.applyFilter(example_json_remove_behavior)
    
    assert example_control.graph is not None
    assert len(example_control.graph.nodes) == 2
    eventlog = example_control.graph.nodes[0].eventLog
    assert len(eventlog.traces) == 2
    eventlog = example_control.graph.nodes[1].eventLog
    assert len(eventlog.traces) == 0
    trie = example_control.graph.trie
    filter = list(trie.child.keys())[1]
    assert filter.getName() == 'filterOut H F'
    assert trie.child[filter]["#"] == 1

def test_getHistoryGraph(example_control, example_json_get_history_graph):
    assert example_control.getEdgesAsJsonHistory() == example_json_get_history_graph

def test_getEdgesAsJson_and_getEdgesAsJsonTrue(example_control, example_json_get_graph, example_json_get_true_graph):
    assert example_control.getEdgesAsJson() == example_json_get_graph
    assert example_control.getEdgesAsJsonTrue() == example_json_get_true_graph
    # at this point in the clean graph and the true graph should be equal
    assert example_control.getEdgesAsJson() == example_control.getEdgesAsJsonTrue()

def test_getEventLog(example_control, example_json_get_event_log):
    example_control.changeLastNode({'id': 0})
    assert example_control.getEventLog() == example_json_get_event_log