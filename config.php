<?php
// NexPath local configuration for XAMPP.
$db_host = "localhost";
$db_user = "root";
$db_pass = "";
$db_name = "nexpath_db";

function db(): mysqli {
    global $db_host, $db_user, $db_pass, $db_name;
    $conn = new mysqli($db_host, $db_user, $db_pass, $db_name);
    if ($conn->connect_error) {
        die("Database connection failed. Start MySQL and import db/nexpath_database.sql.");
    }
    $conn->set_charset("utf8mb4");
    return $conn;
}

function e($value): string {
    return htmlspecialchars((string)$value, ENT_QUOTES, 'UTF-8');
}

function csrf_token(): string {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function check_csrf(): void {
    if (!isset($_POST['csrf_token'], $_SESSION['csrf_token']) ||
        !hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
        http_response_code(419);
        exit("Invalid or expired form token. Please go back and try again.");
    }
}

// Minimum number of completed skill assessments needed to unlock prediction.
// (v2: raised from 2 to 5 so the model has a meaningful skill profile to work with.)
// Students can still choose WHICH skills to assess - they do not need all 25.
define('MIN_SKILLS_REQUIRED', 5);

// Loads a user's previously completed skill scores from the database so
// progress survives logout/login and new sessions.
function load_skill_scores(int $user_id): array {
    $scores = [];
    try {
        $conn = db();
        $stmt = $conn->prepare("SELECT skill, correct, percent, completed_at FROM skill_scores WHERE user_id = ?");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $scores[$row['skill']] = [
                'correct' => (int)$row['correct'],
                'percent' => (int)$row['percent'],
                'completed_at' => $row['completed_at'],
            ];
        }
        $stmt->close();
        $conn->close();
    } catch (Throwable $ex) {
        // If the table/connection is unavailable, fall back to an empty set
        // rather than breaking the page; the session will still work for
        // the current visit.
    }
    return $scores;
}

// Saves/updates one skill's score for a user so it persists across sessions.
function save_skill_score(int $user_id, string $skill, int $correct, int $percent): void {
    try {
        $conn = db();
        $stmt = $conn->prepare(
            "INSERT INTO skill_scores (user_id, skill, correct, percent, completed_at)
             VALUES (?, ?, ?, ?, NOW())
             ON DUPLICATE KEY UPDATE correct = VALUES(correct), percent = VALUES(percent), completed_at = VALUES(completed_at)"
        );
        $stmt->bind_param("isii", $user_id, $skill, $correct, $percent);
        $stmt->execute();
        $stmt->close();
        $conn->close();
    } catch (Throwable $ex) {
        // The score still lives in the session for this visit even if the
        // database write fails, so the current attempt isn't lost.
    }
}

// NexPath v2 helper functions (career config, attempt history, courses, formatting).
require_once __DIR__ . '/helpers_v2.php';
?>