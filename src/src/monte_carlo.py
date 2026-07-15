"""
Monte Carlo pricing for Parisian knock-in options.

Academic project:
Modeling, Pricing and Applications of Parisian Options

Authors:
Souleymane Ouattara, Aboubakar Ouattara, Christ Ange Dylan Kouamé

This script implements a Monte Carlo simulation method for pricing Parisian
knock-in options under a geometric Brownian motion model.
"""

import numpy as np


def payoff(spot: float, strike: float, option_type: str = "call") -> float:
    """
    Compute the payoff of a European call or put option.

    Parameters
    ----------
    spot : float
        Final price of the underlying asset.
    strike : float
        Strike price.
    option_type : str
        "call" or "put".

    Returns
    -------
    float
        Option payoff at maturity.
    """
    if option_type == "call":
        return max(spot - strike, 0.0)
    if option_type == "put":
        return max(strike - spot, 0.0)

    raise ValueError("option_type must be either 'call' or 'put'.")


def is_beyond_barrier(spot: float, barrier: float, barrier_type: str = "up") -> bool:
    """
    Check whether the underlying asset is beyond the barrier.

    Parameters
    ----------
    spot : float
        Current underlying price.
    barrier : float
        Barrier level.
    barrier_type : str
        "up" if activation occurs above the barrier,
        "down" if activation occurs below the barrier.

    Returns
    -------
    bool
        True if the barrier condition is satisfied.
    """
    if barrier_type == "up":
        return spot >= barrier
    if barrier_type == "down":
        return spot <= barrier

    raise ValueError("barrier_type must be either 'up' or 'down'.")


def simulate_geometric_brownian_motion_path(
    spot: float,
    maturity: float,
    rate: float,
    volatility: float,
    n_steps: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Simulate one risk-neutral geometric Brownian motion path.

    Parameters
    ----------
    spot : float
        Initial price of the underlying asset.
    maturity : float
        Time to maturity, in years.
    rate : float
        Constant risk-free interest rate.
    volatility : float
        Constant volatility of the underlying asset.
    n_steps : int
        Number of time steps.
    rng : np.random.Generator
        NumPy random number generator.

    Returns
    -------
    np.ndarray
        Simulated asset price path of length n_steps + 1.
    """
    dt = maturity / n_steps
    prices = np.empty(n_steps + 1)
    prices[0] = spot

    for step in range(1, n_steps + 1):
        z = rng.normal()
        prices[step] = prices[step - 1] * np.exp(
            (rate - 0.5 * volatility**2) * dt
            + volatility * np.sqrt(dt) * z
        )

    return prices


def parisian_knock_in_monte_carlo_price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    volatility: float,
    barrier: float,
    min_time_beyond_barrier: float,
    n_simulations: int,
    n_steps: int,
    option_type: str = "call",
    barrier_type: str = "up",
    random_seed: int | None = 42,
) -> float:
    """
    Price a Parisian knock-in option using Monte Carlo simulation.

    The option is activated if the underlying asset remains beyond the barrier
    for at least `min_time_beyond_barrier` consecutive units of time.

    Parameters
    ----------
    spot : float
        Initial price of the underlying asset.
    strike : float
        Strike price.
    maturity : float
        Time to maturity, in years.
    rate : float
        Constant risk-free interest rate.
    volatility : float
        Constant volatility of the underlying asset.
    barrier : float
        Barrier level.
    min_time_beyond_barrier : float
        Minimum consecutive time spent beyond the barrier required for activation.
    n_simulations : int
        Number of Monte Carlo simulations.
    n_steps : int
        Number of time steps per simulated path.
    option_type : str
        "call" or "put".
    barrier_type : str
        "up" or "down".
    random_seed : int | None
        Random seed for reproducibility. Use None for non-reproducible simulations.

    Returns
    -------
    float
        Discounted Monte Carlo estimate of the Parisian knock-in option price.
    """
    if n_simulations <= 0:
        raise ValueError("n_simulations must be strictly positive.")

    if n_steps <= 0:
        raise ValueError("n_steps must be strictly positive.")

    if min_time_beyond_barrier < 0:
        raise ValueError("min_time_beyond_barrier must be non-negative.")

    dt = maturity / n_steps
    rng = np.random.default_rng(random_seed)
    payoffs = np.empty(n_simulations)

    for simulation in range(n_simulations):
        path = simulate_geometric_brownian_motion_path(
            spot=spot,
            maturity=maturity,
            rate=rate,
            volatility=volatility,
            n_steps=n_steps,
            rng=rng,
        )

        consecutive_time = 0.0
        activated = False

        for current_spot in path[1:]:
            if is_beyond_barrier(current_spot, barrier, barrier_type):
                consecutive_time += dt
            else:
                consecutive_time = 0.0

            if consecutive_time >= min_time_beyond_barrier:
                activated = True
                break

        if activated:
            payoffs[simulation] = payoff(path[-1], strike, option_type)
        else:
            payoffs[simulation] = 0.0

    discounted_price = np.exp(-rate * maturity) * np.mean(payoffs)
    return discounted_price


if __name__ == "__main__":
    price = parisian_knock_in_monte_carlo_price(
        spot=100.0,
        strike=110.0,
        maturity=1.0,
        rate=0.05,
        volatility=0.20,
        barrier=120.0,
        min_time_beyond_barrier=3 / 250,
        n_simulations=10_000,
        n_steps=250,
        option_type="call",
        barrier_type="up",
        random_seed=42,
    )

    print(f"Estimated Parisian knock-in option price: {price:.4f}")
