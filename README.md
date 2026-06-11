# Market-Volatility-Prediction

Using simple Machine Learning to directly predict stock prices is notoriously difficult (if it were that simple we'd all be rich right?) due to so many factors outside of our control, such as internal business decisions, global pandemics, erratic consumer behaviour, and unexpected trends. However, making informed decisions based on how chaotic (or volatile) the ups and downs of prices are is very useful and beneficial. This project aims to use Machine Learning to predict future volatility of the SPDR S&P 500 ETF (SPY) which is an exchange traded fund that tracks the performance of the S&P 500. In a sense, we're predicting unpredictability.

### The Aim
Using multiple different Machine Learning methods this project aims to predict future volatility of the ETF so that data driven decisions can be made in trading or investing. 

### The objective
If I were working at an investment banking firm or other finance related firm the objective might be to make predictions on how volatile a certain asset is and make an automated system so that informed decisions can be made in whether or not to trade/invest now or wait until things calm down. Since we are not working for a financial institution, I will use these finding for my own interests.

### The System Design
Now that we have our objective, we need to think about the general system design.
**Machine Learning Design:**
- This would be a *supervised learning* task, as we can train our model with labelled examples
- This would be a *univariate regression* task as we are predicting a single value (standard deviation of log returns)
- And this would be an *online learning* task as we will be having a continuous stream of data for our model.



