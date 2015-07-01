.. contents::

Beer
====

Panhead American Pale Ale at some place
in Moonee Ponds. 8.

Btrfs
=====
When I set up my current workstation last year, I chose
btrfs, mostly because I wanted to try something new.

This morning I ran into a nasty situation where suddenly
system load was very high and everything on my computer was
running very slowly. I was mostly trying to read webpages at
the time, so initially I suspected that it was in fact a network
problem. High load and low CPU usage often means disk issues
however, so eventually I figured out it was disk or filesystem
related.

Running `df` indicated plenty of space left, so I thought the
problem could be physical. It turns out I didn't have smartmontools
installed, so I tried to install that. Dnf took *AGES* to run, and
eventually failed. I have a plugin that creates snapshots of my
btrfs volumes and subvolumes, and I believe this is what failed,
because it was out of space.

Eventually I could confirm that I was out of space::

    # btrfs fi usage /
    Overall:
        Device size:                 230.11GiB
        Device allocated:       230.11GiB
        Device unallocated:       0.00B
        Device missing:               0.00B
        Used:                      125.22GiB
        Free (estimated):       103.84GiB (min: 103.84GiB)
        Data ratio:         1.00
        Metadata ratio:                2.00
        Global reserve:           512.00MiB   (used: 0.00B)

    Data,single: Size:217.08GiB, Used:113.24GiB
       /dev/mapper/luks-548a9245-7942-4ae5-8fdb-fa8802b54751         217.08GiB

    Metadata,single: Size:8.00MiB, Used:0.00B
       /dev/mapper/luks-548a9245-7942-4ae5-8fdb-fa8802b54751           8.00MiB

    Metadata,DUP: Size:6.50GiB, Used:5.99GiB
       /dev/mapper/luks-548a9245-7942-4ae5-8fdb-fa8802b54751          13.00GiB

    System,single: Size:4.00MiB, Used:0.00B
       /dev/mapper/luks-548a9245-7942-4ae5-8fdb-fa8802b54751           4.00MiB

    System,DUP: Size:8.00MiB, Used:48.00KiB
       /dev/mapper/luks-548a9245-7942-4ae5-8fdb-fa8802b54751          16.00MiB

    Unallocated:
       /dev/mapper/luks-548a9245-7942-4ae5-8fdb-fa8802b54751             0.00B

`btrfs subvolume list` also confirmed that there were many (over 150)
subvolumes existing. I got rid of them all with this command::

    btrfs subvolume list / | head | tail -n8 | awk '{print "/"$NF}' | xargs -n1 btrfs subvolume  delete -c

I ran that until the number of subvolumes was more reasonable.
The "`head | tail -n8`" bit ensures that the first two subvolumes listed were
not deleted (In practice I do not think they would have been removed, as they
had subvolumes.) I checked the amount of subvolumes remaining with `btrfs subvolume list / | wc -l`.

Once this process was complete, `btrfs fi usage /` still showed no unallocated,
although there was a lot of space listed as "Free". I think unallocated still
means that none was available to be allocated for metadata, if that were to
become necessary. So I decided that I also needed to rebalance the filesystem
with these commands::

  btrfs balance start -v -dusage=5 /home
  btrfs balance start -v -dusage=20 /home

These commands move data where a 'chunk' is less than the given percentage
filled, so that some chunks become reallocated. (I am a bit uncertain exactly
what a 'chunk' is, and how it relates to blocks and extents, and even if that
is the correct terminology.)

I used `btrfs balance status -v /home` to monitor the rebalance process.



For more information, see https://btrfs.wiki.kernel.org/index.php/Problem_FAQ
And http://marc.merlins.org/perso/btrfs/post_2014-05-04_Fixing-Btrfs-Filesystem-Full-Problems.html


Clearing the screen in bash vi mode
===================================
2014-07-04

If you are a bash user, and supremely lazy, you can use Ctrl-L to clear your
screen in bash, except if you are in vi mode. You can confirm this with the
'bind' bash built in::

  $ bind -P | grep clear
  clear-screen can be found on "\C-l".
  $ set -o vi
  $ bind -P | grep clear
  clear-screen is not bound to any keys

bind can also be used to bind Ctrl-L to clear-screen, just like in emacs mode::

 $ bind -P | grep clear
 clear-screen is not bound to any keys
 $ bind '"^L": clear-screen'
 $ bind -P | grep clear
 clear-screen can be found on "\C-l".

You need to literally input a Ctrl-L on your keyboard, you cannot type a '^'
and then a 'L'.

Designate
=========

::

    designate domain-list
    designate record-list <domain id>
    designate record-update --data <new ip address> <domain id> <record id>




Emoji and Symbol fonts for Fedora
=================================
Install the package: gdouros-symbola-fonts


Irssi Scripting
===============

http://juerd.nl/site.plp/irssiscripttut

