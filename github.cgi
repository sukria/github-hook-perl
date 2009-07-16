#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use JSON;
use Data::Dumper;

use constant HAPPY_MESSAGE => 'Hello there, thanks for passing by!';
use constant UNHAPPY_MESSAGE => 'You go away nasty web monster!';

my $cgi = CGI->new;
print $cgi->header('text/plain');

unless ($cgi->request_method eq 'POST') {
    print UNHAPPY_MESSAGE;
    exit 0;
}

my $payload = $cgi->param('payload');
unless (defined $payload) {
    print UNHAPPY_MESSAGE;
    exit 0;
}

my $json = from_json($payload);
my $repo = $json->{repository};
my $commits = $json->{commits};

my $subject = "New push submitted to ".$repo->{name}." (".~~@{$commits}." commits)";
my $footer  = "-- \n"
            . $repo->{name}." repository (".$repo->{owner}{name}.")\n"
            . $repo->{url}."\n\n";

my $commits_str = "";
foreach my $c (@$commits) {
    $commits_str .= "\n";
    $commits_str .= $c->{timestamp}.' - '.$c->{author}{name}."\n\n";
    $commits_str .= "  * ".$c->{message}."\n\n";
    $commits_str .= $c->{url}."\n\n";
#    $commits_str .= '-' x 79;
#    $commits_str .= "\n\n";
}   

print "$subject\n"; 
print '-' x 79, "\n";
print "$commits_str";
print "$footer\n";
