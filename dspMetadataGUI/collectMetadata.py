import wx
import wx.lib.scrolledpanel as scrolledPanel
import wx.lib.dialogs as dlgs
import os
import re

from dspMetadataGUI.util.dataHandling import DataHandling
from dspMetadataGUI.util.metaDataSet import MetaDataSet
from dspMetadataGUI.util.utils import Cardinality, Datatype, Validity
from dspMetadataGUI.util.metaDataHelpers import CalendarDlg


################# TODO List #################
#
# - Add some sort of 'import from RDF' functionality
# - give indication of cardinality in help popup
# - ensure that help popup is always on screen entirely
# - document all methods
# - document distribution process etc.
# - implement "zip and export" functionality
# - implement "upload to dsp" functionality
#
# ### for publishing:
#
# - remove all print() statements
# - imports in __init__.py
# - setup.py
# - setup.cfg
#
#############################################

################ Idea List ##################
#
# - Graph visualization would be nice
#
#############################################

def collectMetadata():
    """
    Runner function that launches the app.

    Calling this method initiates a data handler and opens the GUI.

    Example:
        To run the application, simply call:
        ```
        $ collectMetadata()
        ```
    """
    # create a data handler
    global data_handler
    data_handler = DataHandling()
    # open GUI
    app = wx.App()
    ProjectFrame()
    app.MainLoop()


class ProjectFrame(wx.Frame):
    def __init__(self):
        """
        This class holds the frame of the main application window.
        """
        super().__init__(parent=None,
                         title='Project Data Editor', size=(1100, 750))
        self.panel = ProjectPanel(self)
        self.__create_menu()
        self.Show()

    def __create_menu(self):
        """
        Create the menu, add a folder dialog box
        """
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(wx.ID_NEW, 'Add new Project', 'Open a folder with project files')
        self.Bind(event=wx.EVT_MENU, handler=self.panel.on_add_new_project, source=open_folder_menu_item)
        save_menu_item = file_menu.Append(wx.ID_SAVE, "&Save")
        self.Bind(wx.EVT_MENU, self.__on_save, source=save_menu_item)
        menu_bar.Append(file_menu, '&File')
        options_menu = wx.Menu()
        # LATER: add `save on tab change` option
        menu_bar.Append(options_menu, '&Options')
        options_help = wx.Menu()
        # LATER: add `Show Help` option
        menu_bar.Append(options_help, '&Help')
        self.SetMenuBar(menu_bar)

    def __on_save(self, event):
        """
        Menu item for saving the current window
        """
        if data_handler.current_window:
            data_handler.current_window.save()
        else:
            data_handler.save_data()


