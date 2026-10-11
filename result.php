<?php
require_once __DIR__ . '/auth_guard.php';
$user_id = (int)$_SESSION['user_id'];
$error = $_SESSION['prediction_error'] ?? '';
unset($_SESSION['prediction_error']);
$prediction = null; $legacy = false; $viewing_history = false;

if (isset($_GET['id'])) {
    // Open an OLD result. Always filtered by the logged-in user's ID, so nobody can open another user's result.
    $id = filter_var($_GET['id'], FILTER_VALIDATE_INT);
    if ($id === false || $id < 1) { header("Location: progress.php"); exit; }
    try {
        $conn = db();
        $stmt = $conn->prepare("SELECT id, role, confidence, scores_json, details_json, created_at FROM assessment_results WHERE id = ? AND user_id = ?");
        $stmt->bind_param("ii", $id, $user_id);
        $stmt->execute();
        $row = $stmt->get_result()->fetch_assoc();
        $stmt->close(); $conn->close();
    } catch (Throwable $ex) { $row = null; }
    if (!$row) { header("Location: progress.php"); exit; }
    $viewing_history = true;
    $details = $row['details_json'] ? json_decode($row['details_json'], true) : null;
    if ($details && isset($details['assessed'])) {
        $prediction = $details; $prediction['id'] = (int)$row['id']; $prediction['created_at'] = $row['created_at'];
    } else {   // result created before v2: every skill was stored (unassessed ones as 1)
        $legacy = true;
        $stored = json_decode($row['scores_json'], true) ?: [];
        $prediction = ['id' => (int)$row['id'], 'role' => $row['role'], 'confidence' => $row['confidence'],
                       'top' => [['role' => $row['role'], 'score' => round((float)$row['confidence'], 1)]], 'model' => 'Random Forest',
                       'n_features' => count($stored), 'n_assessed' => count($stored), 'assessed' => valid_scores($stored), 'created_at' => $row['created_at']];
    }
} else {
    $prediction = $_SESSION['prediction'] ?? null;
}
if (!$prediction && !$error) { header("Location: prediction.php"); exit; }

if ($prediction) {
    $view = build_career_view($prediction['role'], $prediction['assessed']);
    $top = $prediction['top'] ?? [];
    $alternatives = array_slice($top, 1, 3);
    $primary_score = isset($top[0]) ? (float)$top[0]['score'] : (float)($prediction['confidence'] ?? 0);
    $n_assessed = (int)$prediction['n_assessed'];
    $n_total = (int)$prediction['n_features'];
    $statusText = ['strong' => 'Strong', 'improve' => 'Improve', 'not_assessed' => 'Not assessed'];
}
?>
<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>NexPath | Your Result</title><link rel="stylesheet" href="css/result.css"><link rel="stylesheet" href="css/v2.css"></head><body>
<?php nav_v2('prediction'); ?>
<main class="result-shell">
<?php if($error): ?><section class="result-card error"><span class="eyebrow">PREDICTION ERROR</span><h1>We couldn't generate your result.</h1><p><?=e($error)?></p><a class="btn" href="prediction.php">Back to Assessment</a></section>
<?php else: ?>

<?php if($viewing_history): ?><p class="back-link"><a href="progress.php">← Back to My Progress</a> · Result generated on <?=e(fmt_date($prediction['created_at'], true))?></p><?php endif; ?>
<?php if($legacy): ?><div class="alert warn">This result was created before the NexPath v2 upgrade, so only the primary career is available. Skills that were not tested were stored as 1/10 in that older record.</div><?php endif; ?>

<!-- A. PREDICTED CAREER (primary, clearly separated from the alternatives) -->
<section class="result-card hero-result">
<span class="eyebrow">YOUR PREDICTED CAREER</span>
<div class="role"><?=e($prediction['role'])?></div>
<div class="confidence"><strong>Model Prediction Score: <?=e(number_format($primary_score,1))?>%</strong><span>How strongly the Random Forest model favours this career for your skill profile. It is a model score, not a real-world chance of getting this career.</span></div>
<?php if($view['description']): ?><p><?=e($view['description'])?></p><?php endif; ?>
<div class="actions"><a class="btn" href="<?=e($view['courses_url'])?>">View Recommended Courses →</a>
<a class="btn secondary" href="<?=e($view['job_page'] && is_file(__DIR__.'/'.$view['job_page']) ? $view['job_page'] : 'jobs.html')?>">View Jobs →</a>
<a class="text-btn" href="prediction.php">Retake Assessment</a></div>
</section>

