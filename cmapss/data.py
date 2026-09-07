from pathlib import Path
import pandas as pd



DATA_DIR = Path(__file__).resolve().parents[1] / "data"

COLS = (["unit_nr", "time_cycles"]
        + [f"setting_{i}" for i in range(1, 4)]
        + [f"s_{i}" for i in range(1, 22)])


def load_raw(subset: str, split: str) -> pd.DataFrame:
    path = DATA_DIR / "raw" / f"{split}_{subset}.txt"
    return pd.read_csv(path, sep=r"\s+", header=None, names=COLS)