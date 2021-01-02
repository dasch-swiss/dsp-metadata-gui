import os
import pickle
import shutil

from .metaDataSet import MetaDataSet
from .utils import open_file


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
        self.data_storage = os.path.expanduser("~") + "/DaSCH/config/repos.data"
        # LATER: path could be made customizable
        self.load_data()

    def add_project(self, folder_path: str, shortcode: str, files: list):
        """
        Add a new project.

        This project adds a new project folder to the collection after the user specified the folder.

        The Project is appended at the end of the list.

        Args:
            folder_path (str): path to the project folder
            shortcode (str): the project shortcode
            files (list): the files in the project folder
        """
        folder_name = os.path.basename(folder_path)
        dataset = MetaDataSet(folder_name, folder_path, shortcode)
        self.projects.append(dataset)
        dataset.files += files
        self.save_data()

    def remove_project(self, project):
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
        with open(self.data_storage, 'wb') as file:
            pickle.dump(self.projects, file)

    def process_data(self, index: int):
        """
        ToDo: implement this class.
        """
        # TODO: how do process_data and validate_graph really divide labour?
        project = self.projects[index]
        self.validate_graph(project)
        graph = project.generate_rdf_graph()
        self.export_rdf(project.path, graph)

    def export_rdf(self, path, graph, show=True):
        path += '/metadata'
        if not os.path.exists(path):
            os.makedirs(path)
        p = path + '/metadata.ttl'
        with open(p, 'w') as f:
            s = graph.serialize(format='turtle').decode("utf-8")
            f.write(s)
        p = path + '/metadata.json'
        with open(p, 'w') as f:
            s = graph.serialize(format='json-ld').decode("utf-8")
            f.write(s)
        p = path + '/metadata.xml'
        with open(p, 'w') as f:
            s = graph.serialize(format='xml').decode("utf-8")
            f.write(s)
        if show:
            open_file(path)

    def zip_and_export(self, dataset: MetaDataSet, target: str):
        if not dataset:
            return
        if not target:
            target = dataset.path
        target_file = os.path.join(target, dataset.name)
        # TODO: create metadata if necessary
        p = dataset.path
        tmp = os.path.join(p, '.tmp')
        meta = os.path.join(p, 'metadata')
        os.makedirs(tmp, exist_ok=True)
        tmp_m = os.path.join(tmp, 'metadata')
        os.makedirs(tmp_m, exist_ok=True)
        pickle_path = os.path.join(tmp, 'binary')
        os.makedirs(pickle_path, exist_ok=True)
        for f in dataset.files:
            shutil.copy(os.path.join(p, f), tmp)
        shutil.copytree(meta, tmp_m, dirs_exist_ok=True)
        with open(os.path.join(pickle_path, 'repos.data'), mode='wb') as pick:
            pickle.dump(dataset, pick)
        shutil.make_archive(target_file, 'zip', tmp)
        shutil.rmtree(tmp, ignore_errors=True)
        open_file(target)

    def validate_graph(self, dataset: MetaDataSet) -> tuple:
        """
        Validates all properties in a specific `MetaDataSet.`

        Does not validate each of the properties separately,
        but rather generates the RDF graph, which then gets validated.
        """
        return dataset.validate_graph(dataset.generate_rdf_graph())

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

    def get_project_by_shortcode(self, shortcode):
        for p in self.projects:
            if p.shortcode == shortcode:
                return p