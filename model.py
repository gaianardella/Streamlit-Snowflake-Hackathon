import pandas as pd

url = 'https://raw.githubusercontent.com/username/repo-name/branch-name/path-to-file.csv'
df = pd.read_csv(url)
