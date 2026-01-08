from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

def build_figures(
    fs,
    x,
    x_hp,
    mwi,
    start_s=0,
    dur_s=10,
):
    """
    Constrói figuras matplotlib e as retorna,
    sem chamar plt.show().
    """

def plot_signals(
    x_in: np.ndarray,
    x_hp: np.ndarray,
    mwi: np.ndarray,
    fs: int,
    start_s: float = 0.0,
    dur_s: float = 10.0,
) -> None:
    """
    Plota três figuras separadas:
      1) Sinal de entrada
      2) Saída do passa-alta
      3) MWI

    start_s/dur_s controlam a janela temporal para visualização.
    """
    n = len(x_in)
    i0 = max(0, int(round(start_s * fs)))
    i1 = min(n, int(round((start_s + dur_s) * fs)))
    t = np.arange(i0, i1) / fs

    # 1) Entrada
    plt.figure()
    plt.plot(t, x_in[i0:i1])
    plt.title("Entrada (ECG bruto)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()

    # 2) Passa-alta
    plt.figure()
    plt.plot(t, x_hp[i0:i1])
    plt.title("Saída após filtro passa-alta")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()

    # 3) MWI
    plt.figure()
    plt.plot(t, mwi[i0:i1])
    plt.title("MWI (Moving Window Integration)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude (unidade relativa)")
    plt.grid(True)
    plt.tight_layout()

    plt.show()
