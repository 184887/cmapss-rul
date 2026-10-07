from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

COLS = (["unit_nr", "time_cycles"]
        + [f"setting_{i}" for i in range(1, 4)]
        + [f"s_{i}" for i in range(1, 22)])


def _read(filename: str, names: list[str]) -> pd.DataFrame:
    path = DATA_DIR / "raw" / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Fant ikke {path}. Last ned C-MAPSS fra NASA og legg filene i data/raw/.")
    return pd.read_csv(path, sep=r"\s+", header=None, names=names)


def load_raw(subset: str, split: str) -> pd.DataFrame:
    return _read(f"{split}_{subset}.txt", COLS)


def load_rul_truth(subset: str) -> pd.DataFrame:
    df = _read(f"RUL_{subset}.txt", ["RUL"])
    df["unit_nr"] = df.index + 1
    return df


def add_rul(df: pd.DataFrame, clip: int | None = 125) -> pd.DataFrame:
    """Legg til RUL (sykluser igjen til svikt). Kun for treningsdata."""
    # siste syklus for hver motor, spredt ut på alle radene til motoren
    max_cycle = df.groupby("unit_nr").time_cycles.transform("max")
    df = df.assign(RUL=max_cycle - df.time_cycles)

    if clip is not None:
        df["RUL"] = df["RUL"].clip(upper=clip)
    return df

def plot(val, y_val, y_pred, motorer):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharey=True)
    for ax, motor in zip(axes.flat, motorer):
        maske = (val.unit_nr == motor).values
        ax.plot(val.time_cycles[maske], y_val[maske], "b", label="Sann RUL")
        ax.plot(val.time_cycles[maske], y_pred[maske], "r", label="Predikert RUL")
        ax.set_title(f"Motor {motor}")
        ax.set_xlabel("Syklus")
    axes[0, 0].legend()
    plt.show()

def nasa_score(y_true, y_pred):
    d = np.asarray(y_pred) - np.asarray(y_true)
    return np.sum(np.where(d < 0, np.exp(-d / 13), np.exp(d / 10)) - 1)
