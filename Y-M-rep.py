import json
import os
from datetime import datetime
from collections import defaultdict

# Charger le fichier JSON
with open('tweets_with_locations.json', 'r', encoding='utf-8') as f:
    tweets = json.load(f)

# Dictionnaire pour regrouper les tweets par année/mois
tweets_by_month = defaultdict(list)

# Parcourir chaque tweet
for tweet in tweets:
    timestamp = tweet['timestamp']
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    key = f"{dt.year}/{dt.month:02d}"  # ex: "2024/08"
    tweets_by_month[key].append(tweet)

# Enregistrer chaque groupe de tweets dans un fichier JSON par année/mois
for folder_name, tweets_list in tweets_by_month.items():
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, "tweets.json")
    with open(file_path, 'w', encoding='utf-8') as f_out:
        json.dump(tweets_list, f_out, ensure_ascii=False, indent=4)
