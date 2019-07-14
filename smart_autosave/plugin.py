from gi.repository import GObject, Gedit, Gtk


__all__ = ["SASViewActivatable", "SASWindowActivatable"]


class SASViewActivatable(GObject.Object, Gedit.ViewActivatable):
    __gtype_name__ = "SASViewActivatable"

    view = GObject.property(type=Gedit.View)

    def __init__(self):
        GObject.Object.__init__(self)
        self.timeout_id = None

    def do_activate(self):
        self.document_changed_handler_id = self.document.connect(
            "changed", self.document_changed
        )

    def do_deactivate(self):
        self.document.disconnect(self.document_changed_handler_id)

    def document_changed(self, _document):
        if self.timeout_id is not None:
            GObject.source_remove(self.timeout_id)

        self.timeout_id = GObject.timeout_add(
            500, self.maybe_save, priority=GObject.PRIORITY_LOW
        )

    def maybe_save(self):
        maybe_save(self.window)
        self.timeout_id = None
        return False

    @property
    def document(self):
        return self.view.get_buffer()

    @property
    def window(self):
        return self.view.get_toplevel()


class SASWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "SASWindowActivatable"

    window = GObject.Property(type=Gedit.Window)

    def do_activate(self):
        self.window.smart_autosave_plugin_handler_ids = [
            self.window.connect("active-tab-changed", self.active_tab_changed),
            self.window.connect("focus-out-event", self.focus_out),
            self.window.connect("delete-event", self.delete_event),
        ]

        self.notebook = lookup_widget(self.window, "GeditNotebook")[0]
        self.tab_close_request_handler_id = self.notebook.connect(
            "tab-close-request", self.tab_close_request
        )

    def do_deactivate(self):
        for handler_id in self.window.smart_autosave_plugin_handler_ids:
            self.window.disconnect(handler_id)
        self.notebook.disconnect(self.tab_close_request_handler_id)

    def active_tab_changed(self, window, _new_tab):
        maybe_save(window)

    def focus_out(self, window, _event):
        maybe_save(window)

    def delete_event(self, window, _event):
        pass

    def tab_close_request(self, _notebook, _tab):
        pass


def maybe_save(window):
    for document in window.get_unsaved_documents():
        if document.get_file().is_readonly():
            return False

        if document.is_untitled():
            return False

        if not document.is_local():
            return False

        if not document.get_modified():
            return False

        Gedit.commands_save_document_async(document, window)
        document.set_modified(False)


def lookup_widget(base, widget_name):
    widgets = []
    for widget in base.get_children():
        if widget.get_name() == widget_name:
            widgets.append(widget)
        if isinstance(widget, Gtk.Container):
            widgets += lookup_widget(widget, widget_name)
    return widgets