<!-- B. WHY -->
<section class="v2-card"><div class="v2-head"><span class="eyebrow">WHY THIS CAREER?</span><h2>Why NexPath predicted <?=e($prediction['role'])?></h2>
<p class="muted">Your best assessed skills among the skills this career relies on.</p></div>
<?php if($view['why']): ?><div class="skill-bars">
<?php foreach($view['why'] as $w): ?><div class="sbar"><span><?=e($w['skill'])?></span><div class="bar"><i style="width:<?=$w['score']*10?>%"></i></div><strong><?=e($w['score'])?>/10</strong></div><?php endforeach; ?></div>
<?php else: ?><p class="muted">None of the skills commonly needed for this career were assessed. The prediction came from the overall pattern of your other assessed skills. Assess more skills for a clearer explanation.</p><?php endif; ?>
</section>

<!-- C + D. STRONG / IMPROVE -->
<div class="grid-2">
<section class="v2-card"><div class="v2-head"><span class="eyebrow">STRONG SKILLS</span><h2>Your highest scores</h2></div>
<?php if($view['strong']): ?><ul class="chip-list"><?php foreach($view['strong'] as $s): ?><li><span class="chip good"><?=e($s['skill'])?> <b><?=e($s['score'])?>/10</b></span></li><?php endforeach; ?></ul>
<p class="muted small">Skills you scored 7/10 or higher on.</p>
<?php else: ?><p class="muted">No assessed skill has reached 7/10 yet. Retake tests after some practice to build your strengths.</p><?php endif; ?></section>
<section class="v2-card"><div class="v2-head"><span class="eyebrow">SKILLS TO IMPROVE</span><h2>Relevant to <?=e($prediction['role'])?></h2></div>
<?php if($view['improve']): ?><ul class="chip-list"><?php foreach($view['improve'] as $s): ?><li><span class="chip warn"><?=e($s['skill'])?> <b><?=e($s['score'])?>/10</b> <small>target <?=e($s['target'])?></small></span></li><?php endforeach; ?></ul>
<?php else: ?><p class="muted">All assessed career skills are at or near their targets.</p><?php endif; ?>
<?php if($view['not_assessed']): ?><p class="muted small">Not assessed yet: <?=e(implode(', ', array_column($view['not_assessed'], 'skill')))?></p><?php endif; ?></section>
</div>

<!-- 4. ALTERNATIVES -->
<section class="v2-card alt-card"><div class="v2-head"><span class="eyebrow">OTHER CAREER MATCHES</span><h2>Other career matches based on your current skill profile</h2>
<p class="muted">These are the next-highest model scores. They are not guaranteed career choices and they change as you assess more skills.</p></div>
<div class="primary-row"><span class="tag">PRIMARY CAREER</span><strong><?=e($prediction['role'])?></strong><em>Model Score <?=e(number_format($primary_score,1))?>%</em></div>
<?php if($alternatives): ?><div class="alt-list"><?php foreach($alternatives as $a): ?>
<div class="alt-row"><span><?=e($a['role'])?></span><div class="bar"><i style="width:<?=min(100,max(2,(float)$a['score']))?>%"></i></div><strong><?=e(number_format((float)$a['score'],1))?>%</strong></div><?php endforeach; ?></div>
<?php else: ?><p class="muted">Alternative matches are not available for this older result.</p><?php endif; ?>
<small class="muted">Column meaning: Career &nbsp;|&nbsp; Model Score (Random Forest prediction score).</small></section>

<!-- 5. SKILL GAP -->
<section class="v2-card"><div class="v2-head"><span class="eyebrow">CAREER SKILL GAP</span><h2>How your skills compare with <?=e($prediction['role'])?> targets</h2>
<p class="muted">Targets are the typical scores of students labelled with this career in the NexPath dataset (editable in <code>data/career_config.json</code>). A skill counts as Strong when it is within 1 point of the target.</p></div>
<?php if($view['gap']): ?><div class="table-wrap"><table class="v2-table"><thead><tr><th>Skill</th><th>Your Score</th><th>Target</th><th>Status</th></tr></thead><tbody>
<?php foreach($view['gap'] as $g): ?><tr><td><?=e($g['skill'])?></td>
<td><?= $g['score'] === null ? '<span class="na">Not assessed</span>' : e($g['score']).'/10' ?></td><td><?=e($g['target'])?>/10</td>
<td><span class="badge <?= $g['status']==='strong'?'good':($g['status']==='improve'?'warn':'neutral') ?>"><?=e($statusText[$g['status']])?></span></td></tr><?php endforeach; ?></tbody></table></div>
<div class="grid-2 tight"><div><h3 class="mini">Strong Skills</h3><?= $view['strong_relevant'] ? '<p>'.e(implode(', ', array_column($view['strong_relevant'],'skill'))).'</p>' : '<p class="muted">None yet</p>' ?></div>
<div><h3 class="mini">Skills to Improve</h3><?= $view['improve'] ? '<p>'.e(implode(', ', array_column($view['improve'],'skill'))).'</p>' : '<p class="muted">None - great!</p>' ?></div></div>
<?php else: ?><p class="muted">No skill targets are configured for this career yet. Add it to <code>data/career_config.json</code>.</p><?php endif; ?>
</section>

