import h5py
import numpy as np

import os
from typing import List, Dict

from .file import HDF5


class HDF5Finder(HDF5):
    def __init__(self, columns: list, filename: str):
        super().__init__(columns, filename)

        if not os.path.isfile(self.filename):
            raise EnvironmentError("Invalid hdf5 filename in settings")

    def find_by_column(self, column: str, value: str) -> List[Dict]:
        """Find the data by column and value provided by user"""
        parsed_column = column.strip().lower()
        if parsed_column not in self.columns:
            raise AttributeError("Invalid column provided")

        with h5py.File(self.filename, 'r') as f:
            # get dataset object, convert to numpy array
            # get indexes of elements equals to value
            dset = f.get(parsed_column)
            np_arr = np.array(dset)
            indexes = list(np.where(np_arr == bytes(value, 'utf-8'))[0])

            samples = []
            # for each index get all the data by each column
            for ind in indexes:
                sample = {}

                # add data in the hash map
                for column in self.columns:
                    dset = f.get(column)
                    sample[column] = dset[ind].decode()

                # wrap into Dataset object
                samples.append(sample)

        return samples
