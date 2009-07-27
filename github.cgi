#!/usr/bin/perl

use strict;
use warnings;
use Dancer;
use CGI;
use JSON;
use Email::Send;

# init
my $version = '0.1';
my $config = {
    smtp_host => 'localhost',
};

set content_type 'text/plain';

# all GET requests are droped
get r('.*') => sub { 
    status 'forbidden'; 
    "You go away nasty web monster\n"; 
};

# POST hook-receiver per project
post '/hook/:project' => sub {

    if (not defined $config->{params->{project}}) {
        status 'not_found';
        return "No such project: ".params->{project}."\n";
    }

    # payload is mandatory
    my $payload = params->{'payload'};
    if (not defined $payload) {
        status '404';
        return "Hmm, no payload in your backpack dude\n";
    }

    # inspect the data submitted
    my $json = from_json($payload);
    my $repo = $json->{repository};
    my $commits = $json->{commits};

    # Read the configuration for that repo
    my $repo_config = $config->{$repo->{name}};
    if (not defined $repo_config) {
        print NO_CONFIG_MESSAGE;
        exit 0;
    }

    # Render the email content
    my $tokens = {
        subject    => "New push submitted to ".$repo->{name},
        repository => $repo,
        commits    => $commits,
        nb_commits => (scalar(@$commits)),
        recipient  => $repo_config->{recipient},
        sender     => $repo_config->{sender},
        version    => $version,
    };

    layout 'mail';
    my $message = template('mail', $tokens);

    my $email = Email::Send->new({mailer => 'SMTP'});
    $email->mailer_args([Host => $config->{smtp_host}]);
    if($email->send($message)) {
        status 'ok';
        return $message;
    }
    else { 
        status 'error';
        return "unable to send the mail : $!";
    }
};

Dancer->dance;
