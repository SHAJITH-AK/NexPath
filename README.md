# NexPath

## Project Overview

NexPath is an AI/ML-based career guidance website for students. The original project asked users to manually rate 25 skills from 1–10. The finished version replaces self-rating with randomized knowledge assessments.

**New flow:**

Login → Home → Career Assessment → 10-question skill tests → automatic scores → assessment summary → Python ML prediction → career result → Jobs/Courses

## Features

- Login, signup and logout using PHP sessions.
- Password hashing with `password_hash()` and verification with `password_verify()`.
- Local-development password reset flow.
- Protected home, assessment, prediction and result pages.
- 25 skill assessments matching the actual ML dataset features.
- 12 MCQs per skill; 10 are randomly selected for each attempt.
- Answer options are shuffled without changing the correct answer.
- Automatic 0–10 scoring; the browser cannot submit a fabricated score.
- A 0/10 test is sent to the model as 1 because the supplied training data has a minimum value of 1 (the student still sees the real 0/10).
- Prediction requires a **minimum of 5** assessed skills (`MIN_SKILLS_REQUIRED` in `config.php`, enforced on the server) — not all 25. Skills that were not assessed are **not** treated as scores: they are sent to the model as missing values and filled with the dataset median (see *Missing skills* below).
- Completed skill scores are saved to the database (`skill_scores` table), so progress is not lost on logout or in a new session — logging back in restores previously completed scores.
- Random Forest career prediction using the supplied `career_skill_prediction_250.csv`.
- Model confidence is shown only when the trained classifier supplies `predict_proba`.
- Assessment/prediction history can be stored against the logged-in user.
- Contact messages stored using prepared SQL statements.
- Existing Jobs, Courses and About pages retained rather than unnecessarily redesigning them.
- Responsive assessment/result layouts for desktop and mobile.
- Clean single database setup.

## NexPath v2 Upgrade

### New features

| Feature | Where |
|---|---|
| Explainable career result (why, strong skills, skills to improve, description, model info) | `result.php` |
| Minimum **5** assessed skills, with `n / 5 skills completed` progress | `prediction.php`, `predict.php` |
| ML evaluation page (accuracy, precision, recall, F1, confusion matrix, feature importance) | `model-performance.php` |
| Top career alternatives (3 other matches with Model Score) | `result.php` |
| Skill-gap analysis against editable career targets | `result.php`, `data/career_config.json` |
| Personalised learning roadmap linked to the existing Courses page | `result.php`, `courses.html` |
| Assessment / progress history | `progress.php` |
| Retest tracking (previous vs current, Improved / No Change / Needs Improvement) | `prediction.php`, `progress.php` |
| Aptitude Test (34 topics, timed tests, server-side grading, history) | `aptitude*.php` |

### Navigation

`Home · Prediction · Jobs · Courses · Aptitude Test · Progress · About · Contact`. **Model Performance** is a secondary page, linked from the footers, the result page and the progress page, so the menu stays uncluttered. All new pages require login.

### Database upgrade (existing installs keep all their data)

1. Open phpMyAdmin → select `nexpath_db` → **Import** `db/upgrade_v2.sql`.
2. Import `db/aptitude_questions_seed.sql`.

`upgrade_v2.sql` only adds:

- `assessment_attempts` — one row per skill attempt (history). Existing `skill_scores` rows are copied in as the first attempt.
- `assessment_results.skills_assessed`, `assessment_results.details_json` and an index (existing columns untouched).
- `aptitude_questions` and `aptitude_attempts`.

Both files can be run more than once safely (verified on MariaDB 10.11 / XAMPP). On MySQL 8 the `ADD COLUMN IF NOT EXISTS` lines are not supported; run them once only. For a brand-new install import `db/nexpath_database.sql` first, then the two files above. The site still works if the upgrade has not been run (new pages show a hint), but the new history features need it.

### Career prediction explanation

After prediction the result page shows, in order: the **predicted career**, **why** (your best assessed skills among those the career needs), **strong skills** (assessed 7/10 or more), **skills to improve**, the **career description**, **other career matches**, the **skill-gap table**, the **learning roadmap** and **model information** (Random Forest, number of assessed skills, prediction score).

The percentage is always labelled **Model Prediction Score** / **Model Score**. It is the share of Random Forest trees voting for a career. It is not a real-world probability.

### Missing skills (unassessed skills)

The Random Forest needs a value for all 25 features, but students only assess some. v2 therefore:

- never treats an unassessed skill as a student score (the UI shows **Not assessed**);
- sends it to Python as `null`, and `python/predict.py` fills it with the **median of that skill in the training data**.

