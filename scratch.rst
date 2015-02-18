Scratch
=======
`Vim multiwindow`_

`Docker operations`_

`Fedora 21 : Customising the search path with NetworkManager`_

`reStructuredText : rst : Implicit Hyperlink Targets`_

`Tmux copy and paste using vi mode`_

`Clearing the screen in bash vi mode`_

`Stardict`_ (dictionary for freebsd)


Puppetdb curl test
==================

::

    curl -G 'http://puppetdb.example.com:8080/v4/resources' --data-urlencode  'query= ["or", ["=", "environment", "env1"], ["=", "environment", "env2"] ] '




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

Docker operations
=================
2014-11-15

https://www.youtube.com/watch?v=T7Y669CTuXE#t=23



Tmux copy and paste using vi mode
=================================
2014-11-14

Go to this website and do what it says:
http://blog.sanctum.geek.nz/vi-mode-in-tmux/

reStructuredText : rst : Implicit Hyperlink Targets
===================================================
2014-11-14

Ref: http://docutils.sourceforge.net/docs/user/rst/quickref.html#implicit-hyperlink-targets


Fedora 21 : Customising the search path with NetworkManager
===========================================================
2014-11-14

In another example of 'simplifying', the option to set the dns search path
has been removed from the standard NetworkManager ui. Fortunately if you
install the package nm-connection-editor you can set the search path from
there. see https://bugzilla.redhat.com/show_bug.cgi?id=1046701

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


Stardict
========
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
