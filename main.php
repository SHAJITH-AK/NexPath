<?php session_start(); if (empty($_SESSION["user_id"])) { header("Location: index.html"); exit; } ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexPath | Your Career, Your Path</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

    <!-- Navigation -->
    <header class="navbar">
        <a href="index.php" class="logo">
            <span class="logo-mark">N</span>
            <span>Nex<span>Path</span></span>
        </a>

        <nav class="nav-links">
            <a href="main.php" class="active">Home</a>
            <a href="prediction.php">Prediction</a>
            <a href="jobs.html">Jobs</a>
            <a href="courses.html">Courses</a>
            <a href="aptitude.php">Aptitude Test</a>
            <a href="progress.php">Progress</a>
            <a href="about.html">About</a>
            <a href="contact.php">Contact</a>
        </nav>

        <a href="logout.php" class="logout-btn">Log out</a>
    </header>

    <!-- Hero Section -->
    <main>
        <section class="hero">
            <div class="hero-content">
                <span class="eyebrow">SMARTER CAREER DECISIONS</span>

                <h1>Find the path that<br><span>fits your future.</span></h1>

                <p>
                    NexPath helps students discover suitable career paths,
                    explore job opportunities, and find courses to build
                    the skills they need.
                </p>

                <div class="hero-buttons">
                    <a href="prediction.php" class="primary-btn">Start Prediction <span>→</span></a>
                    <a href="#explore" class="secondary-btn">Explore NexPath</a>
                </div>

                <div class="trust-row">
                    <div class="trust-item">
                        <strong>AI</strong>
                        <span>Career Guidance</span>
                    </div>
                    <div class="divider"></div>
                    <div class="trust-item">
                        <strong>100+</strong>
                        <span>Career Resources</span>
                    </div>
                    <div class="divider"></div>
                    <div class="trust-item">
                        <strong>1</strong>
                        <span>Personalized Path</span>
                    </div>
                </div>
            </div>

            <div class="hero-visual">
                <div class="image-card">
                    <!-- Unsplash image: free to use under the Unsplash License -->
                    <img
                        src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1000&q=85"
                        alt="Students working together on career and technology projects">
                </div>

                <div class="floating-card prediction-card">
                    <div class="mini-icon">✦</div>
                    <div>
                        <small>Your next step</small>
                        <strong>Career Prediction</strong>
                    </div>
                </div>

                <div class="floating-card progress-card">
                    <div class="progress-circle">AI</div>
                    <div>
                        <small>Career match</small>
                        <strong>Strong Match</strong>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features -->
        <section class="features-section" id="explore">
            <div class="section-heading">
                <span class="eyebrow">EXPLORE NEXPATH</span>
                <h2>Everything you need to move forward.</h2>
                <p>From discovering your direction to building the skills for it.</p>
            </div>

            <div class="feature-grid">
                <a href="prediction.php" class="feature-card">
                    <div class="feature-icon">⌁</div>
                    <div>
                        <h3>Career Prediction</h3>
                        <p>Answer a few questions and discover career paths that match your interests and skills.</p>
                        <span class="card-link">Predict my path →</span>
                    </div>
                </a>

                <a href="jobs.html" class="feature-card">
                    <div class="feature-icon">↗</div>
                    <div>
                        <h3>Find Jobs</h3>
                        <p>Explore relevant job roles and understand what skills employers are looking for.</p>
                        <span class="card-link">Explore jobs →</span>
                    </div>
                </a>

                <a href="courses.html" class="feature-card">
                    <div class="feature-icon">▣</div>
                    <div>
                        <h3>Learn Skills</h3>
                        <p>Discover useful courses and learning resources to prepare for your chosen career.</p>
                        <span class="card-link">View courses →</span>
                    </div>
                </a>
            </div>
        </section>

        <!-- CTA -->
        <section class="cta-section">
            <div>
                <span class="eyebrow">YOUR FUTURE STARTS HERE</span>
                <h2>Not sure where to go next?</h2>
                <p>Let NexPath help you turn your interests into a clear career direction.</p>
            </div>
            <a href="prediction.php" class="primary-btn light-btn">Get My Career Path <span>→</span></a>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-brand">
            <a href="index.php" class="logo">
                <span class="logo-mark">N</span>
                <span>Nex<span>Path</span></span>
            </a>
            <p>Discover. Learn. Grow.</p>
        </div>

        <div class="footer-links">
            <a href="about.html">About</a>
            <a href="model-performance.php">Model Performance</a>
            <a href="contact.php">Contact</a>
            <a href="logout.php">Log out</a>
        </div>

        <p class="copyright">© 2026 NexPath. All rights reserved.</p>
    </footer>

</body>
</html>
