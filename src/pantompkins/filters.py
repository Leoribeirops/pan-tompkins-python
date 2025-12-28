from __future__ import annotations
import numpy as np
from scipy.signal import butter, filtfilt


def bandpass_butter(x: np.ndarray, fs: int, low_hz: float = 5.0, high_hz: float = 15.0, order: int = 2) -> np.ndarray:
    nyq = 0.5 * fs
    low = low_hz / nyq
    high = high_hz / nyq
    b, a = butter(order, [low, high], btype="bandpass")
    return filtfilt(b, a, x)
