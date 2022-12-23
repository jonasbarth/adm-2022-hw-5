# Backend
The purpose of this package is to gather functionality for the backend part of the Marvel Hero Graphs. The backend exposes
modules that allow you to:

* create hero graphs from various sources
* query hero graphs
* get information about heroes
* preprocess hero and comic data

# Controller
The entry point that users interact with is a controller system that that exposes an interfaces for running various 
queries against hero graphs.

The controller takes as input an identifier as a string that then is mapped to an associated function that is applied 
to that controller's graph.

## How to use
To use the controller:
```python
import backend.graph.collaborative
from backend import Controller

hero_graph, graph_type = backend.graph.hero_comic.create_from(nodes='data/nodes.csv', edges='data/edges.csv')

controller = Controller(hero_graph, graph_type) # create the controller with the hero graph
controller.run('features') # runs the features function
```