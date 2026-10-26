<!--
SJEKKLISTE FØR INNLEVERING (fredag 30. oktober 2026 kl. 23:59)
- [ ] Alle stikkord og kommentarer fra malen fjernet
- [ ] Under 3500 ord
- [ ] Lenke til nettside og/eller video i seksjon 4
- [ ] Bruk av Claude Code oppgitt i referanser
- [ ] Figurer lagt i figurer/ og vises riktig på GitHub

Ordbudsjett: 1 ~700 · 2 ~600 · 3 ~1200 · 4 ~700 · 5 (referanser teller ikke mye)
Figurer: lagre fra notebooken med plt.savefig("../figurer/navn.png", dpi=150, bbox_inches="tight")
og vis dem her med ![beskrivelse](figurer/navn.png)

Slik bruker du malen: hver seksjon har "Stikkord" (fakta du har), "Spørsmål å svare på"
(ting sensor vil se begrunnet) og "Kilde" (hvor i notebooken/koden tallene står).
Skriv teksten under "#### Tekst", og slett resten til slutt.
-->

# [Prosjektnavn]

[Navn], [Dato]

GitHub: https://github.com/184887/cmapss-rul
Nettside: https://cmapss-rul.onrender.com
Video: [lenke, reserve]


## 1: Beskriv problemet  (~700 ord)

### 1.1 Scope
<!-- Fra malen: mål, hvorfor ML, hvordan systemet brukes, hvordan løses det i dag, manuell løsning uten ML, hvem er brukeren, business impact, system/pipeline, ressurser -->

Stikkord:
- Mål: forutsi RUL (antall sykluser igjen før svikt) for turbofan-motorer
- Bruker: flåteoperatør / vedlikeholdsplanlegger, ikke enkeltpersoner
- Bruk: last opp sensordata for flåten → anbefalt servicedag per motor, mest kritisk først
- Beslutning: service når predikert RUL < x (prediksjon og beslutningsregel er to separate ting)
- Antakelse: 1 syklus ≈ 1 flytur, brukeren velger flyturer per dag
- Dagens løsning: faste serviceintervaller (tid/sykluser) vs. tilstandsbasert vedlikehold
- Uten ML: fast intervall, eller manuelle terskler på enkeltsensorer
- Business impact: for tidlig service = bortkastet levetid og kostnad, for sen = svikt, sikkerhet, AOG
- Pipeline: rådata → features → modell → servicegrense → nettside
- Ressurser: egen PC, gratis hosting (HF Spaces), simulerte data

Spørsmål å svare på:
- Hvorfor er dette et ML-problem og ikke bare en terskel på én sensor?
- Hva er dyrest: for tidlig eller for sen service? (Dette begrunner hele metrikkvalget.)
- Hva er begrensningen ved at dataene er simulerte?

#### Tekst


### 1.2 Metrics og suksesskriterium
<!-- Fra malen: ML-metrikker, kobling til business objective, minimum for suksess -->

Stikkord:
- RMSE: standard, symmetrisk, sammenlignbart med litteraturen
- NASA-score: asymmetrisk, sen prediksjon straffes hardere → passer kostnaden ved svikt
- Hovedmetrikk for modellvalg: snitt NASA-score på rader med sann RUL ≤ G, G = 40
- Hvorfor G = 40: ca. én uke ledetid ved 4–6 flyturer per dag
- Hvorfor bare lav RUL: det er der servicebeslutningen tas, langt fra svikt betyr feilen lite
- Servicegrense x: 95-persentilen av feil (pred − sann) på lav-RUL-rader → 95 % får service før svikt
- Suksesskriterium (forslag): x ≤ G, 0 % sene servicer på validering, slå baseline (Dummy, LR)

Spørsmål å svare på:
- Hvorfor er ikke lav RMSE nok for denne brukeren?
- Hva er minimum for at systemet er nyttig i praksis?

#### Tekst



## 2: Data  (~600 ord)
<!-- Fra malen: hva slags data, kilde, mengde, labels/ground truth, nøyaktighet, personvern/etikk, representasjon, rensing, feature engineering, skalering -->

