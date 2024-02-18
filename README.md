# Python Implementation of the Black-Scholes Model for Pricing Call Options

Primary Author: Dani Lisle
Contributors: Devlin Costello (Derivations), Jay Nasser (Data Scraper)
Affiliation: Department of Applied Mathematics, University of Colorado Boulder

## Abstract

This project is about the Black-Scholes model derivation and its performance on forecasting option call prices of a selected option chain dataset. It describes the financial context, the derivation of the PDE, and how it is solved for European options. We test the model against real-world data analysing its performance. The project discusses factors such as volatility and time to expiration that affect the estimations of call option prices and how this occurs within the dynamics of the model.



## 2 Project Description

### 2.1 Derivation of Black-Scholes

Assumptions:

- The short-term interest rate is known and constant.
- The stock price follows a random walk in continuous time with a variance rate proportional to the square of the stock price. Thus, the distribution of possible stock prices at the end of any finite interval is log-normal. The variance rate of the return on the stock is constant.
- The stock pays no dividends or other distributions.
- There are no transaction costs in buying or selling the stock or the option.
- It is possible to borrow any fraction of the price of a security to buy it or to hold it at the short-term interest rate.
- There are no penalties to short selling. A seller who does not own a security will simply accept the price of the security from a buyer and will agree to settle with the buyer on some future date by paying him an amount equal to the price of the security on that date.

Letting \( S_t \) be the price of a risky asset at time \( t \) and \( S_t^0 \) be the price of a non-risky asset at time \( t \), we can construct the stochastic differential equation that underlies the Black-Scholes model:

\[ dS_t = S_t(\mu dt + \sigma dB_t) \]
\[ dS_t^0 = rS_t^0 dt \]

where \( B_t \) is a Brownian motion, \( \mu \) is the mean rate of return, \( r \) is the interest rate, and \( \sigma > 0 \) is the volatility rate. Brownian motion simulates the continuous time random walk that the stock price follows. Let \( W_t = B_t + \frac{\mu-r}{\sigma}t \) and let the risk-neutral probability \( P \) be defined with respect to \( Q \), where \( Q \) is the underlying probability function of the probability space where the Brownian motion lies.

\[ dP = exp\left(\frac{r - \mu}{\sigma}dB_s - \frac{1}{2}\left(\frac{r - \mu}{\sigma}\right)^2 ds\right) \]

\( W_t \) is still a Brownian motion, and \( \frac{S_t}{S_t^0} \) is a martingale. \( S_t \) must satisfy the following differential equation on \( P \):

\[ dS_t = S_t(rdt + \sigma dW_t) \]

Let us now consider a portfolio of \( H_t \) risky assets and \( H_t^0 \) non-risky assets. The value of the complete portfolio at time \( t \) is:

\[ P_t = H_t S_t + H_t^0 dS_t^0 \]

If we assume that the portfolio is self-financing or that any manipulation of \( H_t \) or \( H_t^0 \) doesn’t require any inflow or outflow of money:

\[ dP_t = H_t dS_t + H_t^0 dS_t^0 \]

From this, we can tell that \( \frac{P_t}{S_t^0} \) is also a martingale. Let \( \phi \) be the payoff function, and a given time \( T > 0 \) be the maturity time. Our goal now is to build a portfolio \( P_T = \phi(S_T) \). There are many options for \( \phi \) depending on what we are dealing with. By the martingale representation theorem, we know that the answer is positive since \( \frac{P_t}{S_t^0} \) is a martingale and \( \phi(S_T) \) is \( F_t \)-measurable. Thus, the portfolio has the following value at time \( t \):

\[ P_T = E \left[ e^{-\int_t^T rds} \phi(S_T) | F_t \right] \]

We should acknowledge that an analytical solution exists only for vanilla options and when \( r \) and \( \sigma \) are constant. If \( r \) and \( \sigma \) were functions of \( t \) and \( S \), we would only be able to evaluate \( \phi \) numerically. Since \( S_t \) is a stochastic process, it follows from the Markov Property that:

\[ P_t = p(t, S_t) \]

where \( p \) is a function of \( t \in [0, T] \) and \( S \in [0, \infty) \) and is the pricing function of the option. Additionally, we know that \( p \) is a deterministic function. By the Markov Property of