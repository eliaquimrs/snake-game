from collections import OrderedDict
import pygame

from utils import ImageObj, get_project_path
from constants import *
from os import path

class BaseScreen:
    def __init__(self, surface, img_settings) -> None:
        self.image_settings = img_settings
        self.display_surface = surface
        self.selected_object = None
        self.img_objects = self.load_images()

    def load_images(self):
        img_objects = OrderedDict(
            __image_by_mode={mode: [] for mode in AVAILABLE_IMAGE_MODES}
        )

        for img_item in self.image_settings['images']:
            if 'path' in img_item:
                name = img_item['_name']
                img_params = {
                    'name': name,
                    '_type': img_item['_type'],
                }
                for _mode in img_item['modes']:
                    img_objects['__image_by_mode'][_mode].append(name)

                img_objects[name] = ImageObj(img_item, **img_params)

        return img_objects

    @staticmethod
    def _is_img_obj(name):
        return not name.startswith("__")

    def get_all_button_objects(self):
        return [
            obj for name, obj in self.img_objects.items()
                if self._is_img_obj(name) and obj.is_button()
        ]

    def get_objects_by_mode(self, mode):
        return [
            self.img_objects[name] for name in self.img_objects['__image_by_mode'][mode]
        ]

    def get_all_clickable_objects(self):
        return self.get_objects_by_mode(CLICKABLE_MODE)

    def get_all_selectable_objects(self):
        return self.get_objects_by_mode(SELECTABLE_MODE)

    def _get_x_center_for_img(self, img_obj):
        half_display_width = self.display_surface.get_width() / 2
        half_img_width = img_obj.get_width() / 2

        return half_display_width - half_img_width
    
    def act_change_image(self, _, button, select, mode):
        if select:
            button.change_image(mode, self.display_surface)
        else:
            button.change_image('default', self.display_surface)

    def act_change_cursor(self, options, _, select, mode):
        if select:
            pygame.mouse.set_cursor(eval(options['cursor'], {'pygame': pygame}, {}))
        else:
            # TODO: configure a CONSTANT FOR DEFAULT CURSOR
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def act_open_new_window(self, options, button, select, mode):
        print("HERE")
        return {
            'method': 'open_new_window',
            'window_name': options['window_name']
        }

    def execute_actions(self, obj, _mouse_under_obj, mode):
        res = {}
        # Execute custom actions
        options = obj.get_options_for_mode(mode)
        if options:
            actions = obj.get_actions_for_mode(mode)
            for action in actions:
                res[action] = getattr(self,f'act_{action}')(options, obj, _mouse_under_obj, mode)

        return res

    def invert_selectable_object(self, obj, _mouse_under_obj):
        obj.invert_select_state()
        self.execute_actions(obj, _mouse_under_obj, SELECTABLE_MODE)

    def left_click_on_object(self, obj):
        if obj.is_clickable():
            act_response = self.execute_actions(obj, True, CLICKABLE_MODE)

        print(act_response)
        if 'open_new_window' in act_response:
            return False, act_response['open_new_window']
        
        return True, ''

    def _valid_button_selection(self, x, y):
        if self.selected_object:
            mouse_under_obj = self.selected_object.is_mouse_under_img(x, y)
            if not mouse_under_obj:
                self.invert_selectable_object(self.selected_object, mouse_under_obj)
                self.selected_object = None

        else:
            for button in self.get_all_selectable_objects():
                mouse_under_obj = button.is_mouse_under_img(x, y)
                if mouse_under_obj:
                    self.invert_selectable_object(button, mouse_under_obj)
                    self.selected_object = button
                    break

    def _standard_events_validation(self, event):
        # image select
        if event.type == pygame.MOUSEMOTION:
            _x, _y = event.pos
            self._valid_button_selection(_x, _y)
            return True, None
        #elif event.type == pygame.MOUSEBUTTONDOWN:
        #    pygame.mouse.set_cursor(pygame.cursors.thickarrow_strings)
        elif event.type == pygame.MOUSEBUTTONUP and self.selected_object and event.button == 1:
            return self.left_click_on_object(self.selected_object)
        elif event.type == pygame.QUIT:
            return False, {'method': 'quit'}

        return True, ''
    
    def clean_all_selected_objects(self):
        for obj in self.get_all_selectable_objects():
            if obj.is_selected():
                obj.invert_select_state()
                if 'change_image' in obj.get_actions_for_mode(SELECTABLE_MODE):
                    obj.change_image('default', self.display_surface)

