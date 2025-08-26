#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, datetime, re

# Sentiment : VADER si dispo, sinon fallback léger
USE_VADER = True
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    an = SentimentIntensityAnalyzer()
except Exception:
    USE_VADER = False
    POS = {"good","great","love","excellent","happy","nice","awesome","cool","super","fantastic","amazing",
           "bravo","merci","génial","genial","top","parfait","formidable","content","joyeux"}
    NEG = {"bad","hate","terrible","sad","angry","awful","worst","horrible",
           "nul","pourri","triste","déteste","colère","fâché","fache","furieux"}
    def naive_sent_score(text):
        t = text.lower()
        p = sum(w in t for w in POS)
        n = sum(w in t for w in NEG)
        return 0.0 if (p+n)==0 else (p-n)/(p+n)

def parse_dt(ts):
    if not ts:
        return None
    s = str(ts)
    # Epoch
    if re.match(r'^\d+(\.\d+)?$', s):
        try:
            return datetime.datetime.utcfromtimestamp(float(s))
        except Exception:
            pass
    # Twitter v1.1
    for fmt in ("%a %b %d %H:%M:%S %z %Y",):
        try:
            return datetime.datetime.strptime(s, fmt)
        except Exception:
            pass
    # ISO 8601 (normalise le tz)
    s2 = s.replace('Z', '+0000')
    s2 = re.sub(r'([+-]\d{2}):(\d{2})$', r'\1\2', s2)
    s2_no_frac = re.sub(r'\.\d+', '', s2)
    for cand in (s2, s2_no_frac, s):
        for fmt in ("%Y-%m-%dT%H:%M:%S%z",
                    "%Y-%m-%d %H:%M:%S%z",
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d"):
            try:
                return datetime.datetime.strptime(cand, fmt)
            except Exception:
                pass
    return None

def get_country(t):
    geo = t.get('geo') or {}
    place = t.get('place') or {}
    c = geo.get('country') or geo.get('country_code') \
        or place.get('country_code') or place.get('country') \
        or t.get('user',{}).get('location_country')
    return (str(c) if c else "UNK").upper()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    # 1ère désérialisation
    try:
        tw = json.loads(line)
    except Exception:
        continue

    # Si c'est une chaîne JSON (ex: "\"{...}\""), re-parse
    if isinstance(tw, str):
        try:
            tw2 = json.loads(tw)
            tw = tw2
        except Exception:
            continue

    # Certains dumps v2 ont l'objet sous "data"
    if isinstance(tw, dict) and isinstance(tw.get('data'), dict) and ('created_at' in tw['data'] or 'text' in tw['data']):
        tw = tw['data']

    # Si ce n'est toujours pas un objet dict → on ignore
    if not isinstance(tw, dict):
        continue

    dt = parse_dt(tw.get('created_at'))
    if not dt:
        continue
    ym  = dt.strftime('%Y-%m')
    day = dt.strftime('%Y-%m-%d')

    # (1) HASHTAGS
    ents = tw.get('entities') or {}
    tags = ents.get('hashtags') or []
    for h in tags:
        tag = h if isinstance(h, str) else (h.get('tag') or h.get('text'))
        tag = (tag or "").lower().strip()
        if tag:
            print("H|{0}|{1}\t1".format(ym, tag))

    # (2) SENTIMENT
    txt = (tw.get('text') or "").strip()
    if txt:
        score = an.polarity_scores(txt)['compound'] if USE_VADER else naive_sent_score(txt)
        print("S|{0}\t{1}\t1".format(day, score))

    # (3) GEO
    country = get_country(tw)
    print("G|{0}\t1".format(country))
