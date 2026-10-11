"""Original, hand-written questions: reasoning text topics and the Verbal Ability category."""
LOG, VER = "Logical Reasoning", "Verbal Ability"
CONC = ["Only conclusion I follows", "Only conclusion II follows", "Both I and II follow", "Neither I nor II follows"]
DS = ["Statement I alone is sufficient", "Statement II alone is sufficient", "Both statements together are needed; neither alone is enough", "Even both statements together are not sufficient"]

STATEMENTS = [  # (statement, I, II, answer_index, explanation, difficulty)
 ("All the flats in Green Court have a balcony. Some flats in Green Court are rented out.", "Some rented flats have a balcony.", "All flats with a balcony are in Green Court.", 0, "Rented flats in Green Court have balconies, but balconies may exist elsewhere too.", "medium"),
 ("Only members can enter the club after 8 p.m. Ritu entered the club at 9 p.m.", "Ritu is a member.", "Ritu is a manager of the club.", 0, "Only members enter after 8 p.m., so Ritu must be a member; nothing says she is a manager.", "medium"),
 ("The price of petrol has been increased by 10%.", "Transport costs may rise.", "All people will stop using vehicles.", 0, "Higher fuel prices can raise transport costs, but a total stop is an extreme claim.", "easy"),
 ("Some books are magazines. No magazine is a newspaper.", "Some books are not newspapers.", "No book is a newspaper.", 0, "The books that are magazines are not newspapers; other books are not covered.", "medium"),
 ("Every student who passes the screening test is called for an interview. Neha was not called for an interview.", "Neha did not pass the screening test.", "Neha did not appear for the screening test.", 0, "If she had passed she would have been called; she may have appeared and failed.", "hard"),
 ("A hospital notice says: 'Visitors are allowed only between 4 p.m. and 6 p.m.'", "A visitor who arrives at 5 p.m. may meet patients.", "A visitor who arrives at 7 p.m. may not meet patients.", 2, "5 p.m. is inside the allowed window and 7 p.m. is outside it.", "medium"),
 ("Most of the shops in Market Street are closed on Sundays.", "All shops in Market Street are closed on Sundays.", "Some shops in Market Street are closed on Sundays.", 1, "'Most' means more than half, so some are closed, but not necessarily all.", "medium"),
 ("No student of Class X may use a mobile phone in school.", "Ankit, a Class X student, may bring a phone and use it in school.", "Ankit, a Class X student, may not use a phone in school.", 1, "The rule bans use in school for every Class X student, including Ankit.", "easy"),
 ("Either the 7:30 bus or the 8:00 bus will get you to the station on time.", "If you miss the 7:30 bus, the 8:00 bus will still get you there on time.", "You can reach on time only by the 8:00 bus.", 0, "The statement offers two working options, so the 7:30 bus also works.", "medium"),
 ("A new metro line will open in the city next year.", "All buses in the city will stop running.", "Everyone in the city will travel by metro.", 3, "Nothing in the statement suggests buses will stop or that everybody will switch.", "easy"),
 ("Only graduates are eligible for the post. Mira is eligible for the post.", "Mira is a graduate.", "A non-graduate is not eligible for the post.", 2, "Eligibility is limited to graduates, so both conclusions follow.", "medium"),
 ("The city council has banned plastic bags in all markets.", "Shoppers in the markets will need alternatives to plastic bags.", "Plastic bags will no longer be produced anywhere in the country.", 0, "The ban covers markets only, not production across the country.", "easy")]

