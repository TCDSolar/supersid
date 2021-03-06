"""
Verify and generate archive structure, specify paths of newly processed files
and archive them accordingly. The default structure of the archive is
{site}/YYYY/MM/DD/{file_type}/.

@author:
    Oscar Sage David O'Hara
@email:
    oharao@tcd.ie
"""

import os
from datetime import datetime
from pathlib import Path

from supersid.config.config import archive_path as config_archive


class Archiver:
    """
    Class used to generate archive structure, specify paths of newly processed
    files and archive them accordingly. The default structure of the archive
    is {site}/YYYY/MM/DD/{file_type}/.
    """

    def __init__(self, temp_data_path):
        self.temp_data_path = temp_data_path

    def archive(self, parameters_dict):
        """
        Archives given file into the appropriate location.

        Parameters
        ----------
        parameters_dict : dict
            VLF header info, containing filename.

        Returns
        -------
        archive dict : dict
            Relevant archive info eg. path.

        """
        path_info = self.get_path_info(parameters_dict)
        image_path, data_path = self.create_path(path_info)
        archive_dict = {'path_info': path_info,
                        'image_path': image_path,
                        'data_path': data_path,
                        'temp_path': self.temp_data_path}
        return archive_dict

    def get_path_info(self, parameters_dict):
        """
        Strip csv file name for appropriate path info, in order to generate
        archive structure.

        Parameters
        ----------
        parameters_dict : dict
            VLF header information.

        Returns
        -------
        path_info : dict
            dict containg relavent info for archiving path
        """
        start_time = datetime.strptime(parameters_dict['UTC_StartTime'],
                                       '%Y-%m-%d%H:%M:%S')
        path_info = {'transmitter': parameters_dict['StationID'],
                     'site': parameters_dict['Site'],
                     'year': start_time.strftime('%Y'),
                     'month': start_time.strftime('%m'),
                     'day': start_time.strftime('%d')}
        return path_info

    def create_path(self, path_info):
        """
        Ensure the archive structure in generated before saving files, if not
        it is created in the appropriate format.

        Parameters
        ----------
        path_info : dict
            Info regarding the exact papth to be generated eg. site name.

        Returns
        -------
        image_path : pathlib.Path object

        data_path : pathlib.Path object
        """
        if path_info['site'] == 'Dunsink':
            file_path = (Path(config_archive) /
                         'dunsink' /
                         str(path_info['year']) /
                         str(path_info['month']) /
                         str(path_info['day']))
        else:
            file_path = (Path(config_archive) /
                         'birr' /
                         str(path_info['year']) /
                         str(path_info['month']) /
                         str(path_info['day']))

        image_path, data_path = file_path / 'png', file_path / 'csv'
        if not os.path.exists(image_path):
            os.system('mkdir ' + str(image_path))
        if not os.path.exists(data_path):
            os.system('mkdir ' + str(data_path))
        return image_path, data_path

    def static_summary_path(self):
        """
        Verifies and generates static paths for Dunsink and Birr summary
        plots.
        """
        bir_summary = (Path(config_archive) / 'birr' / 'live')
        dun_summary = (Path(config_archive) / 'dunsink' / 'live')
        if not os.path.exists(bir_summary):
            os.system('mkdir ' + str(bir_summary))
        if not os.path.exists(dun_summary):
            os.system('mkdir ' + str(dun_summary))
