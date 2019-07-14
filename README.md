gedit-smart-autosave
====================

My WIP attempt at an autosave plugin for gedit. It autosaves the file whenever
you stop editing for half a second, when you change tabs, and when the window
loses focus. I haven't yet managed to get autosave working when a tab or the
window is closed, if the half second timer hasn't already saved the file. I
can't seem to find the right signals to connect to, and seem to be getting into
a race condition with gedit's "Save changes to document before closing?"
dialog.
