#!/usr/bin/perl
# +----------------------------------------------------------------------------+
# | MyFarm v0.3 * Web interface for remote monitoring MMxD devices             |
# | Copyright (C) 2019-2022 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>       |
# | myfarm.cgi                                                                 |
# | CGI program                                                                |
# +----------------------------------------------------------------------------+
#
#   This program is free software: you can redistribute it and/or modify it
# under the terms of the European Union Public License 1.1 version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.

use lib 'cgi-bin';
use Switch;
use File::Path qw(make_path);
use File::Path qw(remove_tree);
use strict;

# variables
my $buffer;
my $channel;
my $cmd;
my $dark;
my %FORM;
my $format;
my $green;
my $i;
my $lng = "hu";
my $myfile;
my $name;
my $pair;
my @pairs;
my $red;
my $rootdir = "../myfarm";
my $row;
my @title;
my $uid;
my $uuid;
my $value;
my $yellow;
my $texthtml = "Content-type:text/html\r\n\r\n";

my @n;
my $i;
for $i (0..24)
{
  $n[$i] = "";
}

# get data from buffer
$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
if ($ENV{'REQUEST_METHOD'} eq "GET")
{
  $buffer = $ENV{'QUERY_STRING'};
}

# test data
# ---------
# - registering UUID
# $buffer='cmd=reg&uuid=be6c2eb6-8b2d-4115-9184-5f80a5ba723d';
# - unregistering UUID
# $buffer='cmd=unreg&uuid=be6c2eb6-8b2d-4115-9184-5f80a5ba723d';
# - store names
# $buffer='cmd=name&uuid=be6c2eb6-8b2d-4115-9184-5f80a5ba723d&0=TH01&1=datum&2=ido&3=T&4=RH&5=be 1&6=be 2&7=be 3&8=be 4&9=ki 1&10=ki 2&11=ki 3&12=ki 4&13=hiba 1&14=hiba 2&15=hiba 3&16=hiba 4';
# - store values
# $buffer='cmd=value&uuid=be6c2eb6-8b2d-4115-9184-5f80a5ba723d&0=TH01&1=2019-03-12&2=12:12&3=12&4=79&5=D&6=G&7=G&8=D&9=Y&10=Y&11=D&12=D&13=D&14=D&15=R&16=R';
# - show data
# $buffer='cmd=show&uuid=be6c2eb6-8b2d-4115-9184-5f80a5ba723d&lng=hu';

# split input data
@pairs = split(/&/, $buffer);
foreach $pair (@pairs)
{
  ($name, $value) = split(/=/, $pair);
  $value =~ tr/+/ /;
  $value =~ s/%(..)/pack("C", hex($1))/eg;
  $FORM{$name} = $value;
}
$cmd = $FORM{cmd};
$uuid = substr(lc($FORM{uuid}),0,50);
$lng = substr($FORM{lng},0,2);
for $i (0..24)
{
  $n[$i] = substr($FORM{"$i"},0,24);
}

