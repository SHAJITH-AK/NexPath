<?php
/* Aptitude topic catalogue: slug => [category, name, icon, description].
   The slug must match the `topic` column of aptitude_questions. Edit this file to rename/describe topics. */
const APT_CATEGORIES = [
    'Numerical Ability' => 'Calculation speed and number sense for placement tests.',
    'Logical Reasoning' => 'Patterns, deductions and puzzles that test clear thinking.',
    'Verbal Ability'    => 'Vocabulary, grammar and comprehension for English sections.',
];
const APT_QUESTIONS_PER_TEST = 10;   // each test picks this many random questions (or fewer if the topic has fewer)
const APT_SECONDS_PER_QUESTION = 60; // 10 questions = 10 minutes

function apt_topics(): array {
    return [
    'number-system'       => ['Numerical Ability', 'Number System', '№', 'Practice HCF, LCM, remainders, divisibility and unit digits.'],
    'percentages'         => ['Numerical Ability', 'Percentages', '%', 'Practice percentage-based aptitude questions.'],
    'profit-and-loss'     => ['Numerical Ability', 'Profit and Loss', '₹', 'Cost price, selling price, discounts and overall profit or loss.'],
    'ratio-and-proportion'=> ['Numerical Ability', 'Ratio and Proportion', '∶', 'Dividing amounts, comparing quantities and mixtures.'],
    'averages'            => ['Numerical Ability', 'Averages', 'x̄', 'Averages, missing values and replacements in groups.'],
    'simple-interest'     => ['Numerical Ability', 'Simple Interest', 'SI', 'Interest, rate, time and principal under simple interest.'],
    'compound-interest'   => ['Numerical Ability', 'Compound Interest', 'CI', 'Compound interest, amounts and the CI-SI difference.'],
    'time-and-work'       => ['Numerical Ability', 'Time and Work', '⏱', 'Combined work, efficiency, pipes and tanks.'],
    'time-speed-distance' => ['Numerical Ability', 'Time, Speed and Distance', '➜', 'Speed, relative motion, trains and boats.'],
    'problems-on-ages'    => ['Numerical Ability', 'Problems on Ages', '⌛', 'Present, past and future age relationships.'],
    'probability'         => ['Numerical Ability', 'Probability', 'P', 'Coins, dice, cards and balls in a bag.'],
    'permutation-combination' => ['Numerical Ability', 'Permutation and Combination', 'nCr', 'Arrangements, selections and counting methods.'],
    'algebra'             => ['Numerical Ability', 'Algebra', 'x²', 'Linear and quadratic equations and identities.'],
    'geometry'            => ['Numerical Ability', 'Geometry', '△', 'Angles, triangles, polygons and right triangles.'],
    'mensuration'         => ['Numerical Ability', 'Mensuration', '▭', 'Area, perimeter and volume of common shapes.'],
    'data-interpretation' => ['Numerical Ability', 'Data Interpretation', '▤', 'Answer questions from small data tables.'],
    'number-series'       => ['Logical Reasoning', 'Number Series', '1·2·3', 'Find the missing number in a pattern.'],
    'letter-series'       => ['Logical Reasoning', 'Letter Series', 'A·B·C', 'Spot patterns in letters and alphabet positions.'],
    'coding-decoding'     => ['Logical Reasoning', 'Coding-Decoding', '⌗', 'Decode letter and word codes.'],
    'blood-relations'     => ['Logical Reasoning', 'Blood Relations', '♡', 'Work out family relationships from clues.'],
    'direction-sense'     => ['Logical Reasoning', 'Direction Sense', '⌖', 'Turns, distances and final directions.'],
    'syllogism'           => ['Logical Reasoning', 'Syllogism', '∴', 'Decide which conclusions follow from statements.'],
    'seating-arrangement' => ['Logical Reasoning', 'Seating Arrangement', '▥', 'Rows, queues and circular arrangements.'],
    'venn-diagrams'       => ['Logical Reasoning', 'Venn Diagrams', '◎', 'Sets, overlaps and relationship diagrams.'],
    'statements-conclusions' => ['Logical Reasoning', 'Statements and Conclusions', '❝', 'Judge which conclusions follow from a statement.'],
    'data-sufficiency'    => ['Logical Reasoning', 'Data Sufficiency', '⊨', 'Decide whether the given information is enough.'],
    'logical-puzzles'     => ['Logical Reasoning', 'Logical Puzzles', '✱', 'Classic puzzles and calendar problems.'],
    'vocabulary'          => ['Verbal Ability', 'Vocabulary', 'Aa', 'Word meanings, idioms and one-word substitutions.'],
    'synonyms'            => ['Verbal Ability', 'Synonyms', '＝', 'Choose the word closest in meaning.'],
    'antonyms'            => ['Verbal Ability', 'Antonyms', '≠', 'Choose the word opposite in meaning.'],
    'grammar'             => ['Verbal Ability', 'Grammar', 'Gr', 'Tenses, agreement, prepositions and articles.'],
    'sentence-correction' => ['Verbal Ability', 'Sentence Correction', '✎', 'Pick the grammatically correct sentence.'],
    'reading-comprehension' => ['Verbal Ability', 'Reading Comprehension', '❡', 'Read a short passage and answer questions.'],
    'sentence-completion' => ['Verbal Ability', 'Sentence Completion', '…', 'Choose the word that completes the sentence.'],
    ];
}