This was chosen over filling with 1 after a quick experiment (random partial profiles, cross-validated): median filling gave about 38% accuracy versus about 28% for filling with 1. Predictions from only a handful of skills remain much less reliable than predictions from many skills (see the table on the Model Performance page). That limitation is stated in the UI.

### Skill-gap analysis

`data/career_config.json` maps each of the 17 careers to its relevant skills and a **target score**, plus a description, job page, and which Courses-page course teaches each skill. It was generated once by `python/generate_career_config.py` from the dataset (for each career: the 6 skills whose average is furthest above the all-student average, target = that career's average, rounded) — no invented numbers. **Edit the JSON by hand** to change targets, add skills or reword descriptions (re-running the script overwrites it unless you edit it first, so it refuses to run if the file exists unless `--force` is given). A skill is **Strong** when your score is within `strong_margin` (1) of the target, **Improve** when lower, and **Not assessed** when the skill has no score.

### Learning roadmap and Courses page

The roadmap lists the career's skills in learning order with status, score, and a recommended resource. Resources are read straight from `courses.html` (title and link), so there is no second course database. Skills with no matching course (Communication, Problem Solving) point to the Aptitude Test; where only a related course exists the roadmap says "Closest course available". **View Recommended Courses** opens `courses.html?path=<career>&courses=<course keys>`; the page JavaScript compares the keys only against its own course names (nothing from the URL is inserted as HTML) and shows a banner with **Show all courses**.

### Progress and retest tracking

- `skill_scores` still holds the latest score per skill (used by prediction). Every attempt is also inserted into `assessment_attempts`, so history is never overwritten.
- Retaking a skill shows **Previous → Current** with `+N points` and a label: **Improved** (higher), **No Change** (equal) or **Needs Improvement** (lower).
- `progress.php` lists past predictions (date, skills tested, predicted career) with a details view (individual scores, alternatives, date, link to the full result), a retest table with a first-vs-latest chart, and aptitude history.
- Every query is filtered by the logged-in user's id (`$_SESSION['user_id']`); `progress.php?id=` and `result.php?id=` return to the list if the record belongs to somebody else. Results created before v2 still open (marked as older records).

### ML evaluation

Run from the project folder:

```bash
python python/evaluate_model.py
```

This trains the same `RandomForestClassifier` used by `predict.py` with **5-fold stratified cross-validation** on `career_skill_prediction_250.csv`: every student is predicted once by a model that never saw that student. It computes accuracy, macro precision/recall/F1 (also per career), the confusion matrix, feature importance and a "partial profile" accuracy check, and writes `data/model_metrics.json`. `model-performance.php` only displays that file — nothing is hard-coded. If the file is missing the page tells you to run the script. Re-run it whenever the dataset changes.

With the supplied dataset the run gives about 88.8% accuracy (macro precision ≈ 89.3%, recall ≈ 88.7%, F1 ≈ 88.6%). These describe how well the model reproduces the labels of a **small (250-row) dataset**; they do not prove that a career is right for a real student. With only 5 assessed skills the measured accuracy drops to roughly 25%, which is why the UI encourages assessing more skills.

### Aptitude test

- `aptitude.php` — three categories (Numerical Ability 16 topics, Logical Reasoning 11, Verbal Ability 7) shown as cards with icon, description, question count, difficulty and **Start Test**.
- `aptitude-test.php?topic=<slug>` — topic is validated against a whitelist; 10 distinct random questions (12+ per topic in the bank), one question at a time with Previous/Next, question dots, a progress bar and a 10-minute timer that submits automatically.
- **Correct answers never reach the browser.** The test page selects only the question and options. `aptitude-submit.php` re-reads the correct answers from MySQL, grades on the server, ignores any score sent by the client, caps the time at the limit, can be submitted only once per test, and checks the CSRF token.
- `aptitude-result.php` — score, percentage, correct/wrong/unanswered, time used, strong areas / needs improvement per sub-topic, answer review with explanations, **Retake Test** and **Back to Aptitude Topics**.
- Attempts are saved to `aptitude_attempts` and shown in **Progress** and on the Aptitude page.
- The question bank (`aptitude_questions`, 409 original questions in the seed) is built by `python/build_aptitude_questions.py`. Numerical and many reasoning questions come from templates, so answers are computed by code; syllogisms are checked against every Venn-diagram model, and verbal questions are hand-written. Nothing is copied from other websites. To add questions, add rows to `aptitude_questions` directly or extend the Python lists and re-run the script, then re-import the seed (duplicates are ignored). Topic names/descriptions live in `aptitude_topics.php`.

### Requirements added in v2

- Python packages unchanged (`pandas`, `scikit-learn`).
- PHP `dom` extension (enabled by default in XAMPP) for reading `courses.html`; without it the roadmap simply omits course links.

### How to run after upgrading

1. Start Apache and MySQL in XAMPP.
2. Import `db/upgrade_v2.sql` and `db/aptitude_questions_seed.sql`.
3. (Optional) `python python/evaluate_model.py` to refresh the metrics.
4. Open `http://localhost/NexPath/`.

## Technology Used

- HTML5
- CSS3
- JavaScript
- PHP
- MySQL
- Python
- Pandas
- Scikit-learn
- Random Forest Classifier

## Project Structure

```text
NexPath/
├── index.html
├── index.php
├── main.html
├── main.php
├── signup.html
├── forgot-password.html
├── reset-password.php
├── auth.php
├── logout.php
├── config.php
├── auth_guard.php
├── prediction.html
├── prediction.php
├── assessment.php
├── assessment_submit.php
├── predict.php
├── result.php
├── contact.php
├── about.html
├── courses.html
├── jobs.html
├── career_skill_prediction_250.csv
├── helpers_v2.php            (v2: career config, skill-gap, history, course lookup, nav)
├── aptitude_topics.php       (v2: aptitude topic catalogue)
├── aptitude.php / aptitude-test.php / aptitude-submit.php / aptitude-result.php   (v2)
├── progress.php              (v2: assessment, retest and aptitude history)
├── model-performance.php     (v2: ML evaluation page)
├── data/
│   ├── question_bank.json
│   ├── career_config.json    (v2: career -> skills -> targets, editable)
│   └── model_metrics.json    (v2: generated by python/evaluate_model.py)
├── python/
│   ├── predict.py            (updated: top-4 scores, missing-skill handling)
│   ├── evaluate_model.py     (v2: 5-fold stratified CV metrics)
│   ├── generate_career_config.py   (v2: builds data/career_config.json)
│   └── build_aptitude_questions.py (+ apt_*.py)  (v2: builds the aptitude SQL seed)
├── db/
│   ├── nexpath_database.sql
│   ├── upgrade_v2.sql        (v2)
│   └── aptitude_questions_seed.sql (v2)
├── css/
│   ├── assessment.css
│   ├── prediction.css
│   ├── result.css
│   └── existing NexPath styles...
├── js/
│   └── assessment.js
└── Jobs/
    └── existing career pages
```

## Requirements

Install:

1. XAMPP for Apache, PHP and MySQL.
2. Python 3.x.
3. Python packages used by the final prediction script.

From a Command Prompt:

```bash
python -m pip install pandas scikit-learn
```

NumPy is installed as a dependency of Pandas/scikit-learn in normal Python environments.

## Installation

### 1. Install and start XAMPP

Open XAMPP Control Panel and start:

- Apache
- MySQL

### 2. Copy the project

Copy the `NexPath` folder into:

```text
C:\xampp\htdocs\
```

The final folder should therefore be:

```text
C:\xampp\htdocs\NexPath\
```

### 3. Create the database

Open:

```text
http://localhost/phpmyadmin/
```

Import:

```text
NexPath/db/nexpath_database.sql
```

The SQL creates the `nexpath_db` database and these tables:

- `users`
- `contact_messages`
- `assessment_results`
- `skill_scores` — one row per user per skill, storing the correct count and percent for that skill's most recent attempt, so a student's progress persists across logins/sessions.

### 4. Database configuration

The default XAMPP configuration in `config.php` is:

```php
$db_host = "localhost";
$db_user = "root";
$db_pass = "";
$db_name = "nexpath_db";
```

If your MySQL root account has a password, change only `db_pass`.

Do not commit real production database credentials to a public repository.

### 5. Start NexPath

Open:

```text
http://localhost/NexPath/
```

If the redirect is not handled by your Apache configuration, open:

```text
http://localhost/NexPath/index.php
```

## Database Setup

Use, in this order:

1. `db/nexpath_database.sql` — original schema (new installs).
2. `db/upgrade_v2.sql` — v2 additions (see *Database upgrade* below).
3. `db/aptitude_questions_seed.sql` — aptitude question bank.

## Python Setup

The prediction backend is:

```text
python/predict.py
```

It reads:

```text
career_skill_prediction_250.csv
```

The PHP prediction endpoint sends a temporary JSON input file to the Python script. The Python script trains the classifier from the supplied dataset and returns JSON containing the predicted role and, when available, classifier probability.

Test the Python backend independently if needed:

```bash
python python\predict.py path\to\test-input.json
```

The website itself creates the temporary input file automatically.

## Running the Project

1. Start Apache and MySQL in XAMPP.
2. Import `db/nexpath_database.sql`.
3. Install Python dependencies.
4. Open `http://localhost/NexPath/`.
5. Create a NexPath account.
6. Log in.
7. Click **Start Prediction / Assessment**.
8. Select a skill.
9. Answer all 10 randomized questions.
10. Submit the test.
11. Repeat until at least `MIN_SKILLS_REQUIRED` (5) skills are completed — assessing more skills gives a fuller profile but isn't required.
12. Click **Predict My Career**.
13. NexPath sends the 25 model features to the Python ML pipeline — assessed skills use your real score, unassessed skills are sent as missing and filled with the dataset median.
14. View the explainable result: predicted career, why, strong skills, skill gaps, alternatives, learning roadmap and model information.
15. Explore the Jobs and Courses sections.
16. Log out and back in any time — completed skill scores are restored from the database.

## ML Model

The supplied CSV (unchanged in v2) contains **250 rows and 26 columns**.

- Input features: 25
- Target: `Role`
- Feature values in the supplied dataset: 1–10
- Target classes: 17

The 25 input features are:

```text
Python, Java, C++, HTML, CSS, JavaScript, React, SQL, MongoDB, Git, Linux, Networking, Cyber Security, Cloud Computing, Machine Learning, Deep Learning, Data Analysis, Statistics, UI UX Design, Figma, Computer Vision, NLP, Communication, Problem Solving, System Design
```

The career labels found in the dataset are:

```text
Backend Developer, Cloud Engineer, Computer Vision Engineer, Cyber Security Engineer, Data Analyst, Data Engineer, Data Scientist, Database Engineer, DevOps Engineer, Frontend Developer, Full Stack Developer, Generative AI Engineer, ML Specialist, NLP Engineer, Network Engineer, Software Engineer, UI UX Designer
```

The final Python pipeline uses:

```text
RandomForestClassifier
n_estimators = 400
random_state = 42
class_weight = "balanced"
```

No arbitrary feature renaming is performed. The feature order is read directly from the CSV, excluding only the `Role` target.

### Important model-input conversion

The assessment produces a real score from 0–10 based on correct answers.

The supplied dataset uses a minimum training value of 1 and a maximum of 10. Therefore:

```text
1–10 correct → 1–10 model input
0 correct     → 1 model input
```

The displayed student result still shows the actual score, such as `0/10`.

This avoids sending a value outside the range represented in the supplied training data.

## Assessment System

The question bank is stored in:

```text
data/question_bank.json
```

There are 25 required skill banks and 12 questions per skill.

For every attempt:

1. The server loads the selected skill's bank.
2. It shuffles the questions.
3. It selects exactly 10.
4. It shuffles each question's options.
5. The selected question set is stored in the PHP session.
6. The student answers the questions.
7. The server compares submitted answers against the server-side correct answers.
8. The server calculates the score.
9. The score is stored in the session **and** saved to the `skill_scores` table for that user, so it survives logout/login.
10. Every attempt is also stored as a new row in `assessment_attempts` (history), so retests never overwrite older results.
11. Once at least `MIN_SKILLS_REQUIRED` (5) skills are complete, prediction is unlocked. Unassessed skills are not required.

The browser never supplies the final numerical skill score.

## Security

The project uses reasonable protections for a local college application:

- `password_hash()`
- `password_verify()`
- prepared SQL statements
- session regeneration after login
- protected pages using `auth_guard.php`
- input validation
- output escaping using `htmlspecialchars()`
- CSRF tokens on assessment/contact/reset forms
- server-side assessment scoring
- prediction input validation
- no database password hardcoded into the Python script

The application is intended for local academic demonstration, not production deployment.

## Forgot Password

There is no external email provider configured in the project.

Instead, the final project includes a **local development reset flow**:

1. Enter an existing account email.
2. NexPath verifies that the account exists.
3. A local session reset state is created.
4. The user enters a new password.
5. The password is stored using `password_hash()`.

For a production website, replace this with a real email-based, expiring reset-token workflow.

## Troubleshooting

### Apache does not start

Another application may already be using port 80/443. Check XAMPP's Apache logs and change the Apache port if required.

### MySQL does not start

Check XAMPP's MySQL logs. Make sure another MySQL/MariaDB service is not conflicting with XAMPP.

### Database not found

Import:

```text
db/nexpath_database.sql
```

Then verify that `nexpath_db` exists in phpMyAdmin.

### PHP database error

Check the values in:

```text
config.php
```

Default XAMPP values are root user with an empty password.

### Python not found

Run:

```bash
python --version
```

If Windows does not recognize `python`, install Python and enable **Add Python to PATH**, or adjust the Python command/path in `predict.php`.

### Prediction not working

Run:

```bash
python -m pip install pandas scikit-learn
```

Then verify:

- `career_skill_prediction_250.csv` is in the NexPath root.
- `python/predict.py` exists.
- Python can read the CSV.
- Apache/PHP has permission to create temporary files.

### Page says a file is missing

Make sure the entire `NexPath` folder was copied to:

```text
C:\xampp\htdocs\NexPath\
```

Do not copy only the HTML files.

### Jobs page links

Career pages are stored in:

```text
NexPath/Jobs/
```

Their shared stylesheet is:

```text
NexPath/Jobs/css/job.css
```

The links were normalized so the career pages return to `../main.php` and the main Jobs page.

## Original Project Problems Found

The original project contained several integration issues:

- The prediction form still used manual 1–10 sliders.
- The form posted to `/predict`, which was not a local NexPath endpoint.
- Navigation mixed `.html` and `.php` filenames even when one of the files did not exist.
- `main.html` linked to `prediction.php`, `courses.php`, `about.php` and `jobs.php` inconsistently.
- `contact.php` linked to nonexistent `logout.html` and used inconsistent page extensions.
- Job pages linked to a missing `blog.html`.
- The job listing contained a capitalization/filename mismatch for the ML Specialist page.
- The database setup existed in duplicate SQL files.
- Authentication had no centralized database configuration.
- The original forgot-password flow only reported that an account was found; it did not reset a password.
- The original prediction page did not have an actual Python/PHP prediction pipeline.
- Assessment scoring was entirely self-reported through sliders.

## What Was Fixed

- Added a real randomized MCQ assessment system.
- Added 300 technically focused questions (12 × 25 skills).
- Added server-side scoring.
- Added session-based assessment progress.
- Added a complete PHP → Python prediction pipeline.
- Matched the 25 actual CSV feature names.
- Used the actual `Role` target from the CSV.
- Added Random Forest prediction.
- Added result and model-confidence display.
- Added assessment result storage.
- Consolidated the database.
- Fixed authentication/session handling.
- Added local password reset.
- Fixed navigation and job-page paths.
- Added responsive assessment/result interfaces.
- Added README and troubleshooting documentation.

## Limitations

1. The supplied dataset has only 250 rows, so the model should be treated as an academic demonstration rather than a scientifically validated career assessment system.
2. The question bank measures knowledge through MCQs; it cannot fully measure practical programming ability, project experience, creativity or real-world performance.
3. The Random Forest is trained from the supplied dataset at prediction time rather than using a permanently serialized model file. This keeps the project easy to understand and avoids a separate model-version file.
4. The local password reset is not suitable for production because no email verification service is configured.
5. The displayed value is the Random Forest vote share, labelled **Model Prediction Score** — it is not a real-world probability and not a guarantee that a student is suited to a career.
6. Jobs and courses remain resource pages; external links should be reviewed before production use.

## Future Improvements

- Expand the dataset with real-world student assessment data.
- Add a separate train/evaluate script and save a versioned model with `joblib`.
- Increase each question bank and tag questions by difficulty.
- Add practical coding questions for programming skills.
- Add real job APIs.
- Add secure email-based password reset.
- Add an admin dashboard for question and resource management.

---

## Login fix + test data (added)

**Login fixes**
- `auth.php`: login now looks the e-mail up case-insensitively, no longer rejects older accounts for e-mail format, and also accepts older accounts whose password was stored as plain text / md5 / sha1 / sha256 (it upgrades them to a secure hash on first successful login). Database errors now show their real reason.
- `index.php`, `main.php`: `session_start()` now runs before any HTML output, so the login session cookie is always sent.

**Test accounts** (import `db/test_data.sql` in phpMyAdmin after `nexpath_database.sql` and `upgrade_v2.sql`, or open `http://localhost/NexPath/seed_test_data.php` once)

| Email | Password | Contents |
|---|---|---|
| test@nexpath.com | Test@123 | 10 skills assessed, retests (improved / no change / needs improvement), 2 predictions, aptitude history |
| demo@nexpath.com | Demo@123 | only 3 skills, so prediction stays locked (needs 5) |
| full@nexpath.com | Full@123 | all 25 skills assessed, 1 prediction |

Running the test data again only resets these three accounts; real users are never touched. Delete `seed_test_data.php` before any non-local use.
