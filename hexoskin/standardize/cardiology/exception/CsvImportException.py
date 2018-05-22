# -*- coding: utf-8 -*-
class CsvImportException(Exception):
    """
    Exception returned when importing data from a CSV file failed
    """

    def __init__(self, message: str):
        """
        Init CsvImportException with the desired message.

        Parameters
        ----------
        message : str
            The exception message.
        """
        super().__init__(message)
