from __future__ import annotations

import numpy as np


def local_peaks(x: np.ndarray) -> np.ndarray:
    """
    Retorna índices i onde x[i] é máximo local estrito:
    x[i-1] < x[i] >= x[i+1]
    """
    if len(x) < 3:
        return np.array([], dtype=int)
    return np.where((x[1:-1] > x[:-2]) & (x[1:-1] >= x[2:]))[0] + 1
