<?php
require_once __DIR__ . '/auth_guard.php';
// All numbers on this page come from data/model_metrics.json, which python/evaluate_model.py computes from the real dataset.
$file = __DIR__ . '/data/model_metrics.json';
$m = is_file($file) ? json_decode((string)file_get_contents($file), true) : null;
$pct = fn($v) => number_format((float)$v * 100, 1) . '%';
?>
<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>NexPath | Model Performance</title><link rel="stylesheet" href="css/v2.css"></head><body>
<?php nav_v2('about'); ?>
<main class="shell">
<section class="page-head"><span class="eyebrow">MODEL PERFORMANCE</span><h1>How well does the <span>NexPath model</span> work?</h1>
<p>This page explains the machine learning model behind your career prediction and how it was tested.</p></section>

<?php if(!$m): ?>
<div class="alert warn"><strong>Metrics have not been generated yet.</strong> Open a terminal in the project folder and run <code>python python/evaluate_model.py</code>, then refresh this page. (No placeholder numbers are shown on purpose.)</div>
<?php else: $o = $m['overall']; $ds = $m['dataset']; ?>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">OVERVIEW</span><h2>Model details</h2></div>
<div class="info-grid">
<div><small>Algorithm</small><strong><?=e($m['algorithm'])?></strong><span><?=e($m['model_params']['n_estimators'])?> trees, class-balanced, random_state <?=e($m['model_params']['random_state'])?></span></div>
<div><small>Dataset</small><strong>Existing NexPath dataset</strong><span><?=e($ds['file'])?> · <?=e($ds['rows'])?> students</span></div>
<div><small>Features</small><strong><?=e(count($ds['features']))?> skill features</strong><span>Scores from 1 to 10 for each skill</span></div>
<div><small>Career classes</small><strong><?=e(count($ds['classes']))?> careers</strong><span>~<?=e(round($ds['rows']/count($ds['classes'])))?> students per career</span></div>
<div><small>Evaluation method</small><strong><?=e($m['evaluation']['method'])?></strong><span>Each fold keeps the same career mix</span></div>
<div><small>Metrics generated</small><strong><?=e($m['generated_at'])?></strong><span>scikit-learn <?=e($m['sklearn_version'])?></span></div>
</div></section>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">RESULTS</span><h2>Cross-validation scores</h2>
<p class="muted">Every student in the dataset was predicted once by a model that had not seen that student during training. Precision, recall and F1 are averaged equally over all <?=e(count($ds['classes']))?> careers (macro average).</p></div>
<div class="stat-row big">
<div class="stat"><small>Accuracy</small><strong><?=$pct($o['accuracy'])?></strong></div>
<div class="stat"><small>Precision</small><strong><?=$pct($o['macro']['precision'])?></strong></div>
<div class="stat"><small>Recall</small><strong><?=$pct($o['macro']['recall'])?></strong></div>
<div class="stat"><small>F1-score</small><strong><?=$pct($o['macro']['f1'])?></strong></div></div>
<p class="muted small">Accuracy per fold: <?=e(implode(', ', array_map(fn($f)=>number_format($f['accuracy']*100,1).'%', $m['folds'])))?> (average <?=$pct($o['fold_accuracy_mean'])?>, spread ±<?=number_format($o['fold_accuracy_std']*100,1)?> points).</p>
<div class="alert info"><strong>Important:</strong> these results are based only on the available dataset (<?=e($ds['rows'])?> rows) and cross-validation. A good score here does not guarantee that a prediction is right for a real student, or that the student will be suited to the career in the real world.</div>
</section>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">EXPLAINER</span><h2>What does this mean?</h2></div>
<div class="grid-2 tight">
<div class="explain"><h3>Accuracy</h3><p>Out of every 100 students in the test data, this is how many got the correct career. Simple to understand, but it can look better than it is if some careers are easier than others.</p></div>
<div class="explain"><h3>Precision</h3><p>When the model says "Data Analyst", how often is it right? High precision means few false alarms for that career.</p></div>
<div class="explain"><h3>Recall</h3><p>Of all the real Data Analysts, how many did the model find? High recall means the model rarely misses students of that career.</p></div>
<div class="explain"><h3>F1-score</h3><p>One number that balances precision and recall. It is only high when both are high.</p></div></div></section>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">PER CAREER</span><h2>Scores for each career</h2></div>
<div class="table-wrap"><table class="v2-table"><thead><tr><th>Career</th><th>Precision</th><th>Recall</th><th>F1-score</th><th>Students</th></tr></thead><tbody>
<?php foreach($m['per_class'] as $c): ?><tr><td><?=e($c['career'])?></td><td><?=$pct($c['precision'])?></td><td><?=$pct($c['recall'])?></td><td><?=$pct($c['f1'])?></td><td><?=e($c['support'])?></td></tr><?php endforeach; ?></tbody></table></div></section>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">CONFUSION MATRIX</span><h2>Where does the model get confused?</h2>
<p class="muted">Each row is the <strong>actual</strong> career, each column is the <strong>predicted</strong> career. The diagonal (outlined) shows correct predictions; any other number is a mistake. Darker green = more students.</p></div>
<?php $labels = $m['confusion_matrix']['labels']; $mx = $m['confusion_matrix']['matrix']; $max = 1; foreach($mx as $row) foreach($row as $v) $max = max($max, $v); ?>
<div class="table-wrap"><table class="cm"><thead><tr><th class="corner">Actual ↓ / Predicted →</th><?php foreach($labels as $i=>$l): ?><th title="<?=e($l)?>"><div class="rot"><?=e($l)?></div></th><?php endforeach; ?></tr></thead><tbody>
<?php foreach($mx as $i=>$row): ?><tr><th class="rowh"><?=e($labels[$i])?></th>
<?php foreach($row as $j=>$v): $a = $v ? 0.12 + 0.88 * $v / $max : 0; ?><td class="<?= $i===$j ? 'diag' : '' ?>" style="background:rgba(21,148,71,<?=round($a,2)?>);color:<?= $a > .55 ? '#fff' : '#173124' ?>" title="Actual <?=e($labels[$i])?> → predicted <?=e($labels[$j])?>: <?=e($v)?>"><?= $v ?: '' ?></td><?php endforeach; ?></tr><?php endforeach; ?></tbody></table></div></section>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">FEATURE IMPORTANCE</span><h2>Which skills matter most to the model?</h2>
<p class="muted">Higher = the Random Forest relied on this skill more when separating careers (model trained on the full dataset). This describes the model, not what makes a good professional.</p></div>
<?php $fi = $m['feature_importance']; $fmax = max(array_column($fi, 'importance')) ?: 1; ?>
<div class="skill-bars"><?php foreach($fi as $f): ?><div class="sbar"><span><?=e($f['skill'])?></span><div class="bar"><i style="width:<?=round($f['importance']/$fmax*100)?>%"></i></div><strong><?=number_format($f['importance']*100,1)?>%</strong></div><?php endforeach; ?></div></section>

