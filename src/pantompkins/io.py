from __future__ import annotations
from dataclasses import dataclass
import wfdb
import numpy as np


@dataclass
class RecordData:
    record_name: str
    fs: int
    signal: np.ndarray
    r_peaks: np.ndarray


def load_mitbih_record(record: str, channel: int = 0, pn_dir: str = "mitdb") -> RecordData:
    """
    Loads MIT-BIH record via PhysioNet using WFDB.
    Default pn_dir='mitdb' makes WFDB fetch/cache the record automatically.
    """
    rec = wfdb.rdrecord(record, pn_dir=pn_dir)
    fs = int(rec.fs)
    sig = rec.p_signal[:, channel].astype(float)

    ann = wfdb.rdann(record, "atr", pn_dir=pn_dir)
    r = np.array(ann.sample, dtype=int)

    return RecordData(record_name=record, fs=fs, signal=sig, r_peaks=r)
