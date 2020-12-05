import wx
import os
import pickle

from metaDataSet import MetaDataSet, Cardinality, Datatype
from metaDataHelpers import CalendarDlg


################# TODO List #################
#
# - more properties, classes
# - call method when something changed in a field; then, call specific validation
# - Add some sort of 'import from RDF' functionality
# - give indication of cardinality in help popup
# - ensure that help popup is always on screen entirely
#
#############################################

################ Idea List ##################
#
# - I'd love to have an over-arching progress bar that indicates to the user, how much of the forms they have filled out
#   (see wx.Gauge)
#
#############################################

def collectMetadata():
    """
    Runner function that launches the app.

    Calling this method initiates a data handler and opens the GUI.
    """
    # create a data handler
    global data_handler
    data_handler = DataHandling()
    # open GUI
    app = wx.App()
    ProjectFrame()
    app.MainLoop()


class DataHandling:
    """ This class handles data.

    It checks for availability in the filesystem, and
    if not, creates the data structure. It also takes care for the storage on disk.
    The data are stored as a pickle file.

    The class should not be called as a static.
    Rather, there should at any given time be an instance of this class (`data_handler`) be available.
    All calls should be done on this instance, as it holds the actual data representation.
    """

    def __init__(self):
        self.current_window = None
        self.projects = []
        self.tabs = []
        self.data_storage = os.path.expanduser(
            "~") + "/DaSCH/config/repos.data"
        # LATER: path could be made customizable
        self.load_data()
        print("Data loaded.")

    def add_project(self, folder_path: str):
        """
        Add a new project.

        This project adds a new project folder to the collection after the user specified the folder.

        The Project is appended at the end of the list.

        Args:
            folder_path (str): path to the project folder
        """
        index = len(self.projects)
        folder_name = os.path.basename(folder_path)
        dataset = MetaDataSet(index, folder_name, folder_path)
        self.projects.append(dataset)
        self.save_data()

    def load_data(self):
        """
        Load data from previous runtimes (if any).

        Currently, this checks `~/DaSCH/config/repos.data`.
        """
        if not os.path.exists(self.data_storage):
            os.makedirs(os.path.dirname(self.data_storage), exist_ok=True)
            return
        with open(self.data_storage, 'rb') as file:
            self.projects = pickle.load(file)
            # LATER: in principal, we could append the data instead of replacing it
            # (for loading multiple data sets and combining them)
            # would have to make sure the indices are correct and no doubles are being added

    def save_data(self):
        """
        Save data to disc.

        Currently, the data are stored under `~/DaSCH/config/repos.data`.
        """
        # LATER: could let the user decide where to store the data.
        print("Saving data...")
        with open(self.data_storage, 'wb') as file:
            pickle.dump(self.projects, file)

    def process_data(self, index: int):
        """
        ToDo: implement this class.
        """
        # TODO: how do process_data and validate_graph really divide labour?
        print(f'Should be processing Dataset: {index}')
        self.validate_graph(self.projects[index])

    def validate_graph(self, dataset):
        """
        Validates all properties in a specific `MetaDataSet.`

        Does not validate each of the properties separately,
        but rather generates the RDF graph, which then gets validated.
        """
        print("should be validating the data")
        validation_result = dataset.validate_graph()
        if validation_result:
            # TODO: give positive feedback to user
            pass
        else:
            # TODO: inform user that validation has failed
            pass

    def update_all(self):
        """
        Update date from GUI.

        Calling this function iterates over each Property in the dataset
        and updates it with the value found in its corresponding GUI component.
        """
        print("update")
        for tab in self.tabs:
            tab.update_data()
        self.refresh_ui()

    def refresh_ui(self):
        """
        Refresh all values in the UI according to the saved values.

        Note: Calling this method discards all unsaved changes.
        """
        for tab in self.tabs:
            tab.refresh_ui()


########## Here starts UI stuff ##############


