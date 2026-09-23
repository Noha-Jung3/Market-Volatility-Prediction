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






