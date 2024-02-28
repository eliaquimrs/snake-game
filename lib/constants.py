from os.path import join

CFG_FOLDER_NAME = 'cfg'
IMAGE_CFG_PATH = join(CFG_FOLDER_NAME, 'image_settings.json')

SELECTABLE_MODE = 'selectable'
CLICKABLE_MODE = 'clickable'
AVAILABLE_IMAGE_MODES = [SELECTABLE_MODE, CLICKABLE_MODE]


SELECTED_STATE = 'selected'
UNSELECTED_STATE = 'unselected'
AVAILABLE_IMAGE_STATES = [SELECTED_STATE, UNSELECTED_STATE]

STATIC_TYPE = 'static'
BUTTON_TYPE = 'button'
AVAILABLE_IMAGE_TYPES = [STATIC_TYPE, BUTTON_TYPE]

DEFAULT_SCREEN_SIZE = (800, 600)