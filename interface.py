

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
except:
    pass

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileQuit'/>
    </menu>
    <menu action='EditMenu'>
      <menuitem action='NetworkSettings'/>
    </menu>
    <menu action='AboutMenu'>
      <menuitem action='About' />
    </menu>
  </menubar>
</ui>
"""

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Генератор кроссвордов")
        self.set_default_size(500, 500)
        ui_manager = self.create_ui_manager()
        menubar = ui_manager.get_widget("/MenuBar")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)

        self.grid = Gtk.Fixed()

        box.pack_start(self.grid, True, True, 0)
        self.add(box)

    def create_ui_manager(self):
        ui_manager = Gtk.UIManager()
        ui_manager.add_ui_from_string(UI_INFO)
        accelgroup = ui_manager.get_accel_group()
        self.add_accel_group(accelgroup)
        action_group = Gtk.ActionGroup()
        self.add_file_menu_actions(action_group)
        self.add_edit_menu_actions(action_group)
        self.add_about_menu_actions(action_group)
        ui_manager.insert_action_group(action_group)
        return ui_manager

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", 'Меню')
        action_group.add_action(action_filemenu)
        action_filequit = Gtk.Action("FileQuit", 'Выход', None, Gtk.STOCK_QUIT)
        action_group.add_action(action_filequit)
        action_filequit.connect("activate", Gtk.main_quit)

    def add_edit_menu_actions(self, action_group):
        action_editmenu = Gtk.Action("EditMenu", "Настройки")
        action_group.add_action(action_editmenu)
        action_about = Gtk.Action("NetworkSettings", 'Настройки сети', None, None)
        action_group.add_action(action_about)

    def add_about_menu_actions(self, action_group):
        action_aboutmenu = Gtk.Action("AboutMenu", 'Справка')
        action_group.add_action(action_aboutmenu)
        action_about = Gtk.Action("About", 'О программе', None, Gtk.STOCK_ABOUT)
        action_group.add_action(action_about)


if __name__ == '__main__':
    window = Window()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()