Stikkord:
- NASA C-MAPSS, delsett FD001: én driftstilstand, én feiltype (HPC-degradering)
- Simulerte run-to-failure-forløp (Saxena et al., 2008)
- Mengde: 100 motorer i train, 100 i test, rader = sykluser (fyll inn antall rader)
- Kolonner: unit_nr, syklus, 3 driftsinnstillinger, 21 sensorer
- Label: RUL = siste syklus − nåværende syklus, klippet ved 125
- Testsett: kuttet før svikt, sann RUL kun for siste syklus (RUL_FD001.txt)
- Rensing: konstante/døde sensorer fjernet → 14 features (cmapss/features.py)
- Skalering: ikke nødvendig for trær/LR, StandardScaler i Pipeline for KNN/SVR/MLP
- Ikke brukt: tidsvinduer, rullerende snitt (→ videre arbeid)
- Etikk/personvern: ingen persondata; risiko ved å stole på modellen i sikkerhetskritisk bruk
- Representasjon: simulert, én tilstand → generaliserer ikke direkte til ekte motorer eller FD002–FD004

Spørsmål å svare på:
- Hvorfor klippe RUL ved 125? (Hva skjer med motoren tidlig i livet?)
- Hvorfor fjerne sensorene, og hvordan fant du ut hvilke?
- Hva betyr det at testmotorene er kuttet før svikt for evalueringen?

Figurer:
- Sensorkurver mot RUL (notebook 3.1)
- Korrelasjon med RUL (notebook 3.2)
- Evt. histogram over levetid per motor

Kilde: notebook seksjon 2–4, cmapss/data.py, cmapss/features.py

#### Tekst



## 3: Modellering  (~1200 ord)
<!-- Fra malen: modeller utforsket, baseline, resultater fra andre, alle metrikker (tabell/graf), feilanalyse, feature importance -->

### 3.1 Oppsett og validering
Stikkord:
- GroupShuffleSplit på unit_nr, 80/20 → hvorfor gruppere på motor? (lekkasje mellom sykluser)
- GroupKFold(5) kryssvalidering på treningsdelen for modellvalg
- Valideringssett: valg av modell og x · Testsett: kun til slutt (unngå lekkasje)
- Baseline: DummyRegressor (snitt) og LinearRegression

### 3.2 Modeller utforsket
Stikkord:
- Trær: RandomForest, ExtraTrees, GradientBoosting, HistGB
- Andre: KNN, SVR, MLP (med StandardScaler)
- Hyperparametersøk: RandomizedSearchCV (50 iter) på ET og GB
- Optuna (100 forsøk, TPE) på GB, inkl. loss og alpha → quantile-loss, alpha ≈ 0,10
- Mønster: fleksible modeller bedre RMSE, men dårligere worst-case på enkelte motorer (90, 65)
- Valgt modell: GB med quantile-loss → predikerer bevisst lavt (konservativ)
- Sjekk mot metric gaming: ut-av-fold service ved median 14 sykluser igjen (LR 28, ET 30), 0 % for sent

Resultattabell (CV, NASA snitt på RUL ≤ 40, lavere er bedre):

| Modell | CV NASA ≤ 40 | CV RMSE | Kommentar |
|---|---|---|---|
| Dummy | | | |
| LinearRegression | 14,8 | | |
| RandomForest | 24,2 | | katastrofal på motor 90/65 |
| ExtraTrees (tunet) | 15,2 | | |
| GradientBoosting (tunet) | 20,6 | | |
| MLP | 22,8 | 18,65 | best RMSE |
| SVR | 28,4 | | |
| KNN | 42,8 | | |
| GB quantile (Optuna) | 1,15 | | valgt |

Validering og test, valgt modell vs. LR:

| Modell | NASA ≤ 40 val | RMSE val | RMSE test | NASA test (sum) | x |
|---|---|---|---|---|---|
| LinearRegression | 8,39 | | | 1299 | |
| GB quantile | 0,77 | 33 | | 2608 | 4,5 |

