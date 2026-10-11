<?php
require_once __DIR__ . '/auth_guard.php';
require_once __DIR__ . '/aptitude_topics.php';
$res = $_SESSION['apt_result'] ?? null;
if (!$res) { header("Location: aptitude.php"); exit; }
$topics = apt_topics();
$name = $topics[$res['topic']][1] ?? $res['topic'];
$wrong = $res['answered'] - $res['score'];
$unanswered = $res['total'] - $res['answered'];
$pct = (int)round($res['percentage']);
$strong = []; $weak = [];
foreach ($res['subtopics'] as $sub => $s) {
    $p = $s['right'] / $s['n'] * 100;
    if ($p >= 75) $strong[$sub] = $s; elseif ($p < 60) $weak[$sub] = $s;
}
$verdict = $pct >= 80 ? 'Excellent work!' : ($pct >= 60 ? 'Good progress - keep practising.' : 'Keep going - practice makes you faster.');
?>
<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>NexPath | Aptitude Result</title><link rel="stylesheet" href="css/v2.css"></head><body>
<?php nav_v2('aptitude'); ?>
<main class="shell narrow">
<section class="v2-card result-hero"><span class="eyebrow">APTITUDE RESULT</span><h1><?=e($name)?></h1>
<div class="big-score"><strong><?=e($res['score'])?> / <?=e($res['total'])?></strong><span><?=$pct?>%</span></div>
<p class="muted"><?=e($verdict)?></p>
<div class="bar thick"><i style="width:<?=$pct?>%"></i></div>
<div class="stat-row"><div class="stat"><small>Score</small><strong><?=e($res['score'])?> / <?=e($res['total'])?></strong></div>
<div class="stat"><small>Percentage</small><strong><?=$pct?>%</strong></div>
<div class="stat"><small>Correct</small><strong class="ok"><?=e($res['score'])?></strong></div>
<div class="stat"><small>Wrong</small><strong class="bad"><?=e($wrong)?></strong></div>
<?php if($unanswered): ?><div class="stat"><small>Unanswered</small><strong><?=e($unanswered)?></strong></div><?php endif; ?>
<div class="stat"><small>Time used</small><strong><?=e(fmt_duration($res['time_taken']))?></strong></div></div>
<?php if(!$res['saved']): ?><div class="alert warn">This attempt could not be saved to your history. Import db/upgrade_v2.sql to enable aptitude history.</div><?php endif; ?>
<div class="actions center"><a class="btn" href="aptitude-test.php?topic=<?=urlencode($res['topic'])?>">Retake Test ↻</a><a class="btn secondary" href="aptitude.php">Back to Aptitude Topics</a></div></section>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">TOPIC PERFORMANCE</span><h2><?=e($name)?> <span class="pct-pill"><?=$pct?>%</span></h2></div>
<div class="grid-2">
<div><h3 class="mini">Strong areas</h3><?php if($strong): ?><ul class="plain"><?php foreach($strong as $sub=>$s): ?><li><span class="chip good"><?=e($sub)?> <b><?=e($s['right'])?>/<?=e($s['n'])?></b></span></li><?php endforeach; ?></ul><?php else: ?><p class="muted">No area reached 75% in this test yet.</p><?php endif; ?></div>
<div><h3 class="mini">Needs improvement</h3><?php if($weak): ?><ul class="plain"><?php foreach($weak as $sub=>$s): ?><li><span class="chip warn"><?=e($sub)?> <b><?=e($s['right'])?>/<?=e($s['n'])?></b></span></li><?php endforeach; ?></ul><?php else: ?><p class="muted">Nothing below 60% - nice!</p><?php endif; ?></div></div>
<p class="muted small">Areas are the sub-topics of the questions in this test, so each area is based on only a few questions.</p></section>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">REVIEW</span><h2>Answers and explanations</h2></div>
<?php foreach($res['review'] as $i => $r): ?>
<details class="review <?= $r['ok'] ? 'ok' : 'bad' ?>"><summary><span class="badge <?= $r['ok'] ? 'good' : 'warn' ?>"><?= $r['ok'] ? 'Correct' : ($r['given'] === null ? 'Unanswered' : 'Wrong') ?></span> Question <?=$i+1?></summary>
<p class="q"><?=nl2br(e($r['question']))?></p>
<ul class="opts"><?php foreach($r['options'] as $L=>$text): ?><li class="<?= $L===$r['correct'] ? 'right' : ($L===$r['given'] ? 'wrongpick' : '') ?>"><b><?=strtoupper($L)?>.</b> <?=e($text)?><?= $L===$r['correct'] ? ' ✓' : ($L===$r['given'] ? ' ✗ (your answer)' : '') ?></li><?php endforeach; ?></ul>
<?php if($r['explanation']): ?><p class="expl"><strong>Explanation:</strong> <?=e($r['explanation'])?></p><?php endif; ?></details>
<?php endforeach; ?></section>
</main></body></html>
