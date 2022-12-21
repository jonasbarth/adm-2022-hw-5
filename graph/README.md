# Purpose
The purpose of the `graph` package is gather functions related to the Marvel hero graphs.

# Creating graphs

## Collaborative (First Graph)
The `collaborative` module exposes methods for creating collaborative graphs. You can create a collaborative graph
from a **path** to a `.csv` file or directly from a **pandas DataFrame**.

### From .csv
To create a collaborative graph from a `.csv`:
```python
import graph.collaborative
graph.collaborative.create_from(path='data/hero-network.csv')
```

When creating the graph from a `.csv`, all of the [preprocessing](#preprocessing) steps will be applied.

### From dataframe
To create the collaborative graph from a pandas dataframe:
```python
import graph.collaborative
import pandas as pd
hero_network = pd.read_csv('data/hero-network.csv')
graph.collaborative.create_from(data=hero_network)
```

When creating the graph from a dataframe, **NONE** of the [preprocessing](#preprocessing) steps will be applied. The data is assumed to be
preprocessed already.


## Weights
The `create_from` function also has a `weight` parameter which is a function that is used to calculate the weights
between two edges. The default is to use the inverse proportion of the number of times two heroes appeared in the 
same comic, i.e. if *hero1* and *hero2* appeared in the same comic 10 times, their weight would be $\frac{1}{10}$.

You can create your own weight function if you want, it should have the following signature:
```python
def my_weight(hero1, hero2, n_edges):
    ...
```

where `hero1` and `hero2` are the names of the two heroes and `n_edges` is the number of edges shared between the 
two heroes.

For more details on using the `create_from` function, check it out [here](collaborative.py).

## Hero-Comic (Second Graph)
The `hero-comic` module exposes a method for creating the hero comic graph where nodes can one of two types:
1. hero
1. comic

You can create the `hero-comic` graph either from pandas dataframes or by specifying the path to a csv to read the data 
from.

### From csv
To create a hero-comic graph from a `.csv`:
```python
import graph.hero_comic
graph.hero_comic.create_from(nodes='data/nodes.csv', edges='data/edges.csv')
```

When creating the graph from a `.csv`, all of the [preprocessing](#preprocessing) steps will be applied.

### From dataframe
To create a hero-comic graph from pandas dataframes:
```python
import graph.hero_comic
import pandas as pd

nodes = pd.read_csv('data/nodes.csv')
edges = pd.read_csv('data/edges.csv')

graph.hero_comic.create_from(nodes=nodes, edges=edges)
```

When creating the graph from a dataframe, **NONE** of the [preprocessing](#preprocessing) steps will be applied. The data is assumed to be
preprocessed already.

# Preprocessing
1. Some of the heroes' names in `hero-network.csv` are not found in `edges.csv`. This inconsistency exists for the following reasons:

* Some heroes' names in `hero-network.csv` have extra spaces at the end of their names compared to their names in `edges.csv`.
* Some heroes' names in `hero-network.csv` have an extra `/` at the end of their names compared to their names in `edges.csv`.
* The hero name 'SPIDER-MAN/PETER PARKER' in `edges.csv` has been changed to 'SPIDER-MAN/PETER PAR' in `hero-network.csv` 
  due to a string length limit in `hero-network.csv`.
  
To fix these problems we:
* trim all extra whitespace at the end of the hero name.
* trim the extra `/` at the end of the hero name.
* rename 'SPIDER-MAN/PETER PAR' in `hero-network.csv` to 'SPIDER-MAN/PETER PARKER' 
  
2. Some entries in the 'hero-network.csv' have the same hero in both columns. In the graph, these entries form a self-loop. 
Because a self-loop makes no sense in this network, we remove those from the dataset.