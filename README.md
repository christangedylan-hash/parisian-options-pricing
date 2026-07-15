# Parisian Options Pricing

This project studies the modeling and pricing of Parisian options, a class of path-dependent exotic options whose activation or cancellation depends not only on crossing a barrier, but also on the amount of time spent beyond that barrier.

The project was developed as part of an academic research project in actuarial science and quantitative finance at ISFA.

## Objective

The objective is to compare numerical methods for pricing Parisian options and related barrier options, with a focus on:

- binomial tree methods;
- Monte Carlo simulation;
- path-dependent activation mechanisms;
- applications of Parisian monitoring in finance and risk management.

## Financial Context

Parisian options extend standard barrier options by requiring the underlying asset to remain beyond a barrier for a minimum duration before the option is activated or deactivated.

This feature makes them more robust to short-lived barrier crossings and more complex to price than vanilla or standard barrier options.

In financial markets, this type of path-dependent structure is relevant for:

- exotic derivatives pricing;
- structured products;
- risk management;
- barrier monitoring mechanisms;
- scenarios where a temporary threshold crossing should not immediately trigger activation or cancellation.

## Methods

The repository includes Python implementations of:

- a binomial tree approach for Parisian knock-in options;
- a Monte Carlo simulation framework for Parisian knock-in options;
- barrier monitoring through consecutive time spent above or below a threshold.

The accompanying academic report also discusses:

- standard barrier options;
- Black-Scholes-Merton modeling;
- trinomial tree improvements;
- Sequential Monte Carlo methods;
- practical applications of Parisian monitoring in finance and risk management.

## Repository Structure

```text
src/
  binomial_tree.py      # Binomial tree implementation for Parisian knock-in options
  monte_carlo.py        # Monte Carlo simulation for Parisian knock-in options

Parisian_Options_Report.pdf
requirements.txt
README.md
```

## Tech Stack

- Python
- NumPy
- Matplotlib
- Monte Carlo simulation
- Binomial tree methods
- Exotic derivatives pricing

## How to Run

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the binomial tree implementation:

```bash
python src/binomial_tree.py
```

Run the Monte Carlo implementation:

```bash
python src/monte_carlo.py
```

## Project Highlights

- Implemented a discrete-time binomial tree framework for Parisian knock-in options.
- Built a Monte Carlo simulation method under a geometric Brownian motion framework.
- Modeled the Parisian activation condition through the consecutive time spent beyond a barrier.
- Compared numerical approaches for path-dependent exotic option pricing.
- Connected the theoretical structure of Parisian options to practical financial risk management applications.

## Authors

Academic group project by:

- Souleymane Ouattara
- Aboubakar Ouattara
- Christ Ange Dylan Kouamé

## Disclaimer

This project is for academic and educational purposes only. It does not constitute financial advice or investment recommendation.
