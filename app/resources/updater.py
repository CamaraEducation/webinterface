from Tkinter import *
import ttk
import json
import tkMessageBox
import tkFileDialog
import shutil
import os
import math

name_lists = {"resource": [], "subject": []}
subject_name_list = []

image_dir = "../images"

edit_or_delete = None

res_or_sub = "resource"

education_levels = ["Primary", "Secondary", "Tertiary"]

file_locations = []
other_image_dir = None

class PasswordDialog(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self)
        self.parent = parent
        self.parent.password = ""
        container = Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        if self.parent.password_success:
            Label(self, text="Password incorrect.", fg="red", justify=LEFT).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.parent.password_success = False

        Label(self, text="The CamaraAdmin password is required to save changes to the Camara Resource Compendium.", wraplength=220, justify=LEFT).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        Label(self, text="Password:").grid(row=2, column=0, padx=(10, 5), pady=10)
        self.entry = Entry(self, show='*')
        self.entry.bind("<KeyRelease-Return>", self.StorePassEvent)
        self.entry.grid(row=2, column=1, padx=(0, 10), pady=10)
        self.button = Button(self, text="Submit", command=self.StorePass)
        self.button.grid(row=3, column=1, padx=(0, 5), pady=10, sticky=E)

    def StorePassEvent(self, event):
        self.StorePass()

    def StorePass(self):
        self.parent.password = self.entry.get()
        self.parent.password_success = True
        self.destroy()

class UpdaterApp(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)

        global chosen_items
        chosen_items = {"resource": {}, "subject": {}}
        global chosen_indices
        chosen_indices = {"resource": None, "subject": None}

        global resource_list_file
        resource_list_file = open("software_list.json", "r")

        global resource_list_data
        resource_list_data = json.load(resource_list_file)

        resource_list_file.close()

        global file_locations
        global other_image_dir
        current_dir = os.getcwd()
        file_locations.append("./software_list.json")
        if "camaraadmin" in current_dir:
            if os.path.exists(current_dir.replace("camaraadmin", "camara")):
                file_locations.append(current_dir.replace("camaraadmin", "camara") + "/software_list.json")
                other_image_dir = current_dir.replace("camaraadmin", "camara") + "/../images"
        elif os.path.exists(current_dir.replace("camara", "camaraadmin")):
            file_locations.append(current_dir.replace("camara", "camaraadmin") + "/software_list.json")
            other_image_dir = current_dir.replace("camara", "camaraadmin") + "/../images"

        container = Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (FrontPage, ChooseItem, AddOrEditResource, AddOrEditSubject):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FrontPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

    def close_updater(self):
        global resource_list_file
        resource_list_file.close()
        print("Closed!")
        self.quit();

class FrontPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="What do you want to change?")
        label.pack()

        edit_resource_button = Button(self, text="Edit Resource", command=lambda: self.edit_or_delete_resource_router(controller, "edit"))
        edit_resource_button.pack()

        add_resource_button = Button(self, text="Add Resource", command=lambda: controller.show_frame(AddOrEditResource))
        add_resource_button.pack()

        remove_resource_button = Button(self, text="Remove Resource", command=lambda: self.edit_or_delete_resource_router(controller, "delete"))
        remove_resource_button.pack()

        edit_subject_button = Button(self, text="Edit Subject", command=lambda: self.edit_or_delete_subject_router(controller, "edit"))
        edit_subject_button.pack()

        add_subject_button = Button(self, text="Add Subject", command=lambda: controller.show_frame(AddOrEditSubject))
        add_subject_button.pack()

        remove_subject_button = Button(self, text="Remove Subject", command=lambda: self.edit_or_delete_subject_router(controller, "delete"))
        remove_subject_button.pack()

        close_button = Button(self, text="Close", command=controller.close_updater)
        close_button.pack()

    def edit_or_delete_resource_router(self, controller, route):
        global edit_or_delete
        edit_or_delete = route
        global res_or_sub
        res_or_sub = "resource"
        controller.show_frame(ChooseItem)

    def add_resource(self):
        print("Resource added")

    def edit_or_delete_subject_router(self, controller, route):
        global edit_or_delete
        edit_or_delete = route
        global res_or_sub
        res_or_sub = "subject"
        controller.show_frame(ChooseItem)

