import pandas as pd

df = pd.DataFrame({
    "name": ["Caren", "Doreen", "Ken"],
    "score": [77, 80, 75]
})

print(df)

print(df["score"].mean())
