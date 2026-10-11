<?php
require_once __DIR__ . '/auth_guard.php';
require_once __DIR__ . '/aptitude_topics.php';
$user_id = (int)$_SESSION['user_id'];   // EVERY query below is filtered by this authenticated user id
$topics = apt_topics();
$results = []; $db_note = '';

try {
    $conn = db();
    $stmt = $conn->prepare("SELECT id, role, confidence, skills_assessed, scores_json, details_json, created_at FROM assessment_results WHERE user_id = ? ORDER BY created_at DESC, id DESC");
} catch (Throwable $ex) { $stmt = null; }
try {
    if (!$stmt) throw new Exception('no db');
    $stmt->bind_param("i", $user_id); $stmt->execute();
    $results = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    $stmt->close();
} catch (Throwable $ex) {
    // upgrade_v2.sql not run yet: read the original columns only
    try {
        $stmt = $conn->prepare("SELECT id, role, confidence, scores_json, created_at FROM assessment_results WHERE user_id = ? ORDER BY created_at DESC, id DESC");
        $stmt->bind_param("i", $user_id); $stmt->execute();
        $results = $stmt->get_result()->fetch_all(MYSQLI_ASSOC); $stmt->close();
        $db_note = 'Run db/upgrade_v2.sql to enable full progress tracking.';
    } catch (Throwable $e2) { $db_note = 'Progress could not be loaded. Please check the database.'; }
}

// ----- Detail view of one assessment (?id=) - only if it belongs to this user -----
$detail = null;
if (isset($_GET['id'])) {
    $id = filter_var($_GET['id'], FILTER_VALIDATE_INT);
    foreach ($results as $r) if ($id !== false && (int)$r['id'] === $id) { $detail = $r; break; }
    if (!$detail) { header("Location: progress.php"); exit; }
    $d = !empty($detail['details_json']) ? json_decode($detail['details_json'], true) : null;
    $detail_legacy = !($d && isset($d['assessed']));
    $detail_scores = $detail_legacy ? valid_scores(json_decode($detail['scores_json'], true) ?: []) : $d['assessed'];
    arsort($detail_scores);
    $detail_top = $detail_legacy ? [['role' => $detail['role'], 'score' => round((float)$detail['confidence'], 1)]] : ($d['top'] ?? []);
}

// ----- Retest tracking: previous vs current per skill -----
$history = get_attempt_history($user_id);
$retests = []; $single = [];
foreach ($history as $skill => $att) {
    $n = count($att);
    if ($n >= 2) $retests[] = ['skill' => $skill, 'prev' => $att[$n-2]['correct'], 'cur' => $att[$n-1]['correct'], 'first' => $att[0]['correct'], 'n' => $n, 'imp' => improvement_info($att[$n-2]['correct'], $att[$n-1]['correct']), 'at' => $att[$n-1]['at']];
    else $single[] = ['skill' => $skill, 'cur' => $att[0]['correct'], 'at' => $att[0]['at']];
}
usort($retests, fn($a, $b) => strcmp($b['at'], $a['at']));
usort($single, fn($a, $b) => $b['cur'] <=> $a['cur']);

// ----- Aptitude history -----
$apt = [];
try {
    $stmt = $conn->prepare("SELECT topic, score, total_questions, percentage, time_taken, attempted_at FROM aptitude_attempts WHERE user_id = ? ORDER BY attempted_at DESC, id DESC LIMIT 15");
    $stmt->bind_param("i", $user_id); $stmt->execute();
    $apt = $stmt->get_result()->fetch_all(MYSQLI_ASSOC); $stmt->close();
} catch (Throwable $ex) { }
if (isset($conn)) $conn->close();
?>
<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>NexPath | My Progress</title><link rel="stylesheet" href="css/v2.css"></head><body>
<?php nav_v2('progress'); ?>
<main class="shell">
<section class="page-head"><span class="eyebrow">MY PROGRESS</span><h1>Your assessment <span>history</span></h1>
<p>Review earlier career predictions, see how your skill scores change when you retake tests, and revisit your aptitude practice.</p></section>
<?php if($db_note): ?><div class="alert warn"><?=e($db_note)?></div><?php endif; ?>