class ChooseItem(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", lambda event, arg=controller: self.on_show_frame(event, arg))

        self.dropdown_label = Label(self, text="Resource:")
        self.dropdown_label.grid(row=0, column=0, sticky=W)

        self.selection_dropdown = ttk.Combobox(self)
        self.selection_dropdown.grid(row=0, column=1, sticky=W)

        back_button = Button(self, text="Back", command=lambda: controller.show_frame(FrontPage), repeatdelay=500)
        back_button.grid(row=1, column=0)

        self.edit_or_delete_resource_button = None

    def edit_or_delete_resource_action(self, controller, selected_item, res_or_sub):
        global edit_or_delete
        global chosen_items
        chosen_items[res_or_sub] = {}
        global chosen_indices
        chosen_indices[res_or_sub] = None
        for index, curr_resource in enumerate(resource_list_data[unicode(res_or_sub+"s")]):
            if curr_resource[u'name'] == unicode(selected_item):
                chosen_items[res_or_sub] = curr_resource
                chosen_indices[res_or_sub] = index
                break

        if(chosen_items[res_or_sub]):
            self.selection_dropdown.set("")
            if edit_or_delete == "edit":
                edit_or_delete = None
                if res_or_sub == "resource":
                    controller.show_frame(AddOrEditResource)
                elif res_or_sub == "subject":
                    controller.show_frame(AddOrEditSubject)
            elif edit_or_delete == "delete":
                edit_or_delete = None
                response = tkMessageBox.askokcancel("Delete "+res_or_sub.title(), ("Are you sure you want to delete "+selected_item+"?"), default=tkMessageBox.CANCEL)
                if response:
                    resource_list_data[unicode(res_or_sub+"s")].pop(chosen_indices[res_or_sub])
                    resource_list_file.seek(0)
                    resource_list_file.truncate()
                    json.dump(resource_list_data, resource_list_file, indent=2)
                    name_lists[res_or_sub].remove(selected_item)
                    chosen_items[res_or_sub] = {}
                    chosen_indices[res_or_sub] = None
                    controller.show_frame(FrontPage)
        else:
            tkMessageBox.showwarning("Alert", res_or_sub.title()+" not found")

    def on_show_frame(self, event, controller):
        global res_or_sub
        global name_lists

        self.dropdown_label['text'] = res_or_sub.title()+":"

        if not name_lists[res_or_sub]:
            global resource_list_data
            for r in resource_list_data[unicode(res_or_sub+"s")]:
                name_lists[res_or_sub].append(str(r[u'name']))
            name_lists[res_or_sub] = sorted(name_lists[res_or_sub], key=lambda s: s.lower())

        self.selection_dropdown['values'] = name_lists[res_or_sub]

        global edit_or_delete

        if self.edit_or_delete_resource_button:
            self.edit_or_delete_resource_button.grid_remove()
        if edit_or_delete == "edit":
            self.edit_or_delete_resource_button = Button(self, text="Edit", command=lambda: self.edit_or_delete_resource_action(controller, self.selection_dropdown.get(), res_or_sub), repeatdelay=500)
            self.edit_or_delete_resource_button.grid(row=1, column=1)
        elif edit_or_delete == "delete":
            self.edit_or_delete_resource_button = Button(self, text="Delete", command=lambda: self.edit_or_delete_resource_action(controller, self.selection_dropdown.get(), res_or_sub), repeatdelay=500)
            self.edit_or_delete_resource_button.grid(row=1, column=1)
        else:
            edit_or_delete = None
            controller.show_frame(FrontPage)

class AddOrEditResource(Frame):
    global chosen_items

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.new_image_filenames = {"icon": None, "screenshot": None}
        self.full_screenshot = None

        self.bind("<<ShowFrame>>", self.on_show_frame)

        Label(self, text="Name:").grid(row=0, column=0, sticky=W)

        self.name_box = Entry(self)
        self.name_box.grid(sticky=W, row=0, column=1, columnspan=2)

        Label(self, text="Subject:").grid(row=1, column=0, sticky=W)

        self.subject_dropdown = ttk.Combobox(self, state='readonly')
        self.subject_dropdown.grid(sticky=W, row=1, column=1, columnspan=2)

        self.image_label = None

        self.change_icon_button = Button(self, text="Change Icon", command=lambda: self.set_new_image("icon"))
        self.change_icon_button.grid(row=2, column=3)

        Label(self, text="Description:").grid(sticky=W, row=2, column=0)
        self.description_box = Text(self, width=60, height=4, wrap=WORD)
        self.description_box.grid(row=3, column=0, columnspan=4)

        Label(self, text="Level(s):").grid(sticky=W, row=4, column=0, pady=5)

        global education_levels
        self.level_checkboxes = [None]*len(education_levels)
        self.level_checkbox_values = []

        for i in range(len(education_levels)):
            self.level_checkbox_values.append(IntVar())

        for index, level in enumerate(education_levels):
            self.level_checkboxes[index] = Checkbutton(self, text=level, variable=self.level_checkbox_values[index])
            self.level_checkboxes[index].grid(sticky=W, row=4, column=(index+1), pady=5)

        Label(self, text="Screenshot (click to enlarge):").grid(sticky=W, row=5, column=0)

        self.change_screenshot_button = Button(self, text="Change Screenshot", command=lambda: self.set_new_image("screenshot"))
        self.change_screenshot_button.grid(sticky=E, row=7, column=3, pady=5)

        self.screenshot_button = None

        self.cancel_button = Button(self, text="Cancel", command=lambda: self.cancel_actions(controller))
        self.cancel_button.grid(sticky=E, row=8, column=2)

        self.save_button = Button(self, text="Save", command=lambda: self.save_changes(controller))
        self.save_button.grid(sticky=E, row=8, column=3)

    def show_full_screenshot(self):
        top = Toplevel()
        top.title("Full-size screenshot")

        if self.full_screenshot:
            self.full_screenshot.destroy()

        self.full_screenshot = Label(top, image=self.original_screenshot)
        self.full_screenshot.pack()

    def set_new_image(self, im_type):
        im_subdir = image_dir + "/app_" + im_type + "s/"
        image_filetypes = (
            ("PNG files", "*.png"),
            ("GIF files", "*.gif")
        );
        image_filepath = tkFileDialog.askopenfilename(title=("Select New "+im_type.title()), initialdir="/home/camaraadmin/Pictures", filetypes=image_filetypes)
        if image_filepath:
            if self.new_image_filenames[im_type]:
                os.remove(im_subdir+self.new_image_filenames[im_type])
            self.new_image_filenames[im_type] = os.path.basename(image_filepath)

            if unicode(im_type) in chosen_items["resource"] and (self.new_image_filenames[im_type] == str(chosen_items["resource"][unicode(im_type)])):
                self.new_image_filenames[im_type] = os.path.splitext(self.new_image_filenames[im_type])[0] + "0" + os.path.splitext(self.new_image_filenames[im_type])[1]
            if self.new_image_filenames[im_type] == "no_"+im_type+".png":
                self.new_image_filenames[im_type] = os.path.splitext(self.new_image_filenames[im_type])[0] + "0" + os.path.splitext(self.new_image_filenames[im_type])[1]

            shutil.copyfile(image_filepath, (im_subdir+self.new_image_filenames[im_type]))
            new_image = PhotoImage(file=(im_subdir+self.new_image_filenames[im_type]))
            if im_type=="icon":
                self.set_icon(new_image)
            elif im_type=="screenshot":
                self.set_screenshot(new_image)

    def set_icon(self, icon_image):
        if self.image_label is not None:
            self.image_label.grid_remove()

        self.image_label = Label(self, image=icon_image)
        self.image_label.image = icon_image
        self.image_label.grid(row=0, column=3, columnspan=2, rowspan=2)

    def set_screenshot(self, screenshot_image):
        if self.screenshot_button is not None:
            self.screenshot_button.grid_remove()

        self.original_screenshot = screenshot_image
        reduction_factor = int(max(math.ceil(screenshot_image.width()/360.0), math.ceil(screenshot_image.height()/180.0)))
        screenshot_image = screenshot_image.subsample(reduction_factor, reduction_factor)
        self.screenshot_button = Button(self, image=screenshot_image, command=self.show_full_screenshot, relief=FLAT)
        self.screenshot_button.image = screenshot_image
        self.screenshot_button.grid(row=6, column=0, columnspan=4)

    def clear_info(self):
        self.name_box.delete(0, END)
        self.description_box.delete("1.0", END)
        self.subject_dropdown.set("")

        for im_type in ["icon", "screenshot"]:
            if self.new_image_filenames[im_type]:
                os.remove(image_dir+"/app_"+im_type+"s/"+self.new_image_filenames[im_type])
                self.new_image_filenames[im_type] = None

        for checkbox in self.level_checkboxes:
            checkbox.deselect()

        if self.image_label is not None:
            self.image_label.grid_remove()
        if self.screenshot_button is not None:
            self.screenshot_button.grid_remove()

        global chosen_items
        global chosen_indices
        chosen_items["resource"] = {}
        chosen_indices["resource"] = None

    def cancel_actions(self, controller):
        self.clear_info()
        controller.show_frame(FrontPage)

    def on_show_frame(self, event):
        if u'name' in chosen_items["resource"]:
            self.name_box.insert(0, chosen_items["resource"][u'name'])
        if u'description' in chosen_items["resource"]:
            self.description_box.insert(END, chosen_items["resource"][u'description'])
        if u'category' in chosen_items["resource"]:
            self.subject_dropdown.set(str(chosen_items["resource"][u'category']))

        global subject_name_list
        self.check_subject_list()
        self.subject_dropdown['values'] = subject_name_list

        app_ims = {}
        for im_type in ["icon", "screenshot"]:
            im_subdir = image_dir + "/app_" + im_type + "s/"
            if unicode(im_type) in chosen_items["resource"]:
                im_path = im_subdir+str(chosen_items["resource"][unicode(im_type)])
                if os.path.exists(im_path):
                    app_ims[im_type] = PhotoImage(file=im_path)
                else:
                    del chosen_items["resource"][unicode(im_type)]
                    app_ims[im_type] = PhotoImage(file=(im_subdir+"no_"+im_type+".png"))
            else:
                app_ims[im_type] = PhotoImage(file=(im_subdir+"no_"+im_type+".png"))

        #App icon label
        self.set_icon(app_ims["icon"])

        #App screenshot button
        self.set_screenshot(app_ims["screenshot"])

        global education_levels
        if u'level' in chosen_items["resource"]:
            for level in chosen_items["resource"][u'level']:
                self.level_checkboxes[education_levels.index(str(level))].select()

    def GetPassword(self):
        self.wait_window(PasswordDialog(self))

    def save_changes(self, controller):
        global name_lists
        global resource_list_data
        global chosen_items
        global chosen_indices
        global file_locations
        global other_image_dir

        name = self.name_box.get().lstrip()

        if name.isspace() or (not name):
            tkMessageBox.showerror("ALERT", "Cannot save resource without name")
            return
        if name in name_lists["resource"]:
            if u'name' not in chosen_items["resource"] or name != chosen_items["resource"][u'name']:
                tkMessageBox.showerror("ALERT", "A resource with that name already exists")
                return

        correct_password = False
        self.password_success = False

        while not correct_password:
            self.GetPassword()
            if not self.password_success:
                return
            res = os.system('echo %s | sudo -S -v' %(self.password))
            if res == 0:
                correct_password = True

        if chosen_indices["resource"] is not None:
            name_lists["resource"][name_lists["resource"].index(str(chosen_items["resource"][u'name']))] = name
        else:
            name_lists["resource"].append(name)

        name_lists["resource"] = sorted(name_lists["resource"], key=lambda s: s.lower())

        chosen_items["resource"][u'name'] = unicode(name)

        for im_type in ["icon", "screenshot"]:
            if self.new_image_filenames[im_type]:
                im_location = image_dir+"/app_"+im_type+"s/"
                if other_image_dir is not None:
                    other_im_location = other_image_dir+"/app_"+im_type+"s/"
                if unicode(im_type) in chosen_items["resource"] and (str(chosen_items["resource"][unicode(im_type)]) != ("no_"+im_type+".png")):
                    os.remove(im_location+str(chosen_items["resource"][unicode(im_type)]))
                    if other_image_dir is not None:
                        os.system('echo %s | sudo -S %s ' %(self.password, "rm "+other_im_location+str(chosen_items["resource"][unicode(im_type)])))
                chosen_items["resource"][unicode(im_type)] = unicode(self.new_image_filenames[im_type])
                if other_image_dir is not None:
                    os.system('echo %s | sudo -S %s ' %(self.password, "cp "+im_location+self.new_image_filenames[im_type]+" "+other_im_location+self.new_image_filenames[im_type]))
                    self.new_image_filenames[im_type] = None
            else:
                if not unicode(im_type) in chosen_items["resource"]:
                    chosen_items["resource"][unicode(im_type)] =unicode("no_"+im_type+".png")

        chosen_items["resource"][u'category'] = unicode(self.subject_dropdown.get())
        chosen_items["resource"][u'description'] = unicode(self.description_box.get(1.0, 'end-1c'))

        global education_levels
        chosen_items["resource"][u'level'] = []
        for index, checkbox_value in enumerate(self.level_checkbox_values):
            if checkbox_value.get() == 1:
                chosen_items["resource"][u'level'].append(unicode(education_levels[index]))

        if chosen_indices["resource"] is not None:
            resource_list_data[u'resources'][chosen_indices["resource"]] = chosen_items["resource"]
        else:
            resource_list_data[u'resources'].append(chosen_items["resource"])

        temp_file = open("./temp_software_list.json", "w")
        json.dump(resource_list_data, temp_file, indent=2)
        temp_file.close()

        saved = False
        file_results = 0
        for file_loc in file_locations:
            file_results += os.system('echo %s | sudo -S %s ' %(self.password, "cp ./temp_software_list.json "+file_loc))
        if file_results == 0:
            saved = True
        os.system('sudo -K')

        if not saved:
            tkMessageBox.showerror("ALERT", "Error occurred when saving.")
            return

        message = ""
        if chosen_indices["resource"] is not None:
            message = "Changes to " + str(chosen_items["resource"][u'name']) + " have been saved."
        else:
            message = "The new resource, " + str(chosen_items["resource"][u'name']) + " has been added."

        tkMessageBox.showinfo("Resource Saved", message)

        self.clear_info()

        controller.show_frame(FrontPage)

    def check_subject_list(self):
        global subject_name_list

        if not subject_name_list:
            for s in resource_list_data[u'subjects']:
                subject_name_list.append(str(s[u'name']))

class AddOrEditSubject(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", self.on_show_frame)

        self.new_image_filename = None

        Label(self, text="Name:").grid(row=0, column=0, sticky=W)

        self.name_entry_box = Entry(self)
        self.name_entry_box.grid(row=0, column=1, sticky=W)

        self.image_label = None

        self.change_icon_button = Button(self, text="Change Icon", command=self.set_new_image)
        self.change_icon_button.grid(row=2, column=3)


        self.cancel_button = Button(self, text="Cancel", command=lambda: self.cancel_actions(controller))
        self.cancel_button.grid(sticky=E, row=3, column=2)

        self.save_button = Button(self, text="Save", command=lambda: self.save_changes(controller))
        self.save_button.grid(sticky=E, row=3, column=3)


    def clear_data(self):
        self.name_entry_box.delete(0, END)

        if self.new_image_filename:
            os.remove(image_dir+"/interface_icons/"+self.new_image_filename)
            self.new_image_filename = None

        if self.image_label is not None:
            self.image_label.grid_remove()

        global chosen_items
        global chosen_indices
        chosen_items["subject"] = {}
        chosen_indices["subject"] = None

    def cancel_actions(self, controller):
        self.clear_data()
        controller.show_frame(FrontPage)

    def set_icon(self, icon_image):
        if self.image_label is not None:
            self.image_label.grid_remove()

        self.image_label = Label(self, image=icon_image)
        self.image_label.image = icon_image
        self.image_label.grid(row=0, column=3, columnspan=3, rowspan=2)

    def on_show_frame(self, event):
        if u'name' in chosen_items["subject"]:
            self.name_entry_box.insert(0, chosen_items["subject"][u'name'])

        im_subdir = image_dir + "/interface_icons/"
        app_im = None
        if u'icon' in chosen_items["subject"]:
            im_path = im_subdir+str(chosen_items["subject"][u'icon'])
            if os.path.exists(im_path):
                app_im = PhotoImage(file=im_path)
            else:
                del chosen_items["subject"][u'icon']
                app_im = PhotoImage(file=(im_subdir+"Symbolsmall.png"))
        else:
            app_im = PhotoImage(file=(im_subdir+"Symbolsmall.png"))

        #App icon label
        self.set_icon(app_im)

    def set_new_image(self):
        im_subdir = image_dir + "/interface_icons/"
        image_filetypes = (
            ("PNG files", "*.png"),
            ("GIF files", "*.gif")
        );
        image_filepath = tkFileDialog.askopenfilename(title="Select New Icon", initialdir="/home/camaraadmin/Pictures", filetypes=image_filetypes)
        if image_filepath:
            if self.new_image_filename:
                os.remove(image_dir+"/interface_icons/"+self.new_image_filename)
            self.new_image_filename = os.path.basename(image_filepath)

            if u'icon' in chosen_items["subject"] and (self.new_image_filename == str(chosen_items["subject"][u'icon'])):
                self.new_image_filename = os.path.splitext(self.new_image_filename)[0] + "0" + os.path.splitext(self.new_image_filename)[1]
            if self.new_image_filename == "Symbolsmall.png":
                self.new_image_filename = os.path.splitext(self.new_image_filename)[0] + "0" + os.path.splitext(self.new_image_filename)[1]

            shutil.copyfile(image_filepath, (im_subdir+self.new_image_filename))
            new_image = PhotoImage(file=(im_subdir+self.new_image_filename))
            self.set_icon(new_image)

    def GetPassword(self):
        self.wait_window(PasswordDialog(self))

    def save_changes(self, controller):
        global name_lists
        global resource_list_data
        global chosen_items
        global chosen_indices
        global other_image_dir

        name = self.name_entry_box.get().lstrip().title()

        if name.isspace() or (not name):
            tkMessageBox.showerror("ALERT", "Cannot save subject without name")
            return
        if name in name_lists["subject"]:
            if u'name' not in chosen_items["subject"] or name != chosen_items["subject"][u'name']:
                tkMessageBox.showerror("ALERT", "A subject with that name already exists")
                return

        correct_password = False
        self.password_success = False

        while not correct_password:
            self.GetPassword()
            if not self.password_success:
                return
            res = os.system('echo %s | sudo -S -v' %(self.password))
            if res == 0:
                correct_password = True

        if chosen_indices["subject"] is not None:
            name_lists["subject"][name_lists["subject"].index(str(chosen_items["subject"][u'name']))] = name
        else:
            name_lists["subject"].append(name)

        name_lists["subject"] = sorted(name_lists["subject"], key=lambda s: s.lower())

        chosen_items["subject"][u'name'] = unicode(name)

        if self.new_image_filename:
            im_location = image_dir+"/interface_icons/"
            if other_image_dir is not None:
                other_im_location = other_image_dir+"/interface_icons/"
            if u'icon' in chosen_items["subject"] and (str(chosen_items["subject"][u'icon']) != ("Symbolsmall.png")):
                os.remove(im_location+str(chosen_items["subject"][u'icon']))
                if other_image_dir is not None:
                    os.system('echo %s | sudo -S %s ' %(self.password, "rm "+other_im_location+str(chosen_items["resource"][u'icon'])))
            chosen_items["subject"][u'icon'] = unicode(self.new_image_filename)
            if other_image_dir is not None:
                os.system('echo %s | sudo -S %s ' %(self.password, "cp "+im_location+self.new_image_filename+" "+other_im_location+self.new_image_filename))
            self.new_image_filename = None
        else:
            if not u'icon' in chosen_items["subject"]:
                chosen_items["subject"][u'icon'] =unicode("Symbolsmall.png")

        if chosen_indices["subject"] is not None:
            resource_list_data[u'subjects'][chosen_indices["subject"]] = chosen_items["subject"]
        else:
            resource_list_data[u'subjects'].append(chosen_items["subject"])

        temp_file = open("./temp_software_list.json", "w")
        json.dump(resource_list_data, temp_file, indent=2)
        temp_file.close()

        saved = False
        file_results = 0
        for file_loc in file_locations:
            file_results += os.system('echo %s | sudo -S %s ' %(self.password, "cp ./temp_software_list.json "+file_loc))
        if file_results == 0:
            saved = True
        os.system('sudo -K')

        if not saved:
            tkMessageBox.showerror("ALERT", "Error occurred when saving.")
            return

        message = ""
        if chosen_indices["subject"] is not None:
            message = "Changes to " + str(chosen_items["subject"][u'name']) + " have been saved."
        else:
            message = "The new subject, " + str(chosen_items["subject"][u'name']) + " has been added."

        tkMessageBox.showinfo("Subject Saved", message)

        self.clear_data()

        controller.show_frame(FrontPage)





root = UpdaterApp()

def on_closing():
    os.remove("./temp_software_list.json")
    print("Closed!")
    root.destroy()

root.wm_protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
