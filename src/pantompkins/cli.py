from __future__ import annotations

from pantompkins.io import load_mitbih_record
from pantompkins.filters import highpass_butter, bandpass_butter
from pantompkins.detector import preprocess_for_qrs
from pantompkins.plots import plot_signals


def main() -> None:
    record = input("Record (ex: 100): ").strip()
    if not record:
        raise ValueError("Record inválido (vazio).")

    data = load_mitbih_record(record, channel=0, pn_dir="mitdb")

    # 1) HPF explícito
    x_hp = highpass_butter(data.signal, data.fs, cutoff_hz=5.0, order=2)

    # 2) Para o MWI, seguimos o pipeline clássico (bandpass -> deriv -> square -> MWI)
    x_bp = bandpass_butter(data.signal, data.fs, low_hz=5.0, high_hz=15.0, order=2)
    feats = preprocess_for_qrs(x_bp, data.fs, mwi_ms=150.0)

    print(f"[OK] record={data.record_name} fs={data.fs} N={len(data.signal)}")
    print(f"[OK] annotations R-peaks: {len(data.r_peaks)}")
    print("[OK] plotting signals (entrada, passa-alta, MWI)")

    # Janela de visualização (ex.: primeiros 10s). Ajuste se quiser.
    plot_signals(
        x_in=data.signal,
        x_hp=x_hp,
        mwi=feats["mwi"],
        fs=data.fs,
        start_s=0.0,
        dur_s=10.0,
    )


if __name__ == "__main__":
    main()
