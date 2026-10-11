<?php
require_once __DIR__ . '/auth_guard.php';
require_once __DIR__ . '/aptitude_topics.php';
$topics = apt_topics();
$slug = $_GET['topic'] ?? '';
if (!is_string($slug) || !isset($topics[$slug])) { header("Location: aptitude.php"); exit; }   // whitelist: unknown topic -> back to list
[$cat, $name] = $topics[$slug];

$questions = [];
try {
    $conn = db();
    // Random questions of this topic; DISTINCT ids so the same question never appears twice in one test.
    // NOTE: correct_answer and explanation are deliberately NOT selected - they never reach the browser.
    $limit = APT_QUESTIONS_PER_TEST;
    $stmt = $conn->prepare("SELECT id, question, option_a, option_b, option_c, option_d FROM aptitude_questions WHERE topic = ? ORDER BY RAND() LIMIT ?");
    $stmt->bind_param("si", $slug, $limit);
    $stmt->execute();
    $questions = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    $stmt->close(); $conn->close();
} catch (Throwable $ex) { $questions = []; }
if (!$questions) { header("Location: aptitude.php"); exit; }

$total = count($questions);
$seconds = $total * APT_SECONDS_PER_QUESTION;
// Server remembers which questions were served and when the test started; grading uses this, not anything from the browser.
$_SESSION['apt_test'] = ['topic' => $slug, 'qids' => array_map(fn($q) => (int)$q['id'], $questions), 'started' => time(), 'limit' => $seconds];
?>
<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title><?=e($name)?> | Aptitude Test | NexPath</title><link rel="stylesheet" href="css/v2.css"></head><body>
<header class="topbar"><a class="brand" href="main.php"><b>N</b>Nex<span>Path</span></a><a class="quit" href="aptitude.php" id="quit">← Quit test</a></header>
<main class="test-shell"><section class="test-card" id="aptTest" data-seconds="<?=$seconds?>">
<div class="test-meta"><div><span class="eyebrow"><?=e(strtoupper($cat))?></span><h1><?=e($name)?></h1></div>
<div class="timer-box"><small>Time left</small><strong id="timer"><?=e(fmt_duration($seconds))?></strong></div></div>
<div class="test-sub"><strong id="counter">Question 1 of <?=$total?></strong><span id="answeredCount">0 answered</span></div>
<div class="progress"><i id="progress"></i></div>
<form id="testForm" action="aptitude-submit.php" method="POST">
<input type="hidden" name="csrf_token" value="<?=e(csrf_token())?>">
<?php foreach($questions as $i => $q): ?>
<fieldset class="question" data-index="<?=$i?>"><legend><span>Question <?=$i+1?></span><?=nl2br(e($q['question']))?></legend>
<div class="options"><?php foreach(['a','b','c','d'] as $L): ?>
<label><input type="radio" name="answer[<?=$i?>]" value="<?=$L?>"><span><?=e($q['option_'.$L])?></span></label><?php endforeach; ?></div></fieldset>
<?php endforeach; ?>
<div class="dots" id="dots"></div>
<div class="controls"><button type="button" id="prev" class="secondary">← Previous</button><button type="button" id="next">Next →</button><button type="submit" id="submit">SUBMIT TEST ✓</button></div>
</form></section></main>
<script src="js/aptitude.js"></script></body></html>
