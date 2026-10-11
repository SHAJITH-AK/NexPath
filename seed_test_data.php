<?php
/* NexPath - one-click test data loader (local XAMPP only).
   Open http://localhost/NexPath/seed_test_data.php once. It runs db/test_data.sql, which only
   touches the 3 test accounts (test@, demo@, full@nexpath.com) and never your real users. */
require_once __DIR__ . '/config.php';

if (!in_array($_SERVER['REMOTE_ADDR'] ?? '', ['127.0.0.1', '::1'], true)) {
    http_response_code(403); exit('This page can only be opened on the local machine.');
}

$msg = ''; $ok = false;
try {
    mysqli_report(MYSQLI_REPORT_OFF);
    $conn = new mysqli($db_host, $db_user, $db_pass, $db_name);
    if ($conn->connect_error) throw new Exception('Cannot connect to MySQL / database "' . $db_name . '". Start MySQL and import db/nexpath_database.sql first.');
    $conn->set_charset('utf8mb4');
    $sql = file_get_contents(__DIR__ . '/db/test_data.sql');
    if (!$conn->multi_query($sql)) throw new Exception($conn->error);
    do { if ($r = $conn->store_result()) $r->free(); } while ($conn->more_results() && $conn->next_result());
    if ($conn->errno) throw new Exception($conn->error . ' (did you import db/upgrade_v2.sql first?)');
    $ok = true; $msg = 'Test data loaded.';
    $conn->close();
} catch (Throwable $ex) { $msg = $ex->getMessage(); }
?><!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NexPath test data</title><link rel="stylesheet" href="css/auth-pages.css"></head><body>
<div class="auth-page"><div class="auth-box"><div class="logo"><span>Nex</span>Path</div>
<h1><?= $ok ? 'Test data ready' : 'Could not load test data' ?></h1>
<p class="subtitle"><?= e($msg) ?></p>
<?php if ($ok): ?>
<div class="info-box">
<b>test@nexpath.com</b> / Test@123 &mdash; 10 skills, retests, 2 predictions<br>
<b>demo@nexpath.com</b> / Demo@123 &mdash; 3 skills (prediction locked)<br>
<b>full@nexpath.com</b> / Full@123 &mdash; all 25 skills
</div>
<?php endif; ?>
<p class="bottom-text"><a href="index.php">Go to Login</a></p></div></div></body></html>