SUFFICIENCY = [  # (question, I, II, answer_index, explanation, difficulty)
 ("What is the price of one notebook?", "Five notebooks cost Rs. 250.", "A pen costs Rs. 10 less than a notebook.", 0, "Statement I gives 250 ÷ 5 = Rs. 50; statement II mentions the pen's price, not the notebook's.", "easy"),
 ("What is Sita's age?", "Sita is 4 years older than her brother.", "Her brother is 12 years old.", 2, "Only by combining both statements: 12 + 4 = 16.", "easy"),
 ("Is the number x even?", "x is divisible by 4.", "x is a multiple of 3.", 0, "Every multiple of 4 is even; a multiple of 3 can be odd or even.", "medium"),
 ("What is the area of a rectangle?", "Its perimeter is 30 cm.", "Its length is 10 cm.", 2, "Together: width = 15 - 10 = 5 cm, so area = 50 cm².", "medium"),
 ("What was the cost price of a bag?", "The shopkeeper made some profit on the bag.", "The bag was sold for Rs. 600 at a 20% profit.", 1, "Statement II gives CP = 600 ÷ 1.2 = Rs. 500; statement I has no numbers.", "medium"),
 ("Who is taller, Amit or Bala?", "Amit is taller than Chetan.", "Chetan is taller than Bala.", 2, "Together: Amit > Chetan > Bala.", "easy"),
 ("What is the value of y?", "y + 3 = 10.", "y² = 49.", 0, "Statement I gives y = 7; statement II allows y = 7 or -7.", "medium"),
 ("Is Kiran older than Ravi?", "Kiran was born in 1998.", "Ravi is 25 years old.", 3, "Without knowing the current year, Ravi's birth year cannot be found.", "hard"),
 ("How many pages does the book have?", "Riya reads 20 pages every day and finishes the book in exactly 15 days.", "The book has more than 200 pages.", 0, "Statement I gives 20 × 15 = 300 pages; statement II gives only a range.", "medium"),
 ("What is the length of a train?", "It crosses a pole in 12 seconds.", "Its speed is 54 km/h.", 2, "Speed 15 m/s × 12 s = 180 m needs both statements.", "hard"),
 ("What is the perimeter of a square?", "All four sides of the square are equal.", "The area of the square is 64 cm².", 1, "Statement II gives side 8 cm, so perimeter 32 cm; statement I is true for every square.", "medium"),
 ("Is the number N a prime number?", "N is greater than 10.", "N is odd.", 3, "11 is prime and 15 is not; both fit the statements.", "hard")]

def _day_puzzles(b):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for d, n in [("Wednesday", 100), ("Friday", 45), ("Sunday", 150), ("Tuesday", 61)]:
        i = (days.index(d) + n) % 7; ans = days[i]
        b.add(LOG, "logical-puzzles", "Calendar puzzles", "medium", f"Today is {d}. What day of the week will it be after {n} days?", ans,
              [days[(i + k) % 7] for k in (1, -1, 2)], f"{n} = 7 × {n // 7} + {n % 7}, so the day moves {n % 7} step(s) forward from {d}.")

PUZZLES = [
 ("A patch of lily pads doubles in size every day and covers the whole pond on day 30. On which day did it cover half the pond?", "Day 29", ["Day 15", "Day 28", "Day 25"], "Doubling once more (day 29 → day 30) fills the pond, so half was covered on day 29.", "medium"),
 ("If 5 machines take 5 minutes to make 5 toys, how many minutes do 100 machines need to make 100 toys?", "5 minutes", ["100 minutes", "20 minutes", "1 minute"], "Each machine makes one toy in 5 minutes, so 100 machines make 100 toys in 5 minutes.", "hard"),
 ("A clock strikes once at 1 o'clock, twice at 2 o'clock and so on up to 12 times at 12 o'clock. How many strikes are there from 1 o'clock to 12 o'clock?", "78", ["66", "72", "144"], "1 + 2 + ... + 12 = 12 × 13 / 2 = 78.", "medium"),
 ("How many squares of all sizes are there on a 3 × 3 grid of small squares?", "14", ["9", "13", "16"], "9 small (1×1) + 4 of size 2×2 + 1 of size 3×3 = 14.", "hard"),
 ("P is taller than Q. Q is taller than R. S is shorter than R. T is taller than P. Who is the shortest?", "S", ["R", "Q", "T"], "The order is T > P > Q > R > S, so S is the shortest.", "easy"),
 ("A father is three times as old as his son. After 12 years he will be twice as old as his son. How old is the son now?", "12 years", ["6 years", "10 years", "15 years"], "3x + 12 = 2(x + 12) gives x = 12.", "medium"),
 ("A 20-metre ribbon is cut into pieces of 2 metres each. How many cuts are needed?", "9", ["10", "8", "11"], "There are 10 pieces, and n pieces need n - 1 cuts.", "easy"),
 ("Nine coins look identical, but one is slightly heavier. What is the minimum number of weighings on a balance scale that is guaranteed to find it?", "2", ["3", "4", "1"], "Weigh 3 against 3 to find the group holding the heavy coin, then weigh two coins from that group.", "hard"),
 ("A bat and a ball together cost Rs. 110. The bat costs Rs. 100 more than the ball. What does the ball cost?", "Rs. 5", ["Rs. 10", "Rs. 15", "Rs. 1"], "Ball + (ball + 100) = 110, so the ball costs Rs. 5.", "hard")]

