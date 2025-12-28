from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MatchResult:
    tp: int
    fp: int
    fn: int
    sensitivity: float
    ppv: float


def match_peaks(
    ref: np.ndarray,
    pred: np.ndarray,
    fs: int,
    tol_ms: float = 150.0,
) -> tuple[int, int, int]:
    """
    Faz matching 1-para-1 entre picos de referência (ref) e preditos (pred)
    usando tolerância temporal em amostras (tol_ms).
    Estratégia greedy ordenada (padrão em avaliação de QRS):
      - Para cada pico predito, tenta casar com o pico ref mais próximo ainda não usado,
        desde que |pred-ref| <= tol.

    Retorna (TP, FP, FN).
    """
    ref = np.asarray(ref, dtype=int)
    pred = np.asarray(pred, dtype=int)

    ref.sort()
    pred.sort()

    tol = int(round((tol_ms / 1000.0) * fs))

    used_ref = np.zeros(len(ref), dtype=bool)
    tp = 0
    fp = 0

    # ponteiro para varrer ref eficientemente
    j = 0

    for p in pred:
        # avança j enquanto ref[j] < p - tol
        while j < len(ref) and ref[j] < p - tol:
            j += 1

        # candidatos possíveis são ref[j] (primeiro >= p-tol) e ref[j-1] (se existir)
        candidates = []
        if j < len(ref):
            candidates.append(j)
        if j - 1 >= 0:
            candidates.append(j - 1)

        best_k = None
        best_dist = None

        for k in candidates:
            if 0 <= k < len(ref) and not used_ref[k]:
                dist = abs(ref[k] - p)
                if dist <= tol and (best_dist is None or dist < best_dist):
                    best_dist = dist
                    best_k = k

        if best_k is not None:
            used_ref[best_k] = True
            tp += 1
        else:
            fp += 1

    fn = int(np.sum(~used_ref))
    return tp, fp, fn


def compute_metrics(tp: int, fp: int, fn: int) -> MatchResult:
    se = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    return MatchResult(tp=tp, fp=fp, fn=fn, sensitivity=se, ppv=ppv)
