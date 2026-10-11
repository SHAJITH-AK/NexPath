<?php
require_once __DIR__ . '/auth_guard.php';

/* =========================
   NexPath Contact Form
   ========================= */
$db_host = "localhost";
$db_user = "root";
$db_pass = "";
$db_name = "nexpath_db";

$success = "";
$error = "";

/* Save submitted message to MySQL */
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    check_csrf();
    $name = trim($_POST["name"] ?? "");
    $email = trim($_POST["email"] ?? "");
    $message = trim($_POST["message"] ?? "");

    if ($name === "" || $email === "" || $message === "") {
        $error = "Please fill in all fields.";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error = "Please enter a valid email address.";
    } else {
        $conn = new mysqli($db_host, $db_user, $db_pass, $db_name);

        if ($conn->connect_error) {
            $error = "Database connection failed. Please check your XAMPP/MySQL setup.";
        } else {
            $conn->set_charset("utf8mb4");

            $stmt = $conn->prepare(
                "INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)"
            );

            if ($stmt) {
                $stmt->bind_param("sss", $name, $email, $message);

                if ($stmt->execute()) {
                    $success = "Your message has been sent successfully!";
                    $_POST = [];
                } else {
                    $error = "Unable to save your message. Please try again.";
                }

                $stmt->close();
            } else {
                $error = "Unable to prepare the database request.";
            }

            $conn->close();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact | NexPath</title>
    <link rel="stylesheet" href="css/contact.css">
</head>
<body>

<!-- Navigation -->
<nav class="navbar">
    <div class="nav-container">
        <a href="index.php" class="brand">
            <span class="brand-mark">N</span>
            <span>Nex<span>Path</span></span>
        </a>

        <div class="nav-links">
            <a href="main.php">Home</a>
            <a href="prediction.php">Prediction</a>
            <a href="jobs.html">Jobs</a>
            <a href="courses.html">Courses</a>
            <a href="aptitude.php">Aptitude Test</a>
            <a href="progress.php">Progress</a>
            <a href="about.html">About</a>
            <a href="contact.php" class="active">Contact</a>
            <a href="logout.php" class="logout-link">Log out</a>
        </div>
    </div>
</nav>

<!-- Hero -->
<section class="contact-hero">
    <div class="hero-content">
        <span class="eyebrow">NEXPATH • CONTACT</span>
        <h1>Let's build your<br><span>next path.</span></h1>
        <p>Have a question, suggestion, or feedback? Send us a message and we'll get back to you.</p>
    </div>
</section>

<!-- Contact Section -->
<section class="contact-section">
    <div class="section-heading">
        <span>GET IN TOUCH</span>
        <h2>We'd love to hear from you.</h2>
        <p>Reach out to NexPath or send a message using the form.</p>
    </div>

    <div class="contact-grid">

        <!-- Left: Contact information + map -->
        <div class="contact-info-card">
            <div class="card-heading">
                <span class="mini-label">CONTACT DETAILS</span>
                <h3>Connect with me</h3>
            </div>

            <div class="info-item">
                <div class="info-icon">✉</div>
                <div>
                    <small>Email</small>
                    <a href="mailto:shajith8047@gmail.com">shajith8047@gmail.com</a>
                </div>
            </div>

            <div class="info-item">
                <div class="info-icon">☎</div>
                <div>
                    <small>Phone</small>
                    <a href="tel:+917448966069">+91 74489 66069</a>
                </div>
            </div>

            <div class="info-item">
                <div class="info-icon">⌖</div>
                <div>
                    <small>Location</small>
                    <a
                        href="https://www.google.com/maps/search/?api=1&query=MEASI+Institute+of+Information+Technology"
                        target="_blank"
                        rel="noopener noreferrer">
                        MEASI Institute of Information Technology
                    </a>
                    <p>Chennai, Tamil Nadu</p>
                </div>
            </div>

            <div class="map-wrapper">
                <iframe
                    src="https://www.google.com/maps?q=MEASI+Institute+of+Information+Technology,+Chennai,+Tamil+Nadu&output=embed"
                    title="MEASI Institute of Information Technology location on Google Maps"
                    loading="lazy"
                    allowfullscreen>
                </iframe>
            </div>

            <a
                class="map-button"
                href="https://www.google.com/maps/search/?api=1&query=MEASI+Institute+of+Information+Technology"
                target="_blank"
                rel="noopener noreferrer">
                Open in Google Maps ↗
            </a>
        </div>

        <!-- Right: Message form -->
        <div class="form-card">
            <div class="card-heading">
                <span class="mini-label">SEND A MESSAGE</span>
                <h3>Tell me what's on your mind.</h3>
                <p>Your message will be securely saved in the NexPath database.</p>
            </div>

            <?php if ($success): ?>
                <div class="alert success-alert">
                    ✓ <?php echo htmlspecialchars($success); ?>
                </div>
            <?php endif; ?>

            <?php if ($error): ?>
                <div class="alert error-alert">
                    ! <?php echo htmlspecialchars($error); ?>
                </div>
            <?php endif; ?>

            <form method="POST" action="contact.php" class="contact-form">
                <input type="hidden" name="csrf_token" value="<?php echo e(csrf_token()); ?>">
                <div class="form-group">
                    <label for="name">Your Name</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        placeholder="Enter your name"
                        value="<?php echo htmlspecialchars($_POST["name"] ?? ""); ?>"
                        maxlength="100"
                        required>
                </div>

                <div class="form-group">
                    <label for="email">Email ID</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        placeholder="you@example.com"
                        value="<?php echo htmlspecialchars($_POST["email"] ?? ""); ?>"
                        maxlength="150"
                        required>
                </div>

                <div class="form-group">
                    <label for="message">Comment / Message</label>
                    <textarea
                        id="message"
                        name="message"
                        placeholder="Write your message here..."
                        maxlength="2000"
                        required><?php echo htmlspecialchars($_POST["message"] ?? ""); ?></textarea>
                </div>

                <button type="submit" class="send-button">
                    Send Message <span>→</span>
                </button>
            </form>
        </div>

    </div>
</section>

<!-- Footer -->
<footer class="footer">
    <div class="footer-inner">
        <div>
            <a href="index.php" class="footer-brand">Nex<span>Path</span></a>
            <p>Find the skills. Choose the path. Build the future.</p>
        </div>

        <div class="footer-contact">
            <a href="mailto:shajith8047@gmail.com">shajith8047@gmail.com</a>
            <a href="tel:+917448966069">+91 74489 66069</a>
        </div>
    </div>

    <div class="footer-bottom">
        <span>© 2026 NexPath. All Rights Reserved.</span>
        <span>Career Guidance Platform</span>
    </div>
</footer>

</body>
</html>
