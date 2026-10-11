-- =====================================================================
-- NexPath TEST DATA  (test users + skill scores + history + predictions)
-- Import AFTER: db/nexpath_database.sql, db/upgrade_v2.sql (and optionally aptitude_questions_seed.sql)
-- Safe to run many times: it only touches the three test accounts below, never your real users.
--
--   Email                Password    What it is for
--   test@nexpath.com     Test@123    10 skills assessed, retest history, 2 predictions, aptitude history
--   demo@nexpath.com     Demo@123    only 3 skills -> prediction stays LOCKED (needs 5)
--   full@nexpath.com     Full@123    all 25 skills assessed, 1 prediction
-- =====================================================================
SET NAMES utf8mb4;
USE nexpath_db;

INSERT INTO users (name, email, password) VALUES ('Test Student', 'test@nexpath.com', '$2b$10$abcdefghijklmnopqrstuuy5KfbK8GkAcp9lvB.uQoxymtdXMInjO')
  ON DUPLICATE KEY UPDATE name = VALUES(name), password = VALUES(password);
INSERT INTO users (name, email, password) VALUES ('Demo Student', 'demo@nexpath.com', '$2b$10$ABCDEFGHIJKLMNOPQRSTUuq4BbBXeDH7JAkcIOz9n4E72h9635dgu')
  ON DUPLICATE KEY UPDATE name = VALUES(name), password = VALUES(password);
INSERT INTO users (name, email, password) VALUES ('Full Profile Student', 'full@nexpath.com', '$2b$10$zyxwvutsrqponmlkjihgferNouNj2xhWLaWfLQyQNjFWoKIPb3qCC')
  ON DUPLICATE KEY UPDATE name = VALUES(name), password = VALUES(password);

DELETE FROM skill_scores        WHERE user_id IN (SELECT id FROM users WHERE email IN ('test@nexpath.com','demo@nexpath.com','full@nexpath.com'));
DELETE FROM assessment_attempts WHERE user_id IN (SELECT id FROM users WHERE email IN ('test@nexpath.com','demo@nexpath.com','full@nexpath.com'));
DELETE FROM assessment_results  WHERE user_id IN (SELECT id FROM users WHERE email IN ('test@nexpath.com','demo@nexpath.com','full@nexpath.com'));
DELETE FROM aptitude_attempts   WHERE user_id IN (SELECT id FROM users WHERE email IN ('test@nexpath.com','demo@nexpath.com','full@nexpath.com'));

-- ---------- test@nexpath.com ----------
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Python', 5, 50, NOW() - INTERVAL 40 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Python', 8, 80, NOW() - INTERVAL 5 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Python', 8, 80, NOW() - INTERVAL 5 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'SQL', 4, 40, NOW() - INTERVAL 38 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'SQL', 7, 70, NOW() - INTERVAL 4 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'SQL', 7, 70, NOW() - INTERVAL 4 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'JavaScript', 6, 60, NOW() - INTERVAL 30 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'JavaScript', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'JavaScript', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Git', 6, 60, NOW() - INTERVAL 25 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Git', 6, 60, NOW() - INTERVAL 2 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Git', 6, 60, NOW() - INTERVAL 2 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Java', 7, 70, NOW() - INTERVAL 28 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Java', 5, 50, NOW() - INTERVAL 2 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Java', 5, 50, NOW() - INTERVAL 2 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'HTML', 9, 90, NOW() - INTERVAL 20 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'HTML', 9, 90, NOW() - INTERVAL 20 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'CSS', 8, 80, NOW() - INTERVAL 20 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'CSS', 8, 80, NOW() - INTERVAL 20 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Communication', 8, 80, NOW() - INTERVAL 15 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Communication', 8, 80, NOW() - INTERVAL 15 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Problem Solving', 7, 70, NOW() - INTERVAL 15 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Problem Solving', 7, 70, NOW() - INTERVAL 15 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'React', 6, 60, NOW() - INTERVAL 10 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'React', 6, 60, NOW() - INTERVAL 10 DAY FROM users WHERE email='test@nexpath.com';

