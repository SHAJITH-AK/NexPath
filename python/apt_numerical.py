"""Numerical Ability generators.  Every answer is computed, never typed by hand."""
from fractions import Fraction
from math import gcd, comb, perm, factorial, sqrt, isqrt
from collections import Counter
from apt_common import fmt, frac, near

CAT = "Numerical Ability"
N = 12  # questions generated per topic

def lcm(a, b): return a * b // gcd(a, b)

def number_system(b):
    r, T = b.rng, "number-system"
    while b.count(T) < N:
        t = r.choice(["hcf", "lcm", "rem", "div9", "unit", "primes", "sum"])
        if t in ("hcf", "lcm"):
            g = r.choice([4, 6, 7, 8, 9, 12, 15]); x, y = [g * v for v in r.sample([2, 3, 4, 5, 6, 7, 9, 10], 2)]
            ans = gcd(x, y) if t == "hcf" else lcm(x, y)
            b.num(CAT, T, "HCF and LCM", "easy", f"Find the {t.upper()} of {x} and {y}.", ans,
                  f"Prime-factorise both numbers; {t.upper()}({x}, {y}) = {ans}.")
        elif t == "rem":
            n, d = r.randint(200, 999), r.choice([7, 9, 11, 13]); ans = n % d
            ws = r.sample([v for v in range(d) if v != ans], 3)
            b.num(CAT, T, "Remainders and divisibility", "medium", f"What is the remainder when {n} is divided by {d}?", ans,
                  f"{n} = {d} × {n // d} + {ans}.", wrongs=ws)
        elif t == "div9":
            c = 9 * r.randint(112, 1100); ws = [c + k for k in r.sample(range(1, 9), 3)]
            b.add(CAT, T, "Remainders and divisibility", "easy", "Which of these numbers is divisible by 9?", str(c), [str(w) for w in ws],
                  f"A number is divisible by 9 when its digit sum is divisible by 9. Digit sum of {c} = {sum(map(int, str(c)))}.")
        elif t == "unit":
            a, n = r.randint(2, 9), r.randint(10, 99); ans = pow(a, n, 10)
            ws = r.sample([v for v in range(10) if v != ans], 3)
            b.num(CAT, T, "Unit digit and primes", "hard", f"What is the unit digit of {a}^{n}?", ans,
                  f"Unit digits of powers of {a} repeat in a cycle; {n} falls at the position that gives {ans}.", wrongs=ws)
        elif t == "primes":
            lo = r.choice([1, 10, 20, 30, 40]); hi = lo + r.choice([20, 30])
            ans = sum(all(p % d for d in range(2, isqrt(p) + 1)) for p in range(max(lo, 2), hi + 1))
            b.num(CAT, T, "Unit digit and primes", "medium", f"How many prime numbers are there between {lo} and {hi} (inclusive)?", ans,
                  f"Check each number from {lo} to {hi}; exactly {ans} have no divisor other than 1 and themselves.")
        else:
            n = r.randint(8, 30); kind = r.choice(["odd", "even", "natural"])
            ans = {"odd": n * n, "even": n * (n + 1), "natural": n * (n + 1) // 2}[kind]
            f = {"odd": "n²", "even": "n(n+1)", "natural": "n(n+1)/2"}[kind]
            b.num(CAT, T, "Number properties", "easy", f"What is the sum of the first {n} {kind} numbers?", ans,
                  f"Sum of first n {kind} numbers = {f}; for n = {n} this is {ans}.")

def percentages(b):
    r, T = b.rng, "percentages"
    while b.count(T) < N:
        t = r.randrange(6)
        if t == 0:
            P, n = r.choice([5, 8, 12, 15, 20, 25, 30, 35, 40, 45, 60, 75]), r.choice(range(200, 2001, 100)); ans = P * n // 100
            b.num(CAT, T, "Basic percentage calculations", "easy", f"What is {P}% of {n}?", ans, f"{P}/100 × {n} = {ans}.")
        elif t == 1:
            w, p = r.choice([40, 60, 80, 120, 150, 200, 250, 300]), r.choice([10, 20, 25, 30, 40, 45, 60, 75, 80])
            if w * p % 100: continue
            b.num(CAT, T, "Basic percentage calculations", "easy", f"What percentage of {w} is {w * p // 100}?", p,
                  f"({w * p // 100}/{w}) × 100 = {p}%.", unit="%")
        elif t == 2:
            o, p = r.choice(range(200, 1501, 50)), r.choice([10, 20, 25, 30, 40, 50])
            if o * (100 + p) % 100: continue
            b.num(CAT, T, "Percentage increase and decrease", "medium",
                  f"After an increase of {p}%, a number becomes {o * (100 + p) // 100}. What was the original number?", o,
                  f"Original × {100 + p}/100 = {o * (100 + p) // 100}, so original = {o}.")
        elif t == 3:
            o, p = r.choice(range(200, 1501, 50)), r.choice([10, 20, 25, 30, 40])
            if o * (100 - p) % 100: continue
            b.num(CAT, T, "Percentage increase and decrease", "medium",
                  f"A price falls by {p}% to Rs. {o * (100 - p) // 100}. What was the original price?", o,
                  f"Original × {100 - p}/100 = {o * (100 - p) // 100}, so original = {o}.", prefix="Rs. ")
        elif t == 4:
            a, c = r.choice([(20, 10), (25, 20), (10, 10), (30, 20), (50, 20), (40, 25), (20, 20), (25, 10)])
            up = r.random() < .5
            net = Fraction(100 + a, 100) * (Fraction(100 + c, 100) if up else Fraction(100 - c, 100)) - 1
            pct = net * 100
            lab = lambda v: f"{fmt(abs(v))}% {'increase' if v > 0 else 'decrease'}" if v != 0 else "No change"
            wr = [lab(a + c if up else a - c), lab(-pct), lab(pct + 2), lab(pct - 2)]
            b.add(CAT, T, "Successive percentage changes", "hard",
                  f"A quantity is first increased by {a}% and then {'increased' if up else 'decreased'} by {c}%. What is the net change?",
                  lab(pct), wr, f"Multiplier = {100 + a}/100 × {(100 + c) if up else (100 - c)}/100 = {fmt(1 + net)}, a net {lab(pct).lower()}.")
        else:
            M, p, y = r.choice([400, 500, 600, 800, 1000]), r.choice([30, 35, 40, 45]), r.choice([10, 15, 20, 25])
            if M * p % 100: continue
            s = M * p // 100 - y
            b.num(CAT, T, "Percentage word problems", "medium",
                  f"A student scored {s} marks and failed by {y} marks. If the pass mark is {p}%, what are the maximum marks?", M,
                  f"Pass mark = {s} + {y} = {s + y}, which is {p}% of the maximum, so maximum = {M}.")

def profit_and_loss(b):
    r, T = b.rng, "profit-and-loss"
    while b.count(T) < N:
        t = r.randrange(6); S1, S2 = "Profit and loss basics", "Discount and marked price"
        if t == 0:
            cp, p = r.choice(range(200, 1501, 20)), r.choice([10, 20, 25, 30, 40, 50]); ans = cp * (100 + p) // 100
            b.num(CAT, T, S1, "easy", f"An article costs Rs. {cp} and is sold at a profit of {p}%. What is the selling price?", ans,
                  f"SP = {cp} × {100 + p}/100 = {ans}.", prefix="Rs. ")
        elif t == 1:
            cp, l = r.choice(range(200, 1501, 50)), r.choice([10, 20, 25, 30]); sp = cp * (100 - l) // 100
            b.num(CAT, T, S1, "medium", f"An article is sold for Rs. {sp} at a loss of {l}%. What was its cost price?", cp,
                  f"CP × {100 - l}/100 = {sp}, so CP = {cp}.", prefix="Rs. ")
        elif t == 2:
            cp, p = r.choice(range(200, 1501, 20)), r.choice([10, 15, 20, 25, 30, 40]); sp = cp * (100 + p) // 100
            if cp * (100 + p) % 100: continue
            b.num(CAT, T, S1, "easy", f"A shopkeeper buys an item for Rs. {cp} and sells it for Rs. {sp}. What is the profit percentage?", p,
                  f"Profit = {sp - cp}; profit% = {sp - cp}/{cp} × 100 = {p}%.", unit="%")
        elif t == 3:
            m, d = r.choice([(20, 10), (25, 20), (40, 25), (50, 20), (30, 10), (20, 25), (10, 20), (60, 25)])
            net = Fraction((100 + m) * (100 - d), 100) - 100
            lab = lambda v: (f"{fmt(abs(v))}% profit" if v > 0 else f"{fmt(abs(v))}% loss") if v != 0 else "No profit, no loss"
            b.add(CAT, T, S2, "hard", f"A trader marks goods {m}% above cost price and then allows a discount of {d}%. What is his overall result?",
                  lab(net), [lab(m - d), lab(-net), lab(net + 3), lab(net - 3)],
                  f"Take CP = 100: marked = {100 + m}, SP = {100 + m} × {100 - d}/100 = {fmt(Fraction((100 + m) * (100 - d), 100))}, so {lab(net).lower()}.")
        elif t == 4:
            mp, d = r.choice(range(400, 3001, 100)), r.choice([10, 20, 25, 30]); ans = mp * (100 - d) // 100
            b.num(CAT, T, S2, "easy", f"The marked price of a shirt is Rs. {mp}. A discount of {d}% is given. What is the selling price?", ans,
                  f"SP = {mp} × {100 - d}/100 = {ans}.", prefix="Rs. ")
        else:
            cp, p, q = r.choice(range(200, 1001, 100)), r.choice([5, 10, 15]), r.choice([20, 25, 30]); extra = cp * (q - p) // 100
            if cp * (q - p) % 100: continue
            b.num(CAT, T, S1, "hard", f"An article sold at a profit of {p}% would give a profit of {q}% if sold for Rs. {extra} more. Find its cost price.", cp,
                  f"The extra Rs. {extra} equals {q - p}% of CP, so CP = {extra} × 100/{q - p} = {cp}.", prefix="Rs. ")

def ratio_and_proportion(b):
    r, T = b.rng, "ratio-and-proportion"
    S1, S2, S3 = "Dividing amounts in a ratio", "Proportion and ratio problems", "Mixtures"
    while b.count(T) < N:
        t = r.randrange(6)
        if t == 0:
            a, c, d, k = r.randint(1, 5), r.randint(2, 6), r.randint(3, 8), r.choice(range(20, 201, 10))
            if len({a, c, d}) < 3: continue
            tot = (a + c + d) * k; big = r.random() < .5
            b.num(CAT, T, S1, "medium", f"Rs. {tot} is divided among three people in the ratio {a}:{c}:{d}. What is the {'largest' if big else 'smallest'} share?",
                  k * (max(a, c, d) if big else min(a, c, d)), f"One part = {tot}/{a + c + d} = {k}; the {'largest' if big else 'smallest'} share is {k} × {max(a, c, d) if big else min(a, c, d)}.", prefix="Rs. ")
        elif t == 1:
            a, c = r.choice([(2, 3), (3, 5), (4, 7), (5, 8), (3, 7), (2, 5)]); m = r.randint(3, 9)
            b.num(CAT, T, S2, "easy", f"If {a} : {c} = {a * m} : x, find x.", c * m, f"x = {c} × {a * m}/{a} = {c * m}.")
        elif t == 2:
            a, c, k = r.choice([(3, 2), (4, 3), (5, 4), (7, 5), (2, 3)]), None, r.randint(4, 15)
            (a, c) = a; n = (a + c) * k
            b.num(CAT, T, S2, "easy", f"In a class of {n} students the ratio of boys to girls is {a}:{c}. How many girls are there?", c * k,
                  f"One part = {n}/{a + c} = {k}; girls = {c} × {k} = {c * k}.")
        elif t == 3:
            a, c, w, k = r.choice([(3, 2, 4, 1), (2, 1, 3, 1), (3, 1, 2, 1), (4, 1, 3, 1), (5, 3, 6, 1)]), None, None, None
            a, bb, cc, _ = a; k = r.randint(2, 9); total = k * (a + bb)
            if cc <= bb: continue
            b.num(CAT, T, S3, "hard", f"A {total}-litre mixture has milk and water in the ratio {a}:{bb}. How much water must be added so the ratio becomes {a}:{cc}?",
                  k * (cc - bb), f"Milk = {a * k} L, water = {bb * k} L. For {a}:{cc} water must be {cc * k} L, so add {cc * k} - {bb * k} = {k * (cc - bb)} L.", unit=" litres")
        elif t == 4:
            a, c = r.choice([(2, 3), (3, 4), (5, 7), (4, 9), (3, 8)]); k = r.randint(4, 20); s = (a + c) * k
            b.num(CAT, T, S2, "medium", f"Two numbers are in the ratio {a}:{c} and their sum is {s}. What is the difference between them?", (c - a) * k,
                  f"One part = {s}/{a + c} = {k}; difference = ({c} - {a}) × {k} = {(c - a) * k}.")
        else:
            a, c, d, e = r.choice([(2, 3, 4, 5), (1, 2, 3, 4), (3, 4, 2, 5), (5, 6, 3, 7), (2, 5, 3, 4)])
            x, y = a * d, c * e; g = gcd(x, y); ans = f"{x // g}:{y // g}"
            wr = [f"{a * e}:{c * d}", f"{a + d}:{c + e}", f"{a * c}:{d * e}", f"{c * d}:{a * e}"]
            b.add(CAT, T, S2, "hard", f"If A:B = {a}:{c} and B:C = {d}:{e}, what is A:C?", ans, wr,
                  f"Make B equal: A:C = ({a} × {d}) : ({c} × {e}) = {x}:{y} = {ans}.")

def averages(b):
    r, T = b.rng, "averages"
    S1, S2 = "Simple averages", "Missing and replaced values"
    while b.count(T) < N:
        t = r.randrange(6)
        if t == 0:
            xs = [r.randint(10, 60) for _ in range(4)]; xs.append(5 - sum(xs) % 5 + r.randrange(0, 40, 5) + 0)
            xs[-1] += (-sum(xs)) % 5
            b.num(CAT, T, S1, "easy", f"Find the average of {', '.join(map(str, xs))}.", sum(xs) // 5, f"Sum = {sum(xs)}; average = {sum(xs)}/5 = {sum(xs) // 5}.")
        elif t == 1:
            n, a = r.randint(6, 15), r.randint(30, 60); a2 = a + r.randint(1, 4); m = (n + 1) * a2 - n * a
            b.num(CAT, T, S2, "medium", f"The average of {n} numbers is {a}. When one more number is included the average becomes {a2}. What is the new number?", m,
                  f"New total = {n + 1} × {a2} = {(n + 1) * a2}; old total = {n * a}; new number = {m}.")
        elif t == 2:
            s4 = 4 * r.randint(20, 60); x = r.randint(20, 90)
            x += (-(s4 + x)) % 5
            b.num(CAT, T, S2, "medium", f"The average of five numbers is {(s4 + x) // 5}. If one of them, {x}, is removed, what is the average of the remaining four?", s4 // 4,
                  f"Total = 5 × {(s4 + x) // 5} = {s4 + x}; remaining total = {s4 + x} - {x} = {s4}; average = {s4 // 4}.")
        elif t == 3:
            k = r.choice(["odd", "even"]); n = r.choice([9, 11, 15, 20, 25, 30, 40])
            b.num(CAT, T, S1, "easy", f"What is the average of the first {n} {'natural numbers' if k == 'odd' else 'even numbers'}?" if k == "odd" and n % 2 else f"What is the average of the first {n} even numbers?",
                  (n + 1) / 2 if k == "odd" and n % 2 else n + 1, "Average of first n natural numbers = (n+1)/2; of first n even numbers = n+1.")
        elif t == 4:
            n, a = r.randint(5, 9), r.randint(28, 45); a2 = a - r.randint(1, 3); x = n * a - (n - 1) * a2
            if not 18 <= x <= 70: continue
            b.num(CAT, T, S2, "hard", f"The average age of {n} people is {a} years. When one person leaves, the average of the rest becomes {a2} years. How old was the person who left?", x,
                  f"Total before = {n * a}; total after = {(n - 1) * a2}; age of the person = {x}.", unit=" years")
        else:
            n1, n2, a1, a2 = r.choice([10, 20, 30]), r.choice([20, 30, 40]), r.choice([50, 60, 70]), r.choice([60, 70, 80, 90])
            if (n1 * a1 + n2 * a2) % (n1 + n2) or a1 == a2: continue
            b.num(CAT, T, S2, "medium", f"Section A has {n1} students with an average score of {a1}; Section B has {n2} students with an average of {a2}. What is the combined average?",
                  (n1 * a1 + n2 * a2) // (n1 + n2), f"Total marks = {n1 * a1} + {n2 * a2}; divide by {n1 + n2} students.")

def simple_interest(b):
    r, T = b.rng, "simple-interest"
    S1, S2, S3 = "Simple interest calculation", "Finding rate, time or principal", "Amount and doubling"
    while b.count(T) < N:
        t, P, R, Y = r.randrange(7), r.choice(range(1000, 10001, 500)), r.choice([4, 5, 6, 8, 10, 12]), r.choice([2, 3, 4, 5])
        si = P * R * Y // 100
        if P * R * Y % 100: continue
        if t == 0: b.num(CAT, T, S1, "easy", f"Find the simple interest on Rs. {P} at {R}% per annum for {Y} years.", si, f"SI = P×R×T/100 = {P}×{R}×{Y}/100 = {si}.", prefix="Rs. ")
        elif t == 1: b.num(CAT, T, S3, "easy", f"What amount will Rs. {P} become in {Y} years at {R}% simple interest per annum?", P + si, f"SI = {si}; amount = {P} + {si} = {P + si}.", prefix="Rs. ")
        elif t == 2: b.num(CAT, T, S2, "medium", f"Simple interest on Rs. {P} for {Y} years is Rs. {si}. Find the rate per annum.", R, f"R = SI×100/(P×T) = {si}×100/({P}×{Y}) = {R}%.", unit="%")
        elif t == 3: b.num(CAT, T, S2, "medium", f"In how many years will Rs. {P} earn Rs. {si} as simple interest at {R}% per annum?", Y, f"T = SI×100/(P×R) = {Y} years.", unit=" years")
        elif t == 4: b.num(CAT, T, S2, "medium", f"A sum earns Rs. {si} simple interest in {Y} years at {R}% per annum. Find the sum.", P, f"P = SI×100/(R×T) = {si}×100/({R}×{Y}) = {P}.", prefix="Rs. ")
        elif t == 5:
            y = r.choice([4, 5, 8, 10, 20, 25]); b.num(CAT, T, S3, "hard", f"A sum of money doubles itself in {y} years at simple interest. What is the rate per annum?", 100 / y,
                                                       f"Interest = principal in {y} years, so R = 100/{y} = {fmt(100 / y)}%.", unit="%")
        else:
            rr = r.choice([5, 8, 10, 20, 25]); b.num(CAT, T, S3, "hard", f"In how many years will a sum triple itself at {rr}% simple interest per annum?", 200 // rr,
                                                    f"Interest = 2 × principal, so T = 200/{rr} = {200 // rr} years.", unit=" years")

def compound_interest(b):
    r, T = b.rng, "compound-interest"
    S1, S2, S3 = "Compound interest calculation", "Difference between CI and SI", "Growth and doubling"
    while b.count(T) < N:
        t, P, R, Y = r.randrange(6), r.choice([2000, 2500, 4000, 5000, 8000, 10000, 12500, 16000, 20000]), r.choice([4, 5, 8, 10, 12, 15, 20]), r.choice([2, 3])
        amt = Fraction(P) * Fraction(100 + R, 100) ** Y
        if t == 0 and amt.denominator == 1: b.num(CAT, T, S1, "medium", f"Find the compound interest on Rs. {P} at {R}% per annum for {Y} years (compounded annually).", int(amt) - P,
                                                 f"Amount = {P} × (1 + {R}/100)^{Y} = {int(amt)}; CI = {int(amt)} - {P} = {int(amt) - P}.", prefix="Rs. ")
        elif t == 1 and amt.denominator == 1: b.num(CAT, T, S1, "medium", f"What will Rs. {P} amount to in {Y} years at {R}% compound interest per annum?", int(amt),
                                                   f"Amount = {P} × (1 + {R}/100)^{Y} = {int(amt)}.", prefix="Rs. ")
        elif t == 2 and Fraction(P * R * R, 10000).denominator == 1: b.num(CAT, T, S2, "hard", f"Find the difference between compound interest and simple interest on Rs. {P} at {R}% per annum for 2 years.", P * R * R // 10000,
                                                                          f"For 2 years, CI - SI = P × (R/100)² = {P} × {R}²/10000 = {P * R * R // 10000}.", prefix="Rs. ")
        elif t == 3:
            a2 = Fraction(P) * Fraction(100 + R, 100) ** 2
            if a2.denominator == 1: b.num(CAT, T, S1, "hard", f"A sum grows to Rs. {int(a2)} in 2 years at {R}% compound interest per annum. What was the original sum?", P,
                                          f"Original = {int(a2)} ÷ (1 + {R}/100)² = {P}.", prefix="Rs. ")
        elif t == 4:
            d, m = r.choice([2, 3, 4, 5]), r.choice([(4, 2), (8, 3)]); b.num(CAT, T, S3, "hard", f"At compound interest a sum doubles in {d} years. In how many years will it become {m[0]} times itself?", d * m[1],
                                                                          f"Doubling repeats every {d} years: {m[0]} times = 2^{m[1]}, so {m[1]} × {d} = {d * m[1]} years.", unit=" years")
        elif t == 5:
            pp = r.choice([1000, 2000, 5000, 10000]); rr = r.choice([4, 5, 8, 10]); b.num(CAT, T, S1, "easy", f"What is the compound interest for the first year on Rs. {pp} at {rr}% per annum?", pp * rr // 100,
                                                                                            "For the first year, compound interest equals simple interest = P × R/100.", prefix="Rs. ")

def time_and_work(b):
    r, T = b.rng, "time-and-work"
    S1, S2, S3 = "Combined work", "Basic time and work", "Pipes and tanks"
    pairs = [(12, 24), (10, 15), (20, 30), (6, 12), (30, 45), (8, 24), (9, 18), (15, 30), (12, 36), (20, 60), (14, 21), (18, 36)]
    while b.count(T) < N:
        t, (x, y) = r.randrange(6), r.choice(pairs)
        if t == 0: b.num(CAT, T, S1, "medium", f"A can complete a job in {x} days and B in {y} days. Working together, how many days do they need?", x * y // (x + y),
                         f"Together they do 1/{x} + 1/{y} = {x + y}/{x * y} of the work per day, so {x * y // (x + y)} days.", unit=" days") if x * y % (x + y) == 0 else None
        elif t == 1: b.num(CAT, T, S1, "hard", f"A and B together finish a work in {x * y // (x + y)} days. A alone takes {x} days. How long would B take alone?", y,
                           f"1/B = 1/{x * y // (x + y)} - 1/{x} = 1/{y}, so B needs {y} days.", unit=" days") if x * y % (x + y) == 0 else None
        elif t == 2:
            k, d = r.choice([2, 3, 4, 5]), r.choice([3, 4, 5, 6, 8]); b.num(CAT, T, S2, "easy", f"A worker completes 1/{k} of a job in {d} days. How many days will he take to finish the whole job?", k * d,
                                                                             f"If 1/{k} takes {d} days, the whole job takes {k} × {d} = {k * d} days.", unit=" days")
        elif t == 3 and y > x and x * y % (y - x) == 0: b.num(CAT, T, S3, "hard", f"A pipe fills a tank in {x} hours and a drain empties it in {y} hours. If both are open, how many hours to fill the empty tank?", x * y // (y - x),
                                                                 f"Net rate = 1/{x} - 1/{y} = {y - x}/{x * y}, so {x * y // (y - x)} hours.", unit=" hours")
        elif t == 4:
            m, d, m2 = r.choice([(12, 10, 8), (5, 12, 6), (8, 15, 10), (6, 20, 8), (10, 18, 12), (15, 8, 10)])
            b.num(CAT, T, S2, "medium", f"{m} men can finish a work in {d} days. How many days will {m2} men take?", m * d // m2, f"Man-days = {m} × {d} = {m * d}; days for {m2} men = {m * d}/{m2} = {m * d // m2}.", unit=" days") if m * d % m2 == 0 else None

def time_speed_distance(b):
    r, T = b.rng, "time-speed-distance"
    S1, S2, S3 = "Speed, distance and time", "Average and relative speed", "Trains and boats"
    while b.count(T) < N:
        t = r.randrange(7)
        if t == 0:
            s, h = r.choice([40, 45, 50, 60, 72, 80]), r.choice([2, 3, 4, 5]); b.num(CAT, T, S1, "easy", f"A car moves at {s} km/h for {h} hours. How far does it travel?", s * h, f"Distance = speed × time = {s} × {h} = {s * h} km.", unit=" km")
        elif t == 1:
            k = r.randint(2, 12); b.num(CAT, T, S1, "easy", f"Convert {18 * k} km/h into m/s.", 5 * k, "Multiply km/h by 5/18 to get m/s.", unit=" m/s")
        elif t == 2:
            a, c = r.choice([(40, 60), (30, 60), (20, 30), (60, 90), (50, 75), (30, 45), (60, 120), (36, 45)]); avg = Fraction(2 * a * c, a + c)
            if avg.denominator == 1: b.num(CAT, T, S2, "hard", f"A man travels a certain distance at {a} km/h and returns the same way at {c} km/h. What is his average speed for the whole trip?", int(avg),
                                            f"Average speed = 2ab/(a+b) = 2×{a}×{c}/{a + c} = {int(avg)} km/h.", unit=" km/h")
        elif t == 3:
            L, sec = r.choice([(150, 10), (200, 20), (120, 8), (300, 20), (180, 12), (90, 6)]); sp = Fraction(L, sec) * Fraction(18, 5)
            if sp.denominator == 1: b.num(CAT, T, S3, "medium", f"A {L} m long train crosses a pole in {sec} seconds. What is its speed in km/h?", int(sp), f"Speed = {L}/{sec} m/s = {fmt(Fraction(L, sec))} m/s = {int(sp)} km/h.", unit=" km/h")
        elif t == 4:
            tot, v = r.choice([36, 54, 72, 90, 108]), None; ms = tot * 5 // 18; sec = r.choice([6, 8, 10, 12]); ln = ms * sec; a = tot // 2 - r.choice([0, 6]) 
            b.num(CAT, T, S3, "hard", f"Two trains run in opposite directions at {a} km/h and {tot - a} km/h. Their total length is {ln} m. How many seconds do they take to cross each other?", sec,
                  f"Relative speed = {tot} km/h = {ms} m/s; time = {ln}/{ms} = {sec} s.", unit=" seconds")
        elif t == 5:
            bs, st, d = r.choice([(12, 3, 60), (15, 5, 80), (10, 2, 96), (18, 6, 72), (14, 2, 84)]); b.num(CAT, T, S3, "medium", f"A boat's speed in still water is {bs} km/h and the stream flows at {st} km/h. How many hours does it take to go {d} km downstream?", d // (bs + st),
                                                                                                   f"Downstream speed = {bs} + {st} = {bs + st} km/h; time = {d}/{bs + st}.", unit=" hours") if d % (bs + st) == 0 else None
        else:
            d, s1, s2 = r.choice([(120, 40, 60), (150, 50, 25), (180, 40, 50), (200, 60, 40)]); tm = Fraction(d, s1 + s2)
            if tm.denominator == 1: b.num(CAT, T, S2, "medium", f"Two cars start {d} km apart and drive toward each other at {s1} km/h and {s2} km/h. After how many hours do they meet?", int(tm), f"Closing speed = {s1 + s2} km/h; time = {d}/{s1 + s2} = {int(tm)} h.", unit=" hours")

def problems_on_ages(b):
    r, T = b.rng, "problems-on-ages"
    S1, S2, S3 = "Present age from conditions", "Ratio of ages", "Average age"
    while b.count(T) < N:
        t = r.randrange(5)
        if t == 0:
            x, n, k = r.randint(6, 18), r.randint(2, 8), r.choice([2, 3, 4]); f = k * (x + n) - n
            if not 26 <= f <= 62: continue
            b.num(CAT, T, S1, "medium", f"The sum of the present ages of a father and his son is {x + f} years. After {n} years the father will be {k} times as old as the son. What is the son's present age?", x,
                  f"Let son = x. Then father = {x + f} - x and {x + f} - x + {n} = {k}(x + {n}); solving gives x = {x}.", unit=" years")
        elif t == 1:
            a, c, m = r.choice([(2, 3), (3, 5), (4, 5), (3, 4), (5, 7)]) + (r.randint(4, 12),); s = (a + c) * m
            b.num(CAT, T, S2, "easy", f"The ages of two friends are in the ratio {a}:{c} and their ages add up to {s} years. What is the age of the younger friend?", a * m,
                  f"One part = {s}/{a + c} = {m}; younger = {a} × {m} = {a * m}.", unit=" years")
        elif t == 2:
            x, n, k = r.randint(12, 25), r.randint(2, 8), r.choice([2, 3, 4]); f = k * (x - n) + n
            if not 30 <= f <= 65 or x - n < 3: continue
            b.num(CAT, T, S1, "hard", f"A father is {f} years old and his daughter is {x}. How many years ago was the father exactly {k} times as old as the daughter?", n,
                  f"{f} - y = {k}({x} - y) gives y = {n}.", unit=" years")
        elif t == 3:
            n, a, x = r.randint(3, 6), r.randint(18, 30), r.randint(20, 40)
            if (n * a + x) % (n + 1): continue
            b.num(CAT, T, S3, "medium", f"The average age of {n} friends is {a} years. A friend aged {x} joins them. What is the new average age?", (n * a + x) // (n + 1),
                  f"New total = {n * a} + {x} = {n * a + x}; average = {n * a + x}/{n + 1}.", unit=" years")
        else:
            d, y = r.randint(3, 12), r.randint(2, 6); a = r.randint(12, 30)
            b.num(CAT, T, S1, "easy", f"Riya is {d} years older than Sana. If Sana is {a} years old now, how old will Riya be after {y} years?", a + d + y, f"Riya now = {a} + {d} = {a + d}; after {y} years = {a + d + y}.", unit=" years")

def probability(b):
    r, T = b.rng, "probability"
    S1, S2, S3 = "Coins and dice", "Cards", "Balls and bags"
    while b.count(T) < N:
        t = r.randrange(6)
        def fr(f): return frac(Fraction(f))
        def opts(ans, extra):
            return [fr(e) for e in extra if Fraction(e) != ans and 0 < Fraction(e) < 1]
        if t == 0:
            n, k = r.choice([(3, 1), (3, 2), (4, 2), (4, 1), (5, 2), (3, 3), (4, 3)]); a = Fraction(comb(n, k), 2 ** n)
            b.add(CAT, T, S1, "medium", f"A fair coin is tossed {n} times. What is the probability of getting exactly {k} head{'s' if k > 1 else ''}?", fr(a),
                  opts(a, [Fraction(k, n), Fraction(1, 2 ** n), Fraction(comb(n, k) + 1, 2 ** n), Fraction(1, 2), Fraction(comb(n, k) - 1, 2 ** n)]) or [fr(Fraction(1, 3))], f"Favourable = C({n},{k}) = {comb(n, k)}; total = 2^{n} = {2 ** n}.")
        elif t == 1:
            s = r.randint(3, 11); w = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s); a = Fraction(w, 36)
            b.add(CAT, T, S1, "medium", f"Two fair dice are rolled. What is the probability that the sum is {s}?", fr(a),
                  opts(a, [Fraction(w + 1, 36), Fraction(w, 12), Fraction(1, 6), Fraction(w + 2, 36), Fraction(w - 1, 36)]), f"{w} of the 36 equally likely outcomes give a sum of {s}.")
        elif t == 2:
            ev = r.choice([("a king", 4), ("a red card", 26), ("a face card (J, Q or K)", 12), ("a heart", 13), ("either a heart or a king", 16), ("a black queen", 2), ("a spade or an ace", 16)]); a = Fraction(ev[1], 52)
            b.add(CAT, T, S2, "easy", f"One card is drawn from a well-shuffled deck of 52 cards. What is the probability that it is {ev[0]}?", fr(a),
                  opts(a, [Fraction(ev[1] + 1, 52), Fraction(ev[1], 51), Fraction(ev[1] + 2, 52), Fraction(1, 4), Fraction(ev[1] - 1, 52), Fraction(1, 2)]), f"{ev[1]} favourable cards out of 52.")
        elif t == 3:
            rd, bl, gr = r.randint(2, 6), r.randint(2, 6), r.randint(1, 5); n = rd + bl + gr; a = Fraction(n - rd, n)
            b.add(CAT, T, S3, "easy", f"A bag holds {rd} red, {bl} blue and {gr} green balls. One ball is drawn at random. What is the probability that it is not red?", fr(a),
                  opts(a, [Fraction(rd, n), Fraction(bl, n), Fraction(n - rd, n + 1), Fraction(n - rd - 1, n)]), f"Not red = {n - rd} balls out of {n}.")
        elif t == 4:
            rd, bl = r.randint(3, 6), r.randint(2, 5); n = rd + bl; a = Fraction(comb(rd, 2), comb(n, 2))
            b.add(CAT, T, S3, "hard", f"A bag has {rd} red and {bl} blue balls. Two balls are drawn without replacement. What is the probability that both are red?", fr(a),
                  opts(a, [Fraction(rd * rd, n * n), Fraction(rd, n), Fraction(bl * (bl - 1), n * (n - 1)), Fraction(rd * bl, n * (n - 1))]), f"C({rd},2)/C({n},2) = {comb(rd, 2)}/{comb(n, 2)}.")
        else:
            a = Fraction(1, 2); q = r.choice([("an even number", 3), ("a number greater than 4", 2), ("a prime number", 3), ("a multiple of 3", 2)]); a = Fraction(q[1], 6)
            b.add(CAT, T, S1, "easy", f"A fair six-sided die is rolled once. What is the probability of getting {q[0]}?", fr(a),
                  opts(a, [Fraction(q[1] + 1, 6), Fraction(1, 6), Fraction(q[1] - 1, 6), Fraction(5, 6), Fraction(1, 4)]), f"{q[1]} favourable outcomes out of 6.")

def permutation_combination(b):
    r, T = b.rng, "permutation-combination"
    S1, S2, S3 = "nPr and nCr", "Arrangements of letters", "Selections and counting"
    words = ["PLANET", "CODING", "MARKET", "SCHOOL", "LETTER", "BANANA", "APPLE", "SUCCESS", "GARDEN", "MISSISSIPPI", "PEPPER", "TOMATO"]
    while b.count(T) < N:
        t = r.randrange(6)
        if t == 0:
            n, k = r.randint(6, 12), r.randint(2, 4); c = r.random() < .5
            b.num(CAT, T, S1, "easy", f"Evaluate {n}{'C' if c else 'P'}{k}.", comb(n, k) if c else perm(n, k), f"{n}{'C' if c else 'P'}{k} = {'n!/(k!(n-k)!)' if c else 'n!/(n-k)!'} = {comb(n, k) if c else perm(n, k)}.")
        elif t == 1:
            w = r.choice(words); cnt = Counter(w); ans = factorial(len(w))
            for v in cnt.values(): ans //= factorial(v)
            rep = ", ".join(f"{ch} ×{v}" for ch, v in cnt.items() if v > 1)
            b.num(CAT, T, S2, "medium", f"In how many different ways can the letters of the word {w} be arranged?", ans, f"{len(w)}! divided by factorials of repeated letters ({rep or 'none repeated'}) = {ans}.")
        elif t == 2:
            m, w, k = r.choice([(5, 4, 3), (6, 4, 3), (5, 3, 3), (6, 5, 4), (4, 4, 3)]); wk = r.randint(1, min(k - 1, w))
            b.num(CAT, T, S3, "hard", f"A committee of {k} is to be formed from {m} men and {w} women. In how many ways can it be formed with exactly {wk} woman{'en' if wk > 1 else ''}?".replace("womanen", "women"),
                  comb(w, wk) * comb(m, k - wk), f"C({w},{wk}) × C({m},{k - wk}) = {comb(w, wk)} × {comb(m, k - wk)}.")
        elif t == 3:
            n, k = r.choice([(5, 3), (6, 3), (6, 4), (7, 3)]); rep = r.random() < .5
            b.num(CAT, T, S3, "medium", f"How many {k}-digit numbers can be formed using the digits 1 to {n} {'if repetition is allowed' if rep else 'without repetition'}?", n ** k if rep else perm(n, k),
                  f"{'n^k' if rep else 'nPk'} = {n ** k if rep else perm(n, k)}.")
        elif t == 4:
            n = r.randint(5, 9); circ = r.random() < .5
            b.num(CAT, T, S3, "medium", f"In how many ways can {n} people be seated {'around a circular table' if circ else 'in a row'}?", factorial(n - 1) if circ else factorial(n),
                  f"{'(n-1)!' if circ else 'n!'} = {factorial(n - 1) if circ else factorial(n)}.")
        else:
            n = r.randint(6, 12); b.num(CAT, T, S3, "easy", f"In a meeting of {n} people everyone shakes hands with everyone else exactly once. How many handshakes take place?", comb(n, 2), f"C({n},2) = {comb(n, 2)}.")

def algebra(b):
    r, T = b.rng, "algebra"
    S1, S2, S3 = "Linear equations", "Quadratic equations", "Identities and expressions"
    while b.count(T) < N:
        t = r.randrange(6)
        if t == 0:
            x, a, c = r.randint(2, 15), r.randint(2, 9), r.randint(1, 20); b.num(CAT, T, S1, "easy", f"Solve for x: {a}x + {c} = {a * x + c}.", x, f"{a}x = {a * x}, so x = {x}.")
        elif t == 1:
            x, y = r.randint(3, 15), r.randint(1, 12)
            if x <= y: continue
            b.num(CAT, T, S1, "medium", f"If x + y = {x + y} and x - y = {x - y}, what is xy?", x * y, f"x = {x}, y = {y}, so xy = {x * y}.")
        elif t == 2:
            p, q = r.sample(range(1, 10), 2); ans = f"{min(p, q)} and {max(p, q)}"
            wr = [f"{min(p, q) + 1} and {max(p, q)}", f"-{min(p, q)} and -{max(p, q)}", f"{min(p, q)} and {max(p, q) + 1}", f"{min(p, q) - 1 if min(p, q) > 1 else 0} and {max(p, q)}"]
            b.add(CAT, T, S2, "medium", f"Find the roots of x² - {p + q}x + {p * q} = 0.", ans, wr, f"Factorise: (x - {p})(x - {q}) = 0.")
        elif t == 3:
            k = r.randint(3, 9); b.num(CAT, T, S3, "medium", f"If a + 1/a = {k}, find the value of a² + 1/a².", k * k - 2, f"Square both sides: a² + 2 + 1/a² = {k * k}, so a² + 1/a² = {k * k - 2}.")
        elif t == 4:
            s, p = r.randint(5, 12), r.randint(3, 20)
            b.num(CAT, T, S3, "hard", f"If x + y = {s} and xy = {p}, find x² + y².", s * s - 2 * p, f"x² + y² = (x + y)² - 2xy = {s * s} - {2 * p} = {s * s - 2 * p}.")
        else:
            p, q = r.sample(range(1, 10), 2); b.num(CAT, T, S2, "easy", f"What is the sum of the roots of x² - {p + q}x + {p * q} = 0?", p + q, "For ax² + bx + c = 0, the sum of roots is -b/a.")

def geometry(b):
    r, T = b.rng, "geometry"
    S1, S2, S3 = "Angles and triangles", "Polygons", "Right triangles"
    trip = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]
    while b.count(T) < N:
        t = r.randrange(7)
        if t == 0:
            a, c = r.randint(30, 80), r.randint(30, 70); b.num(CAT, T, S1, "easy", f"Two angles of a triangle measure {a}° and {c}°. What is the third angle?", 180 - a - c, "The angles of a triangle add up to 180°.", unit="°")
        elif t == 1:
            n = r.choice([5, 6, 8, 9, 10, 12]); b.num(CAT, T, S2, "medium", f"What is the measure of each interior angle of a regular polygon with {n} sides?", 180 - 360 // n, f"Exterior angle = 360/{n} = {360 // n}°, so interior = {180 - 360 // n}°.", unit="°")
        elif t == 2:
            n = r.randint(5, 12); b.num(CAT, T, S2, "easy", f"What is the sum of the interior angles of a polygon with {n} sides?", (n - 2) * 180, f"(n - 2) × 180° = {(n - 2) * 180}°.", unit="°")
        elif t == 3:
            a, c, h = r.choice(trip); k = r.choice([1, 2, 3]); b.num(CAT, T, S3, "easy", f"The two shorter sides of a right-angled triangle are {a * k} cm and {c * k} cm. Find the hypotenuse.", h * k, f"√({a * k}² + {c * k}²) = {h * k}.", unit=" cm")
        elif t == 4:
            a, c, h = r.choice(trip); k = r.choice([1, 2, 3]); b.num(CAT, T, S3, "medium", f"The hypotenuse of a right triangle is {h * k} cm and one side is {a * k} cm. Find the other side.", c * k, f"√({h * k}² - {a * k}²) = {c * k}.", unit=" cm")
        elif t == 5:
            n = r.randint(6, 14); b.num(CAT, T, S2, "medium", f"How many diagonals does a polygon with {n} sides have?", n * (n - 3) // 2, f"n(n - 3)/2 = {n}×{n - 3}/2 = {n * (n - 3) // 2}.")
        else:
            a, c = r.randint(30, 80), r.randint(25, 70); b.num(CAT, T, S1, "medium", f"In a triangle, two interior angles are {a}° and {c}°. What is the exterior angle formed at the third vertex?", a + c, "An exterior angle equals the sum of the two opposite interior angles.", unit="°")

def mensuration(b):
    r, T = b.rng, "mensuration"
    S1, S2, S3 = "Plane figures", "Cuboids and cubes", "Cylinders and spheres"
    while b.count(T) < N:
        t = r.randrange(7)
        if t == 0:
            l, w = r.randint(8, 40), r.randint(5, 25); b.num(CAT, T, S1, "easy", f"A rectangle is {l} m long and {w} m wide. What is its perimeter?", 2 * (l + w), f"2(l + w) = 2({l} + {w}).", unit=" m")
        elif t == 1:
            rad = r.choice([7, 14, 21, 28, 35]); b.num(CAT, T, S1, "medium", f"Find the area of a circle of radius {rad} cm (use π = 22/7).", 22 * rad * rad // 7, f"πr² = 22/7 × {rad} × {rad}.", unit=" cm²")
        elif t == 2:
            l, w, h = r.randint(3, 15), r.randint(3, 12), r.randint(2, 10); b.num(CAT, T, S2, "easy", f"Find the volume of a cuboid of length {l} cm, breadth {w} cm and height {h} cm.", l * w * h, "Volume = l × b × h.", unit=" cm³")
        elif t == 3:
            a = r.randint(3, 15); b.num(CAT, T, S2, "medium", f"What is the total surface area of a cube of side {a} cm?", 6 * a * a, f"6a² = 6 × {a}².", unit=" cm²")
        elif t == 4:
            h = r.randint(3, 20); b.num(CAT, T, S3, "medium", f"Find the volume of a cylinder with radius 7 cm and height {h} cm (π = 22/7).", 154 * h, f"πr²h = 22/7 × 49 × {h} = {154 * h}.", unit=" cm³")
        elif t == 5:
            rad = r.choice([7, 14, 21]); b.num(CAT, T, S3, "hard", f"Find the surface area of a sphere of radius {rad} cm (π = 22/7).", 4 * 22 * rad * rad // 7, f"4πr² = 4 × 22/7 × {rad}².", unit=" cm²")
        else:
            a, c, h = r.randint(6, 20), r.randint(4, 15), r.randint(3, 12); b.num(CAT, T, S1, "medium", f"The parallel sides of a trapezium are {a} cm and {c} cm and the distance between them is {h} cm. Find its area.", Fraction((a + c) * h, 2),
                                                                                    f"½ × ({a} + {c}) × {h} = {fmt(Fraction((a + c) * h, 2))}.", unit=" cm²")

def data_interpretation(b):
    r, T = b.rng, "data-interpretation"
    S1, S2 = "Reading tables", "Percentage and growth from tables"
    while b.count(T) < N:
        names = r.sample(["Laptops", "Phones", "Tablets", "Monitors", "Printers"], 4)
        base = [r.choice(range(100, 401, 20)) for _ in names]; gr = [r.choice([10, 20, 25, 30, 40, -10, -20, -25]) for _ in names]
        new = [bb * (100 + g) // 100 for bb, g in zip(base, gr)]
        if any(bb * (100 + g) % 100 for bb, g in zip(base, gr)) or len(set(gr)) < 3: continue
        tbl = "Units sold (in hundreds):\nProduct | 2024 | 2025\n" + "\n".join(f"{n} | {x} | {y}" for n, x, y in zip(names, base, new))
        t = r.randrange(5); i = r.randrange(4)
        if t == 0: b.num(CAT, T, S1, "easy", f"{tbl}\n\nWhat were the total units sold in 2025 (in hundreds)?", sum(new), f"Add the 2025 column: {' + '.join(map(str, new))} = {sum(new)}.")
        elif t == 1: b.num(CAT, T, S1, "easy", f"{tbl}\n\nBy how many hundred units did {names[i]} sales change from 2024 to 2025 (ignore the sign)?", abs(new[i] - base[i]), f"|{new[i]} - {base[i]}| = {abs(new[i] - base[i])}.")
        elif t == 2:
            g = gr[i]; b.num(CAT, T, S2, "medium", f"{tbl}\n\nWhat was the percentage {'increase' if g > 0 else 'decrease'} in sales of {names[i]} from 2024 to 2025?", abs(g), f"Change = {abs(new[i] - base[i])}; % = {abs(new[i] - base[i])}/{base[i]} × 100 = {abs(g)}%.", unit="%")
        elif t == 3:
            best = max(range(4), key=lambda j: gr[j])
            if sorted(gr)[-1] == sorted(gr)[-2]: continue
            b.add(CAT, T, S2, "hard", f"{tbl}\n\nWhich product showed the highest percentage growth from 2024 to 2025?", names[best], [n for j, n in enumerate(names) if j != best], "Compute (2025 - 2024)/2024 for each product; the largest value belongs to " + names[best] + ".")
        else:
            if sum(base) % 4: continue
            b.num(CAT, T, S1, "medium", f"{tbl}\n\nWhat was the average number of units sold per product in 2024 (in hundreds)?", sum(base) // 4, f"Total = {sum(base)}; average = {sum(base)}/4 = {sum(base) // 4}.")

ALL = [number_system, percentages, profit_and_loss, ratio_and_proportion, averages, simple_interest, compound_interest, time_and_work,
       time_speed_distance, problems_on_ages, probability, permutation_combination, algebra, geometry, mensuration, data_interpretation]
