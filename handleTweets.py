import pandas as pd

# 读取 CSV 文件
user_tweets_df = pd.read_csv("user_tweets.csv", dtype=str)

# 只保留前 5 个 tweet 列以及 id 列
tweet_columns_to_keep = ['id'] + [f'tweet_{i+1}' for i in range(30)]
filtered_user_tweets_df = user_tweets_df[tweet_columns_to_keep]

# 将 NaN 替换为空字符串并确保所有列都是字符串类型
filtered_user_tweets_df = filtered_user_tweets_df.fillna('').astype(str)

# 保存结果到新的 CSV 文件或覆盖原文件
filtered_user_tweets_df.to_csv("user_tweets_filtered.csv", index=False)

# 读取 mbti_labels.csv 和 user_tweets_filtered.csv
mbti_labels_df = pd.read_csv("user_info.csv", dtype=str)
filtered_user_tweets_df = pd.read_csv("user_tweets_filtered.csv", dtype=str)

# 去除两侧的空格和其他不可见字符
filtered_user_tweets_df['id'] = filtered_user_tweets_df['id'].str.strip()
mbti_labels_df['id_str'] = mbti_labels_df['id_str'].str.strip()

# 获取 mbti_labels.csv 中的唯一 id
valid_ids = set(mbti_labels_df['id_str'])

# 检查匹配的数量
print(filtered_user_tweets_df['id'].isin(valid_ids).sum())

# 过滤 user_tweets_filtered.csv，仅保留 id 在 valid_ids 中的行
filtered_user_tweets_df = filtered_user_tweets_df[filtered_user_tweets_df['id'].isin(valid_ids)]

# 保存过滤后的结果到新的 CSV 文件或覆盖原文件
filtered_user_tweets_df.to_csv("user_tweets_filtered.csv", index=False)

print("过滤完成，已将仅包含 mbti_labels.csv 中 id 的记录保存在 user_tweets_filtered.csv。")

filtered_user_tweets_df = pd.read_csv("user_tweets_filtered.csv", dtype=str)

# 去除换行符并合并 tweets
filtered_user_tweets_df = filtered_user_tweets_df.fillna('')  # 替换 NaN
tweet_columns = [f'tweet_{i+1}' for i in range(10)]

# 去除换行符并合并 tweets 列
filtered_user_tweets_df['merged_tweets'] = filtered_user_tweets_df[tweet_columns].apply(
    lambda row: ' '.join(row.str.replace('\n', ' ').replace('\r', '')), axis=1
)

# 保留 id 和合并后的 tweets 列
final_df = filtered_user_tweets_df[['id', 'merged_tweets']]

# 保存结果到 CSV 文件
final_df.to_csv("user_tweets_concatenated.csv", index=False)

print("处理完成，已将结果保存到 user_tweets_concatenated.csv。")
