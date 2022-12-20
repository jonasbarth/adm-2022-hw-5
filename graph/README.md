# graph package
The purpose of this package is gather functions related to the Marvel hero graphs.

# Creating graphs
The `collaborative` module exposes methods for creating collaborative graphs. You can create a collaborative graph
from a **path** to a `.csv` file or directly from a **pandas DataFrame**.

## From .csv
To create a collaborative graph from a `.csv`:
```python
import graph.collaborative
graph.collaborative.create_from(path='data/hero-network.csv')
```

## From dataframe
To create the collaborative graph from a pandas dataframe:
```python
import graph.collaborative
import pandas as pd
hero_network = pd.read_csv('data/hero-network.csv')
graph.collaborative.create_from(data=hero_network)
```

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