class ProjectPanel(wx.Panel):
    def __init__(self, parent: ProjectFrame, selection=None):
        """
        Panel containing the contents of the application's main window.

        The Panel displays a list of projects on top.
        On the bottom left it shows a preview of the turtle serialization of the selected project.
        On the bottom right it holds a number of buttons for various tasks.
        (Adding/removing projects, modifying projects, exporting data, etc.)

        Args:
            parent (ProjectFrame): The parent frame to hold this panel.
            selection ([type], optional): [description]. Defaults to None.
        
        TODO: remove selection param?
        """
        super().__init__(parent)
        self.folder_path = ""
        self.row_obj_dict = {}
        self.project_dependent_buttons = []

        # Create list for projects
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="DaSCH Service Platform - Metadata Collection")
        main_sizer.Add(title, 0, wx.ALL | wx.LEFT, 10)
        self.list_ctrl = wx.ListCtrl(self, size=(-1, 200), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_item_selected)
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 10)

        # Create turtle preview
        bottom_sizer = wx.FlexGridSizer(1, 2, 10, 10)
        bottom_sizer.AddGrowableCol(0)
        scroller = scrolledPanel.ScrolledPanel(self)
        rdf_display = wx.StaticText(scroller, label="No Project selected.")
        self.rdf_display = rdf_display
        scroller.SetMinSize((-1, 400))
        scroller.SetAutoLayout(1)
        scroller.SetupScrolling(scroll_x=False, scroll_y=True)
        innermost = wx.BoxSizer()
        innermost.Add(rdf_display, flag=wx.EXPAND)
        scroller.SetSizer(innermost)
        bottom_sizer.Add(scroller, flag=wx.EXPAND)

        # Create Buttons
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        new_folder_button = wx.Button(self, label='Add new Project')
        new_folder_button.Bind(wx.EVT_BUTTON, self.on_add_new_project)
        button_sizer.Add(new_folder_button, 0, wx.ALL | wx.EXPAND, 7)

        new_folder_button = wx.Button(self, label='Remove selected Project')
        self.project_dependent_buttons.append(new_folder_button)
        new_folder_button.Bind(wx.EVT_BUTTON, self.on_remove_project)
        button_sizer.Add(new_folder_button, 0, wx.ALL | wx.EXPAND, 7)

        edit_tabs_button = wx.Button(self, label='Edit selected Project')
        self.project_dependent_buttons.append(edit_tabs_button)
        edit_tabs_button.Bind(wx.EVT_BUTTON, self.on_edit_tabbed)
        button_sizer.Add(edit_tabs_button, 0, wx.ALL | wx.EXPAND, 7)

        validate_button = wx.Button(self, label='Validate selected Project')
        self.project_dependent_buttons.append(validate_button)
        validate_button.Bind(wx.EVT_BUTTON, self.on_validate)
        button_sizer.Add(validate_button, 0, wx.ALL | wx.EXPAND, 7)

        process_xml_button = wx.Button(self, label='Export selected Project as RDF')
        self.project_dependent_buttons.append(process_xml_button)
        process_xml_button.Bind(wx.EVT_BUTTON, self.on_process_data)
        button_sizer.Add(process_xml_button, 0, wx.ALL | wx.EXPAND, 7)

        zip_and_export_btn = wx.Button(self, label='ZIP and Export Project')
        self.project_dependent_buttons.append(zip_and_export_btn)
        zip_and_export_btn.Bind(wx.EVT_BUTTON, self.__on_zip_and_export)
        button_sizer.Add(zip_and_export_btn, 0, wx.ALL | wx.EXPAND, 7)

        # Layout it all
        bottom_sizer.Add(button_sizer, 0, wx.ALL, 10)
        main_sizer.Add(bottom_sizer, 0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(main_sizer)
        self.Fit()
        self.create_header()
        self.load_view()
        self.Layout()

    def __on_zip_and_export(self, event):
        """
        Export a ZIP archive containing the selected files, metadata and a pickle with the binaries.
        """
        title = "Where to export to?"
        with wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                print(path)
                data_handler.zip_and_export(self.get_selected_project(), path)

    def on_add_new_project(self, event):
        """
        Open a new folder and add it to projects.
        """
        title = "Enter Project Shortcode:\n(4 alphanumeric characters)\n\nIf your project doesn't have a shortcode assigned yet, \nplease contact the DaSCH Client Services)"
        dlg = wx.TextEntryDialog(self, title)
        if dlg.ShowModal() == wx.ID_OK:
            shortcode = dlg.GetValue()
            if not re.match('[a-zA-Z0-9]{4}$', shortcode):
                print("Invalid shortcode entered.")
                return
        else:
            return
        # LATER: should be able to chose an existing project here
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.add_new_project(dlg.GetPath(), shortcode)
        dlg.Destroy()

    def refresh_repos(self):
        """
        Refresh all loaded repos in the list.
        """
        for i, project in enumerate(data_handler.projects):
            if i < self.list_ctrl.GetItemCount():
                self.list_ctrl.SetItem(i, 0, project.path)
            else:
                self.list_ctrl.InsertItem(i, project.path)
            self.list_ctrl.SetItem(i, 1, project.name)
            self.list_ctrl.SetItem(i, 2, project.shortcode)
            self.list_ctrl.SetItem(i, 3, str(project.files))
            self.list_ctrl.SetItem(i, 4, project.get_status())

    def create_header(self):
        """
        Here we create the header
        """
        # Construct a header
        self.list_ctrl.InsertColumn(0, 'Folder', width=300)
        self.list_ctrl.InsertColumn(1, 'Project', width=180)
        self.list_ctrl.InsertColumn(2, 'Shortcode', width=90)
        self.list_ctrl.InsertColumn(3, 'List of files', width=340)
        self.list_ctrl.InsertColumn(4, 'Status', width=350)

    def load_view(self):
        # TODO: rename to refresh
        # TODO: ensure that no remainder of a deleted project is displayed
        self.refresh_repos()
        self.display_rdf()
        self.refresh_buttons()
        self.Layout()

    def refresh_buttons(self):
        if self.get_selected_project():
            flag = True
        else:
            flag = False
        for b in self.project_dependent_buttons:
            if flag:
                b.Enable()
            else:
                b.Disable()

    def display_rdf(self):
        project = self.get_selected_project()
        if project:
            txt = project.get_turtle()
        else:
            txt = "No project selected."
        self.rdf_display.SetLabel(txt)

    def get_selected_project(self) -> MetaDataSet:
        selection = self.list_ctrl.GetFirstSelected()
        if selection < 0:
            return
        shortcode = self.list_ctrl.GetItem(selection, col=2).GetText()
        return data_handler.get_project_by_shortcode(shortcode)

    def on_edit_tabbed(self, event):
        """
        This function calls the EditBaseDialog and hands over pFiles, a list.
        """
        repo = self.get_selected_project()
        if repo:
            window = TabbedWindow(self, repo)
            data_handler.current_window = window
            window.Show()
            self.Disable()

    def on_process_data(self, event):
        """ Set selection and call create_xml """
        # TODO: what does that actually do? export data? -> rename? rework?
        selection = self.list_ctrl.GetFocusedItem()
        if selection >= 0:
            data_handler.process_data(selection)
            # LATER: let this return indication of success. display something to the user.

    def add_new_project(self, folder_path, shortcode):
        """ Add a new project.

            Where is this function called? It is called by on_add_new_project in in the Class ProjectFrame
            What should this function do? It should get a new project, store it and then reload the project list
        """
        dir_list = os.listdir(folder_path)
        if '.DS_Store' in dir_list:
            dir_list.remove('.DS_Store')
        data_handler.add_project(folder_path, shortcode, dir_list)
        self.load_view()

    def on_remove_project(self, event):
        selected = self.get_selected_project()
        msg = f"Are you sure you want to delete the Project '{selected.name} ({selected.shortcode})'"
        with wx.MessageDialog(self, "Sure?", msg, wx.YES_NO) as dlg:
            if dlg.ShowModal() == wx.ID_YES:
                data_handler.remove_project(selected)
                self.list_ctrl.DeleteAllItems()
                self.load_view()

    def on_validate(self, event):
        repo = self.get_selected_project()
        if repo:
            conforms, results_graph, results_text = data_handler.validate_graph(repo)
            if conforms:
                with wx.MessageDialog(self, "Validation Successful", "Validation Successful", wx.OK | wx.ICON_INFORMATION) as dlg:
                    dlg.ShowModal()
            else:

                with dlgs.ScrolledMessageDialog(self, results_text, "Validation Failed", size=(800, 500)) as dlg:
                    dlg.ShowModal()

    def on_item_selected(self, event):
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
        sizer.Add(project_label, pos=(0, 0))
        sizer.Add(project_name, pos=(0, 1))

        # Path to folder
        path_label = wx.StaticText(self, label="Path: ")
        sizer.Add(path_label, pos=(1, 0))
        path_field = wx.TextCtrl(self, style=wx.TE_READONLY, size=(550, -1))
        path_field.SetValue(self.dataset.path)
        sizer.Add(path_field, pos=(1, 1))
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
                    f = str(p)
                    if f.startswith(dataset.path):
                        f = f.replace(f'{dataset.path}/', '')
                    else:
                        continue
                    if f and f not in dataset.files:
                        dataset.files.append(f)
                        listbox.Append(f)

    def remove_file(self, dataset, file_list):
        selection = file_list.GetSelection()
        if selection >= 0:
            string_selected = file_list.GetString(selection)
            dataset.files.remove(string_selected)
            file_list.Delete(selection)


class PropertyRow():

    def __init__(self, parent, prop, sizer, index, metadataset):
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
        self.prop_name = prop.name
        self.metadataset = metadataset
        self.data_widget = None
        self.choice_widget = None
        self.parent = parent
        self.validity_msg = ""
        name_label = wx.StaticText(parent, label=prop.name + ": ")
        sizer.Add(name_label)
        # String or String/URL etc.
        if prop.datatype == Datatype.STRING \
                or prop.datatype == Datatype.STRING_OR_URL \
                or prop.datatype == Datatype.URL \
                or prop.datatype == Datatype.EMAIL \
                or prop.datatype == Datatype.DOWNLOAD \
                or prop.datatype == Datatype.PLACE:
            if prop.cardinality == Cardinality.ONE \
                    or prop.cardinality == Cardinality.ZERO_OR_ONE:  # String or similar, exactly 1 or 0-1
                if prop.multiline:
                    textcontrol = wx.TextCtrl(parent, style=wx.TE_MULTILINE)
                else:
                    textcontrol = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
                    textcontrol.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                sizer.Add(textcontrol, flag=wx.EXPAND)
                self.data_widget = textcontrol
            elif prop.cardinality == Cardinality.ONE_TO_TWO:  # String or similar, 1-2
                inner_sizer = wx.BoxSizer(wx.VERTICAL)
                textcontrol1 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
                textcontrol1.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                inner_sizer.Add(textcontrol1, flag=wx.EXPAND)
                inner_sizer.AddSpacer(5)
                textcontrol2 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
                textcontrol2.SetHint('Second value is optional')
                textcontrol2.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                inner_sizer.Add(textcontrol2, flag=wx.EXPAND)
                sizer.Add(inner_sizer, flag=wx.EXPAND)
                self.data_widget = [textcontrol1, textcontrol2]
            elif prop.cardinality == Cardinality.ZERO_TO_TWO:  # String or similar, 0-2
                inner_sizer = wx.BoxSizer(wx.VERTICAL)
                textcontrol1 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
                textcontrol1.SetHint('Optional')
                textcontrol1.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                inner_sizer.Add(textcontrol1, flag=wx.EXPAND)
                inner_sizer.AddSpacer(5)
                textcontrol2 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
                textcontrol2.SetHint('Optional')
                textcontrol2.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
                inner_sizer.Add(textcontrol2, flag=wx.EXPAND)
                sizer.Add(inner_sizer, flag=wx.EXPAND)
                self.data_widget = [textcontrol1, textcontrol2]
            elif prop.cardinality == Cardinality.ONE_TO_UNBOUND \
                    or prop.cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED \
                    or prop.cardinality == Cardinality.UNBOUND:  # String or similar, 1-n or 0-n
                if prop.multiline:
                    inner_sizer = wx.BoxSizer()
                    text_sizer = wx.BoxSizer(wx.VERTICAL)
                    textcontrol = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
                    textcontrol.Bind(wx.EVT_TEXT_ENTER,
                                     lambda e: parent.add_to_list(e,
                                                                  content_list,
                                                                  textcontrol,
                                                                  textcontrol.GetValue()))
                    text_sizer.Add(textcontrol, flag=wx.EXPAND)
                    text_sizer.AddSpacer(5)
                    content_list = wx.ListBox(parent)
                    text_sizer.Add(content_list, 1, flag=wx.EXPAND)
                    inner_sizer.Add(text_sizer, 1, flag=wx.EXPAND)
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
                else:
                    inner_sizer = wx.BoxSizer()
                    textcontrol = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
                    textcontrol.Bind(wx.EVT_TEXT_ENTER,
                                     lambda e: parent.add_to_list(e,
                                                                  content_list,
                                                                  textcontrol,
                                                                  textcontrol.GetValue()))
                    inner_sizer.Add(textcontrol, 1)
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
                    content_list = wx.ListBox(parent)
                    inner_sizer.Add(content_list, 1, flag=wx.EXPAND)
                sizer.Add(inner_sizer, flag=wx.EXPAND)
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
                sizer.Add(inner_sizer, flag=wx.EXPAND)
                self.data_widget = date
        elif prop.datatype == Datatype.PROJECT:
            txt = wx.StaticText(parent, label=str(prop.value))
            self.data_widget = txt
            sizer.Add(txt, flag=wx.EXPAND)
        elif prop.datatype == Datatype.PERSON_OR_ORGANIZATION or \
                prop.datatype == Datatype.PERSON or \
                prop.datatype == Datatype.ORGANIZATION or \
                prop.datatype == Datatype.GRANT or \
                prop.datatype == Datatype.CONTROLLED_VOCABULARY:
            if prop.cardinality == Cardinality.ZERO_OR_ONE \
                    or prop.cardinality == Cardinality.ONE:
                choice = wx.Choice(parent)
                choice.Bind(wx.EVT_CHOICE, lambda e: self.onValueChange(e, False))
                self.data_widget = choice
                self.choice_widget = choice
                sizer.Add(choice, flag=wx.EXPAND)
            if prop.cardinality == Cardinality.ONE_TO_UNBOUND or \
                    prop.cardinality == Cardinality.UNBOUND:
                inner_sizer = wx.BoxSizer()
                box = wx.ListBox(parent)
                self.data_widget = box
                inner_sizer.Add(box, 10)
                control_sizer = wx.BoxSizer(wx.VERTICAL)
                choice = wx.Choice(parent)
                choice.Bind(wx.EVT_CHOICE,
                            lambda e: parent.add_to_list(e, box, choice,
                                                         choice.GetStringSelection()))
                self.choice_widget = choice
                control_sizer.Add(choice, flag=wx.EXPAND)
                remove_button = wx.Button(parent, label="Del Selected")
                remove_button.Bind(wx.EVT_BUTTON, lambda event: parent.remove_from_list(event, box))
                control_sizer.Add(remove_button)
                inner_sizer.Add(control_sizer, 7)
                sizer.Add(inner_sizer, flag=wx.EXPAND)
        elif prop.datatype == Datatype.DATA_MANAGEMENT_PLAN:
            inner_sizer = wx.BoxSizer(wx.VERTICAL)
            cb = wx.CheckBox(parent, label='is available')
            cb.Bind(wx.EVT_CHECKBOX, lambda e: data_handler.update_all())
            inner_sizer.Add(cb, flag=wx.EXPAND)
            text = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            text.SetHint('Optional URL')
            text.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer.Add(text, flag=wx.EXPAND)
            sizer.Add(inner_sizer, flag=wx.EXPAND)
            self.data_widget = [cb, text]
        elif prop.datatype == Datatype.ADDRESS:
            inner_sizer = wx.BoxSizer(wx.VERTICAL)
            text1 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            text1.SetHint('Street')
            text1.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer.Add(text1, flag=wx.EXPAND)
            text2 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            text2.SetHint('Postal Code')
            text2.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer2 = wx.BoxSizer()
            inner_sizer2.Add(text2, 2)
            inner_sizer2.AddSpacer(5)
            text3 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            text3.SetHint('Locality')
            text3.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer2.Add(text3, 10)
            inner_sizer.AddSpacer(5)
            inner_sizer.Add(inner_sizer2, flag=wx.EXPAND)
            sizer.Add(inner_sizer, flag=wx.EXPAND)
            self.data_widget = [text1, text2, text3]
        elif prop.datatype == Datatype.ATTRIBUTION:
            inner_sizer = wx.BoxSizer()
            input_sizer = wx.BoxSizer(wx.VERTICAL)
            textcontrol = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            textcontrol.SetHint("Role")
            input_sizer.Add(textcontrol, flag=wx.EXPAND)
            choice = wx.Choice(parent)
            choice.SetToolTip("Add a Person or Organization")
            self.choice_widget = choice
            input_sizer.Add(choice, flag=wx.EXPAND)
            inner_sizer.Add(input_sizer, 1)
            inner_sizer.AddSpacer(5)
            button_sizer = wx.BoxSizer(wx.VERTICAL)
            plus_button = wx.Button(parent, label="+")
            button_sizer.Add(plus_button, flag=wx.EXPAND)
            remove_button = wx.Button(parent, label="Del Selected")
            button_sizer.Add(remove_button)
            inner_sizer.Add(button_sizer)
            inner_sizer.AddSpacer(5)
            content_list = wx.ListCtrl(parent, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
            content_list.InsertColumn(0, 'Role')
            content_list.InsertColumn(1, 'Agent')
            inner_sizer.Add(content_list, 1)
            sizer.Add(inner_sizer, flag=wx.EXPAND)
            self.data_widget = content_list
            remove_button.Bind(wx.EVT_BUTTON,
                               lambda event: parent.remove_from_list(event,
                                                                     content_list))
            plus_button.Bind(wx.EVT_BUTTON,
                             lambda e: parent.add_to_list(e,
                                                          content_list,
                                                          (textcontrol, choice),
                                                          (textcontrol.GetValue(), choice.GetStringSelection())))
        elif prop.datatype == Datatype.SHORTCODE:
            text = wx.StaticText(parent)
            self.data_widget = text
            sizer.Add(text, flag=wx.EXPAND)

        btn = wx.Button(parent, label="?")
        btn.Bind(wx.EVT_BUTTON, lambda event: parent.show_help(event, prop.description, prop.example))
        sizer.Add(btn)
        opt = wx.Button(parent, label=Cardinality.get_optionality_string(prop.cardinality))
        opt.Bind(wx.EVT_BUTTON, lambda event: parent.show_validity(event,
                                                                   self.validity_msg,
                                                                   Cardinality.as_sting(prop.cardinality)))
        self.validity_widget = opt
        sizer.Add(opt)
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
                or datatype == Datatype.EMAIL \
                or datatype == Datatype.DOWNLOAD \
                or datatype == Datatype.PLACE:
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                return self.data_widget.GetValue()
            if cardinality == Cardinality.ONE_TO_TWO \
                    or cardinality == Cardinality.ZERO_TO_TWO:
                return [self.data_widget[0].GetValue(), self.data_widget[1].GetValue()]
            if cardinality == Cardinality.ONE_TO_UNBOUND \
                    or cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED \
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
            elif cardinality == Cardinality.ONE:
                sel = self.data_widget.GetSelection()
                if sel >= 0:
                    s = self.data_widget.GetString(sel)
                    if s in self.prop.value_options:
                        return s
                    else:
                        return ""
                else:
                    return ""
        elif datatype == Datatype.GRANT:
            if cardinality == Cardinality.UNBOUND:
                strs = self.data_widget.GetStrings()
                objs = [self.metadataset.get_by_string(s) for s in strs]
                return objs
        elif datatype == Datatype.ATTRIBUTION:
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                w = self.data_widget
                res = []
                for i in range(w.GetItemCount()):
                    t = w.GetItem(i, 0).GetText()
                    o = self.metadataset.get_by_string(w.GetItem(i, 1).GetText())
                    if t and not t.isspace() and o:
                        res.append((t, o,))
                return res
        elif datatype == Datatype.SHORTCODE:
            return self.data_widget.GetLabel()
        print(f"Couldn't find a type here... weird... {datatype}")
        return "Couldn't find my value... sorry"

    def refresh_ui(self):
        self.set_value(self.prop.value)
        if self.choice_widget:
            self.refresh_choice()
        self.validate()

    def refresh_choice(self):
        options = []
        if self.prop.datatype == Datatype.GRANT:
            options = self.metadataset.grants
        elif self.prop.datatype == Datatype.PERSON:
            options = self.metadataset.persons
        elif self.prop.datatype == Datatype.CONTROLLED_VOCABULARY:
            options = self.prop.value_options
        elif self.prop.datatype == Datatype.ORGANIZATION:
            options = self.metadataset.organizations
        elif self.prop.datatype == Datatype.PERSON_OR_ORGANIZATION or \
                self.prop.datatype == Datatype.ATTRIBUTION:
            options = self.metadataset.persons + self.metadataset.organizations
        options_strs = ["Select to add"] + [str(o) for o in options]
        self.choice_widget.SetItems(options_strs)
        if self.choice_widget == self.data_widget:
            self.set_value(self.prop.value)

    def validate(self):
        widget = self.validity_widget
        res, msg = self.prop.validate()
        if res == Validity.VALID:
            widget.SetForegroundColour(wx.Colour(30, 170, 30))
        elif res == Validity.INVALID_VALUE:
            widget.SetForegroundColour(wx.Colour(170, 30, 30))
        elif res == Validity.REQUIRED_VALUE_MISSING:
            widget.SetForegroundColour(wx.Colour(170, 30, 30))
        elif res == Validity.OPTIONAL_VALUE_MISSING:
            widget.SetForegroundColour(wx.NullColour)
        self.validity_msg = msg

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
                or datatype == Datatype.EMAIL \
                or datatype == Datatype.DOWNLOAD \
                or datatype == Datatype.PLACE:
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                self.data_widget.SetValue(val)
            if cardinality == Cardinality.ONE_TO_TWO \
                    or cardinality == Cardinality.ZERO_TO_TWO:
                self.data_widget[0].SetValue(val[0])
                self.data_widget[1].SetValue(val[1])
            if cardinality == Cardinality.ONE_TO_UNBOUND \
                    or cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED \
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
            if cardinality == Cardinality.ZERO_OR_ONE \
                    or cardinality == Cardinality.ONE:
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
        elif datatype == Datatype.ATTRIBUTION:
            if undefined:
                val = [("", "",)]
            self.data_widget.DeleteAllItems()
            for v in val:
                self.data_widget.Append((v[0], str(v[1])))
                self.data_widget.SetColumnWidth(0, -1)
                self.data_widget.SetColumnWidth(1, -1)
        elif datatype == Datatype.SHORTCODE:
            return self.data_widget.SetLabel(val)

    def onValueChange(self, event, navigate: bool = True):
        data_handler.update_all()
        if navigate:
            event.GetEventObject().Navigate()


class DataTab(scrolledPanel.ScrolledPanel):

    def __init__(self, parent, metadataset, dataset, title, multiple=False):
        """
        The class does the following: ToDo: Check the params, dataclass?

        Args:
            parent (object): to be checked
            metadataset (object): to be checked
            dataset (object): to be checked
            title (str): title of the project
            multiple (bool): false
        """
        # wx.Panel.__init__(self, parent, style=wx.EXPAND)
        scrolledPanel.ScrolledPanel.__init__(self, parent, -1)

        self.parent = parent
        self.dataset = dataset
        self.multiple = multiple
        self.metadataset = metadataset
        self.rows = []
        self.multiple_selection = 0
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.FlexGridSizer(4, 10, 10)

        if dataset:
            ds = dataset
            if multiple:
                ds = self.active_dataset
            for i, prop in enumerate(ds.get_properties()):
                row = PropertyRow(self, prop, sizer, i, metadataset)
                self.rows.append(row)

        sizer.AddGrowableCol(1)

        if multiple:
            dataset_sizer = wx.BoxSizer()
            dataset_listbox = wx.ListBox(self)
            for ds in dataset:
                dataset_listbox.Append(str(ds))
            dataset_listbox.Bind(
                wx.EVT_LISTBOX, lambda e: self.change_selection(e))
            dataset_listbox.Select(0)
            self.multiple_listbox = dataset_listbox
            dataset_sizer.Add(dataset_listbox, wx.EXPAND)
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
            outer_sizer.Add(dataset_sizer, flag=wx.EXPAND)
            outer_sizer.AddSpacer(20)
        outer_sizer.Add(sizer, flag=wx.EXPAND)
        self.SetSizer(outer_sizer)
        self.SetupScrolling(scroll_x=True, scroll_y=True)
        self.Fit()
        self.Layout()
        # self.SetScrollbars(0, 16, 60, 15)

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
                self.multiple_selection = len(self.multiple_listbox.GetItems()) - 1
            self.multiple_listbox.SetSelection(self.multiple_selection)
        for row in self.rows:
            row.refresh_ui()
        self.Layout()

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
        if isinstance(widget, tuple):
            role = addable[0]
            agent = addable[1]
            if not role or not agent or \
                    role.isspace() or agent.isspace() or \
                    agent == "Select to add":
                print('invalid input')
                # TODO: check, if already in there
                return
            content_list.Append((role, agent))
        else:
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
        if isinstance(content_list, wx.ListCtrl):
            selection = content_list.GetFirstSelected()
            if selection >= 0:
                content_list.DeleteItem(selection)
        else:
            selection = content_list.GetSelection()
            if selection >= 0:
                content_list.Delete(selection)
        data_handler.update_all()

    def show_help(self, evt, message, sample):
        """
        Show a help dialog
        """
        msg = f"Description:\n{message}\n\nExample:\n{sample}"
        win = HelpPopup(self, msg)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Popup()

    def show_validity(self, evt, val, card):
        """
        Show a help dialog
        """
        msg = f"Validation Result:\n{val}\n\nExpected Cardinality:\n{card}"
        win = HelpPopup(self, msg)
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
    def __init__(self, parent, msg):
        """
        This class provides a help message
        Args:
            parent (object): the parent class
            msg (str): the help text with examples
        """
        wx.PopupTransientWindow.__init__(self, parent)
        panel = wx.Panel(self)
        st = wx.StaticText(panel, -1, msg)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        sizer.Fit(self)
        self.Layout()


class TabbedWindow(wx.Frame):
    def __init__(self, parent, dataset: MetaDataSet):
        """
        This class organizes the different tabs
        ToDo: What exactly is the metadataset?

        Args:
            parent (object): the parent object
            dataset (object): the dataset
            MetaDataSet (object): the metadataset
        """
        wx.Frame.__init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                          size=(1200, 600), style=wx.DEFAULT_FRAME_STYLE,
                          name="Metadata tabs")
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.panel = wx.Panel(self)
        self.parent = parent
        self.dataset = dataset

        # Create a panel and notebook (tabs holder)
        panel = self.panel
        nb = wx.Notebook(panel)
        nb.SetMinSize((-1, 200))
        nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_change)

        # Create the tab windows
        tab1 = TabOne(nb, self.dataset)
        tab2 = DataTab(nb, self.dataset, self.dataset.project, "Project")
        tab3 = DataTab(nb, self.dataset, self.dataset.dataset, "Dataset", multiple=True)
        tab4 = DataTab(nb, self.dataset, self.dataset.persons, "Person", multiple=True)
        tab5 = DataTab(nb, self.dataset, self.dataset.organizations, "Organization", multiple=True)
        tab6 = DataTab(nb, self.dataset, self.dataset.grants, "Grant", multiple=True)

        # Add the windows to tabs and name them.
        nb.AddPage(tab1, "Base Data")
        nb.AddPage(tab2, "Project")
        nb.AddPage(tab3, "Dataset")
        nb.AddPage(tab4, "Person")
        nb.AddPage(tab5, "Organization")
        nb.AddPage(tab6, "Grant")

        data_handler.tabs = [tab2, tab3, tab4, tab5, tab6]

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
        sizer = wx.FlexGridSizer(1, 2, 10)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(nb_sizer, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)
        panel.SetSizer(sizer)
        # sizer.Fit(self)

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