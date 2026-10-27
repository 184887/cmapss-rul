# [Prosjektnavn]

[Navn], [Dato]

GitHub: https://github.com/184887/cmapss-rul  
Nettside: [lenke]  


## 1: Beskriv problemet

### 1.1 Scope

Motorene i en flyflåte slites ned ulikt, men service planlegges fortsatt med faste intervaller. Siden man ikke vet hvor slitt hver motor er, må intervallene settes tidlig nok til at man er sikker på at motorene ikke feiler. Planlegger man service for tidlig, blir det svært kostbart. Å ta den for sent er likevel enda verre, fordi det i verste fall kan føre til at flyet styrter.

Målet med systemet er å forutsi hvor mange sykluser en motor har igjen før den svikter, og ut fra det anbefale en dato da motoren bør tas inn til service. Systemet er tiltenkt den som har ansvar for når motorene i flåten går inn til service.

Hvorfor kan ikke en servicetekniker bare se på en sensor og bestemme selv? Motorene har 21 sensorer, hvorav 14 endrer seg med slitasjen, og det er vanskelig å se ut fra dem hvor nær svikt en motor er. Det er mye lettere for en ML modell, som er god på å oppdage små forskjeller og sammenhenger mellom mange input.

Hvordan bruke systemet:

1. Brukeren laster opp sensordata for flåten og velger hvor mange flyturer motorene er planlagt å fly per dag. Det er lagt ved eksempeldata for testing.
2. Systemet viser en oversikt over flåten med den mest kritiske motoren øverst. For hver motor kan brukeren se en graf over predikert gjenværende levetid over tid, med servicegrensen markert.
3. Systemet anbefaler en servicedato for hver motor.

Fordelen er at hver motor kan tas inn til service nærmere når den faktisk trenger det, i stedet for etter et fast intervall. Slik utnytter man mer av levetiden og sparer penger på service, samtidig som en valgt sikkerhetsmargin gjør at risikoen for piloter og passasjerer holdes lav.

Prosjektet er laget med simulerte data fra NASA, modellen er trent på egen PC, og nettsiden ligger gratis på nettet.

### 1.2 Metrics

RMSE brukes som standardmål for å kunne sammenligne med andre arbeider på samme datasett. Svakheten er at den straffer for tidlige og for sene prediksjoner like mye.

NASA-score er også et feilmål, men den er asymmetrisk og eksponentiell: en for sen prediksjon straffes mye hardere enn en like stor for tidlig prediksjon. Det passer dette problemet, fordi for sen service er det som kan føre til svikt.

For å velge modell brukes NASA-score, men bare når motoren har 40 sykluser eller mindre igjen. Det er i denne perioden man må bestemme når motoren skal til service.
Når en motor har mye levetid igjen, betyr det lite om modellen bommer litt. Nær svikt er det derimot viktig at modellen treffer, fordi en for sen prediksjon kan føre til at motoren går for lenge.
Grensen på 40 sykluser er valgt fordi det tilsvarer omtrent én uke med 4 til 6 flyturer per dag. Da har man tid til å planlegge å få motoren inn på service.

### 1.3 Servicegrense og suksesskriterium

Modellen kan bomme og tro at motoren har mer igjen enn den har. Derfor sender man motoren på service når modellen sier den har under x sykluser igjen. x er satt slik at 95 % av motorene får service før de svikter. For modellen jeg valgte ble x = 4,5 sykluser. Vil man ta mindre risiko, kan man øke prosenten, men da kommer motorene tidligere inn.

Systemet er bra nok når modellen slår de enkle modellene, lineær regresjon (LR) og gjennomsnitt, på NASA-score nær svikt. Minst 95 % av motorene må få service før de svikter, og x må være godt under 40, slik at man har tid til å planlegge.


## 2: Data

### 2.1 Datasett og mengde

### 2.2 Label (RUL)

### 2.3 Rensing og features

![Korrelasjon mellom hver sensor og RUL](figurer/korrelasjon_med_rul.png)

![Sensor som følger slitasjen (s_11) mot sensor som er konstant (s_6)](figurer/levende_vs_dod_sensor.png)

### 2.4 Skalering

### 2.5 Etikk og begrensninger


## 3: Modellering

### 3.1 Oppsett og validering

### 3.2 Baseline

### 3.3 Modeller og hyperparametersøk

| Modell | NASA ≤ 40 (CV) | RMSE (CV) |
|---|---|---|
| Gjennomsnitt (Dummy) | | |
| Lineær regresjon | | |
| RandomForest | | |
| ExtraTrees | | |
| GradientBoosting | | |
| KNN | | |
| SVR | | |
| MLP | | |
| GB quantile (Optuna) | | |

### 3.4 Valgt modell og resultater

| Modell | NASA ≤ 40 (val) | RMSE (val) | RMSE (test) | NASA (test) |
|---|---|---|---|---|
| Lineær regresjon | | | | |
| GB quantile | | | | |

![NASA-score og feil langs levetiden for LR og GB quantile](figurer/nasa_per_rul.png)

![Sann mot predikert RUL på testsettet](figurer/test_sann_vs_pred.png)

![Feilfordeling på testsettet](figurer/test_feilfordeling.png)

### 3.5 Feilanalyse

### 3.6 Feature importance

![Feature importance for valgt modell](figurer/feature_importance.png)

### 3.7 Sammenligning med andre arbeider


## 4: Deployment

### 4.1 Hvordan systemet er deployet

### 4.2 Hvordan prediksjonene brukes

<!-- MANGLER: skjermbilder fra nettsiden
     ![Flåteoversikt på nettsiden](figurer/app_flateoversikt.png)
     ![Graf over predikert RUL og anbefalt service for én motor](figurer/app_graf.png) -->

### 4.3 Overvåking og vedlikehold

### 4.4 Svakheter og forbedringer


## 5: Referanser

- Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). Damage propagation modeling for aircraft engine run-to-failure simulation. *International Conference on Prognostics and Health Management (PHM08)*.
- NASA Prognostics Center of Excellence – C-MAPSS dataset: [lenke]
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR* 12, 2825–2830.
- Akiba, T. et al. (2019). Optuna: A Next-generation Hyperparameter Optimization Framework. *KDD*.
- Gradio: https://www.gradio.app/
- [Hosting]
- Anthropic Claude Code – brukt til: [beskriv]
- [Artikler du sammenligner med på FD001]
