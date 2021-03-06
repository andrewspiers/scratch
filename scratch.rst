.. contents::

Alphabetize every file in the tree
==================================

::

    find . -type f -execdir sort {} -o {} \;


Ansible and Idrac
=================
https://www.stackhpc.com/ansible-drac.html


Ansi escape codes
=================
Because I can never remember how to make text bold, or whatever.
https://pypi.python.org/pypi/ansi/0.1.3


Australian Access Federation Attribute Validator
================================================
https://manager.aaf.edu.au/attributevalidator/snapshot


Brookings ISIS Study
====================
This is a study of ISIS supporters on Twitter. Mainly interesting for
its methods. Randi Harper mentions this in her LCA16 talk mirror.linux.org.au
http://brook.gs/1EpSQIX


Benchmarking Disk I/O ( with fio )
==================================
Nice quick writeup and examples:
https://web.archive.org/web/20170608050506/https://www.binarylane.com.au/support/solutions/articles/1000055889-how-to-benchmark-disk-i-o


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


Conda Cheat Sheet
=================
https://conda.io/docs/_downloads/conda-cheatsheet.pdf


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

Docker: Access Docker socket within container
=============================================
2017-03-03

::

    docker run -v /var/run/docker.sock:/container/path/docker.sock

Not to be done lightly, but sometimes useful.


Docker : Command line tools in containers
=========================================
2017-03-23

There is a reasonably good guide to using command line tools in docker:
https://spin.atomicobject.com/2015/11/30/command-line-tools-docker/
It has some examples here:
https://github.com/atomicobject/docker-cli-distribution

I don't think every problem is solved perfectly, ie you can't really pass in
files outside the current working directory as arguments to command line tools,
but if you need to do it, this is a good starting point.


Docker Compose snippet to set *initial* username and password for Mongodb
=========================================================================

::

    version: "2"
    services:
      worker: # mongo database
        image: library/mongo
        ports:
          - 27017:27017
        environment:
          - MONGO_INITDB_ROOT_USERNAME=user
          - MONGO_INITDB_ROOT_PASSWORD=pass

Docker : Logging
================
The reference https://docs.docker.com/engine/admin/logging/view_container_logs/
Contains useful information about techniques for redirecting process output
from file to stderr and stdout.


Docker : Ubuntu Snap requires root
==================================

https://github.com/docker/docker-snap/issues/1#issuecomment-437654378 ::

    sudo docker ps # which works fine
    docker ps # which doesn't work because of permission failure
    sudo addgroup --system docker
    sudo adduser $USER docker
    newgrp docker
    sudo snap restart docker
    docker ps # this now works because my user is in the group


Edac : Error Detection And Correction
=====================================
https://www.kernel.org/doc/Documentation/edac.txt
The command edac-util will report any errors.
To clear the counters ( ie to silence a nagios alarm which is reporting a
single corrected error) you should write any value into
`/sys/devices/system/edac/mc/mc0/reset_counters`, substituting the correct
memory controller number for `mc0`.

Emlog circular files for linux:
===============================
http://www.circlemud.org/jelson/software/emlog/



Emoji and Symbol fonts for Fedora
=================================
Install the package: gdouros-symbola-fonts

Errno EAI_AGAIN
===============
This is the descriptive error that npm returns when it can't get to the network
to download packages. This could be caused because you are running in a
pbuilder environment and using the default setting which is to switch off
networking. You can permit networking to work in this environment by setting
`USENETWORK=yes` in `/etc/pbuilderrc`.


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

Flask Documentation
===================
2017-03-27

https://www.palletsprojects.com/p/flask/ just because it is not at Pocoo any
more.

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


Gearman : Issues with Documentation
===================================

These are some very rough notes, I could be wrong about all this stuff!!

* The Debian packaged version (from Jessie) 1.0.6-5 doesn't support
  the -vvv switch specified at http://gearman.org/getting-started/

My fork of the source of that is at:
    https://github.com/andrewspiers/gearman.github.io/blob/master/pages/getting_started.txt