class GameSettingScreen(BaseScreen):
    def configure_screen(self,):
        save_button = self.img_objects['save']
        reset_settings_button = self.img_objects['reset_settings']
        check_box =  self.img_objects['check_box']

        
        img_width = save_button.get_width()
        img_height = save_button.get_height()
        
        surface_w = self.display_surface.get_width()
        surface_h = self.display_surface.get_height()

        y = surface_h - img_height - 2

        save_button.put_img_on_screen(self.display_surface, (surface_w - img_width - 2, y))

        r_w = reset_settings_button.get_width()
        reset_settings_button.put_img_on_screen(self.display_surface, (save_button.start_x - r_w - 2, y))

        self.x_center = self._get_x_center_for_img(check_box)
        check_box.put_img_on_screen(self.display_surface, (self.x_center, y))
        self.y_center = self.display_surface.get_height() / 2


    def main_loop(self, _clock):
        project_path = get_project_path()

        image_path = path.join(project_path, 'images', )
        snake_path = path.join(image_path, 'snake_game')
        re_image_name = 'snake_skill_2_{}.png'
        images_loop = [
            pygame.image.load(path.join(snake_path, re_image_name.format(i))) for i in range(1, 24)
        ]


        snake_block_img_original = pygame.image.load(path.join(snake_path, 'snake_bad_skill_1-1.png'))
        #snake_block_img = pygame.transform.scale(snake_block_img, (20, 20))
        #self.display_surface.blit(snake_block_img, (10, 10))
        idx = 0
        operator = 1
        running = True
        count = 0

        oper = 0.125

        wait_f = False
        waiting = 0
        BLOCK_SIZE = [18, 18]
        while running:
            if wait_f:
                waiting += 1
                if waiting == 80:
                    wait_f = False
                    waiting = 0

            if not wait_f:
                self.display_surface.fill("white")
                BLOCK_SIZE[0] += oper
                BLOCK_SIZE[1] += oper
                snake_block_img = pygame.transform.scale(snake_block_img_original, tuple(BLOCK_SIZE))
                self.display_surface.blit(snake_block_img, (100-(BLOCK_SIZE[0]/1.5), 100-(BLOCK_SIZE[0]/1.5)))
                if BLOCK_SIZE[0] == 26:
                    wait_f = True
                    oper = oper * -1
                elif BLOCK_SIZE[0] == 16:
                    oper = oper * -1
            

            count+=1
            if count % 2 == 0:
                idx += operator
                self.display_surface.blit(images_loop[idx], (self.x_center, self.y_center))
                if idx == len(images_loop) - 1 or idx == 0:
                    operator = operator * -1
            #print(self.img_objects['logo'].states)
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                print(event)
                running, _action = self._standard_events_validation(event)

            # update the surface
            pygame.display.update()

            # tick the clock to enforce a max framerate
            _clock.tick(120)  # limits FPS to 60
        if _action['method'] == 'quit':
            _action = {"method": "open_new_window", "window_name": "MenuScreen"}
        return _action


class GameScreen(BaseScreen):
    def configure_screen(self,):
        pass

    def main_loop(self, _clock):
        running = True
        while running:
            #print(self.img_objects['logo'].states)
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                print(event)
                running, _action = self._standard_events_validation(event)

            # update the surface
            pygame.display.update()

            # tick the clock to enforce a max framerate
            _clock.tick(60)  # limits FPS to 60

        return _action

class MenuScreen(BaseScreen):
    def configure_screen(self, ):
        # Tittle logic
        logo_img_obj = self.img_objects['logo']
        logo_y = 20
        logo_x = self._get_x_center_for_img(logo_img_obj)

        logo_img_obj.put_img_on_screen(self.display_surface, (logo_x, logo_y))

        # Buttons Logic
        y_tmp = logo_img_obj.end_y + 50
        for button_obj in self.get_all_button_objects():
            start_x = self._get_x_center_for_img(button_obj)
            button_obj.put_img_on_screen(self.display_surface, (start_x, y_tmp))
            y_tmp += button_obj.get_height() + 10

    def main_loop(self, _clock):
        running = True
        while running:
            #print(self.img_objects['logo'].states)
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                print(event)
                running, _action = self._standard_events_validation(event)

            # update the surface
            pygame.display.update()

            # tick the clock to enforce a max framerate
            _clock.tick(60)  # limits FPS to 60

        return _action