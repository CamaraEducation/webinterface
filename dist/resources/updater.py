from Tkinter import *       #GUI module
import ttk                  #Themed widget module
import json                 #Module for handling json files & data
import tkMessageBox         #Module for simple message box
import tkFileDialog         #Module for dialog for choosing files on computer. Used for choosing new images
import shutil               #Module for high-level file operations. Only used in about two places, could be removed
import os                   #Module for os interfacing
import math                 #You don't need me to tell you what this is for

#Setting up some global variables
name_lists = {"resource": [], "subject": []}
subject_name_list = []

image_dir = "../images"

edit_or_delete = None

res_or_sub = "resource"

education_levels = ["Primary", "Secondary", "Tertiary"]

other_file_location = None
other_image_dir = None

chosen_items = {"resource": {}, "subject": {}}
chosen_indices = {"resource": None, "subject": None}

#Class to handle a password dialog, which is needed for saving changes.
class PasswordDialog(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self)
        self.parent = parent
        self.parent.password = ""
        container = Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #If a password was entered previously, but they're back here, let the user know the password was wrong
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
        Button(self, text="Cancel", command=self.destroy).grid(row=3, column=0, padx=(5,0), pady=10, sticky=E)

    def StorePassEvent(self, event):
        self.StorePass()

    def StorePass(self):
        self.parent.password = self.entry.get()
        self.parent.password_success = True
        self.destroy()

class UpdaterApp(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        #Get the current file
        global resource_list_file
        resource_list_file = open("software_list.json", "r")
        #Get the current data
        global resource_list_data
        resource_list_data = json.load(resource_list_file)

        resource_list_file.close()

        #Need to make sure that if this is on both the camara and camaraadmin accounts that both are updated
        global other_file_location
        global other_image_dir
        current_dir = os.getcwd()
        if "camaraadmin" in current_dir:
            if os.path.exists(current_dir.replace("camaraadmin", "camara")):
                other_file_location = current_dir.replace("camaraadmin", "camara") + "/software_list.json"
                other_image_dir = current_dir.replace("camaraadmin", "camara") + "/../images"
        elif os.path.exists(current_dir.replace("camara", "camaraadmin")):
            other_image_dir = current_dir.replace("camara", "camaraadmin") + "/../images"
            other_file_location = current_dir.replace("camara", "camaraadmin") + "/software_list.json"

        #Setting up the different frames of the application
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

    #Change what's on top
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

    #Handle closing the application.
    def close_updater(self):
        self.quit();

#Landing page of the application
class FrontPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="What do you want to change?")
        label.pack()

        #Buttons for the various options
        edit_resource_button = Button(self, text="Edit Resource", command=lambda: self.edit_or_delete_router(controller, "edit", "resource"))
        edit_resource_button.pack()

        add_resource_button = Button(self, text="Add Resource", command=lambda: controller.show_frame(AddOrEditResource))
        add_resource_button.pack()

        remove_resource_button = Button(self, text="Remove Resource", command=lambda: self.edit_or_delete_router(controller, "delete", "resource"))
        remove_resource_button.pack()

        edit_subject_button = Button(self, text="Edit Subject", command=lambda: self.edit_or_delete_router(controller, "edit", "subject"))
        edit_subject_button.pack()

        add_subject_button = Button(self, text="Add Subject", command=lambda: controller.show_frame(AddOrEditSubject))
        add_subject_button.pack()

        remove_subject_button = Button(self, text="Remove Subject", command=lambda: self.edit_or_delete_router(controller, "delete", "subject"))
        remove_subject_button.pack()

        close_button = Button(self, text="Close", command=controller.close_updater)
        close_button.pack()

    #Gathers some info for the next frame
    def edit_or_delete_router(self, controller, route, resource_or_subject):
        global edit_or_delete
        edit_or_delete = route
        global res_or_sub
        res_or_sub = resource_or_subject
        controller.show_frame(ChooseItem)

