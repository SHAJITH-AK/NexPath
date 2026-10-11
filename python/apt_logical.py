"""Logical Reasoning generators (series, coding, directions, syllogisms, seating, Venn)."""
import itertools
from fractions import Fraction
from math import gcd
from apt_common import fmt, near

CAT = "Logical Reasoning"
N = 12
L = lambda i: chr(65 + i % 26)

def number_series(b):
    r, T = b.rng, "number-series"
    S1, S2, S3 = "Arithmetic and geometric series", "Squares, cubes and differences", "Mixed patterns"
    while b.count(T) < N:
        t = r.randrange(8)
        if t == 0: a, d = r.randint(2, 30), r.randint(3, 12); seq, sub, dif, why = [a + i * d for i in range(6)], S1, "easy", f"Each term adds {d}."
        elif t == 1: a, m = r.randint(1, 5), r.choice([2, 3]); seq, sub, dif, why = [a * m ** i for i in range(6)], S1, "easy", f"Each term is multiplied by {m}."
        elif t == 2: c = r.choice([0, 1, -1, 2]); s = r.randint(1, 5); seq, sub, dif, why = [(s + i) ** 2 + c for i in range(6)], S2, "medium", f"Terms follow n² {'+' if c >= 0 else '-'} {abs(c)} for consecutive n."
        elif t == 3: s = r.randint(1, 4); seq, sub, dif, why = [(s + i) ** 3 for i in range(6)], S2, "medium", "Consecutive cubes."
        elif t == 4:
            a, d0 = r.randint(1, 10), r.randint(1, 3); seq = [a]
            for i in range(5): seq.append(seq[-1] + d0 + i)
            sub, dif, why = S2, "medium", f"The differences increase by 1 each time ({d0}, {d0 + 1}, {d0 + 2}, ...)."
        elif t == 5:
            a, d, m = r.randint(2, 6), r.randint(2, 4), r.choice([2, 3]); seq = [v for i in range(3) for v in (a + i * d, (a + i * d) * m)]
            sub, dif, why = S3, "hard", f"Alternate terms are a number and {m} times that number, and the numbers themselves grow by {d}."
        elif t == 6:
            a, m, c = r.randint(1, 5), r.choice([2, 3]), r.choice([1, 2, -1]); seq = [a]
            for i in range(5): seq.append(seq[-1] * m + c)
            sub, dif, why = S3, "hard", f"Each term = previous × {m} {'+' if c > 0 else '-'} {abs(c)}."
        else:
            x, y = r.randint(1, 6), r.randint(2, 9); seq = [x, y]
            for i in range(4): seq.append(seq[-1] + seq[-2])
            sub, dif, why = S3, "medium", "Each term is the sum of the previous two terms."
        hide = 5 if r.random() < .65 else r.randint(1, 4)
        shown = ", ".join("?" if i == hide else str(v) for i, v in enumerate(seq))
        if max(abs(v) for v in seq) > 5000: continue
        b.num(CAT, T, sub, dif, f"Find the missing number in the series: {shown}", seq[hide], why)

