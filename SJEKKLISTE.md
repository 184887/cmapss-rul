# Sjekkliste – DAT158 ML assignment 2

**Frist: fredag 30. oktober 2026 kl. 23:59** · Lever lenke til repoet på Canvas (hver person leverer selv)

## Oppstart (man 19. – tir 20.)
- [x] Les oppgaveteksten og rapportmalen
- [x] Opprett `RAPPORT.md` og `figurer/`
- [ ] Avklar gruppe (2–3 personer) og fordel arbeid
- [x] Commit ucommittede endringer (d3961ac)

## Modell (ons 21. – fre 23.)
- [x] Sammenlign Dummy, LR og RF på valideringssettet (snitt av NASA-score)
- [x] Graf: NASA-score og feil per sann RUL (`figurer/nasa_per_rul.png`)
- [x] Bestem grensen for «lav RUL»: G = 40 (litt over en uke ledetid)
- [x] Kryssvalidering (GroupKFold, 5 folder) av LR, RF, ExtraTrees, GB og HistGB → LR best (14,8), RF 24,2
- [x] Hyperparametersøk (RandomizedSearchCV, 50 iter) på ExtraTrees og GB → ExtraTrees 15,2, GB 20,6
- [ ] **Velg endelig modell: LR eller ExtraTrees (uavgjort innenfor støyen)** ← her står vi
- [ ] Oppdater 5.3–5.5: sluttsjekk på valideringssettet, ny x, lagre ny modell
- [ ] Feature importance for valgt modell (graf til rapporten)
- [ ] Finn resultater fra andre på FD001 (litteratur-baseline)
- [ ] Rydd i notebooken: fjern TODO-er, oppdater innholdsliste, kort tolkning etter hvert resultat
- [ ] Restart & Run All, så commit

## Nettside (lør 24. – man 26.)
- [x] Bestem hvordan modell og testdata kommer til serveren → alt i Git
- [x] Bygg Gradio-app (`app.py`): last opp fil, flyturer per dag, flåtetabell, graf, feilmeldinger
- [x] Tydelig anbefalt servicedag (ukedag + dato), dager i drift, datoakse i grafen
- [x] Liten testfil til læreren: `eksempeldata/flate_5_motorer.txt`
- [x] Avhengigheter: gradio i `pyproject.toml`, låste versjoner i `requirements.txt`
- [x] Velg hosting → Hugging Face Spaces (`deploy.py`)
- [ ] Lag HF-konto + token, `uv run hf auth login`, kjør `deploy.py`, test i inkognitovindu
- [ ] Ta opp kort skjermvideo som reserve
- [ ] **Hvis ikke deployet innen man 26.: lag video av lokal versjon**

## Rapport (tir 27. – tor 29.) – maks 3500 ord
- [ ] 1: Problem – scope (~700 ord inkl. metrics)
- [ ] 1: Problem – metrics og suksesskriterium
- [ ] 2: Data (~600 ord)
- [ ] 3: Modellering med resultattabell og figurer (~1200 ord)
- [ ] 4: Deployment med lenke/skjermbilder (~700 ord)
- [ ] 5: Referanser, inkl. bruk av Claude Code
- [ ] Fjern alle stikkord og instruksjoner fra malen
- [ ] Sjekk ordtelling

## Repo og reproduserbarhet (tor 29.)
- [ ] Ny `README.md`: kort beskrivelse, lenke til rapport, nettside og video
- [ ] «Kjør selv»: `uv sync`, last ned data til `data/raw/`, tren modell, kjør app, deploy
- [ ] Slett tomme mapper `Test/` og `prep/`
- [ ] Klon repoet i en tom mappe og følg README steg for steg
- [ ] Repoet er offentlig (✅ allerede)

## Levering (fre 30.)
- [ ] Siste push
- [ ] Lever lenken på Canvas (alle i gruppen)
