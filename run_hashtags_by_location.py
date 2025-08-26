#!/usr/bin/env python3
import json
import glob
import os
from collections import defaultdict, Counter

# Dictionnaire pour stocker les hashtags par ville
hashtags_by_city = defaultdict(Counter)

# Parcourir tous les fichiers JSON
for file in glob.glob("2024/*/tweets.json"):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            continue

        # JSON array
        if content.startswith("["):
            try:
                tweets = json.loads(content)
            except:
                continue
            for tweet in tweets:
                location = tweet.get("location", {})
                city = location.get("city", "Unknown")
                hashtags = tweet.get("hashtags", [])
                for tag in hashtags:
                    hashtags_by_city[city][tag] += 1
        else:  # JSONL
            for line in content.splitlines():
                try:
                    tweet = json.loads(line)
                except:
                    continue
                location = tweet.get("location", {})
                city = location.get("city", "Unknown")
                hashtags = tweet.get("hashtags", [])
                for tag in hashtags:
                    hashtags_by_city[city][tag] += 1

# Créer le dossier output si nécessaire et écrire le résultat
os.makedirs("output", exist_ok=True)
output_file = "output/hashtags_by_location.txt"

with open(output_file, "w", encoding="utf-8") as out:
    out.write("city\thashtag\tcount\n")
    for city, counter in hashtags_by_city.items():
        for tag, count in counter.most_common():  # tri par fréquence
            out.write(f"{city}\t{tag}\t{count}\n")

print(f"Analyse thématique par ville générée dans {output_file}")
