-- =====================================================================
-- NexPath v2 upgrade  (safe to run more than once, does not delete data)
-- Run this ONCE on top of an existing nexpath_db (imported from db/nexpath_database.sql).
-- Works with XAMPP's MariaDB. (MySQL 8 users: MySQL has no "ADD COLUMN IF NOT EXISTS" -
-- if you get "Duplicate column" on a second run, that just means it is already applied.)
-- After this, import db/aptitude_questions_seed.sql to load the aptitude questions.
-- =====================================================================
USE nexpath_db;

-- 1) Every skill attempt is kept (skill_scores continues to hold only the LATEST score).
CREATE TABLE IF NOT EXISTS assessment_attempts (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    skill VARCHAR(100) NOT NULL,
    correct TINYINT UNSIGNED NOT NULL,
    percent TINYINT UNSIGNED NOT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_attempt_user_skill (user_id, skill, attempted_at),
    CONSTRAINT fk_attempt_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Copy existing latest scores into the history table so old users start with one attempt per skill.
INSERT INTO assessment_attempts (user_id, skill, correct, percent, attempted_at)
SELECT s.user_id, s.skill, s.correct, s.percent, s.completed_at
FROM skill_scores s
WHERE NOT EXISTS (
    SELECT 1 FROM assessment_attempts a
    WHERE a.user_id = s.user_id AND a.skill = s.skill AND a.attempted_at = s.completed_at
);

-- 2) Extra information stored with each career prediction (existing columns are untouched).
ALTER TABLE assessment_results ADD COLUMN IF NOT EXISTS skills_assessed TINYINT UNSIGNED NULL AFTER confidence;
ALTER TABLE assessment_results ADD COLUMN IF NOT EXISTS details_json JSON NULL AFTER scores_json;
ALTER TABLE assessment_results ADD INDEX IF NOT EXISTS idx_result_user_date (user_id, created_at);

-- 3) Aptitude test question bank.
CREATE TABLE IF NOT EXISTS aptitude_questions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(40) NOT NULL,
    topic VARCHAR(60) NOT NULL,
    subtopic VARCHAR(80) NOT NULL DEFAULT 'General',
    question TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_answer ENUM('a','b','c','d') NOT NULL,
    explanation TEXT NULL,
    difficulty ENUM('easy','medium','hard') NOT NULL DEFAULT 'medium',
    q_hash CHAR(32) NOT NULL,
    UNIQUE KEY uq_aptitude_hash (q_hash),
    INDEX idx_aptitude_topic (topic)
);

-- 4) Aptitude attempts (history).
CREATE TABLE IF NOT EXISTS aptitude_attempts (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    topic VARCHAR(60) NOT NULL,
    score SMALLINT UNSIGNED NOT NULL,
    total_questions SMALLINT UNSIGNED NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    time_taken INT UNSIGNED NOT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_apt_user_date (user_id, attempted_at),
    CONSTRAINT fk_apt_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
