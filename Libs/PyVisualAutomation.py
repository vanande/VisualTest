#!C:\Apps\Python311 python
# encoding: utf8
import os.path
import pyautogui
import pygetwindow as gw
import logging.config
import time
from datetime import datetime
import pyperclip
from subprocess_maximize import Popen
import yaml
from PIL import Image


MOUSE_MOVE_SPEED=0
IMAGES=''
SCREENSHOT=''
TAKE_SCREENSHOT=''
CONTINUE_ON_ERROR=False
CONFIDENCE=0.95
LEFT=0
TOP=0
WIDTH=0
HEIGHT=0
WH_ACTIVE = None
TIMEOUT = 5
X = 0
Y = 0
REGION = (0, 0, 1930, 1060)
TESSERACT = None
def set_mouse_move_speed (speed):
    global MOUSE_MOVE_SPEED
    MOUSE_MOVE_SPEED=float(speed)
def set_image_confidence (confidence):
    global CONFIDENCE
    CONFIDENCE=float(confidence)

def set_pause (pause):
    pyautogui.PAUSE=float(pause)

def set_timeout (timeout):
    global TIMEOUT
    TIMEOUT=timeout

def scroll_down ():
    pyautogui.scroll(-200)
    pyautogui.scroll(-200)
    pyautogui.scroll(-200)
    pyautogui.scroll(-200)

def set_active_app (app):
    global IMAGES
    with open(os.getcwd() + '\\Libs\\PyVisualAutomation.yaml', 'r') as file:
        yaml_config = yaml.safe_load(file)
        IMAGES = yaml_config['IMAGES'] + "\\" + app

def initialize (app):
    global MOUSE_MOVE_SPEED, IMAGES, SCREENSHOT, TAKE_SCREENSHOT, \
        CONFIDENCE, TIMEOUT, TESSERACT, WH_ACTIVE, HEIGHT, WIDTH, \
        CONTINUE_ON_ERROR
    logging.config.fileConfig(os.getcwd() + '\\logging.conf')
    set_active_app(app)
    with open(os.getcwd()+'\\Libs\\PyVisualAutomation.yaml', 'r') as file:
        yaml_config = yaml.safe_load(file)
        pyautogui.FAILSAFE = yaml_config['FAILSAFE']
        pyautogui.PAUSE = yaml_config['PAUSE']
        MOUSE_MOVE_SPEED = yaml_config['MOUSE_MOVE_SPEED']
        SCREENSHOT = yaml_config['SCREENSHOT']
        TAKE_SCREENSHOT = yaml_config['TAKE_SCREENSHOT'].lower()
        CONTINUE_ON_ERROR = yaml_config['CONTINUE_ON_ERROR']
        CONFIDENCE = yaml_config['CONFIDENCE']
        TIMEOUT = yaml_config['TIMEOUT']
        IMAGES = yaml_config['IMAGES'] + "\\" + app
        HEIGHT = yaml_config['HEIGHT']
        WIDTH = yaml_config['WIDTH']

def close_existing_window():
    global WH_ACTIVE
    if WH_ACTIVE is not None:
        WH_ACTIVE.close()
        press ("enter")
        WH_ACTIVE = None

def run_application (app):
    logging.debug("Launch " + app)
    Popen(app, shell=True)

def run_chrome (url):
    cmd = r'"C:\Program Files\Google\Chrome\Application\Chrome" -aggressive-cache-discard -new-window -incognito -start-maximized "' + url + '"'
    logging.debug("Launch " + url)
    Popen(cmd, show='maximize', priority=0)
    time.sleep(2)

def refresh ():
    pyautogui.press('f5')
def press (key):
    pyautogui.press(key)

def next_window ():
    with pyautogui.hold('alt'):
        pyautogui.press('tab')
def resize (h, w):
    global WH_ACTIVE
    if WH_ACTIVE is not None:
        if WH_ACTIVE.width != w or WH_ACTIVE.height != h:
            WH_ACTIVE.resizeTo (h, w)
            WH_ACTIVE.moveTo(0, 0)
            time.sleep(3)
def window_close ():
    global WH_ACTIVE
    with pyautogui.hold('alt'):
        pyautogui.press('f4')
    WH_ACTIVE = None
