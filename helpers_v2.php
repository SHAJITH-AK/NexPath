<?php
/* =====================================================================
   NexPath v2 helpers - loaded from config.php.
   Contains: career/skill-gap logic, attempt history, course lookup, formatting.
   ===================================================================== */

/** Career -> relevant skills -> target score. Editable file: data/career_config.json */
function career_config(): array {
    static $cfg = null;
    if ($cfg === null) {
        $file = __DIR__ . '/data/career_config.json';
        $cfg = is_file($file) ? (json_decode((string)file_get_contents($file), true) ?: []) : [];
    }
    return $cfg;
}

/** The 25 assessable skills = keys of the question bank. */
function all_skill_names(): array {
    static $names = null;
    if ($names === null) {
        $bank = json_decode((string)file_get_contents(__DIR__ . '/data/question_bank.json'), true) ?: [];
        $names = array_keys($bank);
    }
    return $names;
}

/** Keep only valid assessment scores: known skill name and a whole number from 0 to 10. */
function valid_scores(array $scores): array {
    $known = array_flip(all_skill_names());
    $out = [];
    foreach ($scores as $skill => $row) {
        $c = is_array($row) ? ($row['correct'] ?? null) : $row;
        if (isset($known[$skill]) && is_numeric($c) && (int)$c == $c && $c >= 0 && $c <= 10) {
            $out[$skill] = (int)$c;
        }
    }
    return $out;
}

/** Current (latest) score of every skill the user has assessed: skill => 0..10. Database first, session as fallback. */
function current_scores(int $user_id): array {
    $fromDb = valid_scores(load_skill_scores($user_id));
    if ($fromDb) {
        $_SESSION['assessment_scores'] = load_skill_scores($user_id); // keep session in sync
        return $fromDb;
    }
    return valid_scores($_SESSION['assessment_scores'] ?? []);
}

/** Stores one attempt in the history table. skill_scores keeps only the latest score. */
function record_attempt(int $user_id, string $skill, int $correct, int $percent): void {
    try {
        $conn = db();
        $stmt = $conn->prepare("INSERT INTO assessment_attempts (user_id, skill, correct, percent) VALUES (?, ?, ?, ?)");
        $stmt->bind_param("isii", $user_id, $skill, $correct, $percent);
        $stmt->execute();
        $stmt->close(); $conn->close();
    } catch (Throwable $ex) { /* history table missing (upgrade_v2.sql not run) - latest score is still saved */ }
}

/** All attempts of this user, oldest first: skill => [ ['correct'=>int,'at'=>string], ... ] */
function get_attempt_history(int $user_id): array {
    $out = [];
    try {
        $conn = db();
        $stmt = $conn->prepare("SELECT skill, correct, attempted_at FROM assessment_attempts WHERE user_id = ? ORDER BY attempted_at ASC, id ASC");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $res = $stmt->get_result();
        while ($r = $res->fetch_assoc()) {
            $out[$r['skill']][] = ['correct' => (int)$r['correct'], 'at' => $r['attempted_at']];
        }
        $stmt->close(); $conn->close();
    } catch (Throwable $ex) { }
    return $out;
}

/** Previous vs current score -> difference, label and CSS class. */
function improvement_info(int $previous, int $current): array {
    $diff = $current - $previous;
    if ($diff > 0)  return ['diff' => $diff, 'label' => 'Improved', 'class' => 'good', 'text' => '+' . $diff . ' point' . ($diff == 1 ? '' : 's')];
    if ($diff == 0) return ['diff' => 0, 'label' => 'No Change', 'class' => 'neutral', 'text' => '0 points'];
    return ['diff' => $diff, 'label' => 'Needs Improvement', 'class' => 'warn', 'text' => $diff . ' point' . ($diff == -1 ? '' : 's')];
}

/** Reads the existing Courses page (courses.html) so the roadmap reuses the SAME course list - no duplicate course data. */
function load_courses_from_html(): array {
    static $courses = null;
    if ($courses !== null) return $courses;
    $courses = [];
    $file = __DIR__ . '/courses.html';
    if (!is_file($file) || !class_exists('DOMDocument')) return $courses;
    $dom = new DOMDocument();
    libxml_use_internal_errors(true);
    $dom->loadHTML('<?xml encoding="UTF-8">' . file_get_contents($file));
    libxml_clear_errors();
    $xp = new DOMXPath($dom);
    foreach ($xp->query("//article[contains(concat(' ', normalize-space(@class), ' '), ' course-card ')]") as $card) {
        $key = $card->getAttribute('data-name');
        $title = $xp->query('.//h3', $card)->item(0);
        $learn = $xp->query(".//a[contains(@class,'learn-btn')]", $card)->item(0);
        $note  = $xp->query(".//small[contains(@class,'link-note')]", $card)->item(0);
        if ($key !== '' && $title && $learn) {
            $courses[$key] = ['title' => trim($title->textContent), 'url' => $learn->getAttribute('href'), 'provider' => $note ? trim($note->textContent) : ''];
        }
    }
    return $courses;
}

/**
 * Builds everything the result page needs from the predicted career + the student's ASSESSED scores.
 * $assessed contains ONLY skills that were really assessed (skill => 0..10). Unassessed skills are never given a score.
 */
