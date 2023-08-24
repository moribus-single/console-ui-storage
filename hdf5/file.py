class HDF5:
    def __init__(self, columns: list, filename: str):
        self.columns = columns
        self.filename = filename + ".hdf5"
