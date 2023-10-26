from app import msd_df, recommendSongs, echoComparison
import pandas as pd
from itertools import chain, combinations
import numpy as np
import warnings
from tqdm import tqdm

warnings.filterwarnings("ignore")

df = pd.DataFrame(columns=["Columns", 0, 1, 2, 3, 4])

columns = [
    "Year", "Tempo", "Latitude", "Longitude", "Overlapping genres"
]

combs = list(chain.from_iterable(combinations(columns, r) for r in range(len(columns)+1)))

for comb in tqdm(combs[1:10]):
    arr = np.zeros(5)
    for i in tqdm(range(len(msd_df))):
        arr += echoComparison([i], recommendSongs([i], 5, list(comb), msd_df))
    df = pd.concat([df, pd.DataFrame({
        "Columns": str(list(comb)),
        0: arr[0],
        1: arr[1],
        2: arr[2],
        3: arr[3],
        4: arr[4]
    }, index=[combs.index(comb)])])

df.to_csv("data/empirical_analysis.csv")