import os
import pandas as pd

# 文件路径
avatar_folder = 'avatar'  # 替换为你的 avatar 文件夹路径
duplicates_csv = 'duplicates.csv'
user_info_csv = 'user_info.csv'
mbti_labels_csv = 'mbti_labels.csv'
user_tweets_csv = 'user_tweets.csv'

# 读取 duplicates.csv
duplicates_df = pd.read_csv(duplicates_csv)
duplicate_screen_names = duplicates_df['Duplicate_Filenames'].str.replace('.jpg', '', regex=False).tolist()

# 读取 user_info.csv，获取 screen_name 对应的 id
user_info_df = pd.read_csv(user_info_csv)
duplicate_ids = user_info_df[user_info_df['screen_name'].isin(duplicate_screen_names)]['id'].tolist()

# 删除 avatar 文件夹中对应的图片文件
for screen_name in duplicate_screen_names:
    file_path = os.path.join(avatar_folder, f"{screen_name}.jpg")
    if os.path.exists(file_path):
        os.remove(file_path)

# 更新 user_info.csv，删除对应行
user_info_df_filtered = user_info_df[~user_info_df['id'].isin(duplicate_ids)]
user_info_df_filtered.to_csv(user_info_csv, index=False)

# 更新 mbti_labels.csv 和 user_tweets.csv，删除对应的 id
for csv_file in [mbti_labels_csv, user_tweets_csv]:
    df = pd.read_csv(csv_file)
    df_filtered = df[~df['id'].isin(duplicate_ids)]
    df_filtered.to_csv(csv_file, index=False)

print("删除完成，avatar 文件夹和其他 CSV 文件已更新。")
