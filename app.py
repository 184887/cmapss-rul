from datetime import date, timedelta
from pathlib import Path

import gradio as gr
import joblib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from cmapss.data import COLS

ROOT = Path(__file__).resolve().parent
BUNDLE = joblib.load(ROOT / "models" / "rul_modell.joblib")
MODELL, X, FEATURES = BUNDLE["modell"], BUNDLE["x"], BUNDLE["features"]
EKSEMPEL = ROOT / "data" / "raw" / "test_FD001.txt"
EKSEMPEL_LITEN = ROOT / "eksempeldata" / "flate_5_motorer.txt"

UKEDAGER = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]
MÅNEDER = ["januar", "februar", "mars", "april", "mai", "juni", "juli",
           "august", "september", "oktober", "november", "desember"]


def dato_tekst(d: date) -> str:
    return f"{UKEDAGER[d.weekday()]} {d.day}. {MÅNEDER[d.month - 1]} {d.year}"


def dager_til_service(pred_nå, flyturer_per_dag):
    """Hele dager til predikert RUL når servicegrensen x (0 = service nå)."""
    return np.floor(np.clip(pred_nå - X, 0, None) / flyturer_per_dag).astype(int)


def les_fil(path) -> pd.DataFrame:
    """Les en C-MAPSS-fil (26 kolonner skilt med mellomrom). Gir gr.Error ved feil format."""
    if path is None:
        raise gr.Error("Last opp en fil først.")
    try:
        df = pd.read_csv(path, sep=r"\s+", header=None)
    except Exception:
        raise gr.Error("Klarte ikke å lese filen. Den må være tekst med tall skilt med mellomrom.")

    if df.empty:
        raise gr.Error("Filen er tom.")
    if df.shape[1] != len(COLS):
        raise gr.Error(f"Filen har {df.shape[1]} kolonner, men må ha {len(COLS)} "
                       "(motor, syklus, 3 innstillinger og 21 sensorer), som C-MAPSS.")
    if not all(pd.api.types.is_numeric_dtype(t) for t in df.dtypes) or df.isna().any().any():
        raise gr.Error("Filen inneholder tekst eller tomme verdier. Alle verdier må være tall.")

    df.columns = COLS
    return df


