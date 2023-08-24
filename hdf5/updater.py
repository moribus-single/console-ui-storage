import h5py
import numpy as np

import os

from .file import HDF5


class HDF5Updater(HDF5):
    def __init__(self, columns: list, filename: str):
        super().__init__(columns, filename)

        if not os.path.isfile(self.filename):
            raise EnvironmentError("Invalid hdf5 filename in settings")

    def update(self, find_id: str, sample: dict):
        """Update the data in HDF5 file by id column"""
        with h5py.File(self.filename, 'a') as f:
            # get dataset object for IDs, convert to numpy array
            # get indexes of elements equals to value
            dset = f.get(self.columns[0])
            np_arr = np.array(dset)
            indexes = list(np.where(np_arr == bytes(find_id, 'utf-8'))[0])
            if not indexes:
                raise AttributeError("Invalid id!")

            if len(indexes) > 1:
                raise ValueError("Invalid hdf5 file.")

            for col in self.columns[1:]:
                value = sample.get(col)
                if value:
                    dset = f.get(col)
                    dset[indexes[0]] = value