class ProjectFrame(wx.Frame):
    """
    This class sets the Project frame, and creates the file menu.

    Here we open folders and ingest new project files.
    """

    def __init__(self):
        super().__init__(parent=None,
                         title='Project Data Editor', size=(1100, 450))
        self.panel = ProjectPanel(self)
        self.create_menu()
        self.Show()

    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(
            wx.ID_NEW, 'New Folder',
            'Open a folder with project files'
        )
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.on_open_folder,
            source=open_folder_menu_item,
        )
        save_menu_item = file_menu.Append(wx.ID_SAVE, "&Save")
        self.Bind(wx.EVT_MENU, self.on_save, source=save_menu_item)
        menu_bar.Append(file_menu, '&File')
        options_menu = wx.Menu()
        # LATER: add `save on tab change` option
        menu_bar.Append(options_menu, '&Options')
        options_help = wx.Menu()
        # LATER: add `Show Help` option
        menu_bar.Append(options_help, '&Help')
        self.SetMenuBar(menu_bar)

    def on_open_folder(self, event):
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title,
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.add_new_project(dlg.GetPath())
        dlg.Destroy()

    def on_save(self, event):
        if data_handler.current_window:
            data_handler.current_window.save()
        else:
            data_handler.save_data()


class ProjectPanel(wx.Panel):
    """ This class manages the window content.

    It displays a list of projects, which are selectable and provides an edit button.
    """

    def __init__(self, parent, selection=None):
        super().__init__(parent)
        # Here we create the window ...
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(
            self, label="DaSCH Service Platform - Metadata Collection", size=(400, -1))
        main_sizer.Add(title, 0, wx.ALL | wx.LEFT, 10)

        # LATER: Here we might do some cosmetics (Title, info button and the like ...
        self.folder_path = ""
        self.row_obj_dict = {}

        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 200),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )

        self.create_header()

        # Here we create the Edit button
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 20)

        new_folder_button = wx.Button(self, label='New Folder')
        new_folder_button.Bind(wx.EVT_BUTTON, parent.on_open_folder)
        main_sizer.Add(new_folder_button, 0, wx.ALL | wx.CENTER, 5)

        edit_tabs_button = wx.Button(self, label='Edit in Tabs')
        edit_tabs_button.Bind(wx.EVT_BUTTON, self.on_edit_tabbed)
        main_sizer.Add(edit_tabs_button, 0, wx.ALL | wx.CENTER, 5)

        process_xml_button = wx.Button(self, label='Process selected to XML')
        process_xml_button.Bind(wx.EVT_BUTTON, self.on_process_data)
        main_sizer.Add(process_xml_button, 0, wx.ALL | wx.Center, 5)
        self.SetSizer(main_sizer)
        self.Fit()

        self.display_repos()

    def on_open_folder(self, event):
        """
        Open a new folder and add it to projects.
        """
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title,
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            # Here the update function is called. This function is strictly restricted to new folders.
            # New data will be appended to the available structure.
            self.panel.add_new_project(dlg.GetPath())
        dlg.Destroy()

    def display_repos(self):
        """
        Display all loaded repos in the list.
        """
        for project in data_handler.projects:
            self.list_ctrl.InsertItem(project.index, project.path)
            self.list_ctrl.SetItem(project.index, 1, project.name)
            self.list_ctrl.SetItem(project.index, 2, str(project.files))

    def create_header(self):
        """
        Here we create the header for once and always...
        """
        # Construct a header
        self.list_ctrl.InsertColumn(0, 'Folder', width=340)
        self.list_ctrl.InsertColumn(1, 'Project', width=240)
        self.list_ctrl.InsertColumn(2, 'List of files', width=500)

    def load_view(self):
        # The previous list contents is cleared before reloading it
        self.list_ctrl.ClearAll()
        # Construct a header
        self.create_header()
        self.display_repos()

    def on_edit_tabbed(self, event):
        """
        This function calls the EditBaseDialog and hands over pFiles, a list.
        """
        selection = self.list_ctrl.GetFocusedItem()
        if selection >= 0:
            repo = data_handler.projects[selection]
            dlg = TabbedWindow(self, repo)
            data_handler.current_window = dlg
            dlg.Show()
            self.Disable()

    def on_process_data(self, event):
        """ Set selection and call create_xml """
        selection = self.list_ctrl.GetFocusedItem()
        if selection >= 0:
            data_handler.process_data(selection)
            # LATER: let this return indication of success. display something to the user.

    def add_new_project(self, folder_path):
        """ Add a new project.

            Where is this function called? It is called by on_open_folder in in the Class ProjectFrame
            What should this function do? It should get a new project, store it and then reload the project list
        """
        dir_list = os.listdir(folder_path)
        if '.DS_Store' in dir_list:
            dir_list.remove('.DS_Store')

        data_handler.add_project(folder_path)
        self.load_view()