function build_career_view(string $role, array $assessed): array {
    $cfg = career_config();
    $career = $cfg['careers'][$role] ?? ['description' => '', 'skills' => [], 'job_page' => ''];
    $margin = (int)($cfg['strong_margin'] ?? 1);
    $order = array_flip($cfg['skill_order'] ?? all_skill_names());
    $courses = load_courses_from_html();

    $relevant = $career['skills'];
    uksort($relevant, fn($a, $b) => ($order[$a] ?? 99) <=> ($order[$b] ?? 99));

    $gap = [];
    foreach ($relevant as $skill => $target) {
        $score = $assessed[$skill] ?? null;
        $status = $score === null ? 'not_assessed' : ($score >= $target - $margin ? 'strong' : 'improve');
        $gap[] = ['skill' => $skill, 'score' => $score, 'target' => (int)$target, 'status' => $status];
    }

    // Why this career: the student's best ASSESSED skills among the skills this career needs.
    $why = array_filter($gap, fn($g) => $g['score'] !== null);
    usort($why, fn($a, $b) => $b['score'] <=> $a['score']);
    $why = array_slice($why, 0, 5);

    // Strong skills: highest scoring assessed skills overall (7/10 or more).
    $strong = [];
    foreach ($assessed as $skill => $score) if ($score >= 7) $strong[] = ['skill' => $skill, 'score' => $score, 'relevant' => isset($relevant[$skill])];
    usort($strong, fn($a, $b) => $b['score'] <=> $a['score']);
    $strong = array_slice($strong, 0, 6);

    $improve = array_values(array_filter($gap, fn($g) => $g['status'] === 'improve'));
    usort($improve, fn($a, $b) => ($b['target'] - $b['score']) <=> ($a['target'] - $a['score']));
    $notAssessed = array_values(array_filter($gap, fn($g) => $g['status'] === 'not_assessed'));
    $strongRelevant = array_values(array_filter($gap, fn($g) => $g['status'] === 'strong'));

    // Learning roadmap: relevant skills in learning order, each linked to a course that already exists on the Courses page.
    $steps = []; $keys = []; $needKeys = [];
    foreach ($gap as $g) {
        $res = ['title' => '', 'url' => '', 'note' => '', 'key' => ''];
        $sc = $cfg['skill_courses'][$g['skill']] ?? null;
        $sl = $cfg['skill_links'][$g['skill']] ?? null;
        if ($sc && isset($courses[$sc['course']])) {
            $c = $courses[$sc['course']];
            $res = ['title' => $c['title'], 'url' => $c['url'], 'provider' => $c['provider'], 'key' => $sc['course'],
                    'note' => !empty($sc['closest']) ? 'Closest course available on NexPath' : ''];
        } elseif ($sl) {
            $res = ['title' => $sl['title'], 'url' => $sl['link'], 'provider' => 'NexPath', 'key' => '', 'note' => ''];
        }
        if ($res['key'] !== '') { $keys[$res['key']] = true; if ($g['status'] !== 'strong') $needKeys[$res['key']] = true; }
        $steps[] = $g + ['resource' => $res];
    }
    $courseKeys = array_keys($needKeys ?: $keys);
    $coursesUrl = 'courses.html?path=' . rawurlencode($role) . ($courseKeys ? '&courses=' . rawurlencode(implode('|', $courseKeys)) : '');

    return ['description' => $career['description'], 'job_page' => $career['job_page'], 'why' => $why, 'strong' => $strong,
            'improve' => $improve, 'not_assessed' => $notAssessed, 'strong_relevant' => $strongRelevant,
            'gap' => $gap, 'roadmap' => $steps, 'courses_url' => $coursesUrl, 'configured' => !empty($career['skills'])];
}

/** "2026-09-29 18:30:00" -> "29 Sep 2026" */
function fmt_date($ts, bool $withTime = false): string {
    $t = strtotime((string)$ts);
    if (!$t) return '';
    return date($withTime ? 'd M Y, H:i' : 'd M Y', $t);
}

/** Seconds -> "07:42" */
function fmt_duration(int $sec): string {
    $sec = max(0, $sec);
    return sprintf('%02d:%02d', intdiv($sec, 60), $sec % 60);
}

/** Shared top navigation for the new / rewritten pages. */
function nav_v2(string $active = ''): void {
    $items = ['home' => ['main.php', 'Home'], 'prediction' => ['prediction.php', 'Prediction'], 'jobs' => ['jobs.html', 'Jobs'],
              'courses' => ['courses.html', 'Courses'], 'aptitude' => ['aptitude.php', 'Aptitude Test'], 'progress' => ['progress.php', 'Progress'],
              'about' => ['about.html', 'About'], 'contact' => ['contact.php', 'Contact']];
    echo '<header class="topbar"><a class="brand" href="main.php"><b>N</b>Nex<span>Path</span></a><nav>';
    foreach ($items as $key => [$href, $label]) {
        echo '<a href="' . $href . '"' . ($key === $active ? ' class="active"' : '') . '>' . $label . '</a>';
    }
    echo '<a class="logout" href="logout.php">Log out</a></nav></header>';
}