* Building from source: Needs libtool, autoconf, boost ( libboost-all-dev ),
  gperf, libevent-dev, uuid-dev

* In many ways, .travis.yml is better documentation than the getting started
  file.

This is not a complaint about documentation, just a general gripe:

* The debian packaged version of gearmand packaged in gearman-job-server
  logs to a file /var/log/gearmand.log, not to the foreground.

  ( side note: this is poor packaging design IMO. The binary should just behave
  as it is shipped, and there should be a *service* that wraps this, and when
  started, logs to a log file ( or maybe just the journal.) )


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


Git: dump full content of all commits
=====================================
I'm not 100% sure this does what I think it does, but this is what
I'm using at the moment::

    git log --format=format:%H --all | xargs git show

This will not show dangling commits though, so it might be good to
also do::

    git fsck --lost-found 2>/dev/null | awk '{print $3}' | git show


Git: clone subdirectory
=======================
2018-06-07

This is useful for splitting part of a project out into a separate project.

1. Create a new repository with git init
2. Add the source repository as a remote
3. ``git fetch``
4. ``git config core.sparseCheckout true``
5. List trees to be checked out in ``.git/info/sparse-checkout``::

    echo "some/dir/" >> .git/info/sparse-checkout
    echo "another/sub/tree" >> .git/info/sparse-checkout

6. ``git pull <remote> <remote branch>``


reference: stack overflow_


.. _overflow: https://stackoverflow.com/a/13738951/37176


Git: initial empty commit
=========================

2018-08-07

::

    git commit --allow-empty -m 'Initial commit'


Git: remote tracking branch
===========================

Check out a remote branch to track it::

    git checkout --track origin/serverfix

or if you want to call it something other than serverfix ( I often want a copy of someone else's
'master' branch.), you can use::

    git checkout -b new_branch_name origin/serverfix

When you are done, Delete the branch 'oldbranch' from remote 'origin' ::

    git push origin --delete oldbranch

If someone else has deleted remote branches (on the remote) and you
want to remove your local copy of those references, run::

    git fetch --prune

Or alternatively if you want to delete just your local reference to a remote branch
that has already been deleted::

    git branch --delete ---remotes origin/oldbranch


ref:
    https://git-scm.com/book/id/v2/Git-Branching-Remote-Branches


Grep 'or'
=========
I never understood exactly how to do express a disjunction_ until I  read this
helpful `guide`__ .

.. _disjunction: https://en.wikipedia.org/wiki/Logical_disjunction
.. __:  http://web.archive.org/web/20160121075851/http://www.thegeekstuff.com/2011/10/grep-or-and-not-operators/


Haproxy simple SSL Termination
==============================

https://web.archive.org/web/20181129044934/https://www.digitalocean.com/community/tutorials/how-to-implement-ssl-termination-with-haproxy-on-ubuntu-14-04


Haproxy config reference
========================

https://cbonte.github.io/haproxy-dconv/1.6/configuration.html

Haskell Resources
=================

* Haskell fast and hard:
  http://yannesposito.com/Scratch/en/blog/Haskell-the-Hard-Way/#
* Learn you a Haskell for great good:
  http://learnyouahaskell.com/chapters
* A gentle introduction to Haskell:
  https://www.haskell.org/tutorial/index.html
* The Haskell Book
  http://haskellbook.com/
* Monads for Functional Programming
  https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q=Monads+for+Functional+Programming+In+Advanced+Functional+Programming&btnG=

IPv6 rules
==========
I found a good basic set of firewall rules for IPv6 systems. If your system has
any ipv6 addresses with *global scope* you should take a look at
these rules_ from cert_.org. Note they only cover ICMP for IPv6, you will
probably want more rules for other traffic.

.. _rules: https://www.cert.org/downloads/IPv6/ip6tables_rules.txt
.. _cert: https://www.cert.org

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


Javascript : Using Promises
===========================
2018-01-03

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises


