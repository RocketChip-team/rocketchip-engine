import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk

class Handler:
    def __init__(self):
        self.data = [(255, 255, 255),(255, 255, 255),(255, 255, 255),(255, 255, 255),(255, 255, 255),(255, 255, 255),(255, 255, 255),(255, 255, 255)]
        self.file_path = None

    def onDestroy(self, *args):
        Gtk.main_quit()

    def new_file(self, button):
        color = Gdk.RGBA()
        color.red = 0.0
        color.green = 0.0
        color.blue = 0.0
        color.alpha = 1.0
        for i in range(1,9):
            button = builder.get_object("button"+str(i))
            button.set_rgba(color)
        self.file_path = None
        self.data = []
        for y in range(1, 9):
            self.data.append((255, 255, 255))

    def open_file(self, path):
        with open(path, "r") as file:
            data = file.read()
            print(data)
            temp = []
            for y in range(0, 8):
                temp.append((int(data[y*9+0:y*9+0+3]),int(data[y*9+3:y*9+3+3]), int(data[y*9+6:y*9+6+3])))
            print(temp)
            self.data = temp
            #reinitialize colors of colrbuttons
            for i in range(1,9):
                print("i :",i)
                color = Gdk.RGBA()
                color.alpha = 1.0
                print(self.data[i-1])
                color.parse("rgb("+str(self.data[i-1][0])+","+str(self.data[i-1][1])+","+str(self.data[i-1][2])+")")
                button = builder.get_object("button"+str(i))
                button.set_rgba(color)



    def on_file_clicked(self, button):
        dialog = Gtk.FileChooserDialog("Please choose a file", builder.get_object("main_window"),
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            self.file_path = dialog.get_filename()
            self.open_file(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name(".pal files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Text files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def save(self, button):
        print(self.data)
        print(self.file_path)
        if self.file_path != None:
            with open(self.file_path, "w") as file:
                try:
                    for y in range(0, len(self.data)):
                        for x in range(0, len(self.data[y])):
                            data = str(self.data[y][x])
                            if len(data) == 1:
                                data = "00"+data
                            elif len(data) == 2:
                                data = "0"+data
                            file.write(data)
                    file.write("this data and the programs associated with it are made by Rocket-chip team, DON'T STEAL THEM, and credit us")
                except:
                    print("Probleme")
        else:
            no_file_dialog.run()
            no_file_dialog.hide()

    def on_save_as_clicked(self, button):
        file_dialog.run()
        file_dialog.hide()

    def on_dialog_save_clicked(self,button):
        if builder.get_object("file_name_input").get_text() != "":
            self.file_path = file_dialog.get_current_folder()+"/"+builder.get_object("file_name_input").get_text()+".pal"
            self.save(None)
            file_dialog.hide()
        else:
            no_file_dialog.run()
            no_file_dialog.hide()

    def on_color_set(self, button):
        data_tuple = button.get_rgba().to_string().split("(")
        data_tuple = data_tuple[1].split(")")
        data_tuple = data_tuple[0].split(",")
        r = int(data_tuple[0])
        g = int(data_tuple[1])
        b = int(data_tuple[2])
        final_tuple = (r,g,b)
        self.data[int(button.get_name()[len(button.get_name())-1])-1] = final_tuple

    def on_gtk_about_activate(self, menuitem, data=None):
        print(self.file_path)
        print(self.data)
        print("help about selected")
        response = aboutdialog.run()
        aboutdialog.hide()

    def close_no_file_dialog(self, button):
        no_file_dialog.hide()


if __name__ == "__main__":

    #add ui from an xml file
    builder = Gtk.Builder()
    builder.add_from_file("Uis/palette_editor.ui")
    builder.connect_signals(Handler())

    #add main window
    window = builder.get_object("main_window")
    window.set_default_size(750, 200)

    #add about dialog
    aboutdialog = builder.get_object("about_dialog")

    #add file chooser
    file_dialog = builder.get_object("file_chooser_dialog")
    no_file_dialog = builder.get_object("no_file_dialog")

    #init window
    window.show_all()

    #main loop
    Gtk.main()
