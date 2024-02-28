from os import path
import pygame

from constants import *

def get_project_path():
    return path.split(path.dirname(path.abspath(__file__)))[0]

class ImageObj:
    start_x = None
    start_y = None
    end_x = None
    end_y = None
    coordinates = None
    def __init__(self, img_settings, name, _type):
        self.name = name
        self.img_settings = img_settings
        self._type = _type
        self.modes = img_settings['modes']
        self.options = img_settings['options']

        self.states = self._gen_initial_states()

        self.img, self.all_images = self._load_image_with_pygame()

    def is_button(self):
        return self._type == BUTTON_TYPE

    def _gen_initial_states(self):
        states = []
        if self.is_selectable():
            states.append(UNSELECTED_STATE)
        
        elif self.is_clickable():
            states.append('UNCLICKED')

        return states

    def is_clickable(self):
        return CLICKABLE_MODE in self.modes

    def is_selectable(self):
        return SELECTABLE_MODE in self.modes

    def is_selected(self):
        return SELECTED_STATE in self.states

    def _load_image_with_pygame(self):
        img_obj = pygame.image.load(self.img_settings['path']).convert_alpha()
        all_images = {k: pygame.image.load(v['path']).convert_alpha() for k, v in self.options.items()
                      if 'path' in v}
        all_images['default'] = img_obj
        
        return img_obj, all_images

    def get_img(self):
        return self.img
        
    def invert_select_state(self):
        select_state = None
        for _idx, state in enumerate(self.states, start=0):
            if state in AVAILABLE_IMAGE_STATES:
                select_state = state
                break

        self.states.remove(select_state)
        self.states.append(AVAILABLE_IMAGE_STATES[:2][
            AVAILABLE_IMAGE_STATES.index(select_state) -1
        ])

    def get_width(self):
        return self.get_img().get_width()

    def get_height(self):
        return self.get_img().get_height()

    def _caculate_limits(self, coordinates):
        self.coordinates = coordinates
        self.start_x = coordinates[0]
        self.start_y = coordinates[1]
        self.end_x = coordinates[0] + self.get_width()
        self.end_y = coordinates[1] + self.get_height()

    def put_img_on_screen(self, surface, coordinates):
        surface.blit(self.get_img(), coordinates)
        if coordinates != self.coordinates:
            self._caculate_limits(coordinates)

    def is_mouse_under_img(self, x, y):
        return (x > self.start_x and
                x < self.end_x and
                y > self.start_y and
                y < self.end_y)

    def get_actions_for_mode(self, mode):
        return list(self.options.get(mode, {}).get('actions', []))

    def get_options_for_mode(self, mode):
        return self.options.get(mode, {})

    def change_image(self, mode, display):
        self.img = self.all_images[mode]
        self.put_img_on_screen(display, self.coordinates)

if __name__ == '__main__':
    print(get_project_path())
