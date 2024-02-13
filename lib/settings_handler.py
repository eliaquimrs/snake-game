from os import path
from json import load as json_load

from utils import get_project_path
from constants import IMAGE_CFG_PATH


class ImageSettings:
    def __init__(self):
        self.project_path = get_project_path()
        self.setting_path = self._get_full_image_settings_path()
        self.raw_image_settings = self.read_raw_image_settings()
        self.image_settings = self._build_full_paths_from_setting(
                                                        self.raw_image_settings)

    def _build_full_paths_from_setting(self, _dict):
        for k, v in _dict.items():
            if k == 'path' and isinstance(v, (list, tuple)):
                _dict[k] = path.join(self.project_path, *_dict['path'])
            elif isinstance(v, dict):
                _dict[k] = self._build_full_paths_from_setting(v)
            elif (isinstance(v, (list, tuple)) and
                 len(v) > 0 and
                 isinstance(v[0], dict)):
                new_list = []
                for item in v:
                    new_list.append(self._build_full_paths_from_setting(item))
                _dict[k] = new_list

        return _dict

    def _get_full_image_settings_path(self):
        return path.join(self.project_path, IMAGE_CFG_PATH)

    def read_raw_image_settings(self):
        with open(self.setting_path, 'r', encoding='utf-8') as setting_file:
            return json_load(setting_file)

    def get_img_setting(self, topic=None):
        if topic:
            return self.image_settings[topic]
        return self.image_settings

    def get_buttons_settings(self, topic):
        return self.image_settings[topic]['buttons']
