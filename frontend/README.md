# Frontend
The purpose of this package is to gather all necessary functionalities for displaying the 
results from [backend functions](../backend).

It has a single [visualisations](visualisations.py) module with one function per each
backend functionality. The visualisation function names match the ones of the backend
functions and are prefixed with `visualise`.

| Backend                  | Frontend                           |
|--------------------------|------------------------------------|
| `features`               | `visualise_features`               |
| `metrics`                | `visualise_metrics`                |
| `shortest_ordered_route` | `visualise_shortest_ordered_route` |
| `disconnecting_graphs`   | `visualise_disconnecting_graphs`   |
| `extract_communities`    | `visualise_extract_communities`    |

# How to use
You can simply import these functions from the `frontend` package.

```python
from frontend import visualise_features
```