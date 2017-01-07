<?php
/*
    PHP Markov Chain text generator 1.0
    Copyright (c) 2008-2010, Hay Kranen <http://www.haykranen.nl/projects/markov/>
    Fork on Github: < http://github.com/hay/markov >
*/

require 'markov.php';

ini_set('memory_limit','1G');

$outputDir = "/var/db/ngramradio/text/";
$filename = $argv[1];
if (!$filename) {
   exit("Must provide filename.\n");
 }
$algorithm = $argv[2];
if (!$algorithm) {
  $algorithm = null;
}
$length = $argv[3] ;
if (!$length) {
  $length = 25000;
}
$orders = $argv[4] ;
if (!$orders) {
  $orders = range(1,20);
} else {
  $orders = explode(",",$argv[4]);
}

if (file_exists($filename)==FALSE) {
  echo ("$filename does not exist.");
  exit;
}

foreach ($orders as $order) {
    $destination = $outputDir . basename($argv[1],".txt") . "-" . $order . "-" . $length . ".txt";
    echo ("Checking for $destination\n");

    if (file_exists($destination)==FALSE) {
      echo ("$destination is not yet generated.");
      $text = file_get_contents($filename);
      $markov_table = generate_markov_table($text, $order);
      $markov = generate_markov_text($length, $markov_table, $order);
      file_put_contents($destination, $markov);
    }
    echo("Calling:\n");
    $command = "python2.7 ngramaudio.py ";
    if ($algorithm) {
      $command .= "-a $algorithm ";
    }
    $command .= $destination . "\n";
    echo($command);
    passthru($command);
  }