def letter_series(b):
    r, T = b.rng, "letter-series"
    S1, S2 = "Letter patterns", "Alphabet position"
    while b.count(T) < N:
        t = r.randrange(6)
        if t == 0:
            s, d = r.randint(0, 10), r.choice([1, 2, 3, 4]); sq = [L(s + i * d) for i in range(5)]
            b.add(CAT, T, S1, "easy", f"Which letter comes next? {', '.join(sq[:4])}, ?", sq[4], [L(s + 4 * d + k) for k in (1, -1, 2)], f"Each letter moves {d} place(s) forward in the alphabet.")
        elif t == 1:
            s, d = r.randint(14, 25), r.choice([2, 3]); sq = [L(s - i * d) for i in range(5)]
            b.add(CAT, T, S1, "medium", f"Which letter comes next? {', '.join(sq[:4])}, ?", sq[4], [L(s - 4 * d + k) for k in (1, -1, 2)], f"Each letter moves {d} place(s) backward.")
        elif t == 2:
            s = r.randint(0, 8); g = lambda i: L(s + i) + L(25 - s - i)
            b.add(CAT, T, S1, "medium", f"Find the next group: {', '.join(g(i) for i in range(3))}, ?", g(3), [L(s + 3) + L(25 - s - 3 + k) for k in (1, -1, 2)] , "The first letter moves forward by 1 and the second moves backward by 1.")
        elif t == 3:
            s = r.randint(0, 8); off = r.choice([(0, 2, 4), (0, 1, 3), (0, 3, 6)]); g = lambda i: "".join(L(s + i + o) for o in off)
            b.add(CAT, T, S1, "hard", f"Find the next group: {', '.join(g(i) for i in range(3))}, ?", g(3), [g(3)[:2] + L(s + 3 + off[2] + k) for k in (1, -1, 2)], "Every letter of a group moves forward by 1 in the next group.")
        elif t == 4:
            s, n = r.randint(0, 15), r.randint(3, 8); back = r.random() < .5; c = L(s)
            b.add(CAT, T, S2, "easy", f"Which letter is {n} places {'to the left' if back else 'to the right'} of {c} in the English alphabet?", L(s - n if back else s + n),
                  [L(s + (-n if back else n) + k) for k in (1, -1, 2)], f"Count {n} letters {'backward' if back else 'forward'} from {c}.")
        else:
            s, n = r.randint(0, 12), r.randint(2, 5)
            b.add(CAT, T, S2, "easy", f"Which letter is {n} places after {L(s)} and {n} places before {L(s + 2 * n)}?", L(s + n), [L(s + n + k) for k in (1, -1, 2)], f"It sits exactly midway: {L(s)} + {n} = {L(s + n)}.")

def coding_decoding(b):
    r, T = b.rng, "coding-decoding"
    S1, S2, S3 = "Letter shifting codes", "Alphabet position codes", "Word substitution"
    words = ["MANGO", "TABLE", "CHAIR", "BRAIN", "PLANT", "STONE", "RIVER", "CLOUD", "HOUSE", "TRAIN", "PAPER", "LIGHT"]
    shift = lambda w, k: "".join(L(ord(c) - 65 + k) for c in w)
    subs = [("In a code, 'table' is called 'chair', 'chair' is called 'bed', 'bed' is called 'lamp' and 'lamp' is called 'shelf'. On what does a person sleep?", "lamp", ["chair", "bed", "shelf"], "A person sleeps on a bed, and 'bed' is called 'lamp' in this code."),
            ("In a code, 'pen' is called 'book', 'book' is called 'bag', 'bag' is called 'box' and 'box' is called 'pencil'. What do students carry on their back?", "box", ["bag", "book", "pencil"], "Students carry a bag; 'bag' is called 'box'."),
            ("In a code, 'red' is called 'blue', 'blue' is called 'green', 'green' is called 'white' and 'white' is called 'black'. What is the colour of milk?", "black", ["white", "green", "blue"], "Milk is white; 'white' is called 'black'."),
            ("In a code, 'sun' is called 'moon', 'moon' is called 'star', 'star' is called 'cloud' and 'cloud' is called 'rain'. What shines in the sky at midday?", "moon", ["sun", "star", "cloud"], "The sun shines at midday; 'sun' is called 'moon'.")]
    for q, a, w, e in subs: b.add(CAT, T, S3, "medium", q, a, w, e)
    while b.count(T) < N:
        t = r.randrange(3); w1, w2 = r.sample(words, 2)
        if t == 0:
            k = r.choice([1, 2, 3, -1, -2]); b.add(CAT, T, S1, "medium", f"In a certain code, {w1} is written as {shift(w1, k)}. How is {w2} written in that code?", shift(w2, k),
                                                  [shift(w2, k + 1), shift(w2, k - 1), shift(w2, -k)], f"Each letter is moved {k} place(s) {'forward' if k > 0 else 'backward'}.")
        elif t == 1:
            mir = lambda w: "".join(L(25 - (ord(c) - 65)) for c in w)
            b.add(CAT, T, S1, "hard", f"In a code, A is replaced by Z, B by Y, C by X and so on. How is {w1} written in that code?", mir(w1), [shift(mir(w1), 1), shift(mir(w1), -1), w1[::-1]], "Each letter is replaced by its mirror letter (A↔Z, B↔Y...).")
        else:
            val = sum(ord(c) - 64 for c in w1); b.num(CAT, T, S2, "easy", f"If A = 1, B = 2, C = 3 and so on, what is the sum of the letter values in the word {w1}?", val,
                                                     " + ".join(f"{c}({ord(c) - 64})" for c in w1) + f" = {val}.")

