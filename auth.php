<?php
session_start();
require_once __DIR__ . '/config.php';

function result_page(string $title, string $message, string $back = "index.php"): never {
    echo '<!doctype html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>NexPath</title><link rel="stylesheet" href="css/auth-pages.css"></head><body>
    <div class="auth-page"><div class="auth-box"><div class="logo"><span>Nex</span>Path</div>
    <h1>'.e($title).'</h1><p class="subtitle">'.e($message).'</p>
    <p class="bottom-text"><a href="'.e($back).'">Continue</a></p></div></div></body></html>';
    exit;
}

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: index.html"); exit;
}

$action = $_POST["action"] ?? "";

try {
    $conn = db();

    if ($action === "signup") {
        $name = trim($_POST["name"] ?? "");
        $email = trim($_POST["email"] ?? "");
        $password = $_POST["password"] ?? "";
        $confirm = $_POST["confirm_password"] ?? "";

        if ($name === "" || $email === "" || $password === "" || $confirm === "") result_page("Missing Details", "Please fill in all required fields.", "signup.html");
        if (mb_strlen($name) > 100) result_page("Invalid Name", "Your name is too long.", "signup.html");
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) result_page("Invalid Email", "Please enter a valid email address.", "signup.html");
        if (strlen($password) < 6) result_page("Weak Password", "Password must contain at least 6 characters.", "signup.html");
        if ($password !== $confirm) result_page("Password Mismatch", "The passwords do not match.", "signup.html");

        $check = $conn->prepare("SELECT id FROM users WHERE email = ?");
        $check->bind_param("s", $email);
        $check->execute();
        $check->store_result();
        if ($check->num_rows > 0) {
            $check->close(); $conn->close();
            result_page("Account Already Exists", "An account with this email already exists.", "index.php");
        }
        $check->close();

        $hash = password_hash($password, PASSWORD_DEFAULT);
        $stmt = $conn->prepare("INSERT INTO users (name, email, password) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $name, $email, $hash);
        if (!$stmt->execute()) {
            $stmt->close(); $conn->close();
            result_page("Sign Up Failed", "The account could not be created.", "signup.html");
        }
        $stmt->close(); $conn->close();
        result_page("Account Created", "Your NexPath account is ready. Please sign in.", "index.php");
    }

    if ($action === "login") {
        $email = trim($_POST["email"] ?? "");
        $password = $_POST["password"] ?? "";

        // Only require that something was typed (older accounts may not use a strictly valid e-mail format).
        if ($email === "" || $password === "") result_page("Invalid Login", "Please enter your email address and password.", "index.php");

        // Case-insensitive e-mail lookup so "User@Mail.com" and "user@mail.com" are the same account.
        $stmt = $conn->prepare("SELECT id, name, email, password FROM users WHERE LOWER(email) = LOWER(?) LIMIT 1");
        $stmt->bind_param("s", $email); $stmt->execute(); $stmt->store_result();

        if ($stmt->num_rows !== 1) {
            $stmt->close(); $conn->close();
            result_page("Login Failed", "Email address or password is incorrect.", "index.php");
        }
        $stmt->bind_result($id, $name, $dbEmail, $hash); $stmt->fetch();
        $stmt->close();

        // Accept modern password_hash() hashes AND older accounts whose password was saved
        // as plain text / md5 / sha1 / sha256. Old-style passwords are upgraded to a secure hash on first login.
        $ok = false; $needsRehash = false;
        if (password_verify($password, $hash)) {
            $ok = true;
            $needsRehash = password_needs_rehash($hash, PASSWORD_DEFAULT);
        } elseif (password_get_info($hash)['algo'] === null) {
            $h = (string)$hash;
            if (hash_equals($h, $password)
                || hash_equals(strtolower($h), md5($password))
                || hash_equals(strtolower($h), sha1($password))
                || hash_equals(strtolower($h), hash('sha256', $password))) {
                $ok = true; $needsRehash = true;
            }
        }

        if (!$ok) {
            $conn->close();
            result_page("Login Failed", "Email address or password is incorrect.", "index.php");
        }

        if ($needsRehash) {
            $newHash = password_hash($password, PASSWORD_DEFAULT);
            $up = $conn->prepare("UPDATE users SET password = ? WHERE id = ?");
            $up->bind_param("si", $newHash, $id); $up->execute(); $up->close();
        }
        $conn->close();

        session_regenerate_id(true);
        $_SESSION["user_id"] = (int)$id;
        $_SESSION["user_name"] = $name;
        $_SESSION["user_email"] = $dbEmail;
        unset($_SESSION['prediction']);

        // Restore this user's previously completed skill scores from the
        // database so progress carries over between logins/sessions.
        $_SESSION['assessment_scores'] = load_skill_scores((int)$id);

        header("Location: main.php"); exit;
    }

    if ($action === "forgot") {
        $email = trim($_POST["email"] ?? "");
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) result_page("Invalid Email", "Please enter a valid email address.", "forgot-password.html");

        $stmt = $conn->prepare("SELECT id FROM users WHERE email = ?");
        $stmt->bind_param("s", $email); $stmt->execute(); $stmt->store_result();
        $exists = $stmt->num_rows === 1; $stmt->close(); $conn->close();

        if ($exists) {
            $_SESSION['reset_email'] = $email;
            $_SESSION['reset_token'] = bin2hex(random_bytes(32));
            header("Location: reset-password.php"); exit;
        }
        result_page("Account Not Found", "No NexPath account was found for that email address.", "forgot-password.html");
    }

    result_page("Invalid Request", "The requested authentication action is not available.");
} catch (Throwable $ex) {
    result_page("System Error", "Please make sure MySQL is running and db/nexpath_database.sql is imported. Details: " . $ex->getMessage());
}
?>