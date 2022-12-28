# Backend
The purpose of this package is to gather functionality for the backend part of the Marvel Hero Graphs. The backend exposes
modules that allow you to:

* [create hero graphs](graph/README.md) from various sources
* [query hero graphs](manager.py)
* [get information](service/README.md) about heroes
* [preprocess](graph/preprocess.py) hero and comic data

# Manager
The manager module houses all the desired functionality that is used by the controller:
* features
* top superheroes
* shortest ordered route
* disconnecting graphs
* extracting communities

## How to add to Manager
The manager should contain all the functionalities described in the homework instructions, e.g. top superheroes. 
When adding a new function, it needs to follow a certain signature so that it can be integrated into the controller.

The function should only take in **three** parameters:
* the networkx graph
* the N heroes to consider
* `**kwargs` for any additional parameters.

This makes it possible for the controller to simplify the function calls to the manager. The `features` example:
```python
def features(graph: nx.Graph, top_n: int, **kwargs):
    """Extracts the features of the graph.

    :arg
    graph (nx.Graph) - a networkx graph.
    top_n (int) - the top N heroes of which data will be considered.
    **graph_type (GraphType) - the type of the graph. Either the collaborative or hero-comic graph.

    :return
    a GraphFeatures object.
    """
    graph_type = kwargs.get('graph_type')
```

In this example we can see that the `graph_type` is passed as part of the `**kwargs` parameter.

# Controller
The entry point that users interact with is a controller system that that exposes an interfaces for running various 
queries against hero graphs.

The controller takes as input an identifier as a string that then is mapped to an associated function that is applied 
to that controller's graph.

## How to add to Controller
Once your function is in the `manager` module, adding it to the controller is straightforward. All you have to do is to
add the function name and link into the `self.funcs` dictionary as a __key-value__ pair.

In the example below, you can see the `features` functionality in the dictionary. `features.__name__` returns the name
of the function, i.e. `"features"`, and `features` is the actual function.
```python
self.funcs = {features.__name__: features}
```

In the `run` method, the dictionary is then accessed and the function corresponding to the provided identifier is run.

## How to use
To use the controller:
```python
import backend.graph.collaborative
from backend import Controller

hero_graph, graph_type = backend.graph.hero_comic.create_from(nodes='data/nodes.csv', edges='data/edges.csv')

controller = Controller(hero_graph, graph_type) # create the controller with the hero graph
controller.run('features') # runs the features function
```