<?php if($detail): ?>
<section class="v2-card"><p class="back-link"><a href="progress.php">← All assessments</a></p>
<div class="v2-head"><span class="eyebrow">ASSESSMENT DETAILS</span><h2><?=e(fmt_date($detail['created_at'], true))?></h2></div>
<div class="stat-row"><div class="stat"><small>Predicted career</small><strong><?=e($detail['role'])?></strong></div>
<div class="stat"><small>Skills tested</small><strong><?= $detail_legacy ? 'Not recorded' : e(count($detail_scores)) ?></strong></div>
<div class="stat"><small>Assessment date</small><strong><?=e(fmt_date($detail['created_at']))?></strong></div>
<div class="stat"><small>Model Prediction Score</small><strong><?=e(number_format((float)$detail['confidence'],1))?>%</strong></div></div>
<?php if($detail_legacy): ?><div class="alert warn">This is an older record created before v2. Untested skills were stored as 1/10 in it.</div><?php endif; ?>
<div class="grid-2"><div><h3 class="mini">Individual scores</h3><div class="skill-bars">
<?php foreach($detail_scores as $skill=>$score): ?><div class="sbar"><span><?=e($skill)?></span><div class="bar"><i style="width:<?=$score*10?>%"></i></div><strong><?=e($score)?>/10</strong></div><?php endforeach; ?></div></div>
<div><h3 class="mini">Prediction and alternatives</h3>
<div class="primary-row"><span class="tag">PRIMARY</span><strong><?=e($detail['role'])?></strong></div>
<?php foreach(array_slice($detail_top,1,3) as $a): ?><div class="alt-row"><span><?=e($a['role'])?></span><div class="bar"><i style="width:<?=min(100,max(2,(float)$a['score']))?>%"></i></div><strong><?=e(number_format((float)$a['score'],1))?>%</strong></div><?php endforeach; ?>
<?php if(count($detail_top) < 2): ?><p class="muted small">Alternative matches were not stored for this record.</p><?php endif; ?>
<p class="muted small">Scores are model scores, not real-world probabilities.</p>
<a class="btn" href="result.php?id=<?=(int)$detail['id']?>">Open full result →</a></div></div>
</section>
<?php endif; ?>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">PREDICTIONS</span><h2>Assessment history</h2></div>
<?php if($results): ?><div class="table-wrap"><table class="v2-table"><thead><tr><th>Date</th><th>Skills Tested</th><th>Predicted Career</th><th></th></tr></thead><tbody>
<?php foreach($results as $r): $cnt = isset($r['skills_assessed']) && $r['skills_assessed'] !== null ? (int)$r['skills_assessed'] : '—'; ?>
<tr><td><?=e(fmt_date($r['created_at']))?></td><td><?=e($cnt)?></td><td><strong><?=e($r['role'])?></strong></td><td><a class="link" href="progress.php?id=<?=(int)$r['id']?>">View details</a></td></tr><?php endforeach; ?>
</tbody></table></div>
<?php else: ?><div class="empty"><p>No predictions yet.</p><a class="btn" href="prediction.php">Start your first assessment →</a></div><?php endif; ?></section>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">RETEST TRACKING</span><h2>Skill improvement</h2>
<p class="muted">Every attempt is kept. This compares your previous attempt with your latest one.</p></div>
<?php if($retests): ?><div class="table-wrap"><table class="v2-table"><thead><tr><th>Skill</th><th>Previous Attempt</th><th>Current Attempt</th><th>Improvement</th><th>Attempts</th></tr></thead><tbody>
<?php foreach($retests as $t): ?><tr><td><?=e($t['skill'])?></td><td><?=e($t['prev'])?>/10</td><td><strong><?=e($t['cur'])?>/10</strong></td>
<td><span class="badge <?=e($t['imp']['class'])?>"><?=e($t['imp']['label'])?></span> <small><?=e($t['imp']['text'])?></small></td><td><?=e($t['n'])?></td></tr><?php endforeach; ?></tbody></table></div>
<h3 class="mini">Progress chart (first attempt → latest)</h3><div class="skill-bars">
<?php foreach($retests as $t): ?><div class="sbar2"><span><?=e($t['skill'])?></span><div class="dual"><div class="bar ghost"><i style="width:<?=$t['first']*10?>%"></i></div><div class="bar"><i style="width:<?=$t['cur']*10?>%"></i></div></div><strong><?=e($t['first'])?> → <?=e($t['cur'])?></strong></div><?php endforeach; ?>
<p class="muted small">Light bar = first attempt · Green bar = latest attempt.</p></div>
<?php else: ?><p class="muted">No skill has been retaken yet. Retake any test from the <a class="link" href="prediction.php">Assessment page</a> to see your improvement here.</p><?php endif; ?>
<?php if($single): ?><h3 class="mini">Skills assessed once</h3><ul class="chip-list"><?php foreach($single as $s): ?><li><span class="chip neutral"><?=e($s['skill'])?> <b><?=e($s['cur'])?>/10</b></span></li><?php endforeach; ?></ul><?php endif; ?>
</section>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">APTITUDE HISTORY</span><h2>Aptitude practice</h2></div>
<?php if($apt): ?><div class="table-wrap"><table class="v2-table"><thead><tr><th>Topic</th><th>Score</th><th>Percentage</th><th>Time</th><th>Date</th></tr></thead><tbody>
<?php foreach($apt as $a): ?><tr><td><?=e($topics[$a['topic']][1] ?? $a['topic'])?></td><td><?=e($a['score'])?>/<?=e($a['total_questions'])?></td><td><?=e(round((float)$a['percentage']))?>%</td><td><?=e(fmt_duration((int)$a['time_taken']))?></td><td><?=e(fmt_date($a['attempted_at']))?></td></tr><?php endforeach; ?></tbody></table></div>
<?php else: ?><div class="empty"><p>You have not taken an aptitude test yet.</p><a class="btn" href="aptitude.php">Browse aptitude topics →</a></div><?php endif; ?></section>
<p class="muted small center">Curious how the career model works? <a class="link" href="model-performance.php">View model performance</a></p>
</main></body></html>
