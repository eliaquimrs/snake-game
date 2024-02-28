import pygame

import screens
from settings_handler import ImageSettings
from constants import DEFAULT_SCREEN_SIZE


def configure_screen():
    screen = pygame.display.set_mode((800, 600))
    screen.fill('white')
    clock = pygame.time.Clock()
    return screen, clock

class GameController:
    def __init__(self):
        self.image_settings = ImageSettings()
        self.screen_classes = self._get_screen_classes()

        self.pygame_initialize()
        self.default_sys_conf = self._get_default_system_configurations()
        self.clock = pygame.time.Clock()

        self.screens_initialized = {}

    def pygame_initialize(self, ):
        pygame.init()

    @staticmethod
    def _get_default_system_configurations():
        return {
            'cursor': pygame.mouse.get_cursor()
        }

    @staticmethod    
    def _get_screen_classes():
        return {
            screen_name: getattr(screens, screen_name) for screen_name in dir(screens)
                if screen_name.endswith('Screen') and screen_name != 'BaseScreen'
        }

    def _configure_screen(self, screen, setting):
        # TODO: Get this information from setting??
        screen.fill(setting.get('background_color', 'white'))
        pygame.display.set_caption(setting.get('caption', 'Snake Game'))
        #pygame.display.set_icon()

    def initialize_a_new_screen(self, screen_name):
        screen_cls = self.screen_classes[screen_name]

        screen_setting_name, screen_setting = self.get_settings_from_window_name(screen_name)
        size = screen_setting.get('size', DEFAULT_SCREEN_SIZE)

        screen = pygame.display.set_mode(size)
        self._configure_screen(screen, screen_setting)

        self.screens_initialized[screen_name] = {
            'informations': {
                'size': size,
                'setting_name': screen_setting_name,
                'screen_name': screen_name
            },
            'setting_obj': screen_setting,
            'screen_obj': screen,
            'screen_cls': None
        }
        return screen, screen_setting

    def get_settings_from_window_name(self, window_name):
        setting_name = ''
        for idx, letter in enumerate(window_name.replace('Screen', ''), start=0):
            if letter.isupper() and idx != 0:
                setting_name += '_'
            setting_name += letter.lower()

        return setting_name, self.image_settings.get_img_setting(setting_name)

    def restore_defaults(self, ):
        pygame.mouse.set_cursor(self.default_sys_conf['cursor'])

    def execute_action(self, action):
        if action['method'] == 'open_new_window':
            cls_name = action['window_name']

            # New screen
            if cls_name not in self.screens_initialized:
                screen_obj, setting_obj = self.initialize_a_new_screen(cls_name)
                _cls = self.screen_classes[cls_name](screen_obj, setting_obj)
                self.screens_initialized[cls_name]['screen_cls'] = _cls

            else:
                _cls = self.screens_initialized[cls_name]['screen_cls']
                _cls.clean_all_selected_objects()
                self._configure_screen(_cls.display_surface,
                                        _cls.image_settings)

            _cls.configure_screen()
            self.restore_defaults()
            action = _cls.main_loop(self.clock)

        return action

    def main(self, ):
        action = {"method": "open_new_window", "window_name": "MenuScreen"}
        while action['method'] != 'quit':
            action = self.execute_action(action)

        pygame.quit()




if __name__ == "__main__":
    GameController().main()
