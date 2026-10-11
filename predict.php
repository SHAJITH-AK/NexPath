<?php
require_once __DIR__ . '/auth_guard.php';
check_csrf();
$user_id = (int)$_SESSION['user_id'];

// Only genuinely assessed skills (valid 0-10 score) count. Source of truth = database, session as fallback.
$assessed = current_scores($user_id);

// v2 rule: at least MIN_SKILLS_REQUIRED (5) assessed skills - enforced on the server, not only in the browser.
if (count($assessed) < MIN_SKILLS_REQUIRED) {
    $_SESSION['prediction_notice'] = "Please complete at least " . MIN_SKILLS_REQUIRED . " skill assessments before generating your career prediction.";
    header("Location: prediction.php"); exit;
}

// Model input: assessed skills use their real score (0 is sent as 1 because the training data starts at 1).
// Skills that were NOT assessed are sent as null; python/predict.py fills them with the dataset median.
$features = [];
foreach (all_skill_names() as $skill) {
    $features[$skill] = isset($assessed[$skill]) ? max(1, min(10, $assessed[$skill])) : null;
}

$payload=json_encode(['features'=>$features], JSON_UNESCAPED_UNICODE);
$tmp=tempnam(sys_get_temp_dir(),'nexpath_').'.json';
file_put_contents($tmp,$payload);
$script=__DIR__.DIRECTORY_SEPARATOR.'python'.DIRECTORY_SEPARATOR.'predict.py';
$log=tempnam(sys_get_temp_dir(),'nexpath_log_').'.txt';
$command='python '.escapeshellarg($script).' '.escapeshellarg($tmp).' 2> '.escapeshellarg($log);
$output=shell_exec($command);
$logText=is_file($log)?trim((string)file_get_contents($log)):'';
@unlink($tmp); @unlink($log);
$data=json_decode(trim((string)$output),true);

if(!$data || empty($data['success'])){
    $message=$data['error'] ?? ($logText !== '' ? 'Python prediction failed: '.substr($logText,0,500) : 'Python prediction could not be completed. Check the Python installation and packages.');
    $_SESSION['prediction_error']=$message;
    header("Location: result.php?error=1"); exit;
}

$details = [
    'role'=>$data['role'],
    'confidence'=>$data['confidence'] ?? null,
    'top'=>$data['top'] ?? [['role'=>$data['role'],'score'=>round((float)($data['confidence'] ?? 0),1)]],
    'model'=>$data['model'] ?? 'Random Forest',
    'n_features'=>(int)($data['n_features'] ?? count($features)),
    'n_assessed'=>count($assessed),
    'assessed'=>$assessed,
    'created_at'=>date('Y-m-d H:i:s')
];

// Save to history (prepared statement). If upgrade_v2.sql has not been run yet, fall back to the original columns.
$details['id'] = null;
try {
    $conn=db();
    $role=$details['role']; $conf=$details['confidence']; $n=count($assessed);
    $scoresJson=json_encode($features);               // null = not assessed
    $detailsJson=json_encode($details, JSON_UNESCAPED_UNICODE);
    try {
        $stmt=$conn->prepare("INSERT INTO assessment_results (user_id, role, confidence, skills_assessed, scores_json, details_json) VALUES (?, ?, ?, ?, ?, ?)");
        $stmt->bind_param("isdiss",$user_id,$role,$conf,$n,$scoresJson,$detailsJson);
        $stmt->execute();
    } catch(Throwable $ex) {
        $stmt=$conn->prepare("INSERT INTO assessment_results (user_id, role, confidence, scores_json) VALUES (?, ?, ?, ?)");
        $stmt->bind_param("isds",$user_id,$role,$conf,$scoresJson);
        $stmt->execute();
    }
    $details['id']=$conn->insert_id;
    $stmt->close(); $conn->close();
} catch(Throwable $ex) { /* Prediction still works if history table is unavailable. */ }

$_SESSION['prediction']=$details;
header("Location: result.php"); exit;
?>