Jenkins Bitbucket branch source plugin
======================================
This plugin_ enables the automatic creation of Jenkins jobs for repositories
located within a project or personal space within a bitbucket server instance,
or on bitbucket.org. It will try to create jobs for each Jenkins file it finds
on each branch for each repo within the project. There is a trick to setting
it up for bitbucket server: you need define the server within the global
configuration, for it to appear as an option you can use within the job
creation screen.

.. _plugin: https://wiki.jenkins.io/display/JENKINS/Bitbucket+Branch+Source+Plugin


Jenkinsfile Documentation
=========================
::
    // Jenkinsfile , Declarative Pipeline
    // References:
    // https://jenkins.io/doc/book/pipeline/jenkinsfile/
    // https://jenkins.io/doc/book/pipeline/syntax/#declarative-pipeline
    // https://jenkins.io/blog/2016/12/19/declarative-pipeline-beta/
    // https://www.cloudbees.com/sites/default/files/declarative-pipeline-refcard.pdf
    // http://davehunt.co.uk/2017/03/23/migrating-to-declarative-jenkins-pipelines.html


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


Kubectl Cheat Sheet
===================
https://kubernetes.io/docs/reference/kubectl/cheatsheet/


Kubernetes ( kubectl ) Client Side Debugging:
=============================================
Similarly to the openstack client, it is possible to make kubectl log its
outgoing requests. It is not well documented. `kubectl --help` output includes
the following line::

    Use "kubectl options" for a list of global command-line options (applies to all commands).

`kubectl options` includes this line::

    -v, --v=0: log level for V logs

This commit_ adds debugging levels 6,7,8 and 9 to the client. The files
debugging.go, helper.go, and request.go have been moved, although the
functionality seems to remain.

.. _commit: https://github.com/kubernetes/kubernetes/pull/10032/commits/bab0a61ef1e68e2dc780656a9f12eb7d347175ee


LXDE and the Numlock setting.
=============================
2020-08-25

To have the number lock key on at boot, if you are using the *lxdm* display
manager (which I think is the default now), under ``/etc/lxdm/lxdm.conf`` Simply
change ``numlock=0`` to ``numlock=1``. It is simple when you know how!


Maximum Environment Size
========================
http://stackoverflow.com/questions/1078031/what-is-the-maximum-size-of-an-environment-variable-value

http://man7.org/linux/man-pages/man2/execve.2.html

::

    On kernel 2.6.23 and later, most architectures support a size limit
    derived from the soft RLIMIT_STACK resource limit (see getrlimit(2))
    that is in force at the time of the execve() call.  (Architectures
    with no memory management unit are excepted: they maintain the limit
    that was in effect before kernel 2.6.23.)  This change allows
    programs to have a much larger argument and/or environment list.


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


Openstack Neutron Metadata
==========================
https://www.suse.com/communities/blog/vms-get-access-metadata-neutron/


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


Patching and Diffing
====================

To create a diff:
1.  create a copy of the file called file.orig
2.  edit the file
3.  run diff file.orig file > file.patch
To apply it::

    patch file.1 < file.patch

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


Python Decorators
=================
This made a reasonable reference:
https://realpython.com/primer-on-python-decorators/


Python Functional Programming
=============================
An introduction: http://maryrosecook.com/blog/post/a-practical-introduction-to-functional-programming


Python Logging
==============
2018-03-15

Three line logging::

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('message')

Only turn logging up to DEBUG for my script::

    import logging
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger(__name__).setLevel(logging.DEBUG)

Set debug logging everywhere except for that noisy requests module::

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)



Python Merge Dictionaries
=========================
2019-02-26

::

    context = {**defaults, **user}


https://web.archive.org/web/20181015183358/http://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python/



Python Numpy datetime64
=======================
Numpy uses a type called datetime64, which does not have the useful methods
like `.year`, `.month` and so on that regular python datetimes have.
Fortunately you can use pandas to convert to a pandas timestamp which has many
of these convenient methods

