"""
This module holds data handling capabilities for metadatasets.

Concretely, the UI has a globally accessible data handler of type `DataHandling` that will take care of the datasets held by the GUI.
"""

import os
import pickle
from typing import List, Optional

from .converter import convert_string
from .metaDataSet import MetaDataSet


class DataHandling:
    """This class handles data.

    It checks for availability in the filesystem, and
    if not, creates the data structure. It also takes care for the storage on disk.
    The data are stored as a pickle file.

    The class should not be called as a static.
    Rather, there should at any given time be an instance of this class (`data_handler`) be available.
    All calls should be done on this instance, as it holds the actual data representation.
    """

    def __init__(self):
        self.current_window = None
        self.projects: List[MetaDataSet] = []
        self.tabs = []
        self.data_storage = os.path.expanduser("~") + "/DaSCH/config/repos.data"
        # LATER: path could be made customizable
        self.load_data()

    def add_project(self, shortcode: str):
        """
        Add a new project.

        This project adds a new project folder to the collection after the user specified the folder.

        The Project is appended at the end of the list.

        Args:
            folder_path (str): path to the project folder
            shortcode (str): the project shortcode
            files (list): the files in the project folder
        """
        folder_name = ""
        dataset = MetaDataSet(folder_name, shortcode)
        self.projects.append(dataset)
        self.save_data()

    def remove_project(self, project: MetaDataSet):
        """
        Removes a specific project.

        Args:
            project (MetaDataSet): The project to remove.
        """
        if project and project in self.projects:
            self.projects.remove(project)
            self.save_data()

    def load_data(self):
        """
        Load data from previous runtimes (if any).

        Currently, this checks `~/DaSCH/config/repos.data`.
        """
        if not os.path.exists(self.data_storage):
            os.makedirs(os.path.dirname(self.data_storage), exist_ok=True)
            return
        with open(self.data_storage, "rb") as file:
            self.projects = pickle.load(file)
        # TODO: make this resilient

    def save_data(self, dataset: MetaDataSet | None = None):
        """
        Save data to disc.

        Currently, the data are stored under `~/DaSCH/config/repos.data`.

        Args:
            dataset (MetaDataSet, optional): A `Metadataset` to serialize before saving. Defaults to None.
        """
        if dataset:
            dataset.generate_rdf_graph()
        with open(self.data_storage, "wb") as file:
            pickle.dump(self.projects, file)

    def export_as_json(self, dataset: MetaDataSet, target: str):
        if not target:
            return
        if not os.path.exists(target):
            os.makedirs(target)
        target_file = os.path.join(target, dataset.shortcode + ".json")
        graph = dataset.generate_rdf_graph()
        if not graph:
            graph = dataset.graph
        turtle_str = graph.serialize(format="turtle")
        json_str = convert_string(turtle_str)
        with open(target_file, mode="w", encoding="utf-8") as f:
            f.write(json_str)

    def update_all(self):
        """
        Update data according to the values currently in the GUI.

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

    def get_project_by_shortcode(self, shortcode: str) -> Optional[MetaDataSet]:
        """
        Get the project with a specific shortcode.

        Args:
            shortcode (str): The shortcode of the project to be found.

        Returns:
            MetaDataSet: The Project with said shortcode.
        """
        for p in self.projects:
            if p.shortcode == shortcode:
                return p
        return None