class TabOne(wx.Panel):
    """
    Tab holding the project base information
    """

    def __init__(self, parent, dataset):
        wx.Panel.__init__(self, parent)
        self.dataset = dataset

        # Project name as caption
        sizer = wx.GridBagSizer(10, 10)
        project_label = wx.StaticText(self, label="Current Project:")
        project_name = wx.StaticText(self, label=self.dataset.name)
        # QUESTION: should this be changeable?
        sizer.Add(project_label, pos=(0, 0))
        sizer.Add(project_name, pos=(0, 1))

        # Path to folder
        path_label = wx.StaticText(self, label="Path (Readonly): ")
        sizer.Add(path_label, pos=(1, 0))
        path_field = wx.TextCtrl(self, style=wx.TE_READONLY, size=(550, -1))
        path_field.SetValue(self.dataset.path)
        sizer.Add(path_field, pos=(1, 1))
        # QUESTION: add button to change folder
        path_help = wx.Button(self, label="?")
        path_help.Bind(wx.EVT_BUTTON, lambda event: self.show_help(event,
                                                                   "Path to the folder with the data",
                                                                   "/some/path/to/folder"))
        sizer.Add(path_help, pos=(1, 2))

        # Files
        files_label = wx.StaticText(self, label="Files: ")
        sizer.Add(files_label, pos=(2, 0))
        data_sizer = wx.BoxSizer()
        file_list = wx.ListBox(self, size=(550, -1))
        for f in dataset.files:
            file_list.Append(f)
        data_sizer.Add(file_list)
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_add = wx.Button(self, label="Add File(s)")
        btn_add.Bind(wx.EVT_BUTTON, lambda event: self.add_file(
            dataset, file_list))
        btn_del = wx.Button(self, label="Remove Selected")
        btn_del.Bind(wx.EVT_BUTTON, lambda event: self.remove_file(
            dataset, file_list))
        button_sizer.Add(btn_add, flag=wx.EXPAND)
        button_sizer.Add(btn_del, flag=wx.EXPAND)
        data_sizer.Add(button_sizer)
        sizer.Add(data_sizer, pos=(2, 1))
        path_help = wx.Button(self, label="?")
        path_help.Bind(wx.EVT_BUTTON, lambda event: self.show_help(event,
                                                                   "Files associated with the project",
                                                                   "sample_project.zip"))
        # TODO: give some indication on the state of this dataset. (valid, invalid, percentage of properties or similar)
        sizer.Add(path_help, pos=(2, 2))
        sizer.AddGrowableCol(1)
        self.SetSizer(sizer)

    def show_help(self, evt, message, sample):
        win = HelpPopup(self, message, sample)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Popup()

    def add_file(self, dataset, listbox):
        with wx.FileDialog(self, "Choose file(s):",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fd:
            if fd.ShowModal() == wx.ID_OK:
                for p in fd.GetPaths():
                    if p not in dataset.files:
                        # TODO: check if it's actually in project path
                        # TODO: make this relative to project path
                        dataset.files.append(p)
                        listbox.Append(p)

    def remove_file(self, dataset, file_list):
        selection = file_list.GetSelection()
        if selection >= 0:
            string_selected = file_list.GetString(selection)
            dataset.files.remove(string_selected)
            file_list.Delete(selection)


class PropertyRow():
    """
    A row in a tab of the UI

    This Class organizes a single row in the data tabs.
    Upon initiation, the UI elements ara generated and placed.
    Later on, the data handler can let this class return the value that the property should be assigned.

    Args:
        parent (wx.ScrolledWindow): The scrolled panel in which the row is to be placed.
        data_class (Project|Dataset|List[Person]|etc.): The Class that is to be displayed
        prop (Property): The property to be displayed
        sizer (wx.Sizer): The sizer that organizes the layout of the parent component
        index (int): the row in the sizer grid
    """

    def __init__(self, parent, prop, sizer, index, metadataset):
        self.prop_name = prop.name
        self.metadataset = metadataset
        self.data_widget = None
        self.choice_widget = None
        self.parent = parent
        name_label = wx.StaticText(parent, label=prop.name + ": ")
        sizer.Add(name_label, pos=(index, 0))

        # String or String/URL etc.
        if prop.datatype == Datatype.STRING \
                or prop.datatype == Datatype.STRING_OR_URL \
                or prop.datatype == Datatype.URL \
                or prop.datatype == Datatype.IRI \
                or prop.datatype == Datatype.PLACE:
            if prop.cardinality == Cardinality.ONE \
                    or prop.cardinality == Cardinality.ZERO_OR_ONE:  # String or similar, exactly 1 or 0-1
                textcontrol = wx.TextCtrl(parent, size=(550, -1), style=wx.TE_PROCESS_ENTER)
                textcontrol.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                sizer.Add(textcontrol, pos=(index, 1))
                self.data_widget = textcontrol
            elif prop.cardinality == Cardinality.ONE_TO_TWO:  # String or similar, 1-2
                inner_sizer = wx.BoxSizer(wx.VERTICAL)
                textcontrol1 = wx.TextCtrl(parent, size=(550, -1), style=wx.TE_PROCESS_ENTER)
                textcontrol1.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                inner_sizer.Add(textcontrol1)
                inner_sizer.AddSpacer(5)
                textcontrol2 = wx.TextCtrl(parent, size=(550, -1), style=wx.TE_PROCESS_ENTER)
                textcontrol2.SetHint('Second value is optional')
                textcontrol2.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                inner_sizer.Add(textcontrol2)
                sizer.Add(inner_sizer, pos=(index, 1))
                self.data_widget = [textcontrol1, textcontrol2]
            elif prop.cardinality == Cardinality.ZERO_TO_TWO:  # String or similar, 0-2
                inner_sizer = wx.BoxSizer(wx.VERTICAL)
                textcontrol1 = wx.TextCtrl(parent, size=(550, -1), style=wx.TE_PROCESS_ENTER)
                textcontrol1.SetHint('Optional')
                textcontrol1.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                inner_sizer.Add(textcontrol1)
                inner_sizer.AddSpacer(5)
                textcontrol2 = wx.TextCtrl(parent, size=(550, -1), style=wx.TE_PROCESS_ENTER)
                textcontrol2.SetHint('Optional')
                textcontrol2.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                inner_sizer.Add(textcontrol2)
                sizer.Add(inner_sizer, pos=(index, 1))
                self.data_widget = [textcontrol1, textcontrol2]
            elif prop.cardinality == Cardinality.ONE_TO_UNBOUND \
                    or prop.cardinality == Cardinality.UNBOUND:  # String or similar, 1-n, 0-2 or 0-n
                inner_sizer = wx.BoxSizer()
                textcontrol = wx.TextCtrl(parent, size=(200, -1), style=wx.TE_PROCESS_ENTER)
                textcontrol.Bind(wx.EVT_TEXT_ENTER,
                                 lambda e: parent.add_to_list(e,
                                                              content_list,
                                                              textcontrol,
                                                              textcontrol.GetValue()))
                inner_sizer.Add(textcontrol)
                inner_sizer.AddSpacer(5)
                button_sizer = wx.BoxSizer(wx.VERTICAL)
                plus_button = wx.Button(parent, label="+")
                plus_button.Bind(wx.EVT_BUTTON,
                                 lambda e: parent.add_to_list(e,
                                                              content_list,
                                                              textcontrol,
                                                              textcontrol.GetValue()))
                button_sizer.Add(plus_button, flag=wx.EXPAND)

                remove_button = wx.Button(parent, label="Del Selected")
                remove_button.Bind(wx.EVT_BUTTON,
                                   lambda event: parent.remove_from_list(event,
                                                                         content_list))
                button_sizer.Add(remove_button)
                inner_sizer.Add(button_sizer)
                inner_sizer.AddSpacer(5)
                content_list = wx.ListBox(parent, size=(250, -1))
                inner_sizer.Add(content_list)
                sizer.Add(inner_sizer, pos=(index, 1))
                self.data_widget = content_list
        # date
        elif prop.datatype == Datatype.DATE:
            if prop.cardinality == Cardinality.ONE \
                    or prop.cardinality == Cardinality.ZERO_OR_ONE:
                inner_sizer = wx.BoxSizer()
                date = wx.StaticText(parent, size=(100, -1))
                pick_date_button = wx.Button(parent, label="Pick Date")
                pick_date_button.Bind(
                    wx.EVT_BUTTON, lambda event: parent.pick_date(event, date, self.prop))
                inner_sizer.Add(date)
                inner_sizer.Add(pick_date_button)
                sizer.Add(inner_sizer, pos=(index, 1))
                self.data_widget = date
        elif prop.datatype == Datatype.PROJECT:
            txt = wx.StaticText(parent, label=str(prop.value))
            self.data_widget = txt
            sizer.Add(txt, pos=(index, 1))
        elif prop.datatype == Datatype.PERSON_OR_ORGANIZATION or \
                prop.datatype == Datatype.PERSON or \
                prop.datatype == Datatype.ORGANIZATION or \
                prop.datatype == Datatype.GRANT or \
                prop.datatype == Datatype.CONTROLLED_VOCABULARY:
            if prop.cardinality == Cardinality.ZERO_OR_ONE:
                choice = wx.Choice(parent, size=(450, -1))
                choice.SetToolTip("Add a Person or Organization")
                choice.Bind(wx.EVT_CHOICE, lambda e: self.onValueChange(e, False))
                self.data_widget = choice
                self.choice_widget = choice
                sizer.Add(choice, pos=(index, 1))
            if prop.cardinality == Cardinality.ONE_TO_UNBOUND or \
                    prop.cardinality == Cardinality.UNBOUND:
                inner_sizer = wx.BoxSizer()
                box = wx.ListBox(parent, size=(400, -1))
                self.data_widget = box
                inner_sizer.Add(box)
                control_sizer = wx.BoxSizer(wx.VERTICAL)
                choice = wx.Choice(parent, size=(150, -1))
                choice.SetToolTip("Add a Person or Organization")
                choice.Bind(wx.EVT_CHOICE,
                            lambda e: parent.add_to_list(e, box, choice,
                                                         choice.GetStringSelection()))
                self.choice_widget = choice
                control_sizer.Add(choice, flag=wx.EXPAND)
                remove_button = wx.Button(parent, label="Del Selected")
                remove_button.Bind(
                    wx.EVT_BUTTON, lambda event: parent.remove_from_list(event, box))
                control_sizer.Add(remove_button)
                inner_sizer.Add(control_sizer)
                sizer.Add(inner_sizer, pos=(index, 1))
        elif prop.datatype == Datatype.DATA_MANAGEMENT_PLAN:
            inner_sizer = wx.BoxSizer(wx.VERTICAL)
            cb = wx.CheckBox(parent, label='is available')
            cb.Bind(wx.EVT_CHECKBOX, lambda e: data_handler.update_all())
            inner_sizer.Add(cb)
            text = wx.TextCtrl(parent, size=(550, -1), style=wx.TE_PROCESS_ENTER)
            text.SetHint('Optional URL')
            text.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer.Add(text)
            sizer.Add(inner_sizer, pos=(index, 1))
            self.data_widget = [cb, text]
        elif prop.datatype == Datatype.ADDRESS:
            inner_sizer = wx.BoxSizer(wx.VERTICAL)
            text1 = wx.TextCtrl(parent, size=(550, -1), style=wx.TE_PROCESS_ENTER)
            text1.SetHint('Street')
            text1.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer.Add(text1)
            text2 = wx.TextCtrl(parent, size=(100, -1), style=wx.TE_PROCESS_ENTER)
            text2.SetHint('Postal Code')
            text2.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer2 = wx.BoxSizer()
            inner_sizer2.Add(text2)
            inner_sizer2.AddSpacer(5)
            text3 = wx.TextCtrl(parent, size=(445, -1), style=wx.TE_PROCESS_ENTER)
            text3.SetHint('Locality')
            text3.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer2.Add(text3)
            inner_sizer.AddSpacer(5)
            inner_sizer.Add(inner_sizer2)
            sizer.Add(inner_sizer, pos=(index, 1))
            self.data_widget = [text1, text2, text3]

        # TODO: Attribution

        btn = wx.Button(parent, label="?")
        btn.Bind(wx.EVT_BUTTON, lambda event: parent.show_help(
            event, prop.description, prop.example))
        sizer.Add(btn, pos=(index, 2))
        opt = wx.StaticText(
            parent, label=Cardinality.get_optionality_string(prop.cardinality))
        sizer.Add(opt, pos=(index, 3))
        self.refresh_ui()

    @property
    def data_class(self):
        return self.parent.active_dataset

    @property
    def prop(self):
        return self.data_class.get_prop_by_name(self.prop_name)

    def update_data(self):
        self.prop.value = self.get_value()

    def get_value(self):
        """
        Returns the new property value that has been entered to the UI
        """
        datatype = self.prop.datatype
        cardinality = self.prop.cardinality
        # String or String/URL etc.
        if datatype == Datatype.STRING \
                or datatype == Datatype.STRING_OR_URL \
                or datatype == Datatype.URL \
                or datatype == Datatype.IRI \
                or datatype == Datatype.PLACE:
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                return self.data_widget.GetValue()
            if cardinality == Cardinality.ONE_TO_TWO \
                    or cardinality == Cardinality.ZERO_TO_TWO:
                return [self.data_widget[0].GetValue(), self.data_widget[1].GetValue()]
            if cardinality == Cardinality.ONE_TO_UNBOUND \
                    or cardinality == Cardinality.UNBOUND:
                return self.data_widget.GetStrings()
        elif datatype == Datatype.DATE:
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                return self.data_widget.GetLabel()
        elif datatype == Datatype.PERSON_OR_ORGANIZATION or \
                datatype == Datatype.PERSON or \
                datatype == Datatype.ORGANIZATION:
            if cardinality == Cardinality.ZERO_OR_ONE:
                selection = self.data_widget.GetSelection()
                if selection < 0:
                    selection = 0
                string = self.data_widget.GetString(selection)
                return self.metadataset.get_by_string(string)
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                strs = self.data_widget.GetStrings()
                objs = [self.metadataset.get_by_string(s) for s in strs]
                return objs
            if cardinality == Cardinality.UNBOUND:
                strs = self.data_widget.GetStrings()
                objs = [self.metadataset.get_by_string(s) for s in strs]
                return objs
        elif datatype == Datatype.DATA_MANAGEMENT_PLAN:
            return (
                self.data_widget[0].GetValue(),
                self.data_widget[1].GetValue(),
            )
        elif datatype == Datatype.PROJECT:
            return self.metadataset.project
        elif datatype == Datatype.ADDRESS:
            return (
                self.data_widget[0].GetValue(),
                self.data_widget[1].GetValue(),
                self.data_widget[2].GetValue(),
            )
        elif datatype == Datatype.CONTROLLED_VOCABULARY:
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                return self.data_widget.GetStrings()
        elif datatype == Datatype.GRANT:
            if cardinality == Cardinality.UNBOUND:
                strs = self.data_widget.GetStrings()
                objs = [self.metadataset.get_by_string(s) for s in strs]
                return objs
        # TODO: Attribution
        return "Couldn't find my value... sorry"

    def refresh_ui(self):
        self.set_value(self.prop.value)
        if self.choice_widget:
            options = []
            if self.prop.datatype == Datatype.GRANT:
                options = self.metadataset.grants
            elif self.prop.datatype == Datatype.PERSON:
                options = self.metadataset.persons
            elif self.prop.datatype == Datatype.CONTROLLED_VOCABULARY:
                options = self.prop.value_options
            elif self.prop.datatype == Datatype.ORGANIZATION:
                options = self.metadataset.organizations
            elif self.prop.datatype == Datatype.PERSON_OR_ORGANIZATION:
                options = self.metadataset.persons + self.metadataset.organizations
            options_strs = ["Select to add"] + [str(o) for o in options]
            self.choice_widget.SetItems(options_strs)
            if self.choice_widget == self.data_widget:
                self.set_value(self.prop.value)

    def set_value(self, val):
        """
        # TODO: doc
        """
        datatype = self.prop.datatype
        cardinality = self.prop.cardinality
        undefined = False
        if not val:
            undefined = True
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                val = ""
            elif cardinality == Cardinality.ONE_TO_TWO \
                    or cardinality == Cardinality.ZERO_TO_TWO:
                val = ("", "",)
            else:
                val = []
        # String or String/URL etc.
        if datatype == Datatype.STRING \
                or datatype == Datatype.STRING_OR_URL \
                or datatype == Datatype.URL \
                or datatype == Datatype.IRI \
                or datatype == Datatype.PLACE:
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                self.data_widget.SetValue(val)
            if cardinality == Cardinality.ONE_TO_TWO \
                    or cardinality == Cardinality.ZERO_TO_TWO:
                self.data_widget[0].SetValue(val[0])
                self.data_widget[1].SetValue(val[1])
            if cardinality == Cardinality.ONE_TO_UNBOUND \
                    or cardinality == Cardinality.UNBOUND:
                self.data_widget.SetItems(val)
        elif datatype == Datatype.DATE:
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                self.data_widget.SetLabel(val)
        elif datatype == Datatype.PROJECT:
            self.data_widget.SetLabel(str(val))
        elif datatype == Datatype.CONTROLLED_VOCABULARY or \
                datatype == Datatype.GRANT or \
                datatype == Datatype.PERSON_OR_ORGANIZATION or \
                datatype == Datatype.PERSON or \
                datatype == Datatype.ORGANIZATION:
            if cardinality == Cardinality.ZERO_OR_ONE:
                self.data_widget.SetSelection(
                    self.data_widget.FindString(str(val)))
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                self.data_widget.SetItems([str(v) for v in val])
            if cardinality == Cardinality.UNBOUND:
                self.data_widget.SetItems([str(v) for v in val])
        elif datatype == Datatype.DATA_MANAGEMENT_PLAN:
            if undefined:
                val = (False, "",)
            self.data_widget[0].SetValue(val[0])
            self.data_widget[1].SetValue(val[1])
        elif datatype == Datatype.ADDRESS:
            if undefined:
                val = ("", "", "",)
            self.data_widget[0].SetValue(val[0])
            self.data_widget[1].SetValue(val[1])
            self.data_widget[2].SetValue(val[2])
        # TODO: Attribution

    def onValueChange(self, event, navigate: bool = True):
        data_handler.update_all()
        if navigate:
            event.GetEventObject().Navigate()


class DataTab(wx.ScrolledWindow):

    def __init__(self, parent, metadataset, dataset, title, multiple=False):
        wx.Panel.__init__(self, parent, style=wx.EXPAND)

        self.parent = parent
        self.dataset = dataset
        self.multiple = multiple
        self.metadataset = metadataset
        self.rows = []
        self.multiple_selection = 0
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridBagSizer(10, 10)

        if dataset:
            ds = dataset
            if multiple:
                ds = self.active_dataset
            for i, prop in enumerate(ds.get_properties()):
                row = PropertyRow(self, prop, sizer, i, metadataset)
                self.rows.append(row)

        if multiple:
            dataset_sizer = wx.BoxSizer()
            dataset_listbox = wx.ListBox(self, size=(700, -1))
            for ds in dataset:
                dataset_listbox.Append(str(ds))
            dataset_listbox.Bind(
                wx.EVT_LISTBOX, lambda e: self.change_selection(e))
            dataset_listbox.Select(0)
            self.multiple_listbox = dataset_listbox
            dataset_sizer.Add(dataset_listbox)
            dataset_sizer.AddSpacer(5)
            button_sizer = wx.BoxSizer(wx.VERTICAL)
            button_add = wx.Button(self, label="Add New")
            button_add.Bind(wx.EVT_BUTTON, lambda e: self.add_object(
                e, dataset_listbox, title))
            button_sizer.Add(button_add, flag=wx.EXPAND)
            button_remove = wx.Button(self, label="Remove Selected")
            button_remove.Bind(
                wx.EVT_BUTTON, lambda e: self.remove_object(e, dataset_listbox))
            button_sizer.Add(button_remove)
            dataset_sizer.Add(button_sizer)
            outer_sizer.Add(dataset_sizer)
            outer_sizer.AddSpacer(20)
        outer_sizer.Add(sizer)
        self.SetSizer(outer_sizer)

        self.SetScrollbars(0, 16, 60, 15)

    @property
    def active_dataset(self):
        if self.multiple:
            return self.dataset[self.multiple_selection]
        else:
            return self.dataset

    def update_data(self):
        for row in self.rows:
            row.update_data()

    def refresh_ui(self):
        if self.multiple:
            self.multiple_listbox.SetItems([str(ds) for ds in self.dataset])
            if self.multiple_selection < 0:
                self.multiple_selection = len(
                    self.multiple_listbox.GetItems()) - 1
            self.multiple_listbox.SetSelection(self.multiple_selection)
        for row in self.rows:
            row.refresh_ui()

    def add_object(self, event, listbox, title):
        if title == "Person":
            self.metadataset.add_person()
        if title == "Dataset":
            self.metadataset.add_dataset()
        elif title == "Organization":
            self.metadataset.add_organization()
        elif title == "Grant":
            self.metadataset.add_grant()
        self.multiple_selection = -1
        data_handler.refresh_ui()

    def remove_object(self, event, listbox):
        selection = listbox.GetSelection()
        if selection >= 0 and listbox.GetCount() > 1:
            s = listbox.GetStringSelection()
            self.metadataset.remove(self.metadataset.get_by_string(s))
            self.multiple_selection = selection - 1
        data_handler.update_all()
        data_handler.refresh_ui()

    def change_selection(self, event):
        sel = event.GetEventObject().GetSelection()
        data_handler.update_all()
        self.multiple_selection = sel
        data_handler.refresh_ui()

    def add_to_list(self, event, content_list, widget, addable):
        """
        add an object to a listbox.
        """
        if not addable:  # is None
            return
        if str(addable).isspace() or \
                addable == "Select to add" or \
                str(addable) in content_list.GetStrings():
            self.reset_widget(widget)
            return
        content_list.Append(str(addable))
        self.reset_widget(widget)
        data_handler.update_all()

    def reset_widget(self, widget):
        if isinstance(widget, wx.StaticText) or \
                isinstance(widget, wx.TextCtrl):
            widget.SetValue('')
        elif isinstance(widget, wx.Choice):
            widget.SetSelection(0)

    def remove_from_list(self, event, content_list):
        """
        remove an object from a listbox.

        """
        selection = content_list.GetSelection()
        if selection >= 0:
            content_list.Delete(selection)
        data_handler.update_all()

    def show_help(self, evt, message, sample):
        """
        Show a help dialog
        """
        win = HelpPopup(self, message, sample)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Popup()

    def pick_date(self, evt, label: wx.StaticText, prop):
        with CalendarDlg(self, prop.name, label.GetLabel()) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                label.SetLabel(dlg.cal.Date.FormatISODate())
                data_handler.update_all()


class HelpPopup(wx.PopupTransientWindow):
    def __init__(self, parent, message, sample):
        wx.PopupTransientWindow.__init__(self, parent)
        panel = wx.Panel(self)

        st = wx.StaticText(panel, -1, "Description:\n" +
                           message + "\n\n" + "Example:\n" + sample)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        sizer.Fit(self)
        self.Layout()


class TabbedWindow(wx.Frame):
    def __init__(self, parent, dataset: MetaDataSet):
        wx.Frame.__init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                          size=(900, 600), style=wx.DEFAULT_FRAME_STYLE,
                          name="Metadata tabs")
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.panel = wx.Panel(self)
        self.parent = parent
        self.dataset = dataset

        # Create a panel and notebook (tabs holder)
        panel = self.panel
        nb = wx.Notebook(panel)
        nb.SetMinSize((950, 500))
        nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_change)

        # Create the tab windows
        tab1 = TabOne(nb, self.dataset)
        tab2 = DataTab(nb, self.dataset, self.dataset.project, "Project")
        tab3 = DataTab(nb, self.dataset, self.dataset.dataset,
                       "Dataset", multiple=True)
        tab4 = DataTab(nb, self.dataset, self.dataset.persons,
                       "Person", multiple=True)
        tab5 = DataTab(nb, self.dataset, self.dataset.organizations,
                       "Organization", multiple=True)
        tab6 = DataTab(nb, self.dataset, self.dataset.grants,
                       "Grant", multiple=True)

        # Add the windows to tabs and name them.
        nb.AddPage(tab1, "Base Data")
        nb.AddPage(tab2, "Project")
        nb.AddPage(tab3, "Dataset")
        nb.AddPage(tab4, "Person")
        nb.AddPage(tab5, "Organization")
        nb.AddPage(tab6, "Grant")

        data_handler.tabs = [tab2, tab3, tab4, tab5]

        nb_sizer = wx.BoxSizer()
        nb_sizer.Add(nb, 1, wx.ALL | wx.EXPAND)

        # Buttons
        save_button = wx.Button(panel, label='Save')
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        saveclose_button = wx.Button(panel, label='Save and Close')
        saveclose_button.Bind(wx.EVT_BUTTON, self.on_saveclose)
        cancel_button = wx.Button(panel, label='Cancel')
        cancel_button.Bind(wx.EVT_BUTTON, self.on_close)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(save_button, 0, wx.ALL, 5)
        button_sizer.Add(saveclose_button, 0, wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALL, 5)

        # Set notebook in a sizer to create the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb_sizer, 0, wx.ALL | wx.EXPAND, 5)
        sizer.AddSpacer(5)
        sizer.Add(button_sizer, 0, wx.ALL | wx.BOTTOM, 5)
        panel.SetSizer(sizer)
        sizer.Fit(self)

    def on_tab_change(self, event):
        data_handler.update_all()

    def on_save(self, event):
        self.save()

    def on_saveclose(self, event):
        self.save()
        self.close()

    def on_close(self, event):
        self.close()

    def save(self):
        data_handler.update_all()
        data_handler.validate_graph(self.dataset)
        data_handler.save_data()
        data_handler.refresh_ui()

    def close(self):
        self.parent.Enable()
        self.parent.load_view()
        data_handler.current_window = None
        self.Destroy()

    def get_persons(self):
        return self.dataset.persons

    def get_organizations(self):
        return self.dataset.organizations


if __name__ == '__main__':
    collectMetadata()
