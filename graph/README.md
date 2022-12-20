# graph package
The purpose of this package is gather functions related to the Marvel hero graphs.

# Creating graphs
The `collaborative` module exposes methods for creating collaborative graphs. You can create a collaborative graph
from a **path** to a `.csv` file or directly from a **pandas DataFrame**.

## From .csv
To create a collaborative graph from a `.csv`:
```python
import graph.collaborative
graph.collaborative.create_from('data/hero-network.csv')
```

## From dataframe
To create the collaborative graph from a pandas dataframe:
```python
import graph.collaborative
import pandas as pd
hero_network = pd.read_csv('data/hero-network.csv')
graph.collaborative.create_from(hero_network)
```

For more details on using the `create_from` function, check it out [here](collaborative.py).