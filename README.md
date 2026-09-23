# Market-Volatility-Prediction

Using simple Machine Learning to directly predict stock prices is notoriously difficult due to so many factors outside of our control, such as internal business decisions, global pandemics, erratic consumer behaviour, and unexpected trends. However, making informed decisions based on how chaotic the ups and downs (i.e volatililty) of prices are can be very useful and beneficial. This project aims to use Machine Learning to predict future volatility of the SPDR S&P 500 ETF (SPY) which is an exchange traded fund that tracks the performance of the S&P 500. In a sense, we're predicting unpredictability.

### Overview

Market volatility is a measure of how much financial returns fluctuate over a given period. This project focuses on predicting 10 day forward volatility using historical market data.

The project was developed as an end to end machine learning pipeline, covering the process from raw market data through to model deployment and automated prediction.

**What the system does**
- Retrieves historical market data using yfinance
- Engineers return and volatility-related features
- Predicts 10-day forward volatility using a trained CatBoost regression model
- Compares the machine learning model against statistical and naive baselines
- Stores market data, engineered features, and predictions in PostgreSQL
- Exposes predictions through a FastAPI application
- Containerises the application using Docker
- Deploys the application to AWS using ECS Fargate
- Runs automated weekday predictions using Amazon EventBridge Scheduler
- Records application and prediction logs using Amazon CloudWatch
- Uses GitHub Actions for CI/CD deployment

### The Aim
Using multiple different Machine Learning methods, this project aims to predict future volatility of the ETF so that data driven decisions can be made in trading or investing. 

### The objective
If this were an environment in investment banking firm or other finance related firms, the objective might be to make predictions on how volatile a certain asset is and make an automated system so that informed decisions can be made in whether or not to trade/invest now or wait until things calm down.

### The Machine Learning Design

- This would be a *supervised learning* task, as we can train our model with labelled examples
- This would be a *univariate regression* task as we are predicting a single value (standard deviation of log returns)
- And this would be an *online learning* task as we will be having a continuous stream of data for our model.

### Results

| Model       | RMSE  |
| ------------- | -----|
| Naive 10 day volatility | 0.006817 |
| GARCH(1,1) | 0.005938 |
| CatBoost | 0.004985|

The CatBoost model was selected as the deployed model after achieving lower validation error than the statistical baseline.

**Note:** The final deployed model was trained using the modelling pipeline developed in the project and is used to generate 10-day forward volatility predictions in the production application.

### System Architechture
<img width="3965" height="8070" alt="diagram" src="https://github.com/user-attachments/assets/941c6b61-9a53-4a2f-8460-e12de1bc04c8" />

### AWS Deployment

The application was deployed to AWS as a containerised, scheduled machine learning system.

**AWS Services used**

| Service       | Purpose  |
| ------------- | ----- |
|Amazon ECS Fargate |	Hosts the containerised FastAPI application and prediction worker|
|Amazon ECR|	Stores Docker container images|
|Amazon RDS PostgreSQL|	Stores market data, engineered features, and predictions|
|Amazon EventBridge Scheduler|	Automatically launches the prediction worker on weekdays|
|Amazon CloudWatch	|Collects application and prediction logs|
|AWS IAM|	Provides service permissions and secure access to AWS resources|
|Amazon VPC|	Provides network isolation and security controls|
|GitHub Actions|	Automates Docker image builds and ECS deployments|

**Deployment Architechture**

The FastAPI application was packaged as a Docker container and deployed to Amazon ECS using AWS Fargate.
The production database was hosted using Amazon RDS PostgreSQL. Access to the database was restricted through VPC security groups rather than exposing the database publicly.
Amazon EventBridge Scheduler was configured to launch a standalone ECS Fargate task at 8:00 AM Monday–Friday in the Australia/Melbourne timezone. The task runs the complete prediction pipeline and exits after completion.
The resulting application and task logs were captured using Amazon CloudWatch.

**CI/CD**

GitHub Actions was used to automate deployment of the API.

GitHub -> GitHub Actions -> Docker build -> Amazon ECR -> Amazon ECS

### Model Development 

**Prediction Target**

