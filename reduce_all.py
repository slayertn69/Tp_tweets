import sys, heapq

TOPN = int(sys.argv[1]) if len(sys.argv) > 1 else 10

cur_type = None

cur_h_month, cur_h_tag, cur_h_count = None, None, 0
h_heap = []  # (count, tag)

def close_hashtag_tag():
    global cur_h_tag, cur_h_count, h_heap
    if cur_h_tag is not None:
        heapq.heappush(h_heap, (cur_h_count, cur_h_tag))
        if len(h_heap) > TOPN * 2:
            h_heap[:] = heapq.nlargest(TOPN, h_heap)
            heapq.heapify(h_heap)
    cur_h_tag, cur_h_count = None, 0

def flush_hashtag_month():
    global cur_h_month, h_heap
    if cur_h_month is None:
        return
    top = sorted(h_heap, reverse=True)[:TOPN]
    for cnt, tag in top:
        print("HASHTAG_TOP10\t{0}\t{1}\t{2}".format(cur_h_month, tag, cnt))
    cur_h_month, h_heap[:] = None, []

cur_s_day, cur_s_sum, cur_s_n = None, 0.0, 0
def flush_sentiment_day():
    global cur_s_day, cur_s_sum, cur_s_n
    if cur_s_day is not None and cur_s_n > 0:
        avg = cur_s_sum / cur_s_n
        print("SENTIMENT_AVG\t{0}\t{1:.4f}\t{2}".format(cur_s_day, avg, cur_s_n))
    cur_s_day, cur_s_sum, cur_s_n = None, 0.0, 0

cur_g_country, cur_g_count = None, 0
def flush_geo_country():
    global cur_g_country, cur_g_count
    if cur_g_country is not None:
        print("GEO_COUNT\t{0}\t{1}".format(cur_g_country, cur_g_count))
    cur_g_country, cur_g_count = None, 0

def switch_type(new_type):
    global cur_type
    if cur_type == 'H':
        close_hashtag_tag(); flush_hashtag_month()
    elif cur_type == 'S':
        flush_sentiment_day()
    elif cur_type == 'G':
        flush_geo_country()
    cur_type = new_type

for raw in sys.stdin:
    line = raw.rstrip("\n")
    if not line or "\t" not in line:
        continue
    key, val = line.split("\t", 1)
    if "|" not in key:
        continue

    typ = key[0]  # 'H' | 'S' | 'G'
    if cur_type is None:
        cur_type = typ
    elif typ != cur_type:
        switch_type(typ)

    if typ == 'H':
        try:
            _, month, tag = key.split("|", 2)
            cnt = int(val)
        except Exception:
            continue
        if cur_h_month is None:
            cur_h_month, cur_h_tag, cur_h_count = month, tag, cnt
        elif month != cur_h_month:
            close_hashtag_tag(); flush_hashtag_month()
            cur_h_month, cur_h_tag, cur_h_count = month, tag, cnt
        else:
            if cur_h_tag is None:
                cur_h_tag, cur_h_count = tag, cnt
            elif tag == cur_h_tag:
                cur_h_count += cnt
            else:
                close_hashtag_tag()
                cur_h_tag, cur_h_count = tag, cnt

    elif typ == 'S':
        try:
            _, day = key.split("|", 1)
            parts = val.split("\t")
            score = float(parts[0]); one = int(parts[1]) if len(parts) > 1 else 1
        except Exception:
            continue
        if cur_s_day is None:
            cur_s_day, cur_s_sum, cur_s_n = day, score, one
        elif day == cur_s_day:
            cur_s_sum += score; cur_s_n += one
        else:
            flush_sentiment_day()
            cur_s_day, cur_s_sum, cur_s_n = day, score, one

    elif typ == 'G':
        try:
            _, country = key.split("|", 1)
            v = int(val)
        except Exception:
            continue
        if cur_g_country is None:
            cur_g_country, cur_g_count = country, v
        elif country == cur_g_country:
            cur_g_count += v
        else:
            flush_geo_country()
            cur_g_country, cur_g_count = country, v

switch_type(None)
