import pandas as pd
from sentimentanalysis import rate_post  # your actual rating function

# Load your CSV
df = pd.read_csv('../naiveanalysis/reddit_posts_cooccurrence.csv')

# Filter for posts where the three-way condition is 1
filtered_df = df[df['ibd_and_anxiety_and_alzheimer'] == 1]

# Take only the first 2 matching posts
filtered_df_2 = filtered_df.head(2).copy()

# List to store ratings
ratings = []

# Iterate with enumeration to print numbering
for i, row in enumerate(filtered_df_2.itertuples(), start=1):
    post_text = row.selftext  # change if your text column is named differently

    rating = rate_post(post_text)
    ratings.append(rating)

    print(f"{i}. Reddit post: {post_text}\n   Model rating: {rating}\n")

# Add the ratings to the dataframe as a new column
filtered_df_2['sentiment_rating'] = ratings

# Save to new CSV
filtered_df_2.to_csv('sentimental_analysis_posts_v1.csv', index=False)

print("Done processing and saved to sentimental_analysis_posts_v1.csv")