#!/usr/bin/env perl
use strict;
use warnings;
use CGI;
use JSON::XS;
use Path::Class;
use Switch;
print CGI::header;

my $dir = CGI::param("dir") or die "No directory specified\n";
my $src_dir = dir("../$dir");
my $html_ext = ".html";
my $filename = "include.json";

my $file = $src_dir->file($filename);
my $content = $file->slurp();
my $decode = decode_json($content);


switch (CGI::param("type")) { # cgi QUERY_STRING type value
    case "html" {
        for (@{$decode->{"source"}{"html"}}) { 
            print $src_dir->file($_ . $html_ext)->slurp(); # print its contents
        } 
    }

    case "css" {
        my $css_head = $decode->{"css"}{"prefix"};
        my $css_tail = $decode->{"css"}{"suffix"};
        for (@{$decode->{"source"}{"css"}}) {
            print $css_head . $src_dir . "/" . $_ . $css_tail;
        }
    }

    else {
        print "Error parsing CGI query" . "\n";
        last;
    }
}



exit;