The model predicts 10day forward market volatility, calculated as the standard deviation of future log returns. The target was constructed using future returns and shifted so that only information available at prediction time was used as a model input.

**The Data Features**

The feature set includes historical price and volume information together with engineered return and volatility features:

- Open
- High
- Low
- Close
- Volume
- Log return
- High-low price range
- 5-day, 10-day and 20-day return features
- Historical rolling volatility features

Future volatility values were excluded from the model inputs to prevent target leakage.

**Train, Validation, Test Split**

The data was divided chronologically to reflect the time dependent nature of financial data.
| Dataset       | Period  |
| ------------- | -----|
| Training | 2015 ~ 2023 |
| Validation | 2024 ~ 2025 |
| Test | 2026|

The final test period was kept separate from model development and was not used for model selection or hyperparameter tuning.

**Models**

Several regression approaches were evaluated:

- Linear Regression
- Ridge Regression
- Lasso
- Elastic Net
- K-Nearest Neighbours
- Decision Tree
- Random Forest
- Gradient Boosting
- AdaBoost
- XGBoost
- LightGBM
- CatBoost
- GARCH(1,1)

The machine learning models were compared against both a naive volatility baseline and the GARCH statistical model.
CatBoost was ultimately selected for deployment based on its validation performance.

### Monitoring and Automated Prediction

The deployed prediction pipeline performs the following steps:

1. Checks previously generated predictions for available evaluation data.
2. Retrieves new market data using yfinance.
3. Updates the raw market data stored in PostgreSQL.
4. Recalculates engineered features.
5. Loads the trained CatBoost model.
6. Generates a 10-day forward volatility prediction.
7. Stores the prediction in PostgreSQL.
8. Records the execution output in CloudWatch.

Predictions are also categorised into volatility levels based on thresholds calculated from the training target distribution:
- LOW
- MEDIUM
- HIGH

**Example Prediction**

A successful scheduled AWS execution produced:

- Prediction date: 2026-09-22
- Predicted 10-day volatility: 0.005136
- Volatility level: LOW

The prediction task completed successfully with exit code 0.

**Project Structure**
```
Market-Volatility-Prediction/
│
├── api/                    # FastAPI routes and API schemas
├── data/                   # Local datasets
├── frontend/               # Frontend application
├── Models/                 # Trained model artifacts
├── Notebooks/              # Data exploration and modelling notebooks
├── src/
│   ├── database.py         # Database connection
│   ├── features.py         # Feature engineering
│   ├── ingest.py           # Market data ingestion
│   ├── monitor.py          # Prediction monitoring
│   └── predict.py          # Prediction pipeline
│
├── scripts/
│   └── run_prediction.py   # Scheduled prediction entry point
│
├── app.py                  # FastAPI application
├── Dockerfile              # API Docker image
├── docker-compose.yml      # Local development environment
├── market_volatility.sql   # Database schema
├── requirements.txt        # Python dependencies
└── README.md
```

### Local Development

**Requirements**

- Python 3.12
- Docker Desktop
- Git

**Clone the repository**

```bash
git clone https://github.com/Noha-Jung3/Market-Volatility-Prediction.git
cd Market-Volatility-Prediction
```

**Run with Docker Compose**

```bash
docker compose up --build
```

The local services include:

- FastAPI API: `http://localhost:8000`
- FastAPI documentation: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`
- PostgreSQL: `localhost:5432`

**Run the prediction pipeline locally**

The prediction worker can also be executed directly:

```bash
python -m scripts.run_prediction
```

### Future Improvements 

Potential extensions to the project include:

- Implementing systematic hyperparameter tuning and model selection
- Adding additional market and macroeconomic features
- Evaluating model performance across different market regimes
- Adding more comprehensive prediction monitoring and drift detection
- Introducing model versioning and experiment tracking
- Adding automated retraining when model performance degrades
- Deploying the frontend and API behind an application load balancer
- Adding authentication and more granular API access controls

### Summary

This project demonstrates an end to end machine learning workflow, from financial market data ingestion and feature engineering through model development, evaluation, deployment, automated inference, database storage, and monitoring.
The project combines data science and software engineering practices to turn a trained volatility model into a reproducible application that can generate predictions automatically.











