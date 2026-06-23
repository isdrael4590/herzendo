import math
import statistics as _st
from collections import Counter, defaultdict


# ── Helpers ──────────────────────────────────────────────────────────────────

def _nums(values):
    return [float(v) for v in values if v is not None]


def _quartile(s, q):
    n = len(s)
    if not n:
        return None
    pos = q * (n - 1)
    lo = int(pos)
    hi = lo + 1
    if hi >= n:
        return s[lo]
    return s[lo] + (pos - lo) * (s[hi] - s[lo])


def _histogram(data, bins=None):
    if not data:
        return [], []
    n = len(data)
    bins = bins or max(5, min(15, math.ceil(math.log2(n)) + 1))
    lo, hi = min(data), max(data)
    if lo == hi:
        return [str(round(lo, 2))], [n]
    w = (hi - lo) / bins
    counts = [0] * bins
    labels = []
    for i in range(bins):
        a = lo + i * w
        b = a + w
        labels.append(f'{a:.2f}–{b:.2f}')
        for v in data:
            if lo <= v < hi or (i == bins - 1 and v == hi):
                if lo + i * w <= v < lo + (i + 1) * w or (i == bins - 1 and v == hi):
                    pass
    # Rebuild cleanly
    counts = [0] * bins
    for v in data:
        idx = min(int((v - lo) / w), bins - 1)
        counts[idx] += 1
    return labels, counts


# ── Univariado ────────────────────────────────────────────────────────────────

def describe_numeric(all_values):
    raw = _nums(all_values)
    n_total = len(all_values)
    n = len(raw)
    n_miss = n_total - n

    if n == 0:
        return {'tipo': 'numerico', 'n': 0, 'n_missing': n_miss}

    s = sorted(raw)
    mean = _st.mean(raw)
    sd = _st.stdev(raw) if n > 1 else 0.0
    cv = abs(sd / mean * 100) if mean != 0 else None
    q1 = _quartile(s, 0.25)
    median = _st.median(raw)
    q3 = _quartile(s, 0.75)
    g1 = None
    if n > 2 and sd > 0:
        g1 = sum((x - mean) ** 3 for x in raw) / n / sd ** 3

    hist_labels, hist_counts = _histogram(raw)

    return {
        'tipo': 'numerico',
        'n': n,
        'n_missing': n_miss,
        'mean': round(mean, 3),
        'sd': round(sd, 3),
        'cv': round(cv, 1) if cv is not None else None,
        'min': round(s[0], 3),
        'q1': round(q1, 3),
        'median': round(median, 3),
        'q3': round(q3, 3),
        'max': round(s[-1], 3),
        'iqr': round(q3 - q1, 3),
        'skewness': round(g1, 3) if g1 is not None else None,
        'hist_labels': hist_labels,
        'hist_counts': hist_counts,
        'box': [round(s[0], 3), round(q1, 3), round(median, 3), round(q3, 3), round(s[-1], 3)],
    }


def describe_categorical(all_values, choices=None):
    n_total = len(all_values)
    data = [v for v in all_values if v is not None and v != '']
    n = len(data)
    n_miss = n_total - n
    counter = Counter(data)
    lm = {val: lbl for val, lbl in (choices or [])} if choices else {}

    if choices:
        order = [val for val, _ in choices if val and counter.get(val, 0) > 0]
        for val in counter:
            if val not in lm:
                order.append(val)
    else:
        order = [v for v, _ in counter.most_common()]

    tabla = [
        {'valor': lm.get(val, val) or val, 'n': counter[val], 'pct': round(counter[val] / n * 100, 1)}
        for val in order if counter.get(val, 0)
    ]

    return {
        'tipo': 'categorico',
        'n': n,
        'n_missing': n_miss,
        'tabla': tabla,
        'chart_labels': [r['valor'] for r in tabla],
        'chart_values': [r['n'] for r in tabla],
    }


# ── Bivariado ─────────────────────────────────────────────────────────────────