::

    In [5]: t = numpy.datetime64('2017-08-30')

    In [6]: p = pandas.to_datetime(t)

    In [7]: p
    Out[7]: Timestamp('2017-08-30 00:00:00')

    In [8]: p.year
    Out[8]: 2017


Python reimport or reload a module in an interactive session
============================================================
2018-04-11

from my Stack Overflow answer_ ::

    import importlib
    importlib.reload(some_module)

and in ipython::

    %load_ext autoreload
    %autoreload 2

.. _answer: https://stackoverflow.com/a/14390676/37176


Python Profiling
================
2018-02-05

The base of python profilng is cProfile_ . The python profiling module also
includes pstats, which formats the profiling data. The pymotw_ page on these is
worthwhile. You can use gprof2dot_ to create a 'dot' file which is a
representation of a network graph. Alternatively you can use cprofilev_ to
obtain a sortable html view of the cprofile output.

A slightly different approach is taken by line_profiler_ which will give you
line by line performance profiling of certain functions, where you have added a
decorator.


.. _cProfile: https://docs.python.org/3/library/profile.html
.. _cprofilev: https://github.com/ymichael/cprofilev
.. _pymotw: https://pymotw.com/3/profile/
.. _line_profiler: https://github.com/rkern/line_profiler
.. _gprof2dot: https://github.com/jrfonseca/gprof2dot


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

ssh-agent and sourcing it in to your shell
==========================================
2016-10-04

This is of particular benefit if you are logging
in to the system you want ssh-agent running on,
which is not the usual case.

http://mah.everybody.org/docs/ssh


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

SSHFS For Windows
=================
This seems to be the latest hack_ to make it work::


    ## How to use:

    Once you have installed WinFsp and SSHFS-Win you can start an SSHFS session to a remote computer using the following syntax:

        \\sshfs\[locuser=]user@host[!port][\path]

.. _hack: https://github.com/billziss-gh/sshfs-win

SOCKS5 Proxy over SSH
=====================
2017-02-07

I've just got the following stanza in my `~/.ssh/config`::


    Host servername
      Compression yes
      DynamicForward {{ portnumber }}
      Hostname server.example.com
      User username

Chrome permits you to use multiple profiles with different settings and
different plugins. I have a profile set up with a plugin called 'Proxy Helper'
https://github.com/henices/Chrome-proxy-helper with this portnumber configured
in the port number and 127.0.0.1 in the host address field. Now when I connect
to `'servername'` my web traffic is sent over that SOCKS5 port. I believe DNS
lookups originating from this profile are also sent over this link, as I was
able to resolve names I've got listed on a home DNS server. What doesn't change
is my search path, so I just use the full (internal) name to look things up.



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
  ctrl-w ctrl-r    - rotate windows (swap positions)
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


Vim left margin via folding abuse
=================================
You can use `set foldcolumn=12` to give yourself 12 characters of
margin space. This doesn't indent your text and makes things nicer
when you are using full screen.


Visual Studio Code plugins
==========================
I have received the following suggestions:

* Docker
* Paty Intellisense
* vscode-icons

And I like:

* Vim


Wikipedia API for queries
=========================
2017-09-30

Reference_

Example query::

    https://en.wikipedia.org/w/api.php?action=query&titles=Main%20Page&prop=revisions&rvprop=content&format=json

There are several output formats_, but unless you want formatted html, you
should always use `json`. `jsonfm` gives you back formatted html with the
`text/html` Content-type.


.. _Reference: https://www.mediawiki.org/wiki/API:Query
.. _formats: https://www.mediawiki.org/wiki/API:Data_formats


Windows Socks5 Web Tunnelling
=============================

Guide_ I use putty, pageant, and chrome with the 'Feed Proxy' extension.
And I use icanhazip.com_ and Google Maps to verify that the proxy is working.
I haven't double checked if there is any DNS leakage with this method yet, but
it works for my purposes, which is connecting to internally-accessible web
servers at work.

.. _Guide: https://www.ocf.berkeley.edu/~xuanluo/sshproxywin.html
.. _icanhazip.com: http://icanhazip.com