#Choose the subject/resource for editing/deletion
class ChooseItem(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        #When the frame is displayed, the 'on_show_frame' event handler sets up the appropriate info
        self.bind("<<ShowFrame>>", lambda event, arg=controller: self.on_show_frame(event, arg))

        self.dropdown_label = Label(self, text="Resource:")
        self.dropdown_label.grid(row=0, column=0, sticky=W)

        self.selection_dropdown = ttk.Combobox(self)
        self.selection_dropdown.grid(row=0, column=1, sticky=W)

        back_button = Button(self, text="Back", command=lambda: controller.show_frame(FrontPage), repeatdelay=500)
        back_button.grid(row=1, column=0)

        self.edit_or_delete_resource_button = None

    #Once an item has been selected, this handles what needs to be done
    def edit_or_delete_resource_action(self, controller, selected_item, res_or_sub):
        #Global variables for gleaning and setting info
        global edit_or_delete
        global chosen_items
        chosen_items[res_or_sub] = {}
        global chosen_indices
        chosen_indices[res_or_sub] = None
        #Search through the resource and subject data to find the item in question
        for index, curr_resource in enumerate(resource_list_data[unicode(res_or_sub+"s")]):
            if curr_resource[u'name'] == unicode(selected_item):
                chosen_items[res_or_sub] = curr_resource
                chosen_indices[res_or_sub] = index
                break

        if(chosen_items[res_or_sub]):
            #Clear the dropdown selection
            self.selection_dropdown.set("")
            #Choose the correct edit frame
            if edit_or_delete == "edit":
                edit_or_delete = None
                if res_or_sub == "resource":
                    controller.show_frame(AddOrEditResource)
                elif res_or_sub == "subject":
                    controller.show_frame(AddOrEditSubject)
            #Handle deleting the item
            #Todo: it would be nice to add here a warning when deleting a subject if resources list that subject as their category
            #Todo: if the subject/resource has its own (non-default) image, the image ought to be removed
            elif edit_or_delete == "delete":
                #Always good to ask for confirmation before deleting
                response = tkMessageBox.askokcancel("Delete "+res_or_sub.title(), ("Are you sure you want to delete "+selected_item+"?"), default=tkMessageBox.CANCEL)
                if response:
                    #A user needs to have the admin password to delete a resource or subject
                    correct_password = False
                    self.password_success = False

                    while not correct_password:
                        self.wait_window(PasswordDialog(self))
                        if not self.password_success:
                            return
                        #This effectively acts as a check that the password is correct
                        res = os.system('echo %s | sudo -S -v' %(self.password))
                        if res == 0:
                            correct_password = True

                    #Overwrite the file with the new data
                    resource_list_data[unicode(res_or_sub+"s")].pop(chosen_indices[res_or_sub])
                    resource_file = open("./software_list.json", "w")
                    json.dump(resource_list_data, resource_file, indent=2)
                    resource_file.close()

                    #Copy the file to the other location
                    saved = False
                    global other_file_location
                    if other_file_location is not None:
                        #Sudo is needed to copy to a different user's directory
                        file_results = os.system('echo %s | sudo -S %s ' %(self.password, "cp ./software_list.json "+other_file_location))
                        if file_results == 0:
                            saved = True
                    else:
                        saved = True
                    #Clear the sudo permission and password
                    self.password = ""
                    os.system('sudo -K')

                    if not saved:
                        tkMessageBox.showerror("ALERT", "Error occurred while saving changes.")

                    #Keep the list of subjects/resources up-to-date
                    name_lists[res_or_sub].remove(selected_item)

                    #Clear info
                    chosen_items[res_or_sub] = {}
                    chosen_indices[res_or_sub] = None
                    edit_or_delete = None
                    controller.show_frame(FrontPage)
        else:
            tkMessageBox.showwarning("Alert", res_or_sub.title()+" not found")

    #Event handler to set up the Choose Item variables when Frame is shown
    def on_show_frame(self, event, controller):
        global res_or_sub
        global name_lists

        self.dropdown_label['text'] = res_or_sub.title()+":"

        #If the list of resource/subject names has not get been created, populate it
        if not name_lists[res_or_sub]:
            global resource_list_data
            for r in resource_list_data[unicode(res_or_sub+"s")]:
                name_lists[res_or_sub].append(str(r[u'name']))
            name_lists[res_or_sub] = sorted(name_lists[res_or_sub], key=lambda s: s.lower())

        self.selection_dropdown['values'] = name_lists[res_or_sub]

        global edit_or_delete

        #Set the edit/delete button to have the correct text and functionality
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

#Can handle both editing and creating a resource in the same frame
class AddOrEditResource(Frame):
    global chosen_items

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        #Variables for images
        self.new_image_filenames = {"icon": None, "screenshot": None}
        self.full_screenshot = None

        #Bind event handler for when frame is shown
        self.bind("<<ShowFrame>>", self.on_show_frame)

        #Various widgets need to be added to the frame
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

    #Screenshot is minimized to fit within the small frame, this pops it out to a new window
    def show_full_screenshot(self):
        top = Toplevel()
        top.title("Full-size screenshot")

        if self.full_screenshot:
            self.full_screenshot.destroy()

        self.full_screenshot = Label(top, image=self.original_screenshot)
        self.full_screenshot.pack()

    #Handles setting up a new icon/screenshot image
    #Moves the new image into the correct images subdirectory
    def set_new_image(self, im_type):
        im_subdir = image_dir + "/app_" + im_type + "s/"
        #These are the only two types of image that tkinter can display
        image_filetypes = (
            ("PNG files", "*.png"),
            ("GIF files", "*.gif")
        );
        image_filepath = tkFileDialog.askopenfilename(title=("Select New "+im_type.title()), initialdir="/home/camaraadmin/Pictures", filetypes=image_filetypes)
        if image_filepath:
            #If they've changed the image more than once before saving, the previous "new image" should be removed to keep the subdirectory as clean as possible
            if self.new_image_filenames[im_type]:
                os.remove(im_subdir+self.new_image_filenames[im_type])
            self.new_image_filenames[im_type] = os.path.basename(image_filepath)

            #Don't want to overwrite existing image with an image of the same name
            #Todo: Ideally this should be replaced with a check to see if the subdirectory already contains an image with that name using os.path.exists or os.path.isfile
            if unicode(im_type) in chosen_items["resource"] and (self.new_image_filenames[im_type] == str(chosen_items["resource"][unicode(im_type)])):
                self.new_image_filenames[im_type] = os.path.splitext(self.new_image_filenames[im_type])[0] + "0" + os.path.splitext(self.new_image_filenames[im_type])[1]
            if self.new_image_filenames[im_type] == "no_"+im_type+".png":
                self.new_image_filenames[im_type] = os.path.splitext(self.new_image_filenames[im_type])[0] + "0" + os.path.splitext(self.new_image_filenames[im_type])[1]

            #Todo: Could be done with os.system and a cp command instead. May be better, so shutil can be removed
            shutil.copyfile(image_filepath, (im_subdir+self.new_image_filenames[im_type]))
            new_image = PhotoImage(file=(im_subdir+self.new_image_filenames[im_type]))
            if im_type=="icon":
                self.set_icon(new_image)
            elif im_type=="screenshot":
                self.set_screenshot(new_image)

    #Handles setting a new icon
    def set_icon(self, icon_image):
        if self.image_label is not None:
            self.image_label.grid_remove()

        self.image_label = Label(self, image=icon_image)
        self.image_label.image = icon_image
        self.image_label.grid(row=0, column=3, columnspan=2, rowspan=2)

    #Handles setting a new screenshot
    def set_screenshot(self, screenshot_image):
        if self.screenshot_button is not None:
            self.screenshot_button.grid_remove()

        self.original_screenshot = screenshot_image
        reduction_factor = int(max(math.ceil(screenshot_image.width()/360.0), math.ceil(screenshot_image.height()/180.0)))
        screenshot_image = screenshot_image.subsample(reduction_factor, reduction_factor)
        self.screenshot_button = Button(self, image=screenshot_image, command=self.show_full_screenshot, relief=FLAT)
        self.screenshot_button.image = screenshot_image
        self.screenshot_button.grid(row=6, column=0, columnspan=4)

    #Ronseal
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

    #If cancel button is clicked
    def cancel_actions(self, controller):
        self.clear_info()
        controller.show_frame(FrontPage)

    #Event handler for setting things up when frame is shown
    def on_show_frame(self, event):
        #Fills in pre-existing data
        if u'name' in chosen_items["resource"]:
            self.name_box.insert(0, chosen_items["resource"][u'name'])
        if u'description' in chosen_items["resource"]:
            self.description_box.insert(END, chosen_items["resource"][u'description'])
        if u'category' in chosen_items["resource"]:
            self.subject_dropdown.set(str(chosen_items["resource"][u'category']))

        #Sets up list of possible subjects
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
                    #If the image doesn't exist, delete reference to it, set the icon to the default
                    del chosen_items["resource"][unicode(im_type)]
                    app_ims[im_type] = PhotoImage(file=(im_subdir+"no_"+im_type+".png"))
            else:
                app_ims[im_type] = PhotoImage(file=(im_subdir+"no_"+im_type+".png"))

        self.set_icon(app_ims["icon"])
        self.set_screenshot(app_ims["screenshot"])

        global education_levels
        if u'level' in chosen_items["resource"]:
            for level in chosen_items["resource"][u'level']:
                self.level_checkboxes[education_levels.index(str(level))].select()

    #NGL, this is a bit of a mess and a PITA
    def save_changes(self, controller):
        global name_lists
        global resource_list_data
        global chosen_items
        global chosen_indices
        global other_file_location
        global other_image_dir

        name = self.name_box.get().lstrip()

        #No name, no resource
        if name.isspace() or (not name):
            tkMessageBox.showerror("ALERT", "Cannot save resource without name")
            return
        #Resource names must be unique
        if name in name_lists["resource"]:
            if u'name' not in chosen_items["resource"] or name != chosen_items["resource"][u'name']:
                tkMessageBox.showerror("ALERT", "A resource with that name already exists")
                return

        #Editing/adding resources requires sudo permissions. Check for this before going on
        correct_password = False
        self.password_success = False

        while not correct_password:
            self.wait_window(PasswordDialog(self))
            if not self.password_success:
                #Let users cancel out of password request, to continue editing the resource
                return
            res = os.system('echo %s | sudo -S -v' %(self.password))
            if res == 0:
                correct_password = True

        #Add/ammend name of resource on list of resources
        if chosen_indices["resource"] is not None:
            name_lists["resource"][name_lists["resource"].index(str(chosen_items["resource"][u'name']))] = name
        else:
            name_lists["resource"].append(name)

        #Keep the resource list alphabetical
        name_lists["resource"] = sorted(name_lists["resource"], key=lambda s: s.lower())

        chosen_items["resource"][u'name'] = unicode(name)

        #Handle new images
        for im_type in ["icon", "screenshot"]:
            if self.new_image_filenames[im_type]:
                im_location = image_dir+"/app_"+im_type+"s/"
                if other_image_dir is not None:
                    other_im_location = other_image_dir+"/app_"+im_type+"s/"
                #Check if there's an old image to be removed, and remove it
                if unicode(im_type) in chosen_items["resource"] and (str(chosen_items["resource"][unicode(im_type)]) != ("no_"+im_type+".png")):
                    os.remove(im_location+str(chosen_items["resource"][unicode(im_type)]))
                    #Remove it from the corresponding location in the other user
                    if other_image_dir is not None:
                        os.system('echo %s | sudo -S %s ' %(self.password, "rm "+other_im_location+str(chosen_items["resource"][unicode(im_type)])))
                chosen_items["resource"][unicode(im_type)] = unicode(self.new_image_filenames[im_type])
                if other_image_dir is not None:
                    #Copy image to other user's image directory
                    os.system('echo %s | sudo -S %s ' %(self.password, "cp "+im_location+self.new_image_filenames[im_type]+" "+other_im_location+self.new_image_filenames[im_type]))
                self.new_image_filenames[im_type] = None
            else:
                #If there's no new or pre-existing image, set it to the default
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

        #Overwrite the resource file with the new, up-to-date info
        resource_file = open("./software_list.json", "w")
        json.dump(resource_list_data, resource_file, indent=2)
        resource_file.close()

        #Copy the resource file to the other location
        saved = False
        if other_file_location is not None:
            file_results = os.system('echo %s | sudo -S %s ' %(self.password, "cp ./software_list.json "+other_file_location))
            if file_results == 0:
                saved = True
        else:
            saved = True

        #clear sudo permissions and password
        self.password = ""
        os.system('sudo -K')

        if not saved:
            tkMessageBox.showerror("ALERT", "Error occurred when saving.")
            return

        #Polite note to let the user know changes have been saved
        message = ""
        if chosen_indices["resource"] is not None:
            message = "Changes to " + str(chosen_items["resource"][u'name']) + " have been saved."
        else:
            message = "The new resource, " + str(chosen_items["resource"][u'name']) + " has been added."

        tkMessageBox.showinfo("Resource Saved", message)

        #Clear the info so next time the frame is shown the old info won't still be lingering
        self.clear_info()

        #Back to the front page
        controller.show_frame(FrontPage)

    #Checks that the list is already populated, if not, populates it
    def check_subject_list(self):
        global subject_name_list

        if not subject_name_list:
            for s in resource_list_data[u'subjects']:
                subject_name_list.append(str(s[u'name']))

#Subject is different enough to resource to have its own class for adding/editing
class AddOrEditSubject(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        #Binds event handler from when frame is shown
        self.bind("<<ShowFrame>>", self.on_show_frame)

        self.new_image_filename = None

        #Populating frame with various widgets

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

    #Clear data so next time frame is shown it doesn't have stale data lingering
    def clear_data(self):
        self.name_entry_box.delete(0, END)

        #New image added but not saved should be removed
        if self.new_image_filename:
            os.remove(image_dir+"/interface_icons/"+self.new_image_filename)
            self.new_image_filename = None

        if self.image_label is not None:
            self.image_label.grid_remove()

        global chosen_items
        global chosen_indices
        chosen_items["subject"] = {}
        chosen_indices["subject"] = None

    #Cancelling is a two part operation
    def cancel_actions(self, controller):
        self.clear_data()
        controller.show_frame(FrontPage)

    #Setting the icon image
    def set_icon(self, icon_image):
        if self.image_label is not None:
            self.image_label.grid_remove()

        self.image_label = Label(self, image=icon_image)
        self.image_label.image = icon_image
        self.image_label.grid(row=0, column=3, columnspan=3, rowspan=2)

    #Setting up variables when frame is shown
    def on_show_frame(self, event):
        #Fills in pre-existing data, if it exists

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

    #Todo: there should be a way to combine this and the set_new_image function from AddOrEditResource
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

            #Todo: again, this could be replaced using os.system
            shutil.copyfile(image_filepath, (im_subdir+self.new_image_filename))
            new_image = PhotoImage(file=(im_subdir+self.new_image_filename))
            self.set_icon(new_image)

    #Less bad than the other one, still not pretty
    #Could maybe be combined with other save function?
    #Todo: if subject name changes, update resources with that subject as their category to the new subject name
    def save_changes(self, controller):
        global name_lists
        global resource_list_data
        global chosen_items
        global chosen_indices
        global other_image_dir

        name = self.name_entry_box.get().lstrip().title()

        #No name, no subject
        if name.isspace() or (not name):
            tkMessageBox.showerror("ALERT", "Cannot save subject without name")
            return
        #Subjects must be unique
        if name in name_lists["subject"]:
            if u'name' not in chosen_items["subject"] or name != chosen_items["subject"][u'name']:
                tkMessageBox.showerror("ALERT", "A subject with that name already exists")
                return

        #Going to be saving changes, need sudo permissions
        correct_password = False
        self.password_success = False

        while not correct_password:
            self.wait_window(PasswordDialog(self))
            if not self.password_success:
                return
            res = os.system('echo %s | sudo -S -v' %(self.password))
            if res == 0:
                correct_password = True

        #Update list of subjects to reflect changes
        if chosen_indices["subject"] is not None:
            name_lists["subject"][name_lists["subject"].index(str(chosen_items["subject"][u'name']))] = name
        else:
            name_lists["subject"].append(name)

        name_lists["subject"] = sorted(name_lists["subject"], key=lambda s: s.lower())

        chosen_items["subject"][u'name'] = unicode(name)

        #Set new image and copy to other user's directory, as well as deleting obselete images
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
        #If there's no image, old or new, set the image to the default
        else:
            if not u'icon' in chosen_items["subject"]:
                chosen_items["subject"][u'icon'] =unicode("Symbolsmall.png")

        if chosen_indices["subject"] is not None:
            resource_list_data[u'subjects'][chosen_indices["subject"]] = chosen_items["subject"]
        else:
            resource_list_data[u'subjects'].append(chosen_items["subject"])

        #Overwrite reosurce file with new info
        resource_file = open("./software_list.json", "w")
        json.dump(resource_list_data, resource_file, indent=2)
        resource_file.close()

        #Copy to the other user's location
        saved = False
        if other_file_location is not None:
            file_results = os.system('echo %s | sudo -S %s ' %(self.password, "cp ./software_list.json "+other_file_location))
            if file_results == 0:
                saved = True
        else:
            saved = True

        #Clear sudo permissions and password
        self.password = ""
        os.system('sudo -K')

        if not saved:
            tkMessageBox.showerror("ALERT", "Error occurred when saving.")
            return

        #Let the user know the changes have been saved
        message = ""
        if chosen_indices["subject"] is not None:
            message = "Changes to " + str(chosen_items["subject"][u'name']) + " have been saved."
        else:
            message = "The new subject, " + str(chosen_items["subject"][u'name']) + " has been added."

        tkMessageBox.showinfo("Subject Saved", message)

        #Clean up, clean up, everybody everywhere
        #Clean up, clean up, everybody do your share
        self.clear_data()

        controller.show_frame(FrontPage)



root = UpdaterApp()

#This may no longer be necessary, more stuff used to be done in here
def on_closing():
    root.destroy()

root.wm_protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
