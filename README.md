gedit-smart-autosave
====================

`gedit-smart-autosave` autosaves files in
[gedit](https://wiki.gnome.org/Apps/Gedit) in a smarter way than the builtin
autosave setting.

Installation
------------

```
mkdir -p ~/.local/share/gedit/plugins
git clone https://github.com/seanh/gedit-smart-autosave.git ~/.local/share/gedit/plugins/gedit-smart-autosave
```

Then in gedit go to <kbd>Preferences</kbd> → <kbd>Plugins</kbd> and enable the **Smart Autosave** plugin.

## What it does

gedit's builtin autosave feature just saves your file every ten minutes. It can
be configured to autosave every minute at most. So you could still lose work if
your computer crashes.  `gedit-smart-autosave` is much more aggressive about
saving your work:

* Autosaves your file whenever you stop editing for half a second
* Autosaves immediately when you change tabs (if the half second
  timer didn't save it already)
* Autosaves immediately when the gedit window loses focus

It also removes the giant <kbd>Save</kbd> button from gedit's headerbar.
If you use this plugin in combination with
[`gedit-autoname`](https://github.com/seanh/gedit-autoname) you won't be
needing the <kbd>Save</kbd> button.
(You can still use <kbd><kbd>Ctrl</kbd> + <kbd>s</kbd></kbd> to save manually).

As with the builtin autosave feature, this **will not save the "Untitled
Document"s** that you get when you first open a new window or tab. Autosaving
will only kick in after you've saved the file once manually, giving it a
filename and directory. I recommend using `gedit-smart-autosave` together with my
[`gedit-autoname`](https://github.com/seanh/gedit-autoname) plugin which
automatically names untitled documents when you open them so that autosave
works immediately.

**Remote files aren't autosaved** because saving those could be slow so this
kind of aggressive autosaving might not be a good idea for remote files. I
recommend keeping gedit's builtin autosave-every-ten-minutes enabled for use
with remote files.

## What I wasn't able to get working

I wasn't able to get it to autosave immediately:

* When you close a tab
* When you close a window
* When you quit gedit

It'll be fine as long as you wait half a second for the timer-based saving
before doing these actions. Otherwise you'll get gedit's
"Save changes to document before closing?" dialog.

I'd prefer it to just save the changes, rather than asking to save them, but I
couldn't figure out how to get that to work.
