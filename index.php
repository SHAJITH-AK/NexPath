<?php session_start(); if (!empty($_SESSION["user_id"])) { header("Location: main.php"); exit; } ?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NexPath | Login</title>
<link rel="stylesheet" href="css/index.css">
</head>
<body>
<div class="page">
    <div class="visual">
        <div class="visual-content">
            <a href="index.php" class="brand"><b>N</b>Nex<span>Path</span></a>
            <div class="hero-copy">
                <small>YOUR CAREER. YOUR PATH.</small>
                <h1>Turn career<br><span>confusion</span> into<br>direction.</h1>
                <p>Discover suitable career paths, explore jobs and build the skills you need with NexPath.</p>
            </div>
            <div class="visual-bottom">
                <span>Career Prediction</span><span>Jobs</span><span>Courses</span>
            </div>
        </div>
    </div>

    <main class="login-area">
        <div class="login-card">
            <div class="mobile-brand">
                <a href="index.php" class="brand"><b>N</b>Nex<span>Path</span></a>
            </div>

            <div class="heading">
                <small>WELCOME BACK</small>
                <h2>Sign in to NexPath</h2>
                <p>Continue your journey toward the right career.</p>
            </div>

            <form action="auth.php" method="POST">
                <input type="hidden" name="action" value="login">

                <label for="email">Email address</label>
                <input id="email" name="email" type="email" placeholder="you@example.com" autocomplete="email" required>

                <div class="password-label">
                    <label for="password">Password</label>
                    <a href="forgot-password.html">Forgot password?</a>
                </div>
                <input id="password" name="password" type="password" placeholder="Enter your password" autocomplete="current-password" required>

                <button type="submit">Sign In <span>→</span></button>
            </form>

            <div class="divider"><span>or</span></div>

            <p class="signup">Don't have an account? <a href="signup.html">Create an account</a></p>

            <p class="secure">Your account information is protected and validated securely.</p>
        </div>
    </main>
</div>
</body>
</html>