"""Initializes the `lat_longs` variable"""
import pandas as pd

state_abbreviations = [
    "AL", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "ID", "IL", "IN", "IA",
    "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND",
    "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD",
    "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY", 'DC'
]
df = pd.read_csv('colleges.csv')
df = df[df["State"].isin(state_abbreviations)]
lat_longs = [tuple([float(x) for x in item.split(',')]) for item in df['Latitude, Longitude']]
lat_longs = [(54.6 * item[1], -69 * item[0]) for item in lat_longs]