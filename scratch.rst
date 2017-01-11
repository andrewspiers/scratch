.. contents::

Australian Access Federation Attribute Validator
================================================
https://manager.aaf.edu.au/attributevalidator/snapshot

Beer
====

Panhead American Pale Ale at some place
in Moonee Ponds. 8.

Brookings ISIS Study
====================
(Randi mentions this in her LCA16 talk mirror.linux.org.au )
http://brook.gs/1EpSQIX

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

Coreos
======
I only know the high level stuff about CoreOS, but hopefully if I watch this
video_ and play along with the instance I've got at home, I'll soon know more.

.. _video: http://mirror.linux.org.au/linux.conf.au/2015/OGGB_FP/Friday/A_CoreOS_Tutorial.webm

Dataset: Baby Names
===================
2016-02-05

https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data

Search queries get so much more interesting when you add the term 'dataset'.

Designate Basic Commands
========================
API v1 Commands::

    designate domain-list
    designate record-list <domain id>
    designate record-update --data <new ip address> <domain id> <record id>

API v2 commands, using python-openstackclient::

    openstack zone list
    openstack recordset list oboe.instrument.com.
    openstack recordset create --type A oboe.instrument.com. small --records 2.3.4.5 7.8.9.10
    openstack recordset create --type PTR 1.168.192.in-addr.arpa. 25 --records twentyfive.example.com.
    openstack recordset set oboe.instrument.com. small.oboe.instrument.com. --records 11.12.13.14
    openstack recordset show oboe.instrument.com. small.oboe.instrument.com.


Designate Mitaka (Tokyo) Videos
===============================

https://www.openstack.org/summit/tokyo-2015/videos/presentation/dnsaas-for-your-cloud-openstack-designate

https://www.openstack.org/summit/tokyo-2015/videos/presentation/rsvp-required-designate-interactive-workshop-install-and-operate-hands-on-lab

https://www.openstack.org/summit/tokyo-2015/videos/presentation/get-your-instance-by-name-integration-of-nova-neutron-and-designate


DNS Amplification
=================
https://www.us-cert.gov/ncas/alerts/TA13-088A


Docker : Cleaning up after yourself
===================================
2016-12-15

See this post: http://blog.yohanliyanage.com/2015/05/docker-clean-up-after-yourself/

Run these commands::

    docker rm -v $(docker ps -a -q -f status=exited)
    docker rmi $(docker images -f "dangling=true" -q)

Edac : Error Detection And Correction
=====================================
https://www.kernel.org/doc/Documentation/edac.txt
The command edac-util will report any errors.
To clear the counters ( ie to silence a nagios alarm which is reporting a
single corrected error) you should write any value into
`/sys/devices/system/edac/mc/mc0/reset_counters`, substituting the correct
memory controller number for `mc0`.

Errno EAI_AGAIN
===============
This is the descriptive error that npm returns when it can't get to the network
to download packages. This could be caused because you are running in a
pbuilder environment and using the default setting which is to switch off
networking. You can permit networking to work in this environment by setting
`USENETWORK=yes` in `/etc/pbuilderrc`.

Emoji and Symbol fonts for Fedora
=================================
Install the package: gdouros-symbola-fonts

ESPlant
=======
Environmental Sensor Plant - solar WiFi gardening/meteorological sensor using
 ESP8266 processor. I assembled one of these at the open hardware miniconf
 at LCA 2016 and it was a blast. THANKS CCHS MELBOURNE!

https://github.com/CCHS-Melbourne/ESPlant

Findnogit
=========
For when you want a list of all the files in a git repo without everything
under .git::

    find . -not -path './.git*'

or, expressed as an alias (note the handling of single quotes)::

    alias findnogit=' find . -not -path '\''./.git*'\'' '

Flask Installation
==================
I have been having way more trouble than I should installing flask into a
virtualenv. The main problem I had was that the flask binary was not being
created. I tried with freebsd, linux osx, and got the same trobule with a pip
installation.

However, installing from git worked, ie git clone flask, create a virtualenv
and then from the flask dir, `pip install -e .`.  For the record commit
e7d548595e8f2f03fb58c82 seems to work fine.


Galera and Mysql : Check synchronization state
==============================================

::

    mysql -e "SHOW STATUS LIKE 'wsrep_%'"


Gerrit : Delete a review
========================
::

    ssh <username>@<gerrit server> -p 29418 gerrit review <reviewnumber>,<changeset> --delete