def _mc(b, cat, topic, sub, diff, q, a, w, e): b.add(cat, topic, sub, diff, q, a, w, e)

VOCAB = [
 ("Which one word means 'a person who loves books'?", "Bibliophile", ["Philanthropist", "Misanthrope", "Egotist"], "'Biblio' relates to books.", "One-word substitution", "easy"),
 ("Which word describes 'a government in which one ruler holds absolute power'?", "Autocracy", ["Democracy", "Aristocracy", "Theocracy"], "Autocracy means rule by a single person with unlimited power.", "One-word substitution", "medium"),
 ("Choose the correct meaning of 'meticulous'.", "Very careful about details", ["Careless", "Lazy", "Noisy"], "A meticulous person pays close attention to detail.", "Word meanings", "medium"),
 ("Choose the correct meaning of 'ephemeral'.", "Lasting for a very short time", ["Eternal", "Fragile", "Harmful"], "Ephemeral things last only briefly.", "Word meanings", "hard"),
 ("Choose the correct meaning of 'reluctant'.", "Unwilling", ["Eager", "Curious", "Tired"], "Reluctant means not willing to do something.", "Word meanings", "easy"),
 ("What does the idiom 'to break the ice' mean?", "To start a conversation in an awkward situation", ["To damage something", "To feel very cold", "To end a friendship"], "It means to ease the tension when people first meet.", "Idioms and phrases", "easy"),
 ("What does the idiom 'a piece of cake' mean?", "Something very easy", ["A small gift", "A sweet dessert", "A rare chance"], "It describes a task that is effortless.", "Idioms and phrases", "easy"),
 ("What does the idiom 'once in a blue moon' mean?", "Very rarely", ["Every month", "Only at night", "Never"], "It refers to something that happens extremely seldom.", "Idioms and phrases", "medium"),
 ("Choose the correct meaning of 'verbose'.", "Using more words than necessary", ["Silent", "Honest", "Rude"], "Verbose speech or writing is wordy.", "Word meanings", "medium"),
 ("Choose the correct meaning of 'frugal'.", "Careful about spending money", ["Wasteful", "Generous", "Wealthy"], "A frugal person avoids unnecessary expense.", "Word meanings", "medium"),
 ("Choose the correct meaning of 'candid'.", "Honest and direct", ["Secretive", "Angry", "Shy"], "A candid answer is frank and open.", "Word meanings", "medium"),
 ("Which one word means 'a person who is new to a subject or activity'?", "Novice", ["Expert", "Veteran", "Mentor"], "A novice is a beginner.", "One-word substitution", "easy")]

SYN = [("Abundant", "Plentiful", ["Scarce", "Tiny", "Costly"]), ("Brave", "Courageous", ["Timid", "Careless", "Proud"]), ("Rapid", "Swift", ["Slow", "Steady", "Heavy"]),
       ("Commence", "Begin", ["Conclude", "Delay", "Prevent"]), ("Enormous", "Gigantic", ["Modest", "Narrow", "Faint"]), ("Conceal", "Hide", ["Reveal", "Display", "Announce"]),
       ("Diligent", "Hardworking", ["Lazy", "Clever", "Quiet"]), ("Inevitable", "Unavoidable", ["Doubtful", "Unlikely", "Optional"]), ("Tranquil", "Peaceful", ["Noisy", "Troubled", "Rapid"]),
       ("Obstinate", "Stubborn", ["Flexible", "Gentle", "Curious"]), ("Benevolent", "Kind", ["Cruel", "Selfish", "Clumsy"]), ("Hostile", "Unfriendly", ["Welcoming", "Cheerful", "Calm"])]

