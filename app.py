from hdf5 import HDF5Writer, HDF5Reader, HDF5Finder, HDF5Updater
from ui import TableFactory, UIConsole

import settings


class App:
    def __init__(self):
        # Objects for processing hdf5 files
        self.writer = HDF5Writer(
            settings.HDF5_COLUMNS,
            settings.HDF5_FILENAME,
            settings.HDF5_DATASETS_DTYPE,
            settings.HDF5_META_SIZE
        )
        self.reader = HDF5Reader(settings.HDF5_COLUMNS, settings.HDF5_FILENAME)
        self.finder = HDF5Finder(settings.HDF5_COLUMNS, settings.HDF5_FILENAME)
        self.updater = HDF5Updater(settings.HDF5_COLUMNS, settings.HDF5_FILENAME)

        # Objects for UI
        self.console = UIConsole()

    def run(self):
        """Run the app"""
        # while True:
        self.console.pprint(settings.COMMANDS)

        # Program cycle
        while True:
            # Reading the command
            self.console.log("\nWrite the command:")
            command = input("% ")

            # If the command is not allowed
            # Try again
            if command not in settings.COMMANDS:
                self.console.log(f"Invalid command - {command}")
                continue

            # Pattern matching for command
            match command:
                # Close the program
                case settings.AllowedCommands.EXIT:
                    break

                # Adding data into dictionary
                case settings.AllowedCommands.ADD:
                    self.__add()

                # Printing data into dictionary as a table
                case settings.AllowedCommands.PRINT:
                    self.__print()

                # Finding data by column and value
                case settings.AllowedCommands.FIND:
                    while True:
                        try:
                            self.__find()
                            break
                        except AttributeError:
                            self.console.log("Invalid column!")

                # Updating the data by id
                case settings.AllowedCommands.UPDATE:
                    while True:
                        try:
                            self.__update()
                            break
                        except AttributeError:
                            self.console.log("Invalid id!")

    def __add(self):
        self.console.log("Write the data for saving:")

        # wrap the data into sample object and
        # write the data into file
        sample = {col: input(f"Write the {col}: ") for col in settings.HDF5_CUSTOM_COLUMNS}
        self.writer.write(sample)

        self.console.log("Success\n")

    def __print(self):
        # initialize table object
        table = TableFactory(settings.UI_TABLE_TITLE, settings.HDF5_COLUMNS)

        # read the data from hdf5 file and
        # insert it into the table
        for data in self.reader.read():
            unpacked = [s[0].decode() for s in data]
            if '' not in unpacked:
                table.insert(unpacked)

        # print the table
        self.console.print(table.table)

    def __find(self):
        # read the data from console
        column = input('Write the column: ')
        if column not in settings.HDF5_COLUMNS:
            raise AttributeError("Invalid column")

        value = input('Write the value: ')
        table = TableFactory(settings.UI_TABLE_TITLE, settings.HDF5_COLUMNS)

        # find the data, unpack and insert in the table
        data = self.finder.find_by_column(column, value)
        unpacked = [[value for _, value in d.items()] for d in data]
        for instance in unpacked:
            table.insert(instance)

        if unpacked:
            self.console.print(table.table)
        else:
            self.console.log("Not found!")

    def __update(self):
        # read the id from console
        find_id = input('Write the id of the row you want to update: ')

        # wrap the data into dataset object
        sample = {}
        for col in settings.HDF5_CUSTOM_COLUMNS:
            data = input(f'Write the {col} (If you don\'t want to change it, press ENTER): ')
            if data:
                sample[col] = data

        # update the data
        self.updater.update(find_id, sample)
