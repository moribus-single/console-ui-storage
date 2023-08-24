import h5py
import numpy as np
import os

from typing import Iterator

from .file import HDF5


class HDF5Reader(HDF5):
    def __init__(self, columns: list, filename: str):
        super().__init__(columns, filename)

        if not os.path.isfile(self.filename):
            raise EnvironmentError("Invalid hdf5 filename in settings")

    def read(self) -> Iterator[list]:
        """Read the data from the HDF5 file"""
        with h5py.File(self.filename, 'r') as f:
            # get datasets length
            length = np.asarray(f.get(self.columns[0])).shape[0]
            for i in range(length):
                instance = []

                for column in self.columns:
                    dset = f.get(column)
                    instance.append(dset[i:i+1])

                yield instance
