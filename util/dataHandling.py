import os
import pickle

from .metaDataSet import MetaDataSet


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
        for tab in self.tabs:
            tab.update_data()
        self.refresh_ui()

    def refresh_ui(self):
        """
        Refresh all values in the UI according to the saved values.

        This method also invokes on-the-fly validation.
        Note: Calling this method discards all changes that have not been updated in the metaDataSet.
        """
        for tab in self.tabs:
            tab.refresh_ui()