# HDF5 Configuration
HDF5_FILENAME = "example_data"
HDF5_DATASETS_DTYPE = "S20"
HDF5_CUSTOM_COLUMNS = [
    "name",
    "surname",
    "patronymic",
    "company",
    "work_number",
    "personal_number"
]

HDF5_META_SIZE = "size"
HDF5_COLUMNS = ["id"] + HDF5_CUSTOM_COLUMNS

UI_TABLE_TITLE = "Dictionary"


class AllowedCommands:
    ADD = "+"
    FIND = "?"
    UPDATE = "="
    PRINT = "out"
    EXIT = "exit"


COMMANDS = {
    AllowedCommands.PRINT: "Print all the data",
    AllowedCommands.ADD: "Add the row",
    AllowedCommands.FIND: "Find the row by column value",
    AllowedCommands.UPDATE: "Update the row",
    AllowedCommands.EXIT: "Close the program"
}