-- ---------- demo@nexpath.com ----------
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Python', 6, 60, NOW() - INTERVAL 6 DAY FROM users WHERE email='demo@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Python', 6, 60, NOW() - INTERVAL 6 DAY FROM users WHERE email='demo@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'HTML', 7, 70, NOW() - INTERVAL 5 DAY FROM users WHERE email='demo@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'HTML', 7, 70, NOW() - INTERVAL 5 DAY FROM users WHERE email='demo@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Communication', 5, 50, NOW() - INTERVAL 4 DAY FROM users WHERE email='demo@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Communication', 5, 50, NOW() - INTERVAL 4 DAY FROM users WHERE email='demo@nexpath.com';

-- ---------- full@nexpath.com ----------
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Python', 7, 70, NOW() - INTERVAL 30 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Python', 8, 80, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Python', 8, 80, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Java', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Java', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'C++', 9, 90, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'C++', 9, 90, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'HTML', 4, 40, NOW() - INTERVAL 30 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'HTML', 5, 50, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'HTML', 5, 50, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'CSS', 4, 40, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'CSS', 4, 40, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'JavaScript', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'JavaScript', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'React', 5, 50, NOW() - INTERVAL 30 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'React', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'React', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'SQL', 5, 50, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'SQL', 5, 50, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'MongoDB', 8, 80, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'MongoDB', 8, 80, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Git', 6, 60, NOW() - INTERVAL 30 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Git', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Git', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Linux', 9, 90, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Linux', 9, 90, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Networking', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Networking', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Cyber Security', 7, 70, NOW() - INTERVAL 30 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Cyber Security', 8, 80, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Cyber Security', 8, 80, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Cloud Computing', 5, 50, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Cloud Computing', 5, 50, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Machine Learning', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Machine Learning', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Deep Learning', 7, 70, NOW() - INTERVAL 30 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Deep Learning', 8, 80, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Deep Learning', 8, 80, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Data Analysis', 9, 90, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Data Analysis', 9, 90, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Statistics', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Statistics', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'UI UX Design', 3, 30, NOW() - INTERVAL 30 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'UI UX Design', 4, 40, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'UI UX Design', 4, 40, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Figma', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Figma', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Computer Vision', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Computer Vision', 7, 70, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'NLP', 5, 50, NOW() - INTERVAL 30 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'NLP', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'NLP', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Communication', 5, 50, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Communication', 5, 50, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'Problem Solving', 4, 40, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'Problem Solving', 4, 40, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'System Design', 5, 50, NOW() - INTERVAL 30 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at) SELECT id, 'System Design', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at) SELECT id, 'System Design', 6, 60, NOW() - INTERVAL 3 DAY FROM users WHERE email='full@nexpath.com';

