import pandas as pd
import re

# Load the CSV file
df = pd.read_csv('youtube_comments.csv')
comment_column = 'Comment'

# Emoji-only pattern
emoji_pattern = re.compile(
    r'^[\U0001F600-\U0001F64F'
    r'\U0001F300-\U0001F5FF'
    r'\U0001F680-\U0001F6FF'
    r'\U0001F1E0-\U0001F1FF'
    r'\U00002700-\U000027BF'
    r'\U000024C2-\U0001F251'
    r'\u200d\u2640-\u2642\u2600-\u2B55]+$',
    flags=re.UNICODE
)

# Generalized pattern to match usernames: handles @, @@, dots, underscores, hyphens, digits, etc.
username_pattern = re.compile(r'@{1,2}[A-Za-z0-9._-]+')

# Function to clean a comment: remove usernames and apply filters
def clean_and_filter(comment):
    if pd.isna(comment):
        return False

    # Remove usernames from comments
    comment = username_pattern.sub('', comment).strip()

    # Remove comments with only emojis
    if emoji_pattern.fullmatch(comment):
        return False

    # Remove comments with fewer than 3 words
    if len(comment.split()) < 3:
        return False

    return True

# First remove usernames
df[comment_column] = df[comment_column].astype(str).apply(lambda c: username_pattern.sub('', c).strip())

# Then apply filters
df_cleaned = df[df[comment_column].apply(clean_and_filter)]

# Save cleaned data
df_cleaned.to_csv('cleaned_file_1.csv', index=False)

print("Cleaning complete. Saved to 'cleaned_file.csv'.")


df = pd.read_csv('cleaned_file.csv')

# Randomly select 500 rows used for human annotation
df_sample = df.sample(n=500, random_state=42)  # Setting random_state for reproducibility
df_sample.to_csv('output_file.csv', index=False)

#remove those 500 rows from the original cleaned file
df_remaining = df.drop(df_sample.index)
df_remaining.to_csv('remaining_file.csv', index=False)
print("Sampled 500 rows for human annotation. Remaining data saved to 'remaining_file.csv'.")