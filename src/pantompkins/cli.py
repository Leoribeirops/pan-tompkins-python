from __future__ import annotations

from pantompkins.io import load_mitbih_record
from pantompkins.filters import bandpass_butter
from pantompkins.detector import preprocess_for_qrs, detect_r_peaks_from_mwi


def main() -> None:
    record = input("Record (ex: 100): ").strip()
    if not record:
        raise ValueError("Record inválido (vazio).")

    data = load_mitbih_record(record, channel=0, pn_dir="mitdb")

    x_bp = bandpass_butter(data.signal, data.fs, low_hz=5.0, high_hz=15.0, order=2)
    feats = preprocess_for_qrs(x_bp, data.fs, mwi_ms=150.0)

    r_pred = detect_r_peaks_from_mwi(feats["mwi"], x_bp, data.fs)

    print(f"[OK] record={data.record_name} fs={data.fs} N={len(data.signal)}")
    print(f"[OK] annotations R-peaks: {len(data.r_peaks)}")
    print(f"[OK] predicted  R-peaks: {len(r_pred)}")


if __name__ == "__main__":
    main()