def blood_relations(b):
    T, S1, S2 = "blood-relations", "Direct relations", "Relation chains"
    items = [
        ("Pointing to a photograph, Meera says, 'He is the son of my mother's only brother.' How is the man related to Meera?", "Cousin", ["Brother", "Uncle", "Nephew"], "Mother's brother is Meera's maternal uncle; his son is her cousin.", "easy", S1),
        ("A is the brother of B. B is the sister of C. C is the father of D. How is A related to D?", "Uncle", ["Father", "Brother", "Grandfather"], "A and C are siblings, so A is the brother of D's father, i.e. D's uncle.", "medium", S2),
        ("Rohan's mother is the only daughter of Arjun. How is Arjun related to Rohan?", "Maternal grandfather", ["Paternal grandfather", "Father", "Uncle"], "Arjun is the father of Rohan's mother.", "easy", S1),
        ("Pointing to a woman, Vikram says, 'Her son is the husband of my sister.' How is the woman related to Vikram's sister?", "Mother-in-law", ["Sister-in-law", "Aunt", "Grandmother"], "The woman is the mother of the sister's husband.", "medium", S2),
        ("X is the father of Y and Y is the mother of Z. How is X related to Z?", "Maternal grandfather", ["Paternal grandfather", "Father", "Uncle"], "X is the father of Z's mother.", "easy", S1),
        ("Anil introduces Sunita as the daughter of the sister of his mother. How is Sunita related to Anil?", "Cousin", ["Sister", "Niece", "Aunt"], "Mother's sister is Anil's aunt; her daughter is his cousin.", "medium", S2),
        ("Ravi tells Mohan, 'Your mother is the only daughter of my mother.' How is Ravi related to Mohan?", "Maternal uncle", ["Father", "Brother", "Cousin"], "Ravi's sister is Mohan's mother, so Ravi is Mohan's maternal uncle.", "hard", S2),
        ("Pointing to a boy, Tina says, 'He is the son of the only child of my grandfather.' How is the boy related to Tina?", "Brother", ["Cousin", "Uncle", "Nephew"], "The grandfather's only child is Tina's parent, so that parent's son is Tina's brother.", "hard", S2),
        ("A is B's sister. C is B's mother. D is C's father. How is A related to D?", "Granddaughter", ["Daughter", "Niece", "Sister"], "C is also A's mother, so D is A's maternal grandfather and A is his granddaughter.", "medium", S2),
        ("Pointing to a man, a woman says, 'He is the brother of the father of my son.' How is the man related to the woman?", "Brother-in-law", ["Brother", "Uncle", "Cousin"], "The father of her son is her husband; his brother is her brother-in-law.", "medium", S2),
        ("A's mother is B's sister and B's daughter is C. How is C related to A?", "Cousin", ["Sister", "Aunt", "Niece"], "A's mother and B are siblings, so A and B's daughter C are cousins.", "medium", S2),
        ("Nina is the daughter of Om. Om's brother is Piyush and Piyush's wife is Rita. How is Nina related to Rita?", "Niece", ["Daughter", "Sister-in-law", "Cousin"], "Rita is the wife of Nina's father's brother, so Rita is Nina's aunt and Nina is her niece.", "medium", S2)]
    for q, a, w, e, d, s in items: b.add(CAT, T, s, d, q, a, w, e)

