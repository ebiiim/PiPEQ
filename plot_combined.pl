#!/usr/bin/perl -w

print STDERR "WARNING: No sanitization of the input is done at all. A malicious external user (e.g., via a web form) can easily compromise your system.\n";

sub usage() {
	print STDERR "Usage: $0 [sampling_rate] \"effect1 effargs1\" " .
		"\"effect2 effargs2\" ...\n";
	print STDERR "Plots the combined amplitude response of biquad-based " .
		"effects.\n";
	print STDERR "Biquad-based effects are: highpass, lowpass, " .
		"bandpass, bandreject, allpass,\n" . "bass, treble, " .
		"equalizer, band, deemph, riaa, biquad.\n";
	exit(1);
}

usage() if $#ARGV == -1;

my $rate = 48000;
$rate = shift   if $ARGV[0] =~ /^\d+$/ && $ARGV[0] != 0;
usage() if $#ARGV == -1;

my $desc = join(" ", @ARGV);

print <<END;
# gnuplot file
set title 'SoX effects: $desc (rate=$rate)'
set xlabel 'Frequency (Hz)'
set ylabel 'Amplitude Response (dB)'
Fs=$rate
o=2*pi/Fs
set logscale x
set grid xtics ytics
set key off
END

my $l = 0;
foreach (@ARGV) {
	$l++;
	$_ = `sox --plot=gnuplot --rate $rate -n -n $_ | sed -n -e '6 p'`;
	s/([ab][012])/$1_$l/g;
	print;
	print "H_$l(f)=sqrt((b0_$l*b0_$l+b1_$l*b1_$l+b2_$l*b2_$l+2.*(b0_$l*b1_$l+b1_$l*b2_$l)*cos(f*o)+2.*(b0_$l*b2_$l)*cos(2.*f*o))/(1.+a1_$l*a1_$l+a2_$l*a2_$l+2.*(a1_$l+a1_$l*a2_$l)*cos(f*o)+2.*a2_$l*cos(2.*f*o)))\n";
}

my $prod = join("*", map { "H_$_(f)" } (1..$l));
print "H(f)=$prod\n";

print <<END;
plot [f=10:Fs/2] [-35:25] 20*log10(H(f))
pause -1 'Hit return to continue'
END