Git: dump current config
========================
This dumps the current config of git as applies to the current context, ie
local and global combined.

::

     git config --get-regexp '.*'


Grep 'or'
=========
I never understood exactly how to do express a disjunction_ until I  read this
helpful `guide`__ .

.. _disjunction: https://en.wikipedia.org/wiki/Logical_disjunction
.. __:  http://web.archive.org/web/20160121075851/http://www.thegeekstuff.com/2011/10/grep-or-and-not-operators/


Ipython
=======
2016-06-24

New version with better inline editing!::

    pip install --upgrade ipython prompt_toolkit --pre

https://twitter.com/Mbussonn/status/743581861314584576

Irssi Scripting
===============

http://juerd.nl/site.plp/irssiscripttut

http://www.irssi.org/documentation/perl


Journalctl Last 24 hours ago
============================
::
    journalctl --since '24 hours ago'


Kibana Searches
===============
2015-07-14

https://www.elastic.co/guide/en/kibana/3.0/queries.html

One thing to watch out for  is that kibana uses quotes differently, so that
'jenkins-jobs' matches differently to "jenkins-jobs".

Mosquitto
=========
Mosquitto is an implementation of the MQTT protocol. Here are the related
packages in Debian:

http://mosquitto.org/
Packages in Debian::

    libmosquitto-dev            - MQTT version 3.1 client library, developme
    libmosquitto1               - MQTT version 3.1 client library
    libmosquittopp-dev          - MQTT version 3.1 client C++ library, devel
    libmosquittopp1             - MQTT version 3.1 client C++ library
    mosquitto                   - MQTT version 3.1/3.1.1 compatible message
    mosquitto-clients           - Mosquitto command line MQTT clients
    mosquitto-dbg               - debugging symbols for mosquitto binaries
    python-mosquitto            - MQTT version 3.1 Python client library
    python3-mosquitto           - MQTT version 3.1 Python 3 client library

Mysql remove tables from a database
===================================

2016-04-12
::

    mysql -Nse 'show tables' designate | while read table; do mysql -e "drop table $table" designate ; done


Open Sourcing Anti Harassment Methodologies
===========================================

Randi Harper gave this excellent, interesting talk_ . In it she cites a study_
from the Brookings Project_ on U.S. Relations with the Islamic World.

.. _study: http://brook.gs/1EpSQIX
.. _talk: http://mirror.linux.org.au/linux.conf.au/2016/04_Thursday/D4.303_Costa_Theatre/Open_Sourcing_AntiHarassment_Methodologies.webm
.. _Project: http://www.brookings.edu

The anti harassment stuff hits a personal sweet spot of data mining, web
scraping, and network mapping that is technically intriguing as well as being
socially useful.


Openstack Neutron Adding Security Group Rules
=============================================
2016-01-08

This must be one of the worst or at least longest commands ever:

    neutron security-group-rule-create --tenant-id <tenant-uuid> \
    --direction ingress --protocol tcp --ethertype IPv4 \
    --port-range-min <port> --port-range-max <port> \
    --remote-ip-prefix <ip/CIDR> <secgroup-uuid>

Openstack Neutron Associate Fixed ip with instance / reserve ip
===============================================================

http://web.archive.org/web/20160129000655/https://community.hpcloud.com/question/2723/how-associate-fixed-ip-instance

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
set the environment variable PACKER_LOG (to any value) and watch the keypresses
being typed in to the console. If the installer seems to get stuck, then you
can use the vnc console to see why.

Openstack Neutron Metadata
==========================
https://www.suse.com/communities/blog/vms-get-access-metadata-neutron/

PowerDNS
========
http://www.debiantutorials.com/installing-powerdns-as-supermaster-with-slaves/
https://doc.powerdns.com/3/authoritative/modes-of-operation/
https://www.digitalocean.com/community/tutorials/how-to-configure-dns-replication-on-a-slave-powerdns-server-on-ubuntu-14-04


Perl
====
http://www.perl.org/books/beginning-perl/

Puppet Unit Testing
===================
The Openstack instructions for running unit tests for their packages basically
just say to 'bundle exec rake spec'
https://wiki.openstack.org/wiki/Puppet/Unit_testing I exported GEM_HOME to
/usr/local although maybe it should be set to 'Vendor' as described there.


Python Functional Programming
=============================
An introduction: http://maryrosecook.com/blog/post/a-practical-introduction-to-functional-programming

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


