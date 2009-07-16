#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use JSON;
use Data::Dumper;

use Email::Send;

use constant HAPPY_MESSAGE => 'Hello there, thanks for passing by!';
use constant UNHAPPY_MESSAGE => 'You go away nasty web monster!';
use constant FAILED_MESSAGE => 'Ooops, I failed sending an email to teh w0rld';

my $sender = 'sukria+github-webhook@sukria.net';
my $recipient = 'sukria@sukria.net';
my $smtp_host = 'private.sukria.net';

my $version = '0.1';

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
}   

my $content = "$subject\n"
            . '-' x 79 
            . "\n"
            . "$commits_str"
            . "$footer\n";

my $message = "To:  $recipient\n"
            . "From: $sender\n"
            . "X-Mailer: github-webhook-perl $version\n"
            . "X-github-project: ".$repo->{name}."\n"
            . "Subject: $subject\n\n"
            . $content;

my $email = Email::Send->new({mailer => 'SMTP'});
$email->mailer_args([Host => $smtp_host]);
if($email->send($message)) {
    print HAPPY_MESSAGE;
}
else { 
    print FAILED_MESSAGE;
}
