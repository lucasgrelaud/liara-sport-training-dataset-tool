from datetime import datetime

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from numpy import abs

from data_handling import import_unified_file
from data_handling import generate_timecodes
from data_handling import TimecodePresentError


class SharedData(QObject):
    update_sync = pyqtSignal()
    update_tags = pyqtSignal(str, datetime, str)
    tags_updated = pyqtSignal(str, str, str)
    update_export_list = pyqtSignal(str, bool)
    export_list_updated = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        # Attributes dedicated to sync timecode
        self.video_sync = None
        self.data_sync = None

        # Attributes dedicated to the path
        self.video_path = None
        self.data_file_path = None
        self.output_dir = None

        # Attributes dedicated to the data
        self.parameter = None
        self.sampling_rate = None
        self.parameter_export_list = None

        self.update_tags.connect(self.update_tags_action)
        self.update_export_list.connect(self.update_export_list_action)

    def import_parameter(self):
        self.parameter = import_unified_file(self.data_file_path.path())
        self.parameter_export_list = sorted(self.parameter.keys() - {'TIMECODE', 'TAG'})

    def add_timecode(self):
        try:
            generate_timecodes(self.parameter, self.sampling_rate)
        except TimecodePresentError:
            pass

    def update_tags_action(self, action, timecode, tag):
        tag_index = self.nearest_ind(self.parameter['TIMECODE'], timecode)
        local_action = action
        local_tag = tag
        if action == 'add':
            if self.parameter['TAG'][tag_index] != '':
                local_action = 'update'
        else:
            local_tag = ''
        self.parameter['TAG'][tag_index] = local_tag
        self.tags_updated.emit(local_action, self.parameter['TIMECODE'][tag_index]
                               .strftime('%H:%M:%S:') +
                               str(int(self.parameter['TIMECODE'][tag_index].microsecond / 1000)),
                               local_tag)

    def nearest_ind(self, items, pivot):
        time_diff = abs([date - pivot for date in items])
        return time_diff.argmin(0)

    def update_export_list_action(self, parameter, state):
        if self.parameter_export_list is not None:
            if state is True:
                self.parameter_export_list.append(parameter)
                self.parameter_export_list = sorted(self.parameter_export_list)
            else:
                self.parameter_export_list.remove(parameter)
                self.parameter_export_list = sorted(self.parameter_export_list)
            self.export_list_updated.emit()