ANT = [("Abundant", "Scarce", ["Plentiful", "Ample", "Huge"]), ("Ancient", "Modern", ["Old", "Historic", "Antique"]), ("Expand", "Contract", ["Grow", "Stretch", "Spread"]),
       ("Generous", "Stingy", ["Kind", "Giving", "Wealthy"]), ("Victory", "Defeat", ["Triumph", "Success", "Glory"]), ("Transparent", "Opaque", ["Clear", "Bright", "Thin"]),
       ("Optimistic", "Pessimistic", ["Hopeful", "Cheerful", "Confident"]), ("Accept", "Reject", ["Receive", "Welcome", "Approve"]), ("Strengthen", "Weaken", ["Build", "Improve", "Harden"]),
       ("Ascend", "Descend", ["Climb", "Rise", "Mount"]), ("Rigid", "Flexible", ["Stiff", "Firm", "Strict"]), ("Temporary", "Permanent", ["Brief", "Passing", "Short"])]

GRAMMAR = [
 ("She ______ to school every day.", "goes", ["go", "going", "gone"], "A singular subject takes 'goes' in the simple present.", "Subject-verb agreement", "easy"),
 ("Neither of the boys ______ present at the meeting.", "was", ["were", "are", "have been"], "'Neither' is singular and the sentence is in the past.", "Subject-verb agreement", "medium"),
 ("Each of the students ______ a certificate.", "received", ["have received", "were receiving", "are received"], "'Each' is singular; 'received' works for any person.", "Subject-verb agreement", "medium"),
 ("If I ______ you, I would apologise at once.", "were", ["was", "am", "be"], "Unreal conditions use 'were' for every subject.", "Tenses and moods", "medium"),
 ("He has been living in this city ______ 2015.", "since", ["for", "from", "by"], "'Since' marks a starting point in time.", "Prepositions and articles", "easy"),
 ("She is very good ______ mathematics.", "at", ["in", "on", "with"], "The fixed phrase is 'good at'.", "Prepositions and articles", "easy"),
 ("She wants to become ______ engineer.", "an", ["a", "the", "one the"], "'Engineer' begins with a vowel sound, so 'an' is used.", "Prepositions and articles", "easy"),
 ("By the time we reached the hall, the film ______.", "had already started", ["already started", "has already started", "was already start"], "The earlier of two past events takes the past perfect.", "Tenses and moods", "hard"),
 ("This road is much wider ______ the old one.", "than", ["then", "that", "from"], "Comparatives are followed by 'than'.", "Prepositions and articles", "easy"),
 ("The secret is strictly between you and ______.", "me", ["I", "myself", "mine"], "After a preposition, the object form 'me' is used.", "Pronouns", "medium"),
 ("The news from the village ______ good.", "is", ["are", "were", "have been"], "'News' is uncountable and takes a singular verb.", "Subject-verb agreement", "medium"),
 ("I look forward to ______ you next week.", "meeting", ["meet", "met", "have met"], "'Look forward to' is followed by an -ing form.", "Tenses and moods", "hard")]

CORRECT = [  # correct sentence + 3 faulty ones
 ("He doesn't like coffee.", ["He don't like coffee.", "He didn't liked coffee.", "He not like coffee."], "Singular 'he' takes 'doesn't' + base verb."),
 ("The children play in the garden.", ["The children plays in the garden.", "The children is playing in the garden.", "The children has played in the garden."], "'Children' is plural."),
 ("She has fewer friends than I do.", ["She has less friends than I do.", "She have fewer friends than I do.", "She has fewer friend than I do."], "Use 'fewer' with countable nouns."),
 ("He and I went to the market.", ["Me and him went to the market.", "Him and me went to the market.", "He and me went to the market."], "Subject pronouns 'He and I' are needed."),
 ("The books are on the table.", ["The books is on the table.", "The books was on the table.", "The book are on the table."], "Plural subject, plural verb."),
 ("I saw him yesterday.", ["I have seen him yesterday.", "I am seeing him yesterday.", "I had see him yesterday."], "A finished time ('yesterday') needs the simple past."),
 ("She suggested that I take some rest.", ["She suggested me to take some rest.", "She suggested me taking some rest.", "She suggested that I am taking some rest."], "'Suggest' is followed by a 'that' clause."),
 ("He is smarter than his brother.", ["He is more smarter than his brother.", "He is smart than his brother.", "He is most smart than his brother."], "'Smarter' is already comparative."),
 ("Neither of them has arrived.", ["Neither of them have arrived.", "Neither of them are arrived.", "Neither of them were arrive."], "'Neither' takes a singular verb."),
 ("I know the answer.", ["I am knowing the answer.", "I have know the answer.", "I knowing the answer."], "'Know' is a state verb and is not used in the continuous form."),
 ("The information is very useful.", ["The informations are very useful.", "The information are very useful.", "The informations is very useful."], "'Information' is uncountable."),
 ("Each of the players wears a blue jersey.", ["Each of the players wear a blue jersey.", "Each of the player wears a blue jersey.", "Each of the players are wearing a blue jersey."], "'Each' takes a singular verb.")]

