<!--
SJEKKLISTE FØR INNLEVERING (fredag 30. oktober 2026 kl. 23:59)
- [ ] Alle stikkord og kommentarer fra malen fjernet
- [ ] Under 3500 ord
- [ ] Lenke til nettside og/eller video i seksjon 4
- [ ] Bruk av Claude Code oppgitt i referanser
- [ ] Figurer lagt i figurer/ og vises riktig på GitHub

Ordbudsjett: 1 ~700 · 2 ~600 · 3 ~1200 · 4 ~700
Figurer: lagre fra notebooken med plt.savefig("../figurer/navn.png", dpi=150, bbox_inches="tight")
og vis dem her med ![beskrivelse](figurer/navn.png)
-->

# [Prosjektnavn]

[Navn], [Dato]

GitHub: https://github.com/184887/cmapss-rul
Nettside: [lenke]


## 1: Beskriv problemet

### Scope
<!-- Fra malen: mål, hvorfor ML, hvordan systemet brukes, hvordan løses det i dag, manuell løsning uten ML, hvem er brukeren, business impact, system/pipeline, ressurser -->

Stikkord (det du allerede har bestemt):
- Mål: forutsi RUL (sykluser igjen før svikt) for turbofan-motorer
- Bruker: flåteoperatør (ikke enkeltpersoner)
- Bruk: anbefale service når predikert RUL < x
- Dagens løsning: ? (faste intervaller? tilstandsbasert?)
- Uten ML: ?
- Hvorfor ML: ?

#### Tekst


### Metrics
<!-- Fra malen: ML-metrikker, kobling til business objective, minimum for suksess -->

Stikkord:
- RMSE
- NASA-score (asymmetrisk: sen prediksjon straffes hardere) → koble til kostnaden ved svikt
- Servicegrense: 95 % av motorene får service før svikt
- Suksesskriterium: ?

#### Tekst



## 2: Data
<!-- Fra malen: hva slags data, kilde, mengde, labels/ground truth, nøyaktighet, personvern/etikk, representasjon, rensing, feature engineering, skalering -->

Stikkord:
- NASA C-MAPSS, delsett FD001 (simulerte run-to-failure-forløp)
- Mengde: ? motorer i train, ? i test
- Label: RUL = siste syklus − nåværende syklus, kuttet ved 125 (hvorfor?)
- Testsett: motorene er kuttet før svikt, sann RUL i RUL_FD001.txt
- Døde sensorer fjernet → 14 features (hvorfor?)
- Etikk/personvern: ?
- Skalering/tidsvinduer: ikke brukt (hvorfor / videre arbeid)

Figurer: sensorkurver mot RUL, korrelasjonsdiagram

#### Tekst



## 3: Modellering
<!-- Fra malen: modeller utforsket, baseline, resultater fra andre, alle metrikker (tabell/graf), feilanalyse, feature importance -->

Stikkord:
- Split: GroupShuffleSplit på unit_nr, 80/20 (hvorfor gruppere på motor?)
- Baseline: DummyRegressor (gjennomsnitt)
- Modeller: LinearRegression, RandomForest
- Modellvalg: beste NASA-score på valideringssett (ikke testsett → lekkasje)
- Resultater fra litteratur på FD001: ?
- Feilanalyse: feilhistogram, scatter sann vs. predikert
- Feature importance: ? (ikke laget ennå)

Resultattabell:

| Modell | RMSE val | NASA val | RMSE test | NASA test |
|---|---|---|---|---|
| Dummy | | | | |
| LinearRegression | | | | |
| RandomForest | | | | |

#### Tekst



## 4: Deployment
<!-- Fra malen: hvordan deployet, hvordan prediksjonene brukes, overvåking og vedlikehold, forbedringer, lenke/skjermbilder -->

Stikkord:
- Gradio på Hugging Face Spaces
- Modellen trenes lokalt og lagres med joblib, appen laster den inn
- Input: velg testmotor → graf over predikert RUL per syklus, med servicepunkt markert
- Servicegrense x = 95-persentilen av (pred − sann) på validerings-rader med lav sann RUL
- Overvåking: ?
- Forbedringer: FD002–FD004, tidsvinduer, egne data

Lenke: [nettside]  Video: [lenke]
Skjermbilder: figurer/

#### Tekst



## 5: Referanser

- Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). Damage propagation modeling for aircraft engine run-to-failure simulation. *International Conference on Prognostics and Health Management (PHM08)*.
- NASA Prognostics Center of Excellence – C-MAPSS dataset: [lenke]
- scikit-learn: Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR* 12, 2825–2830.
- Gradio: https://www.gradio.app/
- Anthropic Claude Code – AI-kodeverktøy brukt til: [beskriv hva]
- [Artikler du sammenligner resultater med]


