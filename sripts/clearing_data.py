input_file = ""
output_file = ""

unique_tweets = set()

with open(input_file, 'r', encoding='utf-8') as infile:
    for line in infile:
        tweet = line.strip()
        if tweet:
            unique_tweets.add(tweet)

with open(output_file, 'w', encoding='utf-8') as outfile:
    for tweet in sorted(unique_tweets):
        outfile.write(tweet + "\n")