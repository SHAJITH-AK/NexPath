<?php
require_once __DIR__ . '/auth_guard.php';
check_csrf();
$current = $_SESSION['current_assessment'] ?? null;
if (!$current || empty($current['questions'])) { header("Location: prediction.php"); exit; }

$answers = $_POST['answer'] ?? [];
if (!is_array($answers) || count($answers) !== 10 || array_keys($answers) !== range(0, 9)) {
    exit("Please answer all 10 questions before submitting.");
}
$correct=0;
foreach ($current['questions'] as $i=>$q) {
    if (isset($answers[$i]) && is_string($answers[$i]) && hash_equals($q['answer'], $answers[$i])) $correct++;
}
$percent=$correct*10;
$skill=$current['skill'];
$user_id=(int)$_SESSION['user_id'];
if (!isset($_SESSION['assessment_scores'])) $_SESSION['assessment_scores']=[];

// v2: remember the previous result of this skill so the retest improvement can be shown.
$previous = isset($_SESSION['assessment_scores'][$skill]) ? (int)$_SESSION['assessment_scores'][$skill]['correct'] : null;

$_SESSION['assessment_scores'][$skill]=[
    'correct'=>$correct,'percent'=>$percent,'completed_at'=>date('Y-m-d H:i:s')
];

// Persist: latest score (skill_scores) + a NEW history row (assessment_attempts). Old attempts are never overwritten.
save_skill_score($user_id, $skill, $correct, $percent);
record_attempt($user_id, $skill, $correct, $percent);

if ($previous !== null) {
    $_SESSION['flash_retest'] = ['skill'=>$skill, 'previous'=>$previous, 'current'=>$correct];
}

unset($_SESSION['current_assessment']);
header("Location: prediction.php");
exit;
?>
