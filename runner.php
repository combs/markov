<?php
/*
    PHP Markov Chain text generator 1.0
    Copyright (c) 2008-2010, Hay Kranen <http://www.haykranen.nl/projects/markov/>
    Fork on Github: < http://github.com/hay/markov >
*/

require 'markov.php';

$outputDir = "/var/db/ngramradio/text/";

foreach (range(1,20) as $order) {
    $length = 250000;
    $text = file_get_contents($argv[1]);
    $markov_table = generate_markov_table($text, $order);
    $markov = generate_markov_text($length, $markov_table, $order);
    file_put_contents($outputDir . basename($argv[1],".txt") . "-" . $order . ".txt", $markov);
  }
