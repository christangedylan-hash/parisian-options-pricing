# Parisian Options Pricing

This project studies the modeling and pricing of Parisian options, a class of path-dependent exotic options whose activation or cancellation depends not only on crossing a barrier, but also on the amount of time spent beyond that barrier.

The project was developed as part of an academic research project in actuarial science and quantitative finance at ISFA.

## Objective

The objective is to compare numerical methods for pricing Parisian options and related barrier options, with a focus on:

- binomial tree methods;
- Monte Carlo simulation;
- path-dependent activation mechanisms;
- applications of Parisian monitoring in finance and risk management.

## Methods

The project includes Python implementations of:

- a binomial tree approach for Parisian knock-in options;
- a Monte Carlo simulation framework for Parisian knock-in options;
- barrier monitoring through consecutive time spent above or below a threshold.

## Financial Context

Parisian options extend standard barrier options by requiring the underlying asset to remain beyond a barrier for a minimum duration before the option is activated or deactivated. This feature makes them more robust to short-lived barrier crossings and more complex to price than vanilla or standard barrier options.

## Repository Structure

```text
src/
  binomial_tree.py      # Binomial tree implementation for Parisian knock-in options
  monte_carlo.py        # Monte Carlo simulation for Parisian knock-in options

report/
  TER_Parisian_Options.pdf

results/
  Output charts and numerical results
