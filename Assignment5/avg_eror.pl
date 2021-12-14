$mean = 0;
$data = shift;
$dir=$data."_std";
#$dir=$data;
for(my $i=0; $i<10; $i++){
  system("python least_squares_adaptive_eta.py $dir/$data.data $dir/$data.trainlabels.$i > nm_out.$data");
  $err[$i] = `perl error.pl $dir/$data.labels nm_out.$data`;
  chomp $err[$i];
  print "$err[$i]\n";
  $mean += $err[$i];
}
$mean /= 10;
$sd = 0;
for(my $i=0; $i<10; $i++){
  $sd += ($err[$i]-$mean)**2;
}
$sd /= 10;
$sd = sqrt($sd);
print "least_square error = $mean ($sd)\n";

#q^
$mean = 0;
for(my $i=0; $i<10; $i++){
  system("python hinge_adaptive_eta.py $dir/$data.data $dir/$data.trainlabels.$i > nb_out.$data");
  $err[$i] = `perl error.pl $dir/$data.labels nb_out.$data`;
  chomp $err[$i];
  print "$err[$i]\n";
  $mean += $err[$i];
 
}
$mean /= 10;
$sd = 0;
for(my $i=0; $i<10; $i++){
  $sd += ($err[$i]-$mean)**2;
}
$sd /= 10;
$sd = sqrt($sd);
print "hinge_loss error = $mean ($sd)\n";
#^if 0;

q^
$mean = 0;
for(my $i=0; $i<10; $i++){
  system("python3 perceptron.py $dir/$data.data $dir/$data.trainlabels.$i $eta $stop > p_out.$data");
  $err[$i] = `perl error.pl $dir/$data.labels p_out.$data`;
  print $err[$i];
  chomp $err[$i];
  $mean += $err[$i];
}
$mean /= 10;
$sd = 0;
for(my $i=0; $i<10; $i++){
  $sd += ($err[$i]-$mean)**2;
}
$sd /= 10;
$sd = sqrt($sd);
print "Perceptron (eta=$eta) error = $mean ($sd)\n";
if 0;


$mean = 0;
for(my $i=0; $i<10; $i++){
  system("python3 hinge.py $dir/$data.data $dir/$data.trainlabels.$i $eta $stop > p_out");
  $err[$i] = `perl error.pl $dir/$data.labels p_out`;
  print $err[$i];
  chomp $err[$i];
  $mean += $err[$i];
}
$mean /= 10;
$sd = 0;
for(my $i=0; $i<10; $i++){
  $sd += ($err[$i]-$mean)**2;
}
$sd /= 10;
$sd = sqrt($sd);
print "Hinge (eta=$eta) error = $mean ($sd)\n";
if 0;

$mean = 0;
for(my $i=0; $i<10; $i++){
  ##Create the training data and labels for SVM

  ##Obtain the cross-validated value of C
  $C = `perl cv-svm.pl data_cv labels_cv`;

  ##Predict with that value of C
  system("perl run_svm_light.pl $data.data $data.trainlabels.$i $C");
  $err[$i] = `perl error.pl $data.labels svmpredictions`;
  chomp $err[$i];
  $mean += $err[$i];
}
$mean /= 10;
$sd = 0;
for(my $i=0; $i<10; $i++){
  $sd += ($err[$i]-$mean)**2;
}
$sd /= 10;
$sd = sqrt($sd);
print "SVM error = $mean ($sd)\n";
if 0;
^

