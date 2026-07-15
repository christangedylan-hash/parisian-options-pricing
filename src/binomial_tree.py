"""
Binomial tree pricing for Parisian knock-in options.

Academic project:
Modeling, Pricing and Applications of Parisian Options

Authors:
Souleymane Ouattara, Aboubakar Ouattara, Christ Ange Dylan Kouamé

This script implements a discrete-time binomial pricing approach for Parisian
knock-in options. A Parisian option is activated only if the underlying asset
spends a minimum consecutive number of time steps beyond a predefined barrier.
"""

from itertools import product
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


def parisian_knock_in_binomial_price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    volatility: float,
    barrier: float,
    min_steps_beyond_barrier: int,
    n_steps: int,
    option_type: str = "call",
    barrier_type: str = "up",
) -> float:
    """
    Price a Parisian knock-in option using a binomial tree path enumeration.

    The option is activated if the underlying asset remains beyond the barrier
    for at least `min_steps_beyond_barrier` consecutive time steps.

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
    min_steps_beyond_barrier : int
        Minimum number of consecutive time steps beyond the barrier required
        for activation.
    n_steps : int
        Number of time steps in the binomial tree.
    option_type : str
        "call" or "put".
    barrier_type : str
        "up" or "down".

    Returns
    -------
    float
        Discounted risk-neutral price of the Parisian knock-in option.
    """
    if n_steps <= 0:
        raise ValueError("n_steps must be strictly positive.")

    if min_steps_beyond_barrier < 0:
        raise ValueError("min_steps_beyond_barrier must be non-negative.")

    dt = maturity / n_steps
    up_factor = np.exp(volatility * np.sqrt(dt))
    down_factor = 1.0 / up_factor

    risk_neutral_prob = (
        np.exp(rate * dt) - down_factor
    ) / (up_factor - down_factor)

    if not 0.0 <= risk_neutral_prob <= 1.0:
        raise ValueError(
            "Invalid risk-neutral probability. Check the model parameters."
        )

    option_value = 0.0

    # Each path is represented by a sequence of 1 = up and 0 = down.
    for path in product([0, 1], repeat=n_steps):
        current_spot = spot
        consecutive_counter = 0
        activated = False

        n_up = sum(path)
        n_down = n_steps - n_up
        path_probability = (
            risk_neutral_prob ** n_up
            * (1.0 - risk_neutral_prob) ** n_down
        )

        for move in path:
            if move == 1:
                current_spot *= up_factor
            else:
                current_spot *= down_factor

            if is_beyond_barrier(current_spot, barrier, barrier_type):
                consecutive_counter += 1
            else:
                consecutive_counter = 0

            if consecutive_counter >= min_steps_beyond_barrier:
                activated = True

        if activated:
            option_value += path_probability * payoff(
                current_spot, strike, option_type
            )

    discounted_price = np.exp(-rate * maturity) * option_value
    return discounted_price


if __name__ == "__main__":
    # Example parameters inspired by the academic project.
    price = parisian_knock_in_binomial_price(
        spot=60.75,
        strike=80.0,
        maturity=1.0,
        rate=0.023,
        volatility=0.69,
        barrier=70.0,
        min_steps_beyond_barrier=2,
        n_steps=5,
        option_type="call",
        barrier_type="up",
    )

    print(f"Parisian knock-in option price: {price:.4f}")
