"""Creates reference.csv (normal commute) and current.csv (rush-hour & bad weather) for Evidently."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 600

# Make function for ride-hailing data
def make_rides(n, eta_mu, fare_mu, rating_mu, surge_prob):
    vehicle = rng.choice(["Mini", "Sedan", "SUV", "Bike"], size=n,
                         p=[0.40, 0.30, 0.15, 0.15])
    is_surge = rng.choice([0, 1], size=n, p=[1 - surge_prob, surge_prob])
    
    return pd.DataFrame({
        "eta_min": rng.normal(eta_mu, 2.5, n).clip(2, 30).round(1),
        "distance_km": rng.normal(6.5, 3.0, n).clip(1, 35).round(1),
        "fare_amount": rng.normal(fare_mu, 50, n).clip(50, 1200).round(0),
        "customer_rating": rng.normal(rating_mu, 0.4, n).clip(1, 5).round(1),
        "surge_multiplier": np.where(is_surge == 1, rng.choice([1.5, 2.0, 2.5], size=n), 1.0),
        "vehicle_type": vehicle,
    })

# reference = normal traffic, current = rush-hour & rain surge
make_rides(N, eta_mu=8.0, fare_mu=180, rating_mu=4.5, surge_prob=0.10).to_csv("reference.csv", index=False)
make_rides(N, eta_mu=16.5, fare_mu=340, rating_mu=3.9, surge_prob=0.75).to_csv("current.csv", index=False)
print("Created reference.csv and current.csv with 600 rows each (Ride-Hailing Domain)")