COMPLETE = [
 ("The manager was ______ by the team's excellent work, so he praised everyone.", "impressed", ["annoyed", "bored", "worried"], "Praise shows he was pleased."),
 ("It is ______ to wear a helmet while riding a motorbike; the law requires it.", "mandatory", ["optional", "harmful", "pointless"], "A legal requirement is mandatory."),
 ("Because the road was flooded, the villagers were ______ from the town for three days.", "isolated", ["invited", "rewarded", "attracted"], "Flooded roads cut people off."),
 ("Although he was tired, he was ______ to finish the work before leaving.", "determined", ["reluctant", "forgetful", "unable"], "'Although' introduces contrast with being tired."),
 ("The scientist's theory was ______ by many experiments over the years.", "supported", ["ignored", "hidden", "forgotten"], "Experiments can support a theory."),
 ("The shop offers a ______ discount during the festival, so prices are much lower.", "substantial", ["negligible", "tiny", "invisible"], "'Much lower' suggests a large discount."),
 ("Rina is very ______; she never speaks unless she has something important to say.", "reserved", ["talkative", "careless", "boastful"], "A reserved person speaks little."),
 ("The sudden ______ of the bridge shocked the whole town.", "collapse", ["construction", "opening", "painting"], "Only a collapse would shock people."),
 ("He apologised ______ for his rude behaviour, and everyone forgave him.", "sincerely", ["rarely", "loudly", "secretly"], "Forgiveness suggests a sincere apology."),
 ("The plan was so ______ that everyone understood it at once.", "simple", ["complex", "confusing", "vague"], "Immediate understanding needs a simple plan."),
 ("Please ______ the form carefully before you sign it.", "read", ["tear", "lose", "hide"], "You should read a document before signing."),
 ("The company's profits ______ sharply, and the shareholders were delighted.", "rose", ["fell", "vanished", "stalled"], "Delighted shareholders imply rising profits.")]

