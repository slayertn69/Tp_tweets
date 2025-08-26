#!/usr/bin/env python3
import json
from datetime import datetime
from collections import defaultdict
import glob
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Téléchargement des ressources VADER
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Mapper : collecte les sentiments par jour
scores = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0, "total": 0})

for file in glob.glob("2024/*/tweets.json"):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            continue

        # Liste JSON
        if content.startswith("["):
            try:
                tweets = json.loads(content)
            except:
                continue
            for tweet in tweets:
                timestamp = tweet.get("timestamp")
                text = tweet.get("tweet_text", "")
                if timestamp and text:
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    day = dt.strftime("%Y-%m-%d")
                    compound = sia.polarity_scores(text)['compound']
                    if compound >= 0.05:
                        sentiment = "positive"
                    elif compound <= -0.05:
                        sentiment = "negative"
                    else:
                        sentiment = "neutral"
                    scores[day][sentiment] += 1
                    scores[day]["total"] += 1

        else:  # JSONL : un objet par ligne
            for line in content.splitlines():
                try:
                    tweet = json.loads(line)
                except:
                    continue
                timestamp = tweet.get("timestamp")
                text = tweet.get("tweet_text", "")
                if timestamp and text:
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    day = dt.strftime("%Y-%m-%d")
                    compound = sia.polarity_scores(text)['compound']
                    if compound >= 0.05:
                        sentiment = "positive"
                    elif compound <= -0.05:
                        sentiment = "negative"
                    else:
                        sentiment = "neutral"
                    scores[day][sentiment] += 1
                    scores[day]["total"] += 1

# Calculer le pourcentage par jour et écrire le fichier
os.makedirs("output", exist_ok=True)
with open("output/sentiment_daily.txt", "w", encoding="utf-8") as out:
    out.write("day\tpositive%\tneutral%\tnegative%\n")
    for day in sorted(scores):
        total = scores[day]["total"]
        if total == 0:
            continue
        pos_pct = scores[day]["positive"] / total * 100
        neu_pct = scores[day]["neutral"] / total * 100
        neg_pct = scores[day]["negative"] / total * 100
        out.write(f"{day}\t{pos_pct:.2f}\t{neu_pct:.2f}\t{neg_pct:.2f}\n")

print("Analyse des sentiments par jour générée dans output/sentiment_daily.txt")
