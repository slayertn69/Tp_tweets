#!/usr/bin/env python3
import pandas as pd
import os

# 1️⃣ Lire le fichier des sentiments quotidiens
input_file = "output/sentiment_daily.txt"
df = pd.read_csv(input_file, sep="\t")

# 2️⃣ Calculer la moyenne et l'écart-type pour détecter les anomalies
mean_pos = df['positive%'].mean()
std_pos = df['positive%'].std()
mean_neg = df['negative%'].mean()
std_neg = df['negative%'].std()

# Seuil pour considérer un événement comme significatif
threshold = 1.5  # 1.5 écarts-types

# 3️⃣ Identifier les pics positifs ou négatifs
df['event'] = ""
df.loc[df['positive%'] > mean_pos + threshold*std_pos, 'event'] = 'Positive Spike'
df.loc[df['negative%'] > mean_neg + threshold*std_neg, 'event'] = 'Negative Spike'

# 4️⃣ Filtrer seulement les jours avec événement
events = df[df['event'] != ""]

# 5️⃣ Créer le dossier output si nécessaire et sauvegarder le résultat
os.makedirs("output", exist_ok=True)
output_file = "output/sentiment_events.txt"
events.to_csv(output_file, sep="\t", index=False)

print(f"Analyse des événements significatifs générée dans {output_file}")
print(events)
