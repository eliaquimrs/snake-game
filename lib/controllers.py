from ast import literal_eval

import pygame

from settings_handler import ImageSettings
from screens import MenuScreen, GameSettingScreen, GameScreen


def configure_screen():
    screen = pygame.display.set_mode((1280, 800))
    screen.fill('white')
    clock = pygame.time.Clock()
    return screen, clock

def get_default_cursor():
    return pygame.mouse.get_cursor()

if __name__ == "__main__":
    img_setting = ImageSettings()

    pygame.init()
    default_cursor = get_default_cursor()
    
    screens = {}
    action = {"method": "open_new_window", "window_name": "MenuScreen"}
    while action['method'] != 'quit':
        if action['method'] == 'open_new_window':
            cls_name = action['window_name']
            setting_name = ''
            for idx, letter in enumerate(cls_name.replace('Screen', ''), start=0):
                if letter.isupper() and idx != 0:
                    setting_name += '_'
                setting_name += letter.lower()

            if cls_name not in screens:
                screen, clock = configure_screen()
                setting = img_setting.get_img_setting(setting_name)
                cls_screen = eval( cls_name )(screen, setting)
                screens[cls_name] = cls_screen
            else:
                cls_screen = screens[cls_name]

            # TODO: restore_settings (mouse, )
            cls_screen.configure_screen()
            pygame.mouse.set_cursor(default_cursor)
            action = cls_screen.main_loop(clock)

    pygame.quit()
