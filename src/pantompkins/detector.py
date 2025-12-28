from __future__ import annotations

import numpy as np

from pantompkins.peaks import local_peaks


def derivative_5pt(x: np.ndarray) -> np.ndarray:
    y = np.zeros_like(x)
    y[2:-2] = (-x[0:-4] - 2 * x[1:-3] + 2 * x[3:-1] + x[4:]) / 8.0
    return y


def moving_window_integration(x: np.ndarray, window_samples: int) -> np.ndarray:
    if window_samples <= 1:
        return x.copy()
    w = np.ones(window_samples) / float(window_samples)
    return np.convolve(x, w, mode="same")


def preprocess_for_qrs(x_bp: np.ndarray, fs: int, mwi_ms: float = 150.0) -> dict[str, np.ndarray]:
    d = derivative_5pt(x_bp)
    sq = d * d
    win = max(1, int(round((mwi_ms / 1000.0) * fs)))
    mwi = moving_window_integration(sq, win)
    return {"derivative": d, "squared": sq, "mwi": mwi}


def detect_r_peaks_from_mwi(
    mwi: np.ndarray,
    raw_bp: np.ndarray,
    fs: int,
    refractory_ms: float = 200.0,
    init_seconds: float = 2.0,
) -> np.ndarray:
    """
    Detector MVP inspirado no Pan-Tompkins:
      - picos locais no MWI
      - threshold adaptativo (SPKI/NPKI -> THR1)
      - refratário
      - refino do pico: escolhe máximo no raw_bp em janela curta ao redor do candidato

    Retorna índices de amostra (inteiros) aproximando R-peaks.
    """
    n = len(mwi)
    if n == 0:
        return np.array([], dtype=int)

    refr = max(1, int(round((refractory_ms / 1000.0) * fs)))
    init_n = min(n, int(round(init_seconds * fs)))

    # picos candidatos no MWI
    cand = local_peaks(mwi)
    if len(cand) == 0:
        return np.array([], dtype=int)

    # --- inicialização de thresholds (Pan-Tompkins style) ---
    init_peaks = cand[cand < init_n]
    if len(init_peaks) == 0:
        init_peaks = cand[: min(len(cand), 10)]

    init_vals = mwi[init_peaks]
    spki = 0.25 * float(np.max(init_vals))  # sinal
    npki = 0.5 * float(np.mean(init_vals))  # ruído (heurístico)
    thr1 = npki + 0.25 * (spki - npki)

    r_locs: list[int] = []
    last_r = -10**9

    # janela de refino no raw_bp (procura máximo local próximo ao candidato)
    refine = max(1, int(round(0.08 * fs)))  # ~80 ms

    for idx in cand:
        peak_val = float(mwi[idx])

        # respeita refratário (em amostras)
        if idx - last_r < refr:
            continue

        if peak_val >= thr1:
            # classifica como QRS
            spki = 0.125 * peak_val + 0.875 * spki

            # refina posição no raw_bp
            left = max(0, idx - refine)
            right = min(n, idx + refine + 1)
            r = int(left + np.argmax(raw_bp[left:right]))

            r_locs.append(r)
            last_r = r
        else:
            # classifica como ruído
            npki = 0.125 * peak_val + 0.875 * npki

        thr1 = npki + 0.25 * (spki - npki)

    return np.array(r_locs, dtype=int)