def direction_sense(b):
    r, T = b.rng, "direction-sense"
    S1, S2 = "Distance and displacement", "Turns and facing"
    names = {(0, 1): "north", (1, 0): "east", (0, -1): "south", (-1, 0): "west"}
    heads = ["north", "east", "south", "west"]
    while b.count(T) < N:
        t = r.randrange(4)
        if t == 0:
            a, c, h = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)]); z = r.randint(1, 6)
            b.num(CAT, T, S1, "medium", f"A man walks {a + z} km north, then {c} km east and then {z} km south. How far is he from his starting point?", h,
                  f"Net north = {a + z} - {z} = {a} km; east = {c} km; distance = √({a}² + {c}²) = {h} km.", unit=" km")
        elif t == 1:
            n0, k, tr = r.choice(heads), r.randint(2, 4), None; turns = [r.choice(["left", "right"]) for _ in range(k)]; h = heads.index(n0)
            for x in turns: h = (h + (1 if x == "right" else -1)) % 4
            b.add(CAT, T, S2, "medium", f"Sameer is facing {n0}. He turns {', then '.join(turns)}. Which direction is he facing now?", heads[h].capitalize(), [x.capitalize() for x in heads if x != heads[h]],
                  "Each right turn is a 90° clockwise turn and each left turn is 90° anticlockwise.")
        elif t == 2:
            a, c, s = r.randint(3, 9), r.randint(2, 8), r.choice(["left", "right"]); start = r.choice(heads); h = heads.index(start)
            b.num(CAT, T, S1, "hard", f"Priya walks {a} km {start}, turns {s} and walks {c} km, then turns {s} again and walks {a} km. How far is she from the starting point?", c,
                  f"After two turns in the same direction she has walked {a} km out and {a} km back, so only the {c} km sideways leg separates her from the start.", unit=" km")
        else:
            d = r.randint(3, 12); pair = r.choice([("north", "east", "North-East"), ("south", "west", "South-West"), ("north", "west", "North-West"), ("south", "east", "South-East")])
            b.add(CAT, T, S1, "medium", f"A boy walks {d} km {pair[0]} and then {d} km {pair[1]}. In which direction is he from his starting point?", pair[2],
                  [x for x in ["North-East", "South-West", "North-West", "South-East"] if x != pair[2]], f"Equal distances {pair[0]} and {pair[1]} put him exactly {pair[2].lower()} of the start.")

def _holds(m, kind, x, y):
    if kind == "all": return not any((g >> x) & 1 and not (g >> y) & 1 for g in m)
    if kind == "no": return not any((g >> x) & 1 and (g >> y) & 1 for g in m)
    if kind == "some": return any((g >> x) & 1 and (g >> y) & 1 for g in m)
    return any((g >> x) & 1 and not (g >> y) & 1 for g in m)  # somenot

_MODELS = [frozenset(i for i in range(8) if mask >> i & 1) for mask in range(256)]
_MODELS = [m for m in _MODELS if all(any((g >> t) & 1 for g in m) for t in range(3))]  # every group has at least one member

def syllogism(b):
    r, T = b.rng, "syllogism"
    triples = [("pens", "books", "boxes"), ("roses", "lamps", "chairs"), ("cups", "plates", "spoons"), ("towers", "bridges", "roads"), ("clocks", "keys", "doors"), ("bags", "shoes", "hats")]
    text = {"all": "All {} are {}.", "no": "No {} are {}.", "some": "Some {} are {}.", "somenot": "Some {} are not {}."}
    opts = ["Only conclusion I follows", "Only conclusion II follows", "Both I and II follow", "Neither I nor II follows"]
    used = {0: 0, 1: 0, 2: 0, 3: 0}; tries = 0
    while b.count(T) < N and tries < 5000:
        tries += 1; names = list(r.choice(triples)); r.shuffle(names)
        k1, k2 = r.choice(list(text)), r.choice(list(text)); p = [(k1, 0, 1), (k2, 1, 2)]
        sat = [m for m in _MODELS if all(_holds(m, *q) for q in p)]
        if not sat: continue
        cons = [(k, x, y) for k in text for x in range(3) for y in range(3) if x != y and (k, x, y) not in p]
        c1, c2 = r.sample(cons, 2); f = [all(_holds(m, *c) for m in sat) for c in (c1, c2)]
        idx = {(True, False): 0, (False, True): 1, (True, True): 2, (False, False): 3}[tuple(f)]
        if used[idx] >= 4: continue
        used[idx] += 1
        stmt = lambda c: text[c[0]].format(names[c[1]], names[c[2]])
        q = f"Statements: {stmt(p[0])} {stmt(p[1])}\nConclusions: I. {stmt(c1)}  II. {stmt(c2)}\n(Take each group named as having at least one member.)"
        hard = any(k in ("some", "somenot", "no") for k in (k1, k2))
        why = f"Checking every Venn arrangement that fits the statements: Conclusion I {'follows' if f[0] else 'does not follow'} and Conclusion II {'follows' if f[1] else 'does not follow'}."
        b.add_fixed(CAT, T, "Two-premise syllogisms", "hard" if hard else "medium", q, opts, idx, why)