<?php if(!empty($m['partial_profile_accuracy'])): ?>
<section class="v2-card"><div class="v2-head"><span class="eyebrow">LIMITATION</span><h2>What if only some skills are assessed?</h2>
<p class="muted">Students do not assess all 25 skills. To measure the effect, the test rows were repeated with only a random number of skills kept and the rest filled with dataset medians (the same method the website uses).</p></div>
<div class="table-wrap"><table class="v2-table"><thead><tr><th>Skills known</th><th>Accuracy</th></tr></thead><tbody>
<?php foreach($m['partial_profile_accuracy'] as $p): ?><tr><td><?=e($p['skills_known'])?> of <?=e(count($ds['features']))?></td><td><?=$pct($p['accuracy'])?></td></tr><?php endforeach; ?></tbody></table></div>
<p class="muted small">So predictions from just 5 assessed skills are much less reliable than predictions from many skills. NexPath asks for at least 5 skills, but assessing more gives a better result.</p></section>
<?php endif; ?>

<section class="v2-card"><div class="v2-head"><span class="eyebrow">LIMITATIONS</span><h2>Please read</h2></div>
<ul class="plain"><li>The dataset is small (<?=e($ds['rows'])?> students, about <?=e(round($ds['rows']/count($ds['classes'])))?> per career), so the numbers can move a lot if the data changes.</li>
<li>The scores measure how well the model reproduces the labels in its own dataset, not how well careers fit real people.</li>
<li>The "Model Score" shown on your result is a Random Forest vote share, not a real-world probability.</li>
<li>Skill tests are multiple-choice knowledge checks and cannot measure projects, creativity or on-the-job performance.</li></ul>
<p class="muted small">Regenerate these numbers any time with <code>python python/evaluate_model.py</code>.</p></section>
<?php endif; ?>
</main></body></html>
