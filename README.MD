 # CMAPSS Remaining Useful Life Prediction

Tools and experiments for predicting the remaining useful life (RUL) of aircraft engines using the NASA C-MAPSS turbofan engine degradation dataset.

## Overview

The project is intended for developing, training, and evaluating machine-learning models that estimate how many operating cycles remain before an engine reaches failure. The C-MAPSS dataset contains multivariate sensor measurements from simulated run-to-failure trajectories under different operating conditions and fault modes.

## Dataset

Download the C-MAPSS dataset from the [NASA Prognostics Center of Excellence](https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/). Place the extracted files in the location expected by the project code. The dataset includes the commonly used subsets `FD001` through `FD004.

## Getting started

1. Clone the repository.
2. Install the dependencies used by the project.
3. Download and place the C-MAPSS data in the project data directory.
4. Run the available training or evaluation scripts/notebooks.

Example setup:

```bash
git clone <repository-url>
cd cmapss-rul
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Workflow

Typical experiments include:

- Loading and cleaning sensor time-series data
- Adding engine-cycle and RUL labels
- Normalizing sensor measurements
- Creating time-windowed training samples
- Training and evaluating RUL regression models

## Evaluation

Models can be evaluated with regression metrics such as mean squared error (MSE), root mean squared error (RMSE), and the NASA scoring function commonly used for the C-MAPSS benchmark.

## License

Add the project license here.