<!-- 6. ROADMAP -->
<section class="v2-card"><div class="v2-head"><span class="eyebrow">LEARNING ROADMAP</span><h2>Your <?=e($prediction['role'])?> roadmap</h2>
<p class="muted">Steps follow a sensible learning order. Courses come from the NexPath Courses page.</p></div>
<ol class="roadmap">
<?php foreach($view['roadmap'] as $i => $st): $r = $st['resource']; ?>
<li class="step <?=e($st['status'])?>"><div class="step-no">STEP <?=$i+1?></div><div class="step-body">
<h3><?=e($st['skill'])?> <span class="badge <?= $st['status']==='strong'?'good':($st['status']==='improve'?'warn':'neutral') ?>"><?=e($statusText[$st['status']])?></span></h3>
<p class="muted small">Current: <?= $st['score']===null ? 'Not assessed' : e($st['score']).'/10' ?> · Target: <?=e($st['target'])?>/10</p>
<?php if($r['title']): ?><p class="resource">Recommended: <a href="<?=e($r['url'])?>"<?= strpos($r['url'],'http')===0 ? ' target="_blank" rel="noopener"' : '' ?>><?=e($r['title'])?> ↗</a>
<?php if(!empty($r['provider'])): ?><small>(<?=e($r['provider'])?>)</small><?php endif; ?><?php if($r['note']): ?><small class="muted"> · <?=e($r['note'])?></small><?php endif; ?></p>
<?php else: ?><p class="resource muted">No course is listed for this skill yet.</p><?php endif; ?>
</div></li><?php endforeach; ?>
</ol>
<div class="actions"><a class="btn" href="<?=e($view['courses_url'])?>">View Recommended Courses →</a></div>
</section>

<!-- F. MODEL INFO -->
<section class="v2-card model-card"><div class="v2-head"><span class="eyebrow">MODEL INFORMATION</span><h2>How this result was produced</h2></div>
<div class="stat-row">
<div class="stat"><small>Model used</small><strong>Random Forest</strong></div>
<div class="stat"><small>Skills assessed</small><strong><?=e($n_assessed)?> of <?=e($n_total)?></strong></div>
<div class="stat"><small>Prediction result</small><strong><?=e($prediction['role'])?></strong></div>
<div class="stat"><small>Model Prediction Score</small><strong><?=e(number_format($primary_score,1))?>%</strong></div></div>
<p class="muted small"><?php if(!$legacy): ?>The model needs a value for all <?=e($n_total)?> skills. The <?=e($n_total-$n_assessed)?> skill(s) you did not assess were filled with the typical (median) value from the training data instead of being treated as your score, so a result built from only a few assessed skills is less reliable.<?php endif; ?>
The score is the model's own estimate from a small academic dataset and does not guarantee real-world career suitability.
<a href="model-performance.php">See how the model was evaluated →</a></p></section>

<!-- Existing skill-profile section kept -->
<section class="profile-card"><div><span class="eyebrow">YOUR SKILL PROFILE</span><h2>Assessment scores</h2></div><div class="scores-grid">
<?php foreach($prediction['assessed'] as $skill=>$score): ?><div class="score-row"><span><?=e($skill)?></span><div class="bar"><i style="width:<?=((int)$score*10)?>%"></i></div><strong><?=e($score)?>/10</strong></div><?php endforeach; ?>
</div>
<?php $missing = array_diff(all_skill_names(), array_keys($prediction['assessed'])); if($missing && !$legacy): ?><p class="muted small"><strong>Not assessed:</strong> <?=e(implode(', ', $missing))?></p><?php endif; ?></section>
<?php endif; ?></main></body></html>