PASSAGES = [
 ("Many cities now face water shortages because their populations are growing faster than their water supplies. Experts say that fixing leaking pipes, collecting rainwater and reusing treated water can save millions of litres every year. However, these steps only work when people also change their habits, such as turning off taps and avoiding waste.",
  [("What is the main idea of the passage?", "Cities can reduce water shortages through better systems and careful habits", ["Rainwater is unsafe to use", "Populations should stop growing", "Leaking pipes are harmless"], "The passage combines technical fixes with changes in behaviour.", "medium"),
   ("Which step is mentioned as a way to save water?", "Collecting rainwater", ["Building more roads", "Importing bottled water", "Digging deeper wells only"], "Rainwater collection is listed among the steps.", "easy"),
   ("Why do the technical steps also need changes in people's habits?", "Systems alone cannot solve the problem if people keep wasting water", ["Pipes cannot be repaired", "Treated water is expensive", "Experts disagree with each other"], "The passage says the steps only work along with habit change.", "medium")]),
 ("A survey of students found that those who read for even twenty minutes a day had a richer vocabulary and wrote clearer essays. The researchers noted that the type of reading did not matter as much as the regular habit. Students who read only before exams showed little improvement.",
  [("According to the researchers, what matters most?", "Reading regularly", ["Reading only difficult books", "Reading before exams", "Reading for several hours"], "They said the regular habit mattered more than the type of reading.", "easy"),
   ("What happened to students who read only before exams?", "They showed little improvement", ["They wrote the clearest essays", "They gained the richest vocabulary", "They stopped reading"], "The passage states they improved very little.", "easy"),
   ("Which title suits the passage best?", "The Power of a Daily Reading Habit", ["Why Exams Are Difficult", "How to Write Long Essays", "The Cost of School Books"], "The passage is about the benefit of daily reading.", "medium")]),
 ("Electric vehicles produce no exhaust while driving, which improves air quality in crowded cities. Yet their batteries need minerals that are mined with heavy machinery, and the electricity used to charge them may come from coal. Therefore, experts say that the real environmental benefit of electric vehicles depends on how clean the power supply is.",
  [("According to the experts, the environmental benefit of electric vehicles depends on", "how clean the electricity supply is", ["the colour of the vehicle", "the number of roads in a city", "the price of petrol"], "This is stated in the last sentence.", "medium"),
   ("Which drawback of electric vehicles is mentioned?", "Battery minerals are mined with heavy machinery", ["They cannot be driven in cities", "They produce more exhaust", "They are always slower"], "The passage names mining of battery minerals.", "easy"),
   ("The word 'Yet' in the passage introduces", "a contrast to the earlier benefit", ["a repeated point", "a personal opinion", "a final conclusion"], "'Yet' turns from the benefit to the limitations.", "hard")]),
 ("Teenagers need about eight to ten hours of sleep, but many get much less because of late-night screen use and early school hours. Lack of sleep affects memory and mood, and it can make it harder to concentrate in class. Simple habits, like keeping phones away from the bed, can help.",
  [("How many hours of sleep do teenagers need, according to the passage?", "Eight to ten hours", ["Five to six hours", "Six to seven hours", "Eleven to twelve hours"], "The first sentence gives the range.", "easy"),
   ("Which of these is NOT mentioned as an effect of too little sleep?", "Weight gain", ["Poor memory", "Bad mood", "Difficulty concentrating"], "Weight gain does not appear in the passage.", "medium"),
   ("What simple habit does the passage suggest?", "Keeping phones away from the bed", ["Starting school later", "Sleeping during the day", "Studying at midnight"], "It is mentioned in the final sentence.", "easy")])]

def generate(b):
    for st, c1, c2, idx, why, dif in STATEMENTS:
        b.add_fixed(LOG, "statements-conclusions", "Statement and conclusions", dif, f"Statement: {st}\nConclusions: I. {c1}  II. {c2}", CONC, idx, why)
    for q, s1, s2, idx, why, dif in SUFFICIENCY:
        b.add_fixed(LOG, "data-sufficiency", "Sufficiency of information", dif, f"{q}\nI. {s1}\nII. {s2}", DS, idx, why)
    _day_puzzles(b)
    for q, a, w, e, d in PUZZLES: b.add(LOG, "logical-puzzles", "Classic puzzles", d, q, a, w, e)
    for q, a, w, e, s, d in VOCAB: b.add(VER, "vocabulary", s, d, q, a, w, e)
    for w, a, ws in SYN: b.add(VER, "synonyms", "Word pairs", "easy" if w in ("Brave", "Rapid", "Commence") else "medium", f"Choose the word closest in meaning to '{w}'.", a, ws, f"'{w}' and '{a}' mean nearly the same thing.")
    for w, a, ws in ANT: b.add(VER, "antonyms", "Word pairs", "easy" if w in ("Ancient", "Victory", "Accept") else "medium", f"Choose the word opposite in meaning to '{w}'.", a, ws, f"'{a}' is the opposite of '{w}'.")
    for q, a, w, e, s, d in GRAMMAR: b.add(VER, "grammar", s, d, "Fill in the blank: " + q, a, w, e)
    for a, ws, e in CORRECT: b.add(VER, "sentence-correction", "Correct usage", "medium", "Which of the following sentences is grammatically correct?", a, ws, e, by_options=True)
    for q, a, w, e in COMPLETE: b.add(VER, "sentence-completion", "Context clues", "medium", "Choose the word that best completes the sentence:\n" + q, a, w, e)
    for passage, qs in PASSAGES:
        for q, a, w, e, d in qs: b.add(VER, "reading-comprehension", "Passage questions", d, f"Passage: {passage}\n\nQuestion: {q}", a, w, e)