def _pearson(x, y):
    n = len(x)
    if n < 3:
        return None
    mx, my = sum(x) / n, sum(y) / n
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    dx = math.sqrt(sum((a - mx) ** 2 for a in x))
    dy = math.sqrt(sum((b - my) ** 2 for b in y))
    if dx == 0 or dy == 0:
        return None
    return round(num / (dx * dy), 4)


def bivar_num_num(vals1, vals2):
    pairs = [
        (float(a), float(b))
        for a, b in zip(vals1, vals2)
        if a is not None and b is not None
    ]
    if not pairs:
        return {'tipo': 'num_num', 'error': 'Sin datos pareados'}
    x, y = zip(*pairs)
    r = _pearson(list(x), list(y))
    return {
        'tipo': 'num_num',
        'n': len(pairs),
        'r': r,
        'r2': round(r ** 2, 4) if r is not None else None,
        'scatter': [{'x': round(xi, 3), 'y': round(yi, 3)} for xi, yi in pairs],
    }


def bivar_num_cat(num_vals, cat_vals, choices_cat=None):
    lm = {v: l for v, l in (choices_cat or [])} if choices_cat else {}
    pairs = [(float(a), b) for a, b in zip(num_vals, cat_vals) if a is not None and b]
    if not pairs:
        return {'tipo': 'num_cat', 'error': 'Sin datos'}

    groups = defaultdict(list)
    for val, cat in pairs:
        groups[cat].append(val)

    grupos = []
    for cat, vals in sorted(groups.items()):
        s = sorted(vals)
        n = len(s)
        mean = _st.mean(s)
        sd = _st.stdev(s) if n > 1 else 0.0
        q1 = _quartile(s, 0.25)
        med = _st.median(s)
        q3 = _quartile(s, 0.75)
        grupos.append({
            'grupo': lm.get(cat, cat) or cat,
            'n': n,
            'mean': round(mean, 3),
            'sd': round(sd, 3),
            'min': round(s[0], 3),
            'q1': round(q1, 3),
            'median': round(med, 3),
            'q3': round(q3, 3),
            'max': round(s[-1], 3),
        })

    return {
        'tipo': 'num_cat',
        'n': len(pairs),
        'grupos': grupos,
        'chart_labels': [g['grupo'] for g in grupos],
        'chart_means': [g['mean'] for g in grupos],
        'chart_sd': [g['sd'] for g in grupos],
    }


def bivar_cat_cat(vals1, vals2, choices1=None, choices2=None):
    lm1 = {v: l for v, l in (choices1 or [])} if choices1 else {}
    lm2 = {v: l for v, l in (choices2 or [])} if choices2 else {}
    pairs = [(a, b) for a, b in zip(vals1, vals2) if a and b]
    if not pairs:
        return {'tipo': 'cat_cat', 'error': 'Sin datos'}

    cats1 = sorted(set(a for a, _ in pairs))
    cats2 = sorted(set(b for _, b in pairs))
    tabla = defaultdict(lambda: defaultdict(int))
    for a, b in pairs:
        tabla[a][b] += 1

    row_totals = {r: sum(tabla[r].values()) for r in cats1}
    col_totals = {c: sum(tabla[r].get(c, 0) for r in cats1) for c in cats2}
    total = sum(row_totals.values())

    chi2 = 0.0
    for r in cats1:
        for c in cats2:
            obs = tabla[r].get(c, 0)
            exp = row_totals[r] * col_totals[c] / total if total else 0
            if exp > 0:
                chi2 += (obs - exp) ** 2 / exp
    df = (len(cats1) - 1) * (len(cats2) - 1)

    # Cramér's V
    v = math.sqrt(chi2 / (total * max(1, min(len(cats1), len(cats2)) - 1))) if total else None

    return {
        'tipo': 'cat_cat',
        'n': len(pairs),
        'chi2': round(chi2, 3),
        'df': df,
        'cramers_v': round(v, 4) if v else None,
        'labels1': [lm1.get(c, c) or c for c in cats1],
        'labels2': [lm2.get(c, c) or c for c in cats2],
        'matrix': [[tabla[r].get(c, 0) for c in cats2] for r in cats1],
    }
