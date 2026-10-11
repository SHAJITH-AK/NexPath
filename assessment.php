<?php
require_once __DIR__ . '/auth_guard.php';
$bank = json_decode(file_get_contents(__DIR__ . '/data/question_bank.json'), true);
$skill = $_GET['skill'] ?? '';
if (!isset($bank[$skill]) || count($bank[$skill]) < 10) { header("Location: prediction.php"); exit; }

$questions = $bank[$skill];
shuffle($questions);
$questions = array_slice($questions, 0, 10);
foreach ($questions as &$q) { shuffle($q['options']); }
unset($q);
$_SESSION['current_assessment'] = ['skill'=>$skill, 'questions'=>$questions, 'started'=>time()];
?>
<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title><?=e($skill)?> Assessment | NexPath</title><link rel="stylesheet" href="css/assessment.css"></head><body>
<header class="topbar"><a class="brand" href="prediction.php"><b>N</b>Nex<span>Path</span></a><a href="prediction.php">← Assessment Overview</a></header>
<main class="test-shell"><section class="test-card">
<div class="test-meta"><div><span class="eyebrow">SKILL TEST</span><h1><?=e($skill)?></h1></div><strong id="counter">Question 1 of 10</strong></div>
<div class="progress"><i id="progress"></i></div>
<form id="testForm" action="assessment_submit.php" method="POST">
<input type="hidden" name="csrf_token" value="<?=e(csrf_token())?>">
<?php foreach($questions as $i=>$q): ?>
<fieldset class="question" data-index="<?=$i?>">
<legend><span>Question <?=$i+1?></span><?=e($q['question'])?></legend>
<div class="options"><?php foreach($q['options'] as $option): ?>
<label><input type="radio" name="answer[<?=$i?>]" value="<?=e($option)?>"><span><?=e($option)?></span></label>
<?php endforeach; ?></div>
</fieldset>
<?php endforeach; ?>
<div class="controls"><button type="button" id="prev" class="secondary">← Previous</button><button type="button" id="next">Next →</button><button type="submit" id="submit">Submit Test ✓</button></div>
</form></section></main>
<script src="js/assessment.js"></script></body></html>