<?php
require_once __DIR__ . '/auth_guard.php';
require_once __DIR__ . '/aptitude_topics.php';
check_csrf();
$user_id = (int)$_SESSION['user_id'];
$test = $_SESSION['apt_test'] ?? null;
if (!$test || empty($test['qids'])) { header("Location: aptitude.php"); exit; }
unset($_SESSION['apt_test']);          // a test can be submitted only once

$qids = array_values(array_map('intval', $test['qids']));
$total = count($qids);
$raw = $_POST['answer'] ?? [];
if (!is_array($raw)) $raw = [];

// Grade on the SERVER: correct answers come from the database, never from the browser.
$rows = [];
try {
    $conn = db();
    $ph = implode(',', array_fill(0, $total, '?'));
    $stmt = $conn->prepare("SELECT id, subtopic, question, option_a, option_b, option_c, option_d, correct_answer, explanation FROM aptitude_questions WHERE id IN ($ph)");
    $stmt->bind_param(str_repeat('i', $total), ...$qids);
    $stmt->execute();
    foreach ($stmt->get_result()->fetch_all(MYSQLI_ASSOC) as $r) $rows[(int)$r['id']] = $r;
    $stmt->close();
} catch (Throwable $ex) { header("Location: aptitude.php"); exit; }

$score = 0; $review = []; $sub = [];
foreach ($qids as $i => $qid) {
    if (!isset($rows[$qid])) continue;
    $r = $rows[$qid];
    $given = (isset($raw[$i]) && is_string($raw[$i]) && in_array($raw[$i], ['a','b','c','d'], true)) ? $raw[$i] : null;
    $ok = $given !== null && hash_equals($r['correct_answer'], $given);
    if ($ok) $score++;
    $sub[$r['subtopic']] = $sub[$r['subtopic']] ?? ['right' => 0, 'n' => 0];
    $sub[$r['subtopic']]['n']++; if ($ok) $sub[$r['subtopic']]['right']++;
    $review[] = ['question' => $r['question'], 'options' => ['a'=>$r['option_a'],'b'=>$r['option_b'],'c'=>$r['option_c'],'d'=>$r['option_d']],
                 'given' => $given, 'correct' => $r['correct_answer'], 'ok' => $ok, 'explanation' => $r['explanation']];
}
$total = count($review);
if ($total === 0) { header("Location: aptitude.php"); exit; }
$answered = count(array_filter($review, fn($x) => $x['given'] !== null));
$pct = round($score / $total * 100, 2);
// Time is measured by the server and capped at the test's time limit.
$time_taken = max(0, min((int)$test['limit'], time() - (int)$test['started']));

$attempt_id = null;
try {
    $stmt = $conn->prepare("INSERT INTO aptitude_attempts (user_id, topic, score, total_questions, percentage, time_taken) VALUES (?, ?, ?, ?, ?, ?)");
    $topic = $test['topic'];
    $stmt->bind_param("isiidi", $user_id, $topic, $score, $total, $pct, $time_taken);
    $stmt->execute(); $attempt_id = $conn->insert_id; $stmt->close();
} catch (Throwable $ex) { /* history table missing: the result is still shown */ }
$conn->close();

$_SESSION['apt_result'] = ['topic' => $test['topic'], 'score' => $score, 'total' => $total, 'answered' => $answered, 'percentage' => $pct,
                           'time_taken' => $time_taken, 'subtopics' => $sub, 'review' => $review, 'saved' => $attempt_id !== null];
header("Location: aptitude-result.php"); exit;
