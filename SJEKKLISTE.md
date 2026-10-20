# Sjekkliste – DAT158 ML assignment 2

**Frist: fredag 30. oktober 2026 kl. 23:59** · Lever lenke til repoet på Canvas (hver person leverer selv)

## Oppstart (man 19. – tir 20.)
- [x] Les oppgaveteksten og rapportmalen
- [x] Opprett `RAPPORT.md` og `figurer/`
- [ ] Avklar gruppe (2–3 personer) og fordel arbeid
- [ ] Commit ucommittede endringer

## Modell (ons 21. – fre 23.)
- [x] Sammenlign Dummy, LR og RF på valideringssettet (snitt av NASA-score)
- [x] Graf: NASA-score og feil per sann RUL (`figurer/nasa_per_rul.png`)
- [x] Bestem grensen for «lav RUL»: G = 40 (litt over en uke ledetid)
- [x] Velg modell på snitt-NASA for rader med RUL ≤ 40 → RandomForest
- [x] Regn ut servicegrensen x = 95-persentilen av (pred − sann) på de samme radene → x ≈ 28
- [ ] Feature importance for RF (graf til rapporten)
- [ ] Finn resultater fra andre på FD001 (litteratur-baseline)
- [x] Lagre endelig modell (trent på `X_train`) + x + features med `joblib` → `models/rul_modell.joblib` (18 MB)
- [ ] Rydd i notebooken: fjern TODO-er, oppdater innholdsliste, kort tolkning etter hvert resultat
- [ ] Restart & Run All, så commit

## Nettside (lør 24. – man 26.)
- [ ] Bestem hvordan modell, `test_FD001.txt` og `RUL_FD001.txt` kommer til serveren
- [ ] Bygg Gradio-app: velg testmotor, vis graf av predikert RUL per syklus, marker servicepunkt
- [ ] Legg `gradio` og `joblib` i `pyproject.toml`, lås sklearn-versjon
- [ ] Deploy til Hugging Face Spaces og test i inkognitovindu
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