# select operation mode
switch ($cmd)
{
  # UUID registration
  case "reg"
  {
    if ( not -d "$rootdir/data/$uuid")
    {
      make_path("$rootdir/data/$uuid");
      print $texthtml;
      print "UUID $uuid is registered.\n";
    } else
    {
      print $texthtml;
      print "UUID $uuid is already registered.\n";
    }
  }
  # UUID unregistration
  case "unreg"
  {
    if ( -d "$rootdir/data/$uuid")
    {
      remove_tree("$rootdir/data/$uuid");
      print $texthtml;
      print "UUID $uuid is unregistered.\n";
    } else
    {
      print $texthtml;
      print "UUID $uuid is not registered.\n";
    }
  }
  # store name of growing house and lights
  case "name"
  {
    if ( not -d "$rootdir/data/$uuid/$n[0]")
    {
      make_path("$rootdir/data/$uuid/$n[0]");
    }
    open($myfile, '>', "$rootdir/data/$uuid/$n[0]/names.csv");
    print $myfile "$n[0],$n[1],$n[2],$n[3],$n[4],$n[5],$n[6],$n[7],$n[8],$n[9],$n[10],$n[11],$n[12],$n[13],$n[14],$n[15],$n[16],$n[17],$n[18],$n[19],$n[20],$n[21],$n[22],$n[23],$n[24]\n";
    close $myfile;
    print $texthtml;
    print "Names are stored under $uuid UUID.\n";
  }
  # store values
  case "value"
  {
    if ( not -d "$rootdir/data/$uuid/$n[0]")
    {
      make_path("$rootdir/data/$uuid/$n[0]");
    }
    open($myfile, '>', "$rootdir/data/$uuid/$n[0]/values.csv");
    print $myfile "$n[0],$n[1],$n[2],$n[3],$n[4],$n[5],$n[6],$n[7],$n[8],$n[9],$n[10],$n[11],$n[12],$n[13],$n[14],$n[15],$n[16],$n[17],$n[18],$n[19],$n[20],$n[21],$n[22],$n[23],$n[24],\n";
    close $myfile;
    print $texthtml;
    print "Values are stored under $uuid UUID.\n";
  }
  # create webpage (show data)
  case "show" {
    print $texthtml;
    # write header
    open HEADER, "$rootdir/headers/" . $lng . ".html";
    while (<HEADER>)
    {
      chomp;
      print "$_\n";
    }
    close HEADER;
    # write body
    if ( not -d "$rootdir/data/$uuid" or $uuid eq "")
    {
      switch ($lng)
      {
        case  "en" { print "<h3>Bad UUID!</h3><br><br>" };
        case  "hu" { print "<h3>Hibás UUID!</h3><br><br>" };
      }
    }
    else
    {
      # lights
      $dark = "<img src=\"../myfarm/images/dark.png\" height=\"16\" width=\"16\">";
      $green = "<img src=\"../myfarm/images/green.png\" height=\"16\" width=\"16\">";
      $red = "<img src=\"../myfarm/images/red.png\" height=\"16\" width=\"16\">";
      $yellow = "<img src=\"../myfarm/images/yellow.png\" height=\"16\" width=\"16\">";

      opendir my $dh, "$rootdir/data/$uuid" or die $!;
      my @folderlist = grep { -d "$rootdir/data/$uuid/$_" } readdir $dh;
      close $dh;
      my @sorted_folderlist = sort @folderlist;
      foreach my $n0 (@sorted_folderlist)
      {
        if ($n0 eq '.' or $n0 eq '..')
        {
          next;
        }
        # load tooltips
        open DATA, "< $rootdir/data/$uuid/$n0/names.csv" or die "Cannot open names.csv!";
        while (<DATA>)
        {
          chop;
          my(@columns) = split(",");
          my($colnum) = $#columns;
          $row = "";
          foreach $colnum (@columns)
          {
            $row = $row . $colnum;
          }
          my(@datarow) = split("\"\"",$row);
          my($datarownum) = $#datarow;

          for $i (0..$colnum)
          {
              $title[$i] = $columns[$i];
          }
          last;
        }
        close DATA;
        # load values
        open DATA, "< $rootdir/data/$uuid/$n0/values.csv" or die "Cannot open values.csv!";
        while (<DATA>)
        {
          chop;
          my(@columns) = split(",");
          my($colnum) = $#columns;
          $row = "";
          foreach $colnum (@columns)
          {
            $row = $row . $colnum;
          }
          my(@datarow) = split("\"\"",$row);
          my($datarownum) = $#datarow;
          for $i (0..$colnum)
          {
            if ($columns[$i] eq "R") { $columns[$i] = $red };
            if ($columns[$i] eq "G") { $columns[$i] = $green };
            if ($columns[$i] eq "Y") { $columns[$i] = $yellow };
            if ($columns[$i] eq "D") { $columns[$i] = $dark };
          }
          print"              <tr align=\"center\">\n";
          print"                <td>$columns[0]</td>\n";
          for $i (1..$colnum)
          {
            print"                <td title=\"$title[$i]\">$columns[$i]</td>\n";
          }
          print"              </tr>\n";
          last;
        }
        close DATA;
      }
    }
    print"            </tbody>\n";
    print"          </table>\n";
    switch ($lng)
    {
      case  "en" { print"          Hint: Move the mouse over data to show their name.<br>\n"};
      case  "hu" { print"          Tipp: Mozgassa az egérkurzort az adat fölé a nevük mutatásához.<br>\n"};
    }
    print"          <br>\n";
    print"        </div>\n";
    print"        <ul class=\"actions\">\n";
    print"          <li>\n";
    print"            <form action=\"http://www.szerafingomba.hu/cgi-bin/myfarm.cgi\" method=\"get\">\n";
    print"              <input type=\"hidden\" name=\"uuid\" value=\"$uuid\">\n";
    print"              <input type=\"hidden\" name=\"cmd\" value=\"show\">\n";
    print"              <input type=\"hidden\" name=\"lng\" value=\"$lng\">\n";
    switch ($lng)
    {
      case  "en" { print"              <input value=\"Update\" type=\"submit\">\n" };
      case  "hu" { print"              <input value=\"Frissít\" type=\"submit\">\n" };
    }
    print"            </form>\n";
    print"          </li>\n";
    print"        </ul>\n";
    print"      </div>\n";
    print"    </section>\n";

    # write footer to stdout
    open FOOTER, "$rootdir/footers/" . $lng . ".html";
    while (<FOOTER>)
    {
      chomp;
      print "$_\n";
    }
    close FOOTER;
  }
}
exit 0;