-- ---------- saved career predictions ----------
INSERT INTO assessment_results (user_id, role, confidence, skills_assessed, scores_json, details_json, created_at) SELECT id, 'Backend Developer', 48.2, 5, '{"Python": 5, "Java": 7, "C++": null, "HTML": null, "CSS": null, "JavaScript": 6, "React": null, "SQL": 4, "MongoDB": null, "Git": 6, "Linux": null, "Networking": null, "Cyber Security": null, "Cloud Computing": null, "Machine Learning": null, "Deep Learning": null, "Data Analysis": null, "Statistics": null, "UI UX Design": null, "Figma": null, "Computer Vision": null, "NLP": null, "Communication": null, "Problem Solving": null, "System Design": null}', '{"role": "Backend Developer", "confidence": 48.2, "top": [{"role": "Backend Developer", "score": 48.2}, {"role": "Software Engineer", "score": 22.5}, {"role": "Full Stack Developer", "score": 14.1}], "model": "Random Forest", "n_features": 25, "n_assessed": 5, "assessed": {"Python": 5, "SQL": 4, "JavaScript": 6, "Git": 6, "Java": 7}, "created_at": "2026-09-30 10:00:00", "id": null}', NOW() - INTERVAL 35 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_results (user_id, role, confidence, skills_assessed, scores_json, details_json, created_at) SELECT id, 'Full Stack Developer', 63.7, 10, '{"Python": 8, "Java": 5, "C++": null, "HTML": 9, "CSS": 8, "JavaScript": 7, "React": 6, "SQL": 7, "MongoDB": null, "Git": 6, "Linux": null, "Networking": null, "Cyber Security": null, "Cloud Computing": null, "Machine Learning": null, "Deep Learning": null, "Data Analysis": null, "Statistics": null, "UI UX Design": null, "Figma": null, "Computer Vision": null, "NLP": null, "Communication": 8, "Problem Solving": 7, "System Design": null}', '{"role": "Full Stack Developer", "confidence": 63.7, "top": [{"role": "Full Stack Developer", "score": 63.7}, {"role": "Frontend Developer", "score": 17.4}, {"role": "Backend Developer", "score": 9.8}], "model": "Random Forest", "n_features": 25, "n_assessed": 10, "assessed": {"Python": 8, "SQL": 7, "JavaScript": 7, "Git": 6, "Java": 5, "HTML": 9, "CSS": 8, "Communication": 8, "Problem Solving": 7, "React": 6}, "created_at": "2026-09-30 10:00:00", "id": null}', NOW() - INTERVAL 1 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO assessment_results (user_id, role, confidence, skills_assessed, scores_json, details_json, created_at) SELECT id, 'Data Scientist', 58.9, 25, '{"Python": 8, "Java": 6, "C++": 9, "HTML": 5, "CSS": 4, "JavaScript": 7, "React": 6, "SQL": 5, "MongoDB": 8, "Git": 7, "Linux": 9, "Networking": 7, "Cyber Security": 8, "Cloud Computing": 5, "Machine Learning": 7, "Deep Learning": 8, "Data Analysis": 9, "Statistics": 7, "UI UX Design": 4, "Figma": 6, "Computer Vision": 7, "NLP": 6, "Communication": 5, "Problem Solving": 4, "System Design": 6}', '{"role": "Data Scientist", "confidence": 58.9, "top": [{"role": "Data Scientist", "score": 58.9}, {"role": "ML Specialist", "score": 20.3}, {"role": "Data Analyst", "score": 11.6}], "model": "Random Forest", "n_features": 25, "n_assessed": 25, "assessed": {"Python": 8, "Java": 6, "C++": 9, "HTML": 5, "CSS": 4, "JavaScript": 7, "React": 6, "SQL": 5, "MongoDB": 8, "Git": 7, "Linux": 9, "Networking": 7, "Cyber Security": 8, "Cloud Computing": 5, "Machine Learning": 7, "Deep Learning": 8, "Data Analysis": 9, "Statistics": 7, "UI UX Design": 4, "Figma": 6, "Computer Vision": 7, "NLP": 6, "Communication": 5, "Problem Solving": 4, "System Design": 6}, "created_at": "2026-09-30 10:00:00", "id": null}', NOW() - INTERVAL 2 DAY FROM users WHERE email='full@nexpath.com';

-- ---------- aptitude test history (needs db/upgrade_v2.sql) ----------
INSERT INTO aptitude_attempts (user_id, topic, score, total_questions, percentage, time_taken, attempted_at) SELECT id, 'percentages', 8, 10, 80.00, 420, NOW() - INTERVAL 12 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO aptitude_attempts (user_id, topic, score, total_questions, percentage, time_taken, attempted_at) SELECT id, 'number-system', 6, 10, 60.00, 540, NOW() - INTERVAL 9 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO aptitude_attempts (user_id, topic, score, total_questions, percentage, time_taken, attempted_at) SELECT id, 'averages', 9, 10, 90.00, 380, NOW() - INTERVAL 5 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO aptitude_attempts (user_id, topic, score, total_questions, percentage, time_taken, attempted_at) SELECT id, 'number-series', 7, 10, 70.00, 500, NOW() - INTERVAL 2 DAY FROM users WHERE email='test@nexpath.com';
INSERT INTO aptitude_attempts (user_id, topic, score, total_questions, percentage, time_taken, attempted_at) SELECT id, 'algebra', 8, 10, 80.00, 450, NOW() - INTERVAL 4 DAY FROM users WHERE email='full@nexpath.com';
INSERT INTO aptitude_attempts (user_id, topic, score, total_questions, percentage, time_taken, attempted_at) SELECT id, 'percentages', 5, 10, 50.00, 590, NOW() - INTERVAL 3 DAY FROM users WHERE email='demo@nexpath.com';
