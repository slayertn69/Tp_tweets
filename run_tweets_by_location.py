#!/usr/bin/env python3
import json
import glob
import os
from collections import defaultdict

# Dictionnaire pour compter les tweets par ville
location_counts = defaultdict(int)

# Parcourir tous les fichiers JSON des tweets
for file in glob.glob("2024/*/tweets.json"):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            continue

        # Si le fichier est un tableau JSON
        if content.startswith("["):
            try:
                tweets = json.loads(content)
            except:
                continue
            for tweet in tweets:
                location = tweet.get("location", {})
                city = location.get("city", "Unknown")
                location_counts[city] += 1
        else:  # Sinon JSONL (un objet par ligne)
            for line in content.splitlines():
                try:
                    tweet = json.loads(line)
                except:
                    continue
                location = tweet.get("location", {})
                city = location.get("city", "Unknown")
                location_counts[city] += 1

# Créer le dossier output si nécessaire et écrire le résultat
os.makedirs("output", exist_ok=True)
output_file = "output/tweets_by_location.txt"

with open(output_file, "w", encoding="utf-8") as out:
    out.write("city\ttweet_count\n")
    for city, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True):
        out.write(f"{city}\t{count}\n")

print(f"Distribution des tweets par ville générée dans {output_file}")
