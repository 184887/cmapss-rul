# Når bør motoren på service?

Prediksjon av gjenværende levetid (RUL) for turbofanmotorer med NASA C-MAPSS (FD001), og en nettside som anbefaler servicedato for hver motor i en flåte. Laget som ML-prosjekt i DAT158 ved HVL.

- **Nettside:** https://cmapss-rul.onrender.com
- **Rapport:** [RAPPORT.md](RAPPORT.md)

## Prøv nettsiden

Nettsiden ligger på gratisplanen til Render og sovner når den ikke er i bruk, så første besøk kan ta 30–60 sekunder. Klikk på en av eksempelfilene og trykk *Analyser*.

- `flate_5_motorer.txt`: en liten flåte på 5 motorer
- `test_FD001.txt`: hele testsettet fra NASA (100 motorer)

Du kan også laste opp din egen fil i samme format som C-MAPSS (mellomromsseparert, 26 kolonner: motornummer, syklus, 3 driftsinnstillinger og 21 sensorer).

## Kort om løsningen

- **Data:** FD001 (én driftstilstand, én feiltype). 14 av 21 sensorer brukes, de 7 konstante er fjernet. RUL er kuttet ved 125.
- **Modell:** GradientBoosting med quantile loss (alpha ≈ 0,10), tunet med Optuna. Den gjetter heller for lavt enn for høyt, siden det er farligst å komme for sent.
- **Modellvalg:** gjennomsnittlig NASA-score for rader med sann RUL ≤ 40, med 5-delt kryssvalidering delt per motor.
- **Servicegrense:** service anbefales når predikert RUL går under x = 4,5 sykluser. x er satt på valideringssettet slik at 95 % får service før svikt.

| Modell           | NASA ≤ 40 (val) | RMSE (test) | NASA (test) |
| ---------------- | --------------- | ----------- | ----------- |
| Lineær regresjon | 8,39            | 21,9        | 1 299       |
| GB quantile      | 0,77            | 32,3        | 2 608       |

GB quantile har dårligere RMSE totalt, men er mye bedre nær svikt, som er der servicen bestemmes. Se rapporten for detaljer.

## Struktur

```
app.py                  Nettsiden (Gradio)
cmapss/data.py          Innlesing, RUL-label, NASA-score og plott
cmapss/features.py      Listen over de 14 sensorene som brukes
notebooks/RUL.ipynb     Utforsking, modellvalg, tuning, servicegrense og testing
models/rul_modell.joblib  Lagret modell med x, features og scikit-learn-versjon
eksempeldata/           Eksempelfil for nettsiden
figurer/                Figurer brukt i rapporten
data/raw/               C-MAPSS-filer (bare testfilene for FD001 ligger i Git)
```

## Kjør selv

Prosjektet bruker Python 3.12. Med [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/184887/cmapss-rul.git
cd cmapss-rul
uv sync
uv run python app.py
```

Eller med pip:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Nettsiden kjører da på http://localhost:7860. Den bruker den lagrede modellen, så den trenger ikke treningsdata.

For å kjøre notebooken og trene modellen på nytt trengs også `train_FD001.txt`. Last ned C-MAPSS fra [NASA sitt data-repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) og legg filene i `data/raw/`.

## Data

Saxena, A., Goebel, K., Simon, D. & Eklund, N. (2008). *Damage propagation modeling for aircraft engine run-to-failure simulation.* PHM08.