http://www.irssi.org/documentation/perl

Packer
======
We use the binary versions from http://packer.io

Some working json files are in https://github.com/NeCTAR-RC/nectar-images
In order to get this to work on ubuntu, using the qemu builder, the
qemu-system-x86 package is required. Also, the user running packer needs to be
in the kvm group, so for example::

    sudo usermod -a -G kvm ubuntu

I have found that monitoring the installation with vncviewer can interfere with
the keypresses that packer inserts during the build phase, so it is better to
set the environment variable PACKER_LOG (to any value) and watch the keypresses being typed in to the console. If the installer seems to get stuck, then you can
use the vnc console to see why.

Perl
====
http://www.perl.org/books/beginning-perl/

Puppet file permissions
=======================
2015-07-01

From https://docs.puppetlabs.com/references/latest/type.html#file :
"When specifying numeric permissions for directories, Puppet sets the search
permission wherever the read permission is set."

::

    $ puppet apply -e "file {'/home/andrew/tmp/test': mode=>'0644', } "
    Notice: Compiled catalog for <HOSTNAME> in environment production in 0.07 seconds
    Notice: /Stage[main]/Main/File[/home/andrew/tmp/test]/mode: mode changed '0777' to '0755'
    Notice: Finished catalog run in 0.02 seconds

If you really want a directory with restrictive permissions, you can use
symbolic permissions::

    $ puppet apply -e "file {'/home/andrew/tmp/test': mode=>'u+rw-x,g+r-x,o+r-x', } "
    Notice: Compiled catalog for <HOSTNAME> in environment production in 0.08 seconds
    Notice: /Stage[main]/Main/File[/home/andrew/tmp/test]/mode: mode changed '0744' to '0644' (u+rw-x,g+r-x,o+r-x)
    Notice: Finished catalog run in 0.02 seconds

It also seems that if the mode of a file is not specified anywhere in the
manifest, puppet uses the permission of the source file on the server. This
can be overridden by doing something like::

    File {
      owner => 'root',
      group => 'root',
      mode  => '0644'
    }

in site.pp, or somehere that everything will inherit from.


Puppetdb curl test
==================

::

    curl -G 'http://puppetdb.example.com:8080/v4/resources' --data-urlencode  'query= ["or", ["=", "environment", "env1"], ["=", "environment", "env2"] ] '


Puppet srv records
==================

::

     dig _x-puppet._tcp.rc.example.com SRV



Selinux list port mappings and bindings
=======================================
2015-03-02

`semanage port -l`



reStructuredText rst Implicit Hyperlink Targets
===============================================
2014-11-14

Ref: http://docutils.sourceforge.net/docs/user/rst/quickref.html#implicit-hyperlink-targets


Tmux copy and paste using vi mode
=================================
2014-11-14

Go to this website and do what it says:
http://blog.sanctum.geek.nz/vi-mode-in-tmux/


Fedora 21 Customising the search path with NetworkManager
=========================================================
2014-11-14

In another example of 'simplifying', the option to set the dns search path
has been removed from the standard NetworkManager ui. Fortunately if you
install the package nm-connection-editor you can set the search path from
there. see https://bugzilla.redhat.com/show_bug.cgi?id=1046701


Stardict Dictionary
===================
(Just some notes here about what else needs to be done.)
::

    Message for sdcv-0.4.2_2:
    **************************************************************************
    sdcv is now installed.
    you have to fetch the dictionaries to make it work correctly.

    1. Make directory for dictionaries files :

            # mkdir -p /usr/local/share/stardict/dict


    2. Please put your dictionary file at :

            /usr/local/share/stardict/dict/

    **************************************************************************

Options
=======
maraschino
sickrage


Vim multiwindow
===============
2014-12-10

multiwindow commands::

  :split filename  - split window and load another file
  ctrl-w up arrow  - move cursor up a window
  ctrl-w ctrl-w    - move cursor to another window (cycle)
  ctrl-w_          - maximize current window
  ctrl-w=          - make all equal size
  10 ctrl-w+       - increase window size by 10 lines
  :vsplit file     - vertical split
  :sview file      - same as split, but readonly
  :hide            - close current window
  :only            - keep only this window open
  :ls              - show current buffers
  :b 2             - open buffer #2 in this window


Vim folding
===========
Vim folding commands::

    zf#j creates a fold from the cursor down # lines.
    zf/string creates a fold from the cursor to string .
    zj moves the cursor to the next fold.
    zk moves the cursor to the previous fold.
    zo opens a fold at the cursor.
    zO opens all folds at the cursor.
    zm increases the foldlevel by one.
    zM closes all open folds.
    zr decreases the foldlevel by one.
    zR decreases the foldlevel to zero -- all folds will be open.
    zd deletes the fold at the cursor.
    zE deletes all folds.
    [z move to start of open fold.
    ]z move to end of open fold.
