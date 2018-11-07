#!/usr/bin/perl -w

# Forked from Ulrich Klauer's plot_combined.pl https://sourceforge.net/p/sox/feature-requests/162/

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
# set term pdfcairo enhanced size 8in, 3in
set term pngcairo enhanced size 480, 160
# set title 'SoX effects: $desc (rate=$rate)'
set xlabel 'Frequency (Hz)'
# set ylabel 'Amplitude Response (dB)'
set ylabel 'Gain (dB)'
Fs=$rate
o=2*pi/Fs
set logscale x
set grid xtics ytics
# set xtics (20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, "1k" 1000, "1k25" 1250, "1k6" 1600, "2k" 2000, "2k5" 2500, "3k15" 3150, "4k" 4000, "5k" 5000, "6k3" 6300, "8k" 8000, "10k" 10000, "12k5" 12500, "16k" 16000, "20k" 20000)
# set ytics -15, 3, 15
set xtics (20, 31.5, 50, 80, 125, 200, 315, 500, 800, "1k25" 1250, "2k" 2000, "3k15" 3150, "5k" 5000, "8k" 8000, "12k5" 12500, "20k" 20000)
set ytics -15, 6, 15

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
# plot [f=10:Fs/2] [-35:25] 20*log10(H(f))
# plot [f=20:20000] [-20:20] 20*log10(H(f))
plot [f=20:20000] [-15:15] 20*log10(H(f))
END
