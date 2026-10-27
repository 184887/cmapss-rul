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
- [x] KNN, SVR og MLP (med StandardScaler i Pipeline) → MLP 22,8, SVR 28,4, KNN 42,8
- [x] Optuna (100 forsøk) på GB med loss og alpha → quantile-loss, alpha ≈ 0,10: NASA 1,15
- [x] Velg endelig modell → GradientBoosting med quantile-loss (Optuna)
- [x] Sluttsjekk på valideringssettet (NASA ≤ 40: 0,77 mot LR 8,39), ny x = 4,5, lagret modell (0,4 MB)
- [x] Feature importance for valgt modell (`figurer/feature_importance.png`)
- [ ] Finn resultater fra andre på FD001 (litteratur-baseline)
- [ ] Rydd i notebooken: fjern TODO-er, oppdater innholdsliste, kort tolkning etter hvert resultat
- [x] Restart & Run All (27.10)
- [ ] Commit

## Nettside (lør 24. – man 26.)
- [x] Bestem hvordan modell og testdata kommer til serveren → alt i Git
- [x] Bygg Gradio-app (`app.py`): last opp fil, flyturer per dag, flåtetabell, graf, feilmeldinger
- [x] Tydelig anbefalt servicedag (ukedag + dato), dager i drift, datoakse i grafen
- [x] Liten testfil til læreren: `eksempeldata/flate_5_motorer.txt`
- [x] Avhengigheter: gradio i `pyproject.toml`, låste versjoner i `requirements.txt`
- [x] Velg hosting → Render gratisplan (HF Spaces krever PRO for Gradio)
- [x] Deployet på Render: https://cmapss-rul.onrender.com
- [ ] Test i inkognitovindu
- [ ] Ta opp kort skjermvideo som reserve
- [ ] **Hvis ikke deployet innen man 26.: lag video av lokal versjon**

## Rapport (tir 27. – tor 29.) – maks 3000 ord (ikke minimum)
### Toppen
- [ ] Prosjektnavn, navn og dato
- [ ] Videolenke (eller fjern linjen)

### 1.1 Scope
- [x] Problem: ulik slitasje, faste intervaller, for sent er verst
- [ ] Overgang: man vet ikke hvor slitt hver motor er
- [x] Mål og bruker
- [x] Hvorfor ML (vurder å legge til støy og flåtestørrelse)
- [x] Hvordan systemet brukes (3 steg)
- [x] Business impact
- [ ] Ressurser: simulerte NASA-data, egen PC, gratis hosting

### 1.2 Metrics og suksesskriterium
- [ ] RMSE og hvorfor den ikke er nok
- [ ] NASA-score: sen prediksjon straffes hardere (kobles til problemet)
- [ ] Hovedmetrikk: NASA-score på RUL ≤ 40, og hvorfor G = 40
- [ ] Servicegrense x: 95 % får service før svikt
- [ ] Suksesskriterium: hva er minimum for at systemet er nyttig?

### 2: Data (maks ~500 ord)
- [ ] Kilde og delsett FD001 (simulert, én driftstilstand, én feiltype)
- [ ] Mengde: antall motorer og rader i train og test
- [ ] Label: RUL og hvorfor den klippes ved 125
- [ ] Testsettet er kuttet før svikt
- [ ] Fjernede sensorer → 14 features, og hvorfor
- [ ] Skalering og tidsvinduer (brukt / ikke brukt, og hvorfor)
- [ ] Etikk og representasjon
- [ ] Figurer: sensorkurver og korrelasjon (lagre til `figurer/`)

### 3: Modellering (maks ~1000 ord)
- [ ] Oppdeling gruppert på motor og kryssvalidering, og hvorfor
- [ ] Baseline: Dummy og LR
- [ ] Modellene som ble testet, hyperparametersøk og Optuna
- [ ] Fyll inn tomme celler i resultattabellene fra notebooken
- [ ] Hvorfor GB-quantile tross dårligere RMSE (feilanalyse)
- [ ] Feature importance (graf ferdig, tekst mangler)
- [ ] Sammenligning med litteraturen på FD001 (kilder mangler)
- [ ] Figurer: nasa_per_rul, scatter, feilhistogram, RUL per syklus

### 4: Deployment (maks ~550 ord)
- [ ] Hvor og hvordan den er deployet (nettside-lenken)
- [ ] Modellpakken (joblib) og låste versjoner
- [ ] Hva brukeren legger inn og får ut
- [ ] Overvåking og vedlikehold
- [ ] Svakheter og forbedringer
- [ ] Skjermbilder av tabell og graf

### 5: Referanser
- [ ] Artikler du sammenligner med på FD001
- [ ] Beskriv hva Claude Code er brukt til
- [ ] Hosting-referansen stemmer med der appen faktisk ligger
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
