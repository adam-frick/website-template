#!/usr/bin/env perl
use warnings;
use strict;
use CGI;
use JSON::XS;
use Path::Class;
use Switch;
print CGI::header;

my $css_prefix = "<link rel=\"stylesheet\" href=\"";
my $css_suffix = "\" type=\"text/css\">";
my $local_file_dir = dir("../" . 
    substr(CGI::url(), 
    length(CGI::url(base=>1) . "included:////."),
    -length(CGI::url(relative=>1))
    )
);

my $global_file_dir = dir("../global");

my $json_filename = "include.json";
my $html_ext = ".html";
my $inc_file = $local_file_dir->file($json_filename);

my $json_content = $inc_file->slurp();
my $json_decode = decode_json($json_content);

switch (CGI::param("type")) { # cgi QUERY_STRING type value
    case "html" {
        for (@{$json_decode->{"html"}}) { 
            print get_file($_, ".html")->slurp(); # print its contents
        } 
    }

    case "css" {
        for (@{$json_decode->{"css"}}) {
            print $css_prefix . get_file($_, ".css") . $css_suffix;
        }
    }

    else {
        print "Error parsing CGI query\n";
        last;
    }
}

sub get_file { # returns source file reference
    my $get_file_dir;

    switch ($_->{"scope"}) { # source file scope directory
        case "global" {
            $get_file_dir = $global_file_dir;
        }
        case "local" {
            $get_file_dir = $local_file_dir;
        }
        else {
            print "Error parsing source file scope\n";
        }
    }    
    return dir($get_file_dir)->file($_->{"name"} . "$_[1]");
}

exit;
