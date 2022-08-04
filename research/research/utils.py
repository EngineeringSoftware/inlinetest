from typing import Callable, Dict, Union

import numpy as np

SUMMARIES_FUNCS: Dict[str, Callable[[Union[list, np.ndarray]], Union[int, float]]] = {
    "AVG": lambda l: np.mean(l).item() if len(l) > 0 else np.NaN,
    "SUM": lambda l: np.sum(l).item() if len(l) > 0 else np.NaN,
    "MAX": lambda l: np.max(l).item() if len(l) > 0 else np.NaN,
    "MIN": lambda l: np.min(l).item() if len(l) > 0 else np.NaN,
    "MEDIAN": lambda l: np.median(l).item()
    if len(l) > 0 and np.NaN not in l
    else np.NaN,
    "STDEV": lambda l: np.std(l).item() if len(l) > 0 else np.NaN,
    "CNT": lambda l: len(l),
}
