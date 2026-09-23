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

### The Data
For this project, the yfincance API will be used to get around eleven years worth of historical Open, High, Low, Close, Volume data from 1st Jan 2015 to 31st December 2025. There are no missing values or duplicate values, which means no imputation, however we will need to get rid of some outilers.

- Open = Price at the start of the day
- High = Highest price of that day
- Low = Lowest price of that day
- Close = Price at the end of the day
- Volume = Volume traded

### Results

| Model       | RMSE  |
| ------------- | -----:|
| Naive 10 day volatility | 0.006817 |
| GARCH(1,1) | 0.005938 |
| CatBoost | 0.004985|

The CatBoost model was selected as the deployed model after achieving lower validation error than the statistical baseline.

**Note:** The final deployed model was trained using the modelling pipeline developed in the project and is used to generate 10-day forward volatility predictions in the production application.

### System Architechture
flowchart TD

subgraph group_http["HTTP Boundary"]
  node_http_client(("HTTP API Client<br/>external caller"))
  node_fastapi["FastAPI Application<br/>[app.py]"]
  node_routes["Prediction Routes<br/>API routes"]
end

subgraph group_market["Market Data Pipeline"]
  node_yahoo(("Yahoo Finance<br/>external market data"))
  node_ingest["Raw Market Ingestion<br/>pipeline stage"]
  node_features["Feature Engineering<br/>pipeline stage"]
end

subgraph group_forecast["Forecast Execution"]
  node_orchestrator["Prediction Orchestrator<br/>workflow service"]
  node_inference["CatBoost Inference<br/>model service"]
  node_model["CatBoost Model<br/>model artifact"]
end

subgraph group_monitoring["Monitoring"]
  node_monitor["Prediction Monitoring<br/>metrics service"]
end

subgraph group_state["Persistence"]
  node_database["Database Engine<br/>SQLAlchemy adapter"]
  node_store[("PostgreSQL State Store<br/>database")]
end

node_http_client -->|"HTTP request"| node_fastapi
node_fastapi -->|"dispatches"| node_routes
node_routes -->|"runs prediction"| node_orchestrator
node_routes -->|"gets metrics"| node_monitor
node_orchestrator -->|"runs monitoring"| node_monitor
node_monitor -->|"reads and writes"| node_store
node_orchestrator -->|"ingests data"| node_ingest
node_ingest -->|"reads and appends"| node_store
node_ingest -->|"downloads data"| node_yahoo
node_orchestrator -->|"rebuilds features"| node_features
node_features -->|"replaces features"| node_store
node_orchestrator -->|"predicts latest"| node_inference
node_inference -->|"reads and stores"| node_store
node_inference -->|"loads model"| node_model
node_ingest -->|"uses engine"| node_database
node_features -->|"uses engine"| node_database
node_monitor -->|"uses engine"| node_database
node_inference -->|"uses engine"| node_database
node_database -->|"connects to"| node_store

click node_fastapi "https://github.com/noha-jung3/market-volatility-prediction/blob/main/app.py"
click node_routes "https://github.com/noha-jung3/market-volatility-prediction/blob/main/api/routes.py"
click node_ingest "https://github.com/noha-jung3/market-volatility-prediction/blob/main/src/ingest.py"
click node_features "https://github.com/noha-jung3/market-volatility-prediction/blob/main/src/features.py"
click node_orchestrator "https://github.com/noha-jung3/market-volatility-prediction/blob/main/src/predict.py"
click node_inference "https://github.com/noha-jung3/market-volatility-prediction/blob/main/src/predict.py"
click node_model "https://github.com/noha-jung3/market-volatility-prediction/blob/main/Models/catboost_volatility_model.pkl"
click node_monitor "https://github.com/noha-jung3/market-volatility-prediction/blob/main/src/monitor.py"
click node_database "https://github.com/noha-jung3/market-volatility-prediction/blob/main/src/database.py"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_http_client,node_fastapi,node_routes toneBlue
class node_yahoo,node_ingest,node_features toneAmber
class node_orchestrator,node_inference,node_model toneMint
class node_monitor toneRose
class node_database,node_store toneIndigo






