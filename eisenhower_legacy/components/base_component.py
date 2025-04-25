import os
import json


class BaseComponent:
    def __init__(self, fig):
        self.fig = fig
        self.config = self.get_config()
        self.ax = None

    def get_config(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                   'config',
                                   'properties.json',
                                   )
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    @property
    def font_size(self):
        return self.config['font_size']

    @font_size.setter
    def font_size(self, value):
        self.config['font_size'] = value

    def set_axis(self, ax):
        """축 설정"""
        self.ax = ax
