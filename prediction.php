<?php
require_once __DIR__ . '/auth_guard.php';
$user_id = (int)$_SESSION['user_id'];
$required = all_skill_names();
$scores = current_scores($user_id);               // skill => latest score (0-10), assessed skills only
$history = get_attempt_history($user_id);         // for "previous vs current" on retests
$done_count = count($scores);
$min = MIN_SKILLS_REQUIRED;
$complete = $done_count >= $min;
$notice = $_SESSION['prediction_notice'] ?? ''; unset($_SESSION['prediction_notice']);
$flash = $_SESSION['flash_retest'] ?? null; unset($_SESSION['flash_retest']);
$progress_pct = min(100, round($done_count / $min * 100));
?>
<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>NexPath | Career Assessment</title><link rel="stylesheet" href="css/prediction.css"><link rel="stylesheet" href="css/v2.css"></head><body>
<?php nav_v2('prediction'); ?>
<main class="assessment-shell">
<section class="intro"><span class="eyebrow">CAREER ASSESSMENT</span><h1>Test your skills. <span>Find your path.</span></h1>
<p>Instead of rating yourself, NexPath checks your knowledge with randomized MCQ tests. Choose any skills you want to test and complete at least <?=$min?> of them to unlock a career prediction. You do not need to finish all <?=count($required)?> skills, and you can retake any test later to track your improvement.</p></section>

<?php if($notice): ?><div class="alert warn"><?=e($notice)?></div><?php endif; ?>
<?php if($flash):
    $imp = improvement_info((int)$flash['previous'], (int)$flash['current']); ?>
<div class="alert <?=e($imp['class'])?>"><strong><?=e($flash['skill'])?> retest:</strong> previous <?=e($flash['previous'])?>/10 → current <?=e($flash['current'])?>/10 &nbsp;(<?=e($imp['text'])?>) <span class="badge <?=e($imp['class'])?>"><?=e($imp['label'])?></span></div>
<?php endif; ?>

<div class="summary-banner"><div><strong><?=min($done_count, $min)?> / <?=$min?> skills completed</strong><span><?= $complete
    ? 'You have completed enough assessments. You can generate your prediction now, or assess more skills first for a fuller skill profile.'
    : 'Please complete at least '.$min.' skill assessments before generating your career prediction.' ?></span></div>
<div class="overall-bar"><i style="width:<?=$progress_pct?>%"></i></div>
<small class="muted-line"><?=$done_count?> of <?=count($required)?> skills assessed in total</small></div>

<section class="skills-grid">
<?php foreach ($required as $skill): $done=isset($scores[$skill]);
    $attempts = $history[$skill] ?? []; $n = count($attempts); ?>
<article class="skill-card <?=$done?'done':''?>">
<div class="skill-head"><div class="skill-icon"><?=e(strtoupper(substr($skill,0,1)))?></div><div><h2><?=e($skill)?></h2><p>10 randomized questions</p></div></div>
<?php if($done): ?><div class="score"><strong><?=e($scores[$skill])?>/10</strong><span><?=e($scores[$skill]*10)?>%</span></div>
<?php if($n >= 2): $imp = improvement_info($attempts[$n-2]['correct'], $attempts[$n-1]['correct']); ?>
<div class="retest-line">Previous <?=e($attempts[$n-2]['correct'])?>/10 → Current <?=e($attempts[$n-1]['correct'])?>/10 <span class="badge <?=e($imp['class'])?>"><?=e($imp['text'])?></span></div>
<?php endif; ?>
<a class="test-btn secondary" href="assessment.php?skill=<?=urlencode($skill)?>">Retake Test ↻</a>
<?php else: ?><div class="pending">Not assessed</div><a class="test-btn" href="assessment.php?skill=<?=urlencode($skill)?>">Take <?=e($skill)?> Test →</a><?php endif; ?>
</article>
<?php endforeach; ?>
</section>

<?php if($complete): ?>
<form class="predict-panel" action="predict.php" method="POST"><input type="hidden" name="csrf_token" value="<?=e(csrf_token())?>">
<div><span class="eyebrow">READY?</span><h2>You've met the minimum to predict.</h2><p>The server validates your saved assessment scores. Skills you have not assessed are never treated as real scores; the model fills them with neutral dataset values, so assessing more skills gives a more complete profile.</p></div>
<button type="submit">Predict My Career →</button></form>
<?php else: ?>
<div class="predict-panel locked"><div><span class="eyebrow">LOCKED</span><h2>Career prediction is locked</h2><p>Complete <?=$min - $done_count?> more skill assessment<?=($min-$done_count)==1?'':'s'?> to unlock it (<?=$done_count?> / <?=$min?> completed).</p></div><button type="button" disabled>Predict My Career →</button></div>
<?php endif; ?>
</main></body></html>
