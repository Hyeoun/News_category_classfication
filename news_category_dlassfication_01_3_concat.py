import pandas as pd
import glob

data_paths = glob.glob('./crawling/team_crawling/*')
print(data_paths)
df = pd.DataFrame()
for data_path in data_paths:
    df_temp = pd.read_csv(data_path, index_col=0)
    df = pd.concat([df, df_temp])

df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
print(df.head())
print(df.tail())
print(df['category'].value_counts())
print(df.info())
df.to_csv('./crawling/naver_news.csv', index=False)

# df = pd.read_csv('./crawling/team_crawling/news_Culture_1-50.csv', index_col=0)
# df_temp = pd.read_csv('./crawling/team_crawling/news_Culture_51-100.csv', index_col=0)
# df = pd.concat([df, df_temp])
# print(df.head())
# print(df.tail())
# print(df['category'].value_counts())