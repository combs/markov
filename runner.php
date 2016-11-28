<?php
/*
    PHP Markov Chain text generator 1.0
    Copyright (c) 2008-2010, Hay Kranen <http://www.haykranen.nl/projects/markov/>
    Fork on Github: < http://github.com/hay/markov >
*/

require 'markov.php';

$outputDir = "/var/db/ngramradio/text/";
$filename = $argv[1];
foreach (range(1,20) as $order) {
    $destination = $outputDir . basename($argv[1],".txt") . "-" . $order . ".txt";
    echo ("Checking for $destination\n");
    if (file_exists($destination)==FALSE) {
      echo ("Does not exist.");
      $length = 250000;
      $text = file_get_contents($filename);
      $markov_table = generate_markov_table($text, $order);
      $markov = generate_markov_text($length, $markov_table, $order);
      file_put_contents($destination, $markov);
    }
    echo("Calling:\n");
    echo("python ngramaudio.py " . $outputDir . basename($argv[1],".txt") . "-" . $order . ".txt\n");
    system("python ngramaudio.py " . $outputDir . basename($argv[1],".txt") . "-" . $order . ".txt");
  }
