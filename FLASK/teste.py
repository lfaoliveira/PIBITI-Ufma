import pandas as pd

data = {"Name": ["Alice", "Bob", "eve"], "Age": [25, 30, 40]}
df = pd.DataFrame(data)
print(df)

# Add a new row using loc[]
data = {"Name": ["Alice", "Bob"], "Age": [250, 300]}
df2 = pd.DataFrame(data)
print(df2)
df.update(df2)
print(df)

print("Alice" in df['Name'].values)
