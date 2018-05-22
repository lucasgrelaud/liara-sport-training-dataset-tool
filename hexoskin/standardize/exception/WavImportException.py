# -*- coding: utf-8 -*-
class WavImportException(Exception):
    """
    Exception returned when importing data from a WAV file failed
    """

    def __init__(self, message: str):
        """
        Init WavImportException with the desired message.

        Parameters
        ----------
        message : str
            The exception message.
        """
        super().__init__(message)
