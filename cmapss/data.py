from pathlib import Path
import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"

COLS = (["unit_nr", "time_cycles"]
        + [f"setting_{i}" for i in range(1, 4)]
        + [f"s_{i}" for i in range(1, 22)])


def load_raw(subset: str, split: str) -> pd.DataFrame:
    path = DATA_DIR / "raw" / f"{split}_{subset}.txt"
    if not path.exists():
        raise FileNotFoundError(
            f"Fant ikke {path}. Last ned C-MAPSS fra NASA og legg filene i data/raw/.")
    return pd.read_csv(path, sep=r"\s+", header=None, names=COLS)


def add_rul(df: pd.DataFrame, clip: int | None = 125) -> pd.DataFrame:
    """Legg til RUL (sykluser igjen til svikt). Kun for treningsdata."""
    # siste syklus for hver motor, spredt ut på alle radene til motoren
    max_cycle = df.groupby("unit_nr").time_cycles.transform("max")
    df = df.assign(RUL=max_cycle - df.time_cycles)

    # motoren er «frisk» tidlig i livet, så RUL over clip gir ingen info
    if clip is not None:
        df["RUL"] = df["RUL"].clip(upper=clip)
    return df