def close_tab ():
    with pyautogui.hold('ctrl'):
        pyautogui.press('z')
    with pyautogui.hold('ctrl'):
        pyautogui.press('w')


def page_down ():
    pyautogui.press('pagedown')
def page_up ():
    pyautogui.press('pageup')
def clear_input ():
    pyautogui.doubleClick()
    # pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
def dt_fr (dt_sep, time_sep):
    dt_fr = datetime.now().strftime("%Y"+dt_sep+"%m"+dt_sep+"%dT%H"+time_sep+"%M"+time_sep+"%S")
    return(dt_fr)
def switch_to (window_title, maximize):
    global WH_ACTIVE, TIMEOUT, LEFT, TOP, WIDTH, HEIGHT, WH_ACTIVE, \
            REGION, HEIGHT, WIDTH, CONTINUE_ON_ERROR

    title = ""
    i = 0
    logging.debug("Timeout {0}".format(TIMEOUT))
    while i < TIMEOUT:
        titles = gw.getAllTitles()
        # search window
        for title in titles:
            if title.lower().find(window_title.lower())>=0:
                logging.debug("Windows {0} found".format(title.encode()))
                break
        # window found
        if title.lower().find(window_title.lower())>=0:
            logging.debug("Window found {0}".format(window_title))
            WH_ACTIVE = gw.getWindowsWithTitle(window_title)[0]
            if not maximize or  not WH_ACTIVE.isMaximized:
                if maximize and not WH_ACTIVE.isMaximized:
                    logging.debug("Windows {0} maximized".format(WH_ACTIVE))
                    WH_ACTIVE.maximize()
                    time.sleep(3)
                #else:
                #    logging.debug("Windows {0} resized to WIDTH {1} HEIGHT {2}".format(WH_ACTIVE,WIDTH,HEIGHT ))
                #    resize(WIDTH, HEIGHT)
            TOP=WH_ACTIVE.top+8
            LEFT=WH_ACTIVE.left+8
            WIDTH =  WH_ACTIVE.width+8
            HEIGHT= WH_ACTIVE.height+8
            WH_ACTIVE.show()
            try:
                WH_ACTIVE.activate()
            except:
                print ("error activate")
            REGION = (LEFT, TOP, WIDTH, HEIGHT)
            return (WH_ACTIVE)
        time.sleep(1)
        i+=1
    if CONTINUE_ON_ERROR:
        logging.warning("Window not found with title " + window_title)
    else:
        logging.error("Window not found with title " + window_title)
        raise Exception ("Window not found with title " + window_title)
    return (None)

def get_images (image_name):
    global IMAGES
    folder = IMAGES + "\\" + image_name
    images = []
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, file)):
                images.append(folder + "\\" + file)
    else:
        if os.path.isfile(folder):
            images.append (folder+".PNG")
        else:
            os.makedirs(folder)
    return (images)
def find_image (image_name, timeout):
    global WH_ACTIVE, SCREENSHOT, CONFIDENCE, LEFT, TOP, CONTINUE_ON_ERROR
    timeout = int (timeout)
    repeat=0
    image = None
    images = get_images (image_name)
    if len(images)==0:
        if CONTINUE_ON_ERROR:
            logging.warning('Image file found  ' + image_name)
        else:
            raise Exception ('Image file found  ' + image_name)

    logging.debug("Looking for image {0}  with timeout {1} in region {2}".format(image_name, timeout, REGION))

    while repeat < timeout*5:
        repeat += 1
        for file in images:
            if not os.path.isfile(file):
                if CONTINUE_ON_ERROR:
                    logging.warning("File doesn't exists " + file)
                else:
                    raise Exception ("File doesn't exists " + file)
            logging.debug("Looking for image {0} in region {1}".format(file, timeout, REGION))
            try:
                images = list(pyautogui.locateAllOnScreen(file, region=REGION, confidence=CONFIDENCE))
                image = images[0]
            except:
                logging.debug("Image not found")
            if image is not None:
                break
            repeat += 1

        if WH_ACTIVE is not None:
            WH_ACTIVE.show()
            WH_ACTIVE.activate()

        if image is not None:
            break

    if image is None:
        ag_take_screenshot(IMAGES + "\\" + image_name)
        if CONTINUE_ON_ERROR:
            logging.warning("Image not found {0}".format(image_name))
        else:
            logging.error("Image not found {0}".format(image_name))
            raise Exception ('Image not found on the screen ' + image_name)
    else:
        x=image.left+(image.width/2)
        y=image.top+(image.height/2)
        logging.debug("Image found {0} region  {1} , {2}, {3}, {4}".format(file, image.left, image.top, image.width, image.height ))
        return (x, y)
