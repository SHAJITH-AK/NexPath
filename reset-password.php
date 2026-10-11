<?php
session_start();
require_once __DIR__ . '/config.php';

if (empty($_SESSION['reset_email']) || empty($_SESSION['reset_token'])) {
    header("Location: forgot-password.html"); exit;
}
$error = "";
$done = false;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    check_csrf();
    $password = $_POST['password'] ?? "";
    $confirm = $_POST['confirm_password'] ?? "";
    if (strlen($password) < 6) $error = "Password must contain at least 6 characters.";
    elseif ($password !== $confirm) $error = "Passwords do not match.";
    else {
        try {
            $conn = db();
            $hash = password_hash($password, PASSWORD_DEFAULT);
            $stmt = $conn->prepare("UPDATE users SET password=? WHERE email=?");
            $stmt->bind_param("ss", $hash, $_SESSION['reset_email']);
            $stmt->execute();
            $stmt->close(); $conn->close();
            unset($_SESSION['reset_email'], $_SESSION['reset_token']);
            $done = true;
        } catch (Throwable $ex) { $error = "Could not update the password."; }
    }
}
?>
<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Reset Password - NexPath</title><link rel="stylesheet" href="css/auth-pages.css"></head><body>
<div class="auth-page"><div class="auth-box"><div class="logo"><span>Nex</span>Path</div>
<?php if ($done): ?>
<h1>Password Updated</h1><p class="subtitle">Your password has been changed for this local NexPath project.</p>
<p class="bottom-text"><a href="index.php">Back to Login</a></p>
<?php else: ?>
<h1>Reset Password</h1><p class="subtitle">Local development reset for the verified account.</p>
<?php if ($error): ?><div class="info-box"><?=e($error)?></div><?php endif; ?>
<form method="POST"><input type="hidden" name="csrf_token" value="<?=e(csrf_token())?>">
<div class="input-group"><label for="password">New Password</label><input id="password" name="password" type="password" minlength="6" required></div>
<div class="input-group"><label for="confirm_password">Confirm Password</label><input id="confirm_password" name="confirm_password" type="password" minlength="6" required></div>
<button type="submit">Update Password</button></form>
<p class="bottom-text"><a href="index.php">← Back to Login</a></p>
<?php endif; ?></div></div></body></html>