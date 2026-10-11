"""Shared helpers for the aptitude question builder (see build_aptitude_questions.py)."""
import hashlib, random
from fractions import Fraction

LETTERS = "abcd"

def fmt(x):
    """Number -> clean string (no trailing .0)."""
    if isinstance(x, Fraction):
        x = float(x)
    if isinstance(x, float):
        x = round(x, 2)
        if x.is_integer():
            return str(int(x))
        return ("%.2f" % x).rstrip("0").rstrip(".")
    return str(x)

def frac(f):
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

def near(rng, ans, k=3):
    """k distinct plausible wrong numbers close to ans."""
    is_int = float(ans).is_integer()
    mag = max(abs(ans), 4)
    steps = sorted({1, 2, 3, 4, 5, 10} | {max(1, round(mag * p)) for p in (.05, .1, .15, .2, .25, .3, .5)})
    cands = []
    for s in steps:
        for sign in (1, -1):
            v = ans + sign * s
            if not is_int:
                v = round(v, 2)
            if v != ans and (v > 0 or ans <= 0):
                cands.append(v)
    cands = sorted(dict.fromkeys(cands), key=lambda v: abs(v - ans))
    return rng.sample(cands[:10], k)

class Bank:
    def __init__(self, seed=2026):
        self.rng = random.Random(seed)
        self.rows = []
        self._seen = set()
        self._count = {}

    def count(self, topic):
        return self._count.get(topic, 0)

    def _store(self, category, topic, sub, diff, question, options, ans_idx, expl, by_options=False):
        # by_options=True: questions with identical wording (e.g. "Which sentence is correct?") differ only by their options.
        ident = question + ("||" + "|".join(sorted(options)) if by_options else "")
        key = (topic, ident)
        if key in self._seen:
            return False
        assert len(options) == 4 and len(set(options)) == 4, (topic, question, options)
        self._seen.add(key)
        self._count[topic] = self._count.get(topic, 0) + 1
        self.rows.append(dict(category=category, topic=topic, subtopic=sub, difficulty=diff, question=question,
                              options=options, answer=LETTERS[ans_idx], explanation=expl,
                              q_hash=hashlib.md5(f"{topic}|{ident}".encode()).hexdigest()))
        return True

    def add(self, category, topic, sub, diff, question, correct, wrongs, expl, by_options=False):
        """Correct answer + wrong answers (strings); option positions are shuffled."""
        wrongs = [w for w in dict.fromkeys(wrongs) if w != correct][:3]
        opts = [correct] + wrongs
        self.rng.shuffle(opts)
        return self._store(category, topic, sub, diff, question, opts, opts.index(correct), expl, by_options)

    def add_fixed(self, category, topic, sub, diff, question, options, ans_idx, expl):
        """Options keep the given order (needed for 'Only I follows'-style answers)."""
        return self._store(category, topic, sub, diff, question, list(options), ans_idx, expl)

    def num(self, category, topic, sub, diff, question, ans, expl, unit="", prefix="", wrongs=None):
        """Numeric answer; wrong options are generated near the answer unless supplied."""
        ws = wrongs if wrongs is not None else near(self.rng, ans)
        f = lambda v: f"{prefix}{fmt(v)}{unit}"
        return self.add(category, topic, sub, diff, question, f(ans), [f(w) for w in ws], expl)