def wait_vanish (image_name, timeout):
    global CONTINUE_ON_ERROR
    CONTINUE_ON_ERROR = True
    found = find_image(image_name, 2)
    i = 1
    while found and i < timeout:
        try:
            found = find_image(image_name, 5)
        except:
            found = None
        i += 1
    if found is not None:
        if CONTINUE_ON_ERROR:
            logging.warning("Image still on screen " + image_name)
        else:
            raise Exception ("Image still on screen " + image_name)
    else:
        logging.debug("Image vanished  {0} ".format(image_name))
    return (found is None)
def click_on_image (image_name):
    global TIMEOUT, MOUSE_MOVE_SPEED
    image = find_image (image_name, TIMEOUT)
    if image is not None:
        logging.debug("Clicking on image  {0} at {1}:".format(image_name, image))
        pyautogui.moveTo(image[0], image [1], MOUSE_MOVE_SPEED)
        pyautogui.click(image)
    return (image)

def click_on_image_offset (image_name, x, y):
    global TIMEOUT, MOUSE_MOVE_SPEED
    x = int(x)
    y = int(y)
    image = find_image (image_name, TIMEOUT)
    if image is not None:
        logging.debug("Clicking on image  {0} at {1}:".format(image_name, image))
        pyautogui.moveTo(image[0]+x, image [1]+y, MOUSE_MOVE_SPEED)
        pyautogui.click((image[0]+x, image [1]+y))
    return ((image[0]+x, image [1]+y))

def image_type_text(image, text, clear):
    click_on_image(image)
    type(text, clear)

def special_type (car):
    pyperclip.copy(car)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy("")


def type(text, clear):
    logging.debug("Type text : {0}".format(text))
    if clear:
        clear_input ()
    parts = text.split('@')
    if len(parts)>1:
        pyautogui.write(parts[0], interval=0)
        pyperclip.copy("@")
        pyautogui.hotkey('ctrl', 'v')
        pyperclip.copy("")
        pyautogui.write(parts[1], interval=0)
    else:
        pyautogui.typewrite(text, interval=0)
def image_type_text_offset(image, text, x, y, clear):
    x = int(x)
    y=int(y)
    found = find_image(image, 10)
    click_at(found[0] + x, found[1]+y, clear)
    type(text, True)
def click_at (x, y, offset):
    global X, Y
    mouve_mouse_at(x, y, offset)
    pyautogui.click(X, Y)
def mouve_mouse_at (x, y, offset):
    global LEFT, TOP, X, Y
    x = int (x)
    y = int (y)
    logging.debug("Position {0} {1}".format(x, y))
    logging.debug("Screen {0} {1}".format(LEFT, TOP))
    if offset:
        X = x+LEFT
        Y = y+TOP
    else:
        X = x
        Y = y
    pyautogui.moveTo(X, Y, MOUSE_MOVE_SPEED)
    logging.debug("Mouse moved at {0}, {1}".format(X, Y))
def ag_take_screenshot (name):
    im1 = pyautogui.screenshot(region=REGION)
    if os.path.isdir(name):
        file = name + "\\error-" + dt_fr('', '') + ".png"
    else:
        file = os.path.dirname(name) + "\\error-" + dt_fr('', '') + ".png"
    im1.save(file)
def ag_take_region_screenshot (region, name):
    im1 = pyautogui.screenshot(region=region)
    im1.save(SCREENSHOT + "\\" + name + "-" + dt_fr('', '') + ".png")
    return (SCREENSHOT + "\\" + name + "-" + dt_fr('', '') + ".png")
