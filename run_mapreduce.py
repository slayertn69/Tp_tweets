#!/usr/bin/env python3
import json
from datetime import datetime
from collections import defaultdict, Counter
import glob

# Mapper
mapped = []

# Parcours tous les fichiers JSON
for file in glob.glob("2024/*/tweets.json"):
    with open(file, "r", encoding="utf-8") as f:
        tweets = json.load(f)
        for tweet in tweets:
            timestamp = tweet.get("timestamp")
            hashtags = tweet.get("hashtags", [])
            if timestamp and hashtags:
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                month = f"{dt.year}-{dt.month:02d}"
                for hashtag in hashtags:
                    mapped.append((month, hashtag, 1))

# Reducer
counter = defaultdict(Counter)
for month, hashtag, count in mapped:
    counter[month][hashtag] += count

# Top 10 par mois
with open("hashtags_top10.txt", "w", encoding="utf-8") as out:
    for month in sorted(counter):
        top10 = counter[month].most_common(10)
        for hashtag, count in top10:
            out.write(f"{month}\t{hashtag}\t{count}\n")

print("Top hashtags par mois générés dans hashtags_top10.txt")