### 3.3 Feilanalyse
Stikkord:
- GB-quantile: høy RMSE og test-NASA fordi den underestimerer ~30 sykluser langt fra svikt
- Nær svikt (sann RUL ≤ 40, n = 28): NASA-sum 30 for GB vs. 756 for LR → det er her beslutningen tas
- Avveining: total score vs. score der det betyr noe
- Prediksjonene er støyete mellom sykluser; beslutning bruker bare siste syklus
- Klipp ved 125 gjør at modellen aldri sier mer enn 125 igjen

Spørsmål å svare på:
- Hvorfor er en "dårligere" modell på RMSE likevel det riktige valget?
- Er det rettferdig å sammenligne med litteraturen når du optimaliserer en annen metrikk?

### 3.4 Feature importance og litteratur
Stikkord:
- Feature importance for GB-quantile (ikke laget ennå → graf)
- Litteratur på FD001: typisk RMSE ~12–20 med LSTM/CNN og tidsvinduer (finn konkrete kilder)

Figurer:
- figurer/nasa_per_rul.png (NASA-score og feil per sann RUL)
- Sann vs. predikert (scatter) og feilhistogram (notebook 6)
- Predikert RUL per syklus for noen motorer
- Feature importance

Kilde: notebook seksjon 5.1–5.5 og 6

#### Tekst



## 4: Deployment  (~700 ord)
<!-- Fra malen: hvordan deployet, hvordan prediksjonene brukes, overvåking og vedlikehold, forbedringer, lenke/skjermbilder -->

Stikkord:
- Gradio-app (app.py) på Render (gratisplan), bygges automatisk fra GitHub ved hver push til main
- Hugging Face Spaces ble forkastet: Gradio-Spaces krever nå betalt PRO
- Gratisplanen sover etter inaktivitet → første besøk tar 30–60 sek
- Modellen trenes lokalt i notebooken, lagres som én joblib-pakke: modell, x, features, sklearn-versjon
- Låste versjoner i requirements.txt (joblib/sklearn må matche)
- Input: last opp fil i C-MAPSS-format, eksempelfil til læreren (eksempeldata/flate_5_motorer.txt)
- Brukeren velger flyturer per dag → servicedato
- Output: flåtetabell (mest kritisk først, dager i drift), anbefalt servicedag med ukedag + dato
- Graf per motor: predikert RUL per syklus, datoakse, "i dag"-linje, servicepunkt markert
- Feilhåndtering: tydelige feilmeldinger ved feil filformat
- Overvåking: sammenligne predikert vs. faktisk svikt/service, data drift i sensorene, retrening
- Vedlikehold: ny modell = kjør notebooken, lagre pakke, deploy på nytt

Svakheter / forbedringer:
- Beslutning bare på siste prediksjon → glatting over flere sykluser
- Klipp ved 125 → maks ~19 dager til service ved 5 flyturer per dag
- Tidsvinduer/rullerende features, FD002–FD004, ekte data, usikkerhetsintervall

Spørsmål å svare på:
- Hvordan ville en ekte flåteoperatør brukt dette i hverdagen?
- Hva må på plass før dette kan brukes i en sikkerhetskritisk setting?

Figurer: skjermbilde av flåtetabell og graf

Lenke: [nettside]  Video: [lenke]

#### Tekst



## 5: Referanser

- Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). Damage propagation modeling for aircraft engine run-to-failure simulation. *International Conference on Prognostics and Health Management (PHM08)*.
- NASA Prognostics Center of Excellence – C-MAPSS dataset: [lenke]
- scikit-learn: Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR* 12, 2825–2830.
- Optuna: Akiba et al. (2019). Optuna: A Next-generation Hyperparameter Optimization Framework. *KDD*.
- Gradio: https://www.gradio.app/
- Render: https://render.com/docs/free
- Anthropic Claude Code – AI-kodeverktøy brukt til: [beskriv hva, f.eks. kode til app og deploy, forklaring av begreper; modellvalg og beslutninger tatt selv]
- [Artikler du sammenligner resultater med på FD001]
