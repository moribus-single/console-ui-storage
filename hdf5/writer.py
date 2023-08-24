import h5py
import os

from .file import HDF5


class HDF5Writer(HDF5):
    def __init__(self, columns: list, filename: str, dtype: str, meta_size: str):
        super().__init__(columns, filename)
        self.meta_size = meta_size
        self.shape = 100
        self.delta = 100

        if not os.path.isfile(self.filename):
            # if file is not exist, create it and create
            # datasets for each column and for meta info
            with h5py.File(self.filename, 'w') as f:
                for column in self.columns:
                    f.create_dataset(name=column, shape=(self.shape,), dtype=dtype)
                f.create_dataset(name=meta_size, shape=(1,), dtype=dtype, data="0")
            self.filled = 0
        else:
            # if file exists, read the size
            with h5py.File(self.filename, 'r') as f:
                self.filled = int(f.get(meta_size)[0])

    def write(self, instance: dict):
        """Write the data into HDF5 file"""
        # adding id value automatically
        instance[self.columns[0]] = str(self.filled)

        # validate instance and
        # resize dataset if it is neccessary
        self._validate_data(instance)
        if self.filled == self.shape:
            self._resize_datasets()

        with h5py.File(self.filename, 'a') as f:
            for column in self.columns:
                dset = f.get(column)
                data = instance[column]
                dset[self.filled:self.filled + 1] = bytes(data, encoding='ascii')

            dset = f.get(self.meta_size)
            dset[0] = str(self.filled+1)

        self.filled += 1

    def _resize_datasets(self):
        with h5py.File(self.filename, 'a') as f:
            for column in self.columns:
                dset = f.get(column)

                curr_shape = dset.shape[0]
                new_shape = curr_shape + self.delta
                dset.resize((new_shape,))

        self.shape += self.delta

    def _validate_data(self, data: dict):
        for column in self.columns[1:]:
            value = data.get(column)
            if not value:
                raise AttributeError("Invalid dataset")
