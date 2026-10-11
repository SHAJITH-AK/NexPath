<?php
require_once __DIR__ . '/auth_guard.php';
require_once __DIR__ . '/aptitude_topics.php';
$user_id = (int)$_SESSION['user_id'];
$topics = apt_topics();
$stats = []; $recent = []; $db_error = '';
try {
    $conn = db();
    $res = $conn->query("SELECT topic, COUNT(*) AS n, SUM(difficulty='easy') AS e, SUM(difficulty='medium') AS m, SUM(difficulty='hard') AS h FROM aptitude_questions GROUP BY topic");
    while ($r = $res->fetch_assoc()) $stats[$r['topic']] = $r;
    $stmt = $conn->prepare("SELECT topic, score, total_questions, attempted_at FROM aptitude_attempts WHERE user_id = ? ORDER BY attempted_at DESC, id DESC LIMIT 5");
    $stmt->bind_param("i", $user_id); $stmt->execute();
    $recent = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    $stmt->close(); $conn->close();
} catch (Throwable $ex) {
    $db_error = 'The aptitude question tables were not found. Import db/upgrade_v2.sql and then db/aptitude_questions_seed.sql in phpMyAdmin.';
}
?>
<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>NexPath | Aptitude Test</title><link rel="stylesheet" href="css/v2.css"></head><body>
<?php nav_v2('aptitude'); ?>
<main class="shell">
<section class="page-head"><span class="eyebrow">PLACEMENT PRACTICE</span><h1>APTITUDE <span>TEST</span></h1>
<p>Practice aptitude questions and improve your placement readiness.</p></section>
<?php if($db_error): ?><div class="alert warn"><?=e($db_error)?></div><?php endif; ?>

<?php if($recent): ?><section class="v2-card"><div class="v2-head"><span class="eyebrow">APTITUDE HISTORY</span><h2>Your recent tests</h2></div>
<div class="table-wrap"><table class="v2-table"><thead><tr><th>Topic</th><th>Score</th><th>Date</th></tr></thead><tbody>
<?php foreach($recent as $r): ?><tr><td><?=e($topics[$r['topic']][1] ?? $r['topic'])?></td><td><?=e($r['score'])?>/<?=e($r['total_questions'])?></td><td><?=e(fmt_date($r['attempted_at']))?></td></tr><?php endforeach; ?></tbody></table></div>
<p class="muted small"><a class="link" href="progress.php">See full history in My Progress →</a></p></section><?php endif; ?>

<?php foreach(APT_CATEGORIES as $cat => $blurb): ?>
<section class="apt-cat"><div class="cat-head"><h2><?=e($cat)?></h2><p><?=e($blurb)?></p></div>
<div class="topic-grid">
<?php foreach($topics as $slug => [$c, $name, $icon, $desc]): if ($c !== $cat) continue; $s = $stats[$slug] ?? null; $n = $s ? (int)$s['n'] : 0; ?>
<article class="topic-card">
<div class="topic-icon"><?=e($icon)?></div>
<h3><?=e($name)?></h3><p><?=e($desc)?></p>
<dl class="topic-meta"><div><dt>Questions</dt><dd><?=$n?></dd></div>
<div><dt>Difficulty</dt><dd><?php if($s): ?><?php if((int)$s['e']): ?><span class="dif easy">Easy</span><?php endif; ?><?php if((int)$s['m']): ?><span class="dif medium">Medium</span><?php endif; ?><?php if((int)$s['h']): ?><span class="dif hard">Hard</span><?php endif; ?><?php else: ?>—<?php endif; ?></dd></div></dl>
<?php if($n > 0): $per = min(APT_QUESTIONS_PER_TEST, $n); ?>
<small class="muted"><?=$per?> random questions · <?=$per * APT_SECONDS_PER_QUESTION / 60?> min timer</small>
<a class="btn full" href="aptitude-test.php?topic=<?=urlencode($slug)?>">Start Test →</a>
<?php else: ?><a class="btn full disabled" aria-disabled="true">No questions yet</a><?php endif; ?>
</article>
<?php endforeach; ?>
</div></section>
<?php endforeach; ?>
</main></body></html>