Puppet : Install specific versions from gems into rvm
=====================================================
Fedora packages puppet 4, our environment runs on puppet 3, so for local
testing and validation I install puppet in a gemset and reference it with
wrapper scripts. To create the gemset::

    rvm gemset create p3
    rvm gemset use p3
    gem install puppet -v 3.8.7
    gem install puppet-lint

The wrapper script I use to use the gemset is at
https://github.com/andrewspiers/pup/


Puppet roles and profiles
=========================
http://www.craigdunn.org/2012/05/239/


Puppetdb curl test
==================

::

    curl -G 'http://puppetdb.example.com:8080/v4/resources' --data-urlencode  'query= ["or", ["=", "environment", "env1"], ["=", "environment", "env2"] ] '

Puppet librarian local checkout
===============================
First login as rvm user, then `rvm gemset use librarian`. Then::

    librarian-puppet install --path=~/puppet/testing

Puppet srv records
==================

::

     dig _x-puppet._tcp.rc.example.com SRV

Reboot on Hung Task
===================
*warning: data not synced to disk may be lost if you implement this!*

A guide to making a machine_ reboot_ when it hits a hung task timeout.

.. _machine: http://www.nico.schottelius.org/blog/reboot-linux-if-task-blocked-for-more-than-n-seconds/
.. _reboot: http://web.archive.org/web/20160505042425/http://www.nico.schottelius.org/blog/reboot-linux-if-task-blocked-for-more-than-n-seconds/

Here is a puppet class to make it happen::

    # reboot when a task hangs.
    class reboot {
      sysctl::value { 'kernel.panic': value => '10'}
      sysctl::value { 'kernel.hung_task_panic': value => '1'}
      sysctl::value { 'kernel.hung_task_timeout_secs': value => '300'}
    }

    # set sysctls back to ubuntu defaults
    class noreboot {
      sysctl::value { 'kernel.panic': value => '0'}
      sysctl::value { 'kernel.hung_task_panic': value => '1'}
      sysctl::value { 'kernel.hung_task_timeout_secs': value => '120'}
    }

    include reboot

And finally, the documentation for all the linux kernel sysctls:
https://www.kernel.org/doc/Documentation/sysctl/kernel.txt

Removing Old Kernels on Ubuntu and Debian Systems
=================================================
I've tried out a few alternatives_, and using 'unattended-upgrade'
seems to work the best for me, ie: "Locate the line:

    //Unattended-Upgrade::Remove-Unused-Dependencies "false";

Uncomment the line AND change the value to "true".

.. _alternatives: https://help.ubuntu.com/community/Lubuntu/Documentation/RemoveOldKernels


reStructuredText rst Implicit Hyperlink Targets
===============================================
2014-11-14

Ref: http://docutils.sourceforge.net/docs/user/rst/quickref.html#implicit-hyperlink-targets


Selinux list port mappings and bindings
=======================================
2015-03-02

`semanage port -l`

Slack Enormous Emoji
====================

https://github.com/andybotting/chrome-slack-enormous-emoji


Sql
===

http://www.sqlstyle.guide/

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


Openstack Nova Metadata Service
===============================

ec2 api ::

    # curl 169.254.169.254/latest/meta-data
    ami-id
    ami-launch-index
    ami-manifest-path
    block-device-mapping/
    hostname
    instance-action
    instance-id
    instance-type
    kernel-id
    local-hostname
    local-ipv4
    placement/
    public-hostname
    public-ipv4
    public-keys/
    ramdisk-id
    reservation-id

I haven't yet found where this is documented. The api is extremely easy to use
however.

openstack api ::

    # curl http://169.254.169.254/openstack/latest/



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

Swift
=====
`Runbook <http://docs.openstack.org/developer/swift/ops_runbook/index.html>`_


Timezones
=========

A yet to be implemented idea for a commandline summary of timezones I care
about::

    (local TZ name)            UTC
    -------------------------------
    10:00                    day X
    11:00                   day X+1
    etc


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

    :set foldmethod=indent  : fold on indent (good for python)
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


Windows Socks5 Web Tunnelling
=============================

Guide_ I use putty, pageant, and chrome with the 'Feed Proxy' extension.
And I use icanhazip.com_ and Google Maps to verify that the proxy is working.
I haven't double checked if there is any DNS leakage with this method yet, but
it works for my purposes, which is connecting to internally-accessible web
servers at work.

.. _Guide: https://www.ocf.berkeley.edu/~xuanluo/sshproxywin.html
.. _icanhazip.com: http://icanhazip.com