def _solve(people, checks, query):
    answers = set()
    for perm in itertools.permutations(people):
        pos = {p: i + 1 for i, p in enumerate(perm)}
        if all(c(pos) for c in checks): answers.add(query(pos))
    return answers

def seating_arrangement(b):
    r, T = b.rng, "seating-arrangement"
    S1, S2, S3 = "Positions in a row", "Circular arrangements", "Row arrangement puzzles"
    P = ["A", "B", "C", "D", "E"]
    puzzles = [
        ("Five friends A, B, C, D and E sit in a row facing north. E sits at one of the two ends. A sits exactly in the middle. C does not sit next to A. B sits somewhere to the left of D. Who sits immediately to the right of A?",
         [lambda p: p["E"] in (1, 5), lambda p: p["A"] == 3, lambda p: abs(p["C"] - 3) != 1, lambda p: p["B"] < p["D"]], lambda p: [x for x in P if p[x] == 4][0], "D"),
        ("A, B, C, D and E sit in a row facing north. B sits at the extreme left. D sits immediately next to B. C sits at the extreme right. A is not next to C. Who sits in the middle?",
         [lambda p: p["B"] == 1, lambda p: abs(p["D"] - p["B"]) == 1, lambda p: p["C"] == 5, lambda p: abs(p["A"] - 5) != 1], lambda p: [x for x in P if p[x] == 3][0], "A"),
        ("Five people A, B, C, D and E stand in a queue. C is third from the front. A is directly behind C. B is somewhere ahead of E. D is at the very front. Who is at the very back?",
         [lambda p: p["C"] == 3, lambda p: p["A"] == 4, lambda p: p["B"] < p["E"], lambda p: p["D"] == 1], lambda p: [x for x in P if p[x] == 5][0], "E")]
    for q, checks, query, expect in puzzles:
        sol = _solve(P, checks, query); assert sol == {expect}, (q, sol)
        b.add(CAT, T, S3, "hard", q, expect, [x for x in P if x != expect][:3], "Place the fixed positions first, then use the remaining conditions to eliminate options.")
    while b.count(T) < N:
        t = r.randrange(5)
        if t == 0:
            k, m = r.randint(3, 15), r.randint(3, 15); b.num(CAT, T, S1, "easy", f"In a row, Aarav is {k}th from the left end and {m}th from the right end. How many people are in the row?", k + m - 1, f"Total = {k} + {m} - 1 = {k + m - 1}.")
        elif t == 1:
            n, k = r.randint(20, 40), r.randint(5, 18); b.num(CAT, T, S1, "easy", f"In a row of {n} students, Kavya's position from the left is {k}. What is her position from the right?", n - k + 1, f"{n} - {k} + 1 = {n - k + 1}.")
        elif t == 2:
            n = r.choice([8, 10, 12]); k = r.randint(1, n); b.num(CAT, T, S2, "medium", f"{n} people sit around a circular table at equal gaps and are numbered 1 to {n} in clockwise order. Who sits directly opposite person {k}?", (k - 1 + n // 2) % n + 1,
                                                              f"The person opposite is {n // 2} seats away: ({k} + {n // 2}) counted within 1-{n}.")
        elif t == 3:
            n, j, y = r.randint(20, 35), r.randint(8, 14), r.randint(7, 15); k = r.randint(15, 19)
            b.num(CAT, T, S1, "hard", f"In a row, A is {k}th from the left and B is {y}th from the right. After they exchange places, A becomes {j}th from the left. How many people are in the row?", j + y - 1,
                  f"After the exchange A stands where B stood, so B was {j}th from the left and {y}th from the right; total = {j} + {y} - 1 = {j + y - 1}.")
        else:
            n, a, m = r.randint(25, 40), r.randint(5, 12), r.randint(5, 12); pb = n - m + 1
            if pb - a < 2: continue
            b.num(CAT, T, S1, "medium", f"In a row of {n} students, Dev is {a}th from the left and Esha is {m}th from the right. How many students stand between them?", pb - a - 1,
                  f"Esha is {n} - {m} + 1 = {pb}th from the left; students between = {pb} - {a} - 1 = {pb - a - 1}.")

def venn_diagrams(b):
    r, T = b.rng, "venn-diagrams"
    S1, S2, S3 = "Two-set problems", "Three-set problems", "Set relationships"
    rel = [("Which diagram best represents the relationship between Doctors, Surgeons and Humans?", "A circle for Surgeons inside a circle for Doctors, both inside a larger circle for Humans", ["Three separate circles", "Doctors and Surgeons as two overlapping circles outside Humans", "Humans inside Surgeons inside Doctors"], "Every surgeon is a doctor and every doctor is a human, so the sets are nested."),
           ("Which diagram best represents Cats, Dogs and Animals?", "Cats and Dogs as two separate circles, both inside a larger circle for Animals", ["Cats and Dogs overlapping inside Animals", "Three overlapping circles of equal size", "Animals inside Cats, Cats inside Dogs"], "Cats and dogs are different animals, so they do not overlap, but both belong to Animals."),
           ("Which diagram best represents Teachers, Women and Doctors?", "Three circles overlapping each other partially", ["Three separate circles", "Teachers inside Women inside Doctors", "Women and Doctors separate, Teachers containing both"], "A person can be a teacher, a woman and a doctor, but none of the sets contains another."),
           ("Which diagram best represents Pens, Stationery and Erasers?", "Pens and Erasers as two separate circles inside a larger circle for Stationery", ["Pens and Erasers overlapping outside Stationery", "Pens inside Erasers inside Stationery", "Three separate circles"], "Pens and erasers are different objects that both belong to stationery.")]
    for q, a, w, e in rel: b.add(CAT, T, S3, "medium", q, a, w, e)
    while b.count(T) < N:
        t = r.randrange(4)
        if t == 0:
            n, a, c, x = r.choice([60, 80, 100, 120]), r.randint(30, 60), r.randint(25, 55), r.randint(8, 25)
            if a + c - x > n or x >= min(a, c): continue
            b.num(CAT, T, S1, "easy", f"In a group of {n} people, {a} like tea, {c} like coffee and {x} like both. How many like neither?", n - (a + c - x), f"Either = {a} + {c} - {x} = {a + c - x}; neither = {n} - {a + c - x}.")
        elif t == 1:
            n, a, c = r.choice([50, 60, 80, 100]), r.randint(30, 60), r.randint(30, 60)
            if a + c <= n or a > n or c > n: continue
            b.num(CAT, T, S1, "medium", f"Every student in a class of {n} plays cricket or football. {a} play cricket and {c} play football. How many play both?", a + c - n, f"Both = {a} + {c} - {n} = {a + c - n}.")
        elif t == 2:
            a, c, d, ab, bc, ac, abc = r.randint(30, 50), r.randint(30, 50), r.randint(30, 50), r.randint(8, 15), r.randint(8, 15), r.randint(8, 15), r.randint(3, 7)
            b.num(CAT, T, S2, "hard", f"In a survey, n(A) = {a}, n(B) = {c}, n(C) = {d}, n(A∩B) = {ab}, n(B∩C) = {bc}, n(A∩C) = {ac} and n(A∩B∩C) = {abc}. Find n(A∪B∪C).", a + c + d - ab - bc - ac + abc,
                  f"{a} + {c} + {d} - {ab} - {bc} - {ac} + {abc} = {a + c + d - ab - bc - ac + abc}.")
        else:
            n, a, c = r.choice([40, 50, 60, 100]), r.randint(15, 35), r.randint(15, 35); x = r.randint(3, 10)
            if a + c - x > n: continue
            b.num(CAT, T, S1, "medium", f"In a class of {n} students, {a} study French and {c} study German. {x} study both. How many study exactly one of the two languages?", a + c - 2 * x, f"Exactly one = ({a} - {x}) + ({c} - {x}) = {a + c - 2 * x}.")

ALL = [number_series, letter_series, coding_decoding, blood_relations, direction_sense, syllogism, seating_arrangement, venn_diagrams]
