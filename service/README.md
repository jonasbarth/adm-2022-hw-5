# Purpose
The `service` package contains modules that exposes some sort of service related to the Marvel universe.

# TopHeroService
The `TopHeroService` allows you to extract information about top Marvel heroes, e.g. getting the top N heroes.

## Creating the Service
The service can be created from a `.csv` file or from an existing pandas DataFrame.

### From CSV
Creating the service from a `.csv` file, e.g. the `edges.csv` file:
```python
from service import TopHeroService

hero_service = TopHeroService.create_from(data='data/edges.csv', preprocess=True)
```

Setting the `preprocess=True` will:
1. replace 'SPIDER-MAN/PETER PAR' with 'SPIDER-MAN/PETER PARKER'.
1. remove trailing whitespace and `/` characters.

### From DataFrame
Creating the service from a pandas DataFrame:
```python
from service import TopHeroService
import pandas as pd

edges = 'data/edges.csv'
hero_service = TopHeroService.create_from(data=edges, preprocess=True)
```

## Getting the top N Heroes.
To get the top N heroes, first create the `TopHeroService` using the preferred method. Then, call the `top_n` method
using the number of heroes that you want to get.
```python
hero_service.top_n(10)
```