def analyser(path, flyturer_per_dag):
    if not flyturer_per_dag or flyturer_per_dag <= 0:
        raise gr.Error("Flyturer per dag må være større enn 0.")

    df = les_fil(path)
    df["pred"] = MODELL.predict(df[FEATURES])

    siste = df.groupby("unit_nr").tail(1)
    sykluser = (siste["pred"] - X).clip(lower=0)      # sykluser til predikert RUL når x
    dager = dager_til_service(siste["pred"].values, flyturer_per_dag)

    tabell = pd.DataFrame({
        "Motor": siste["unit_nr"].values,
        "Sykluser kjørt": siste["time_cycles"].values,
        "Dager i drift": (siste["time_cycles"].values // flyturer_per_dag).astype(int),
        "Predikert RUL": siste["pred"].round().astype(int).values,
        "Sykluser til service": sykluser.round().astype(int).values,
        "Dager til service": dager,
        "Anbefalt servicedag": [(date.today() + timedelta(days=int(d))).isoformat() for d in dager],
        "Status": np.where(siste["pred"].values <= X, "Service nå", "OK"),
    }).sort_values(["Dager til service", "Predikert RUL"]).reset_index(drop=True)

    nå = (tabell["Status"] == "Service nå").sum()
    flåte = (f"### {nå} av {len(tabell)} motorer trenger service nå" if nå
             else f"### Ingen av {len(tabell)} motorer trenger service nå")

    motorer = tabell["Motor"].tolist()
    valgt = motorer[0]
    return (flåte, tabell, df, gr.Dropdown(choices=motorer, value=valgt),
            *tegn(df, valgt, flyturer_per_dag))


def tegn(df, motor, flyturer_per_dag):
    if df is None or motor is None:
        return None, ""
    d = df[df.unit_nr == motor]
    sist_syklus, sist_pred = d["time_cycles"].iloc[-1], d["pred"].iloc[-1]
    i_dag = date.today()
    dager = int(dager_til_service(sist_pred, flyturer_per_dag))
    service_dag = i_dag + timedelta(days=dager)

    # syklus -> dato: siste syklus er i dag, hver syklus er 1/flyturer_per_dag dag
    def til_dato(syklus):
        return pd.Timestamp(i_dag) + pd.to_timedelta((np.asarray(syklus) - sist_syklus) / flyturer_per_dag, unit="D")

    under = d[d["pred"] <= X]
    # allerede under grensen: marker første syklus det skjedde, ellers forventet syklus fremover
    service_syklus = under["time_cycles"].iloc[0] if sist_pred <= X else sist_syklus + (sist_pred - X)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(til_dato(d["time_cycles"]), d["pred"], color="#2a78d6", lw=2, label="Predikert RUL")
    if sist_pred > X:   # forleng med stigningstall −1 frem til servicegrensen
        ax.plot(til_dato([sist_syklus, service_syklus]), [sist_pred, X], color="#2a78d6", lw=2, ls=":",
                label="Forventet videre")
    ax.axhline(X, color="0.4", lw=1, ls="--", label=f"Servicegrense x = {X:.0f}")
    ax.axvline(pd.Timestamp(i_dag), color="0.2", lw=1)
    ax.text(pd.Timestamp(i_dag), ax.get_ylim()[1], " i dag", va="top", color="0.2")
    ax.plot(til_dato([service_syklus]), [X], "o", color="#eb6834", ms=10, zorder=3, label="Anbefalt service")
    punkt = til_dato([service_syklus])[0]   # for «service nå»: dagen grensen ble passert
    ax.annotate(f"{'' if dager else 'passert '}{punkt.day}. {MÅNEDER[punkt.month - 1]}",
                (punkt, X), textcoords="offset points", xytext=(0, -20),
                ha="center", color="#eb6834", fontweight="bold")

    ax.set_title(f"Motor {motor}")
    ax.set_xlabel("Dato"); ax.set_ylabel("Predikert RUL (flyturer)")
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax.grid(axis="y", color="0.9"); ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="center left")
    plt.close(fig)

    i_drift = int(sist_syklus // flyturer_per_dag)
    if dager == 0:
        overskrift = f"## Motor {motor}: anbefalt service **i dag**, {dato_tekst(i_dag)}"
    else:
        overskrift = f"## Motor {motor}: anbefalt service **{dato_tekst(service_dag)}** (om {dager} dager)"
    info = (f"{overskrift}\n"
            f"I drift i ca. {i_drift} dager ({sist_syklus} flyturer). "
            f"Predikert gjenværende levetid: ca. {sist_pred:.0f} flyturer.")
    return fig, info


with gr.Blocks(title="RUL – turbofan-motorer") as demo:
    gr.Markdown(
        "# Når bør motoren på service?\n"
        "Last opp sensordata for én eller flere turbofan-motorer i C-MAPSS-format. "
        f"Modellen ({type(MODELL).__name__}) predikerer gjenværende levetid (RUL) og anbefaler service "
        f"når predikert RUL går under **{X:.0f} sykluser**. "
        "Har du ikke egne data, klikk på eksempelfilen under."
    )
    with gr.Row():
        fil = gr.File(label="Sensordata (.txt)", file_types=[".txt"])
        flyturer = gr.Number(value=5, minimum=1, label="Flyturer per dag (1 syklus = 1 flytur)")
    knapp = gr.Button("Analyser", variant="primary")
    gr.Examples([[str(EKSEMPEL_LITEN), 5], [str(EKSEMPEL), 5]], inputs=[fil, flyturer],
                label="Eksempler: flåte på 5 motorer, eller hele NASA C-MAPSS testsett FD001 (100 motorer)")

    flåte = gr.Markdown()
    tabell = gr.Dataframe(label="Flåteoversikt (mest kritisk øverst)", interactive=False)
    motor = gr.Dropdown(label="Vis motor", choices=[])
    info = gr.Markdown()
    graf = gr.Plot(label="Predikert RUL")
    data = gr.State()

    knapp.click(analyser, [fil, flyturer], [flåte, tabell, data, motor, graf, info])
    motor.change(tegn, [data, motor, flyturer], [graf, info])


if __name__ == "__main__":
    demo.launch()
