"""
# Automatisation Visuelle d'Environnement
# Automatisation de tâches répétitives sur des applications graphiques
# Utilisation de pyautogui, pygetwindow, pyperclip, pywinauto, pytesseract, opencv-python, pillow

Description globale du projet:
Automatisation de manipulation d'interfaces graphiques d'applications.
A pour but final d'être simplifié en interface d'automatisation prompté; traduit du langage naturel en code.

Contraintes globales:
- Facteurs de reconnaisance d'images, aucun accès au code source
- Utiliser des librairies/outils reconnus

Limitations actuelles:
- Les images doivent être exactement similaire à celles recherchées (pas de rotation, de déformation, de changement de couleur)
"""

import os
import logging.config
import time
from datetime import datetime
import pyperclip
import pyautogui
import pygetwindow as gw
from subprocess_maximize import Popen
import yaml
import cv2
from PIL import Image
import pytesseract
import numpy as np
import re


# Global Variables
MOUSE_MOVE_SPEED = 0
IMAGES = ""
SCREENSHOT = ""
TAKE_SCREENSHOT = ""
CONTINUE_ON_ERROR = False
CONFIDENCE = 0.55
LEFT = 0
TOP = 0
WIDTH = 0
HEIGHT = 0
WH_ACTIVE = None
TIMEOUT = 5
X = 0
Y = 0
REGION = (0, 0, 1920, 1080)
TESSERACT = None


def set_mouse_move_speed(speed):
    global MOUSE_MOVE_SPEED
    MOUSE_MOVE_SPEED = float(speed)


def set_image_confidence(confidence):
    global CONFIDENCE
    CONFIDENCE = float(confidence)


def set_pause(pause):
    pyautogui.PAUSE = float(pause)


def set_timeout(timeout):
    global TIMEOUT
    TIMEOUT = timeout


def scroll_down(occurences):
    for _ in range(occurences):
        pyautogui.scroll(-200)


def scroll_up(occurences):
    for _ in range(occurences):
        pyautogui.scroll(200)


def set_active_app(app):
    """
    définit le répertoire des images
    :param app: nom de l'application
    """
    global IMAGES
    with open(
        os.path.join(os.getcwd(), "Libs", "PyVisualAutomation.yaml"), "r"
    ) as file:
        yaml_config = yaml.safe_load(file)
        IMAGES = os.path.join(yaml_config["IMAGES"], app)


def initialize(app):
    """
    initialise les variables globales
    :param app: nom de l'application
    """
    global MOUSE_MOVE_SPEED, IMAGES, SCREENSHOT, TAKE_SCREENSHOT, CONFIDENCE, TIMEOUT, TESSERACT, WH_ACTIVE, HEIGHT, WIDTH, CONTINUE_ON_ERROR
    logging.config.fileConfig(os.path.join(os.getcwd(), "logging.conf"))
    set_active_app(app)
    with open(
        os.path.join(os.getcwd(), "Libs", "PyVisualAutomation.yaml"), "r"
    ) as file:
        yaml_config = yaml.safe_load(file)
        pyautogui.FAILSAFE = yaml_config["FAILSAFE"]
        pyautogui.PAUSE = yaml_config["PAUSE"]
        MOUSE_MOVE_SPEED = yaml_config["MOUSE_MOVE_SPEED"]
        SCREENSHOT = yaml_config["SCREENSHOT"]
        TAKE_SCREENSHOT = yaml_config["TAKE_SCREENSHOT"].lower()
        CONTINUE_ON_ERROR = yaml_config["CONTINUE_ON_ERROR"]
        CONFIDENCE = yaml_config["CONFIDENCE"]
        TIMEOUT = yaml_config["TIMEOUT"]
        IMAGES = os.path.join(yaml_config["IMAGES"], app)
        WIDTH, HEIGHT = pyautogui.size()


def close_existing_window():
    global WH_ACTIVE
    if WH_ACTIVE:
        WH_ACTIVE.close()
        press("enter")
        WH_ACTIVE = None


def run_application(app):
    logging.debug(f"Launch {app}")
    Popen(app, shell=True)


def run_chrome(url, wait_time=3):
    """
    lance une nouvelle fenêtre de chrome en mode privé
    :param url: url à ouvrir
    !! à adapter en fonction de l'emplacement de chrome sur le poste
    ++ plus de modularité en ajoutant des arguments à la fonction (ex: chemin de chrome, mode privé, fenêtre maximisée)
    """
    cmd = f'"C:\\Program Files\\Google\\Chrome\\Application\\Chrome" -aggressive-cache-discard -new-window -incognito -start-maximized "{url}"'
    logging.debug(f"Launch {url}")
    Popen(cmd, show="maximize", priority=0)
    time.sleep(wait_time)


def refresh():
    pyautogui.press("f5")


def press(key):
    pyautogui.press(key)


def next_window():
    with pyautogui.hold("alt"):
        pyautogui.press("tab")


def resize(h, w):
    global WH_ACTIVE
    if WH_ACTIVE and (WH_ACTIVE.width != w or WH_ACTIVE.height != h):
        WH_ACTIVE.resizeTo(h, w)
        WH_ACTIVE.moveTo(0, 0)
        time.sleep(3)


def window_close():
    global WH_ACTIVE
    with pyautogui.hold("alt"):
        pyautogui.press("f4")
    WH_ACTIVE = None


def close_tab():
    with pyautogui.hold("ctrl"):
        pyautogui.press(["z", "w"])


def page_down():
    pyautogui.press("pagedown")


def page_up():
    pyautogui.press("pageup")


def clear_input():
    with pyautogui.hold("ctrl"):
        pyautogui.press("a")
    pyautogui.press("delete")


def dt_fr(dt_sep, time_sep):
    return datetime.now().strftime(f"%Y{dt_sep}%m{dt_sep}%dT%H{time_sep}%M{time_sep}%S")


def switch_to(window_title, maximize):
    """
    rend actif la fenêtre
    :param window_title: titre de la fenêtre
    :param maximize: maximiser la fenêtre
    """
    global WH_ACTIVE, TIMEOUT, LEFT, TOP, WIDTH, HEIGHT, REGION, CONTINUE_ON_ERROR

    title = ""
    i = 0
    while i < TIMEOUT:
        titles = gw.getAllTitles()
        for title in titles:
            if window_title.lower() in title.lower():
                logging.debug(f"Windows {title.encode()} found")
                WH_ACTIVE = gw.getWindowsWithTitle(window_title)[0]
                if maximize and not WH_ACTIVE.isMaximized:
                    WH_ACTIVE.maximize()
                    time.sleep(3)

                LEFT = WH_ACTIVE.left + 8
                TOP = WH_ACTIVE.top + 8
                WIDTH = WH_ACTIVE.width + 8
                HEIGHT = WH_ACTIVE.height + 8
                REGION = (LEFT, TOP, WIDTH, HEIGHT)
                WH_ACTIVE.show()
                try:
                    WH_ACTIVE.activate()
                except Exception as e:
                    logging.error(f"Error activating window: {e}")
                return WH_ACTIVE
        time.sleep(1)
        i += 1

    if CONTINUE_ON_ERROR:
        logging.warning(f"Window not found with title {window_title}")
    else:
        logging.error(f"Window not found with title {window_title}")
        raise Exception(f"Window not found with title {window_title}")


def get_images(image_name):
    """
    récupère les images
    :param image_name: nom de l'image
    :return: liste des images
    ?? si le dossier n'existe pas, le crée
    """
    global IMAGES
    folder = os.path.join(IMAGES, image_name)

    if os.path.isdir(folder):
        images = []
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                images.append(file_path)
        return images

    elif os.path.isfile(folder):
        return [folder + ".PNG"]

    else:
        os.makedirs(folder)
        return []


def find_image(image_name, timeout, confidence):
    """
    cherche une image sur l'écran
    :param image_name: nom de l'image
    :param timeout: temps d'attente
    :param confidence: seuil de confiance
    :return: coordonnées de l'image
    ?? si l'image n'est pas trouvée, prend un screenshot et le sauvegarde dans le dossier IMAGES
    """
    global IMAGES, CONTINUE_ON_ERROR, REGION

    timeout = int(timeout)
    images = get_images(image_name)

    if not images:
        ag_take_screenshot(image_name)
        handle_image_not_found(image_name)

    logging.debug(
        f"Looking for image {image_name} with timeout {timeout} in region {REGION}"
    )
    end_time = time.time() + timeout

    while time.time() < end_time:
        for file in images:
            if not os.path.isfile(file):
                handle_file_not_found(file)
            image = locate_image_on_screen(file, confidence)
            if image:
                x, y = image.left + image.width / 2, image.top + image.height / 2
                logging.debug(
                    f"Image found {file} region {image.left}, {image.top}, {image.width}, {image.height}"
                )
                return x, y
        time.sleep(0.2)

    ag_take_screenshot(IMAGES + "\\" + image_name)
    handle_image_not_found(image_name)


def handle_image_not_found(image_name):
    if CONTINUE_ON_ERROR:
        logging.warning(f"Image file not found: {image_name}")
    else:
        raise Exception(f"Image file not found: {image_name}")


def handle_file_not_found(file):
    if CONTINUE_ON_ERROR:
        logging.warning(f"File doesn't exist: {file}")
    else:
        raise Exception(f"File doesn't exist: {file}")


def locate_image_on_screen(file, confidence):
    """
    localise une image sur l'écran
    :param file: image à localiser
    :param confidence: seuil de confiance
    :return: coordonnées de l'image
    """
    try:
        return pyautogui.locateOnScreen(file, region=REGION, confidence=confidence)
    except Exception as e:
        logging.debug(f"Image not found due to error: {e}")
        return None


def wait_vanish(image_name, timeout):
    """
    attend que l'image ne soit plus trouvée sur l'écran
    :param image_name: nom de l'image
    :param timeout: temps d'attente
    """
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
    if found:
        if CONTINUE_ON_ERROR:
            logging.warning(f"Image still on screen: {image_name}")
        else:
            raise Exception(f"Image still on screen: {image_name}")
    else:
        logging.debug(f"Image vanished: {image_name}")
    return not found


def click_on_image(image_name, confidence=None):
    if confidence is None:
        confidence = CONFIDENCE

    image = find_image(image_name, TIMEOUT, confidence)
    if image:
        logging.debug(f"Clicking on image {image_name} at {image}")
        pyautogui.moveTo(image[0], image[1], MOUSE_MOVE_SPEED)
        pyautogui.click(image)
    return image


def click_on_image_offset(image_name, x, y):
    """
    clique sur une image avec un décalage, utilisée en plan b
    :param image_name: nom de l'image
    :param x: décalage en x
    :param y: décalage en y
    !! à remplacer, solution non optimale
    """
    x, y = int(x), int(y)
    image = find_image(image_name, TIMEOUT)
    if image:
        logging.debug(f"Clicking on image {image_name} at offset {x}, {y}")
        pyautogui.moveTo(image[0] + x, image[1] + y, MOUSE_MOVE_SPEED)
        pyautogui.click((image[0] + x, image[1] + y))
    return (image[0] + x, image[1] + y)


def image_type_text(image, text, clear):
    click_on_image(image)
    type_text(text, clear)


def special_type(car):
    pyperclip.copy(car)
    pyautogui.hotkey("ctrl", "v")
    pyperclip.copy("")


def prev_field():
    """
    permet de naviguer entre les champs de saisie
    ?? dans ce cas, le champs précédent
    """
    with pyautogui.hold("shift"):
        pyautogui.press("tab")


def next_field():
    """
    ?? dans ce cas, le champs suivant
    """
    pyautogui.press("tab")


def type_text(text, clear=False):
    """
    écrit du texte
    :param text: texte à écrire
    :param clear: efface le champ avant d'écrire, par défaut False
    """
    logging.debug(f"Type text: {text}")
    if clear:
        clear_input()
    parts = text.split("@")
    if len(parts) > 1:
        pyautogui.write(parts[0], interval=0)
        pyperclip.copy("@")
        pyautogui.hotkey("ctrl", "v")
        pyperclip.copy("")
        pyautogui.write(parts[1], interval=0)
    else:
        pyautogui.typewrite(text, interval=0)


def image_type_text_offset(image, text, x, y, clear):
    x, y = int(x), int(y)
    found = find_image(image, 10)
    click_at(found[0] + x, found[1] + y, clear)
    type_text(text, True)


def click_at(x, y, offset=False):
    move_mouse_at(x, y, offset)
    pyautogui.click(X, Y)


def move_mouse_at(x, y, offset=False):
    global LEFT, TOP, X, Y
    x, y = int(x), int(y)
    if offset:
        X, Y = x + LEFT, y + TOP
    else:
        X, Y = x, y
    pyautogui.moveTo(X, Y, MOUSE_MOVE_SPEED)
    logging.debug(f"Mouse moved to {X}, {Y}")


def ag_take_screenshot(name, save_format=""):
    """
    prend un screenshot
    :param name: nom du fichier ou du dossier de sauvegarde
    :param save_format: format dans lequel on souhaite sauvegarder (pas de sauvegarde par défaut)
    :return: chemin du fichier
    """

    if save_format == "file":
        im1 = pyautogui.screenshot(region=REGION)
        file_path = os.path.join(SCREENSHOT, f"{name}-{dt_fr('', '')}.png")
        im1.save(file_path)
        return file_path

    elif save_format == "dir":
        im1 = pyautogui.screenshot(region=REGION)
        save_dir = os.path.join(SCREENSHOT, name)
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f"{name}-{dt_fr('', '')}.png")
        im1.save(file_path)
        return file_path

    else:
        im1 = pyautogui.screenshot(region=REGION)
        if os.path.isdir(os.path.join(SCREENSHOT, name)):
            save_dir = os.path.join(SCREENSHOT, name)
        else:
            save_dir = os.path.join(SCREENSHOT, os.path.basename(name))
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f"{name}-{dt_fr('', '')}.png")
        im1.save(file_path)
        return file_path


def ag_take_region_screenshot(region, name):
    """
    prend un screenshot d'une région spécifique
    :param region: la région de l'écran à capturer
    :param name: nom du fichier ou du dossier de sauvegarde
    :return: chemin du fichier
    ?? utilisée pour stocker les éléments dans le fichier correspondant
    ?? utilisation du regex pour trouver le dossier correspondant aux éléments, ex:
        - "Navbar31.png" sera stocké dans "Navbar"
    """
    global WIDTH, HEIGHT
    im1 = pyautogui.screenshot(region=region)

    base_name = re.sub(r"\d+$", "", name)
    base_name = f"{base_name}_{WIDTH}x{HEIGHT}"
    base_dir = os.path.join(IMAGES, base_name)

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    file_path = os.path.join(base_dir, f"{name}.png")

    im1.save(file_path)
    return file_path


def grayscale(image):
    """
    convertit une image en nuances de gris
    :param image: image à griser
    :return: image en nuances de gris
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def noise_removal(image):
    """
    nettoie les imperfections, inutile pour environnements numériques, utile pour documents
    :param image: image à nettoyer
    :return: image sans bruit
    """
    kernal = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernal, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 1)
    return image


def thin_font(image, shape):
    """
    :param image: image avec du texte à affiner
    :param shape: intensité
    :return: image avec le texte affiné
    """
    image = cv2.bitwise_not(image)
    kernel = np.ones((shape), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image


def thick_font(image, shape):
    """
    :param image: image avec du texte à rendre gras
    :param shape: intensité
    :return: image avec le texte rendu gras
    """
    image = cv2.bitwise_not(image)
    kernel = np.ones((shape), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image


def find_highest_hierarchy_level(hierarchy):
    """
    trouve le plus petit enfant pour chaque contour
    :param hierarchy: hiérarchie des contours
    :return: liste des niveaux les plus élevés
    ?? afin de ne pas prendre en compte les contours internes, soient les champs de saisie uniquement
    """
    highest_levels = []
    for i in range(len(hierarchy)):
        level = 0
        parent = hierarchy[i][3]
        while parent != -1:
            level += 1
            parent = hierarchy[parent][3]
        highest_levels.append(level)
    return highest_levels


def extract_highest_level_contours(contours, highest_levels, max_level):
    """
    extrait les contours les plus élevés (les plus petits dans l'imbrication)
    :param contours: contours
    :param highest_levels: niveaux les plus élevés
    :param max_level: niveau maximal
    :return: contours les plus élevés
    """
    highest_level_contours = []
    for i in range(len(contours)):
        if highest_levels[i] == max_level:
            highest_level_contours.append(contours[i])
    return highest_level_contours


def get_element(folder, name):
    """
    récupère l'image d'un élément dans un dossier particulier
    :param folder: nom du dossier
    :param name: nom du fichier
    :return: chemin du fichier
    """
    global IMAGES

    for dir_name in os.listdir(IMAGES):
        dir_path = os.path.join(IMAGES, dir_name)
        if dir_name.startswith(folder) and os.path.isdir(dir_path):
            file_path = os.path.join(dir_path, name + ".PNG")
            if os.path.exists(file_path):
                return file_path

    handle_file_not_found(os.path.join(IMAGES, folder, name + ".PNG"))


def find_element(folder, image, confidence=None, timeout=None):
    """
    cherche l'image sur l'écran courant
    :param folder: nom du dossier
    :param image: nom du fichier
    :param confidence: seuil de confiance
    :param timeout: temps d'attente maximal
    :return: coordonnées de l'image
    """
    global IMAGES, TIMEOUT, CONFIDENCE, REGION

    timeout = timeout if timeout is not None else TIMEOUT
    confidence = confidence if confidence is not None else CONFIDENCE
    end_time = time.time() + timeout

    try:
        image_path = get_element(folder, image)
    except FileNotFoundError:
        # ag_take_screenshot(image)
        handle_image_not_found(image)

    logging.debug(
        f"Looking for image '{image}' in folder '{folder}' with timeout {timeout} in region {REGION}."
    )

    while time.time() < end_time:
        try:
            if not os.path.isfile(image_path):
                handle_file_not_found(image_path)
            image_location = locate_image_on_screen(image_path, confidence)
            if image_location:
                x, y = (
                    image_location.left + image_location.width / 2,
                    image_location.top + image_location.height / 2,
                )
                return x, y
        except Exception as e:
            logging.error(f"Error locating image: {e}")
        time.sleep(0.2)

    # ag_take_screenshot(IMAGES + "\\" + image)
    raise FileNotFoundError(
        f"Could not find image '{image}' in folder '{folder}' within the timeout period."
    )


def click_on_element(folder, image, confidence=None, timeout=None):
    """
    clique sur l'image
    :param folder: nom du dossier
    :param image: nom de l'image
    :param confidence: seuil de confiance
    :param timeout: temps d'attente maximal
    :return: positions x, y
    """
    global CONFIDENCE, TIMEOUT

    if confidence is None:
        confidence = CONFIDENCE

    element = find_element(folder, image, confidence, timeout)

    x = element[0]
    y = element[1]

    pyautogui.moveTo(x, y, MOUSE_MOVE_SPEED)
    pyautogui.click()
    return element


def store_elements(
    project,
    element_searched,
    field_width,
    field_height,
    w_marge=None,
    h_marge=None,
    i=0,
):
    """
    recherche les éléments correspondant aux tailles indiquées
    :param project: projet (nom du dossier principal)
    :param element_searched: éléments recherchés (nom du sous-dossier)
    :param field_width: largeur de l'élément recherché
    :param field_height: hauteur
    :param w_marge: marge de largeur
    :param h_marge: marge de hauteur
    :param i: indice d'identification des éléments
    :return: nombre d'éléments trouvés
    """

    if w_marge is None:
        w_marge = field_width * 0.1

    if h_marge is None:
        h_marge = field_height * 0.1

    initialize(project)
    screencast_path = ag_take_screenshot(element_searched)
    actual_screen = cv2.imread(screencast_path)
    os.remove(screencast_path)

    count = 0

    gray = cv2.cvtColor(actual_screen, cv2.COLOR_BGR2GRAY)
    thicked = thick_font(gray, 8)
    blurred = cv2.GaussianBlur(thicked, (9, 1), 0)
    threshed = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_OTSU)[1]

    cnts, hierarchy = cv2.findContours(
        threshed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    hierarchy = hierarchy[0]

    highest_levels = find_highest_hierarchy_level(hierarchy)
    max_hierarchy_level = max(highest_levels)
    highest_hierarchy_contours = extract_highest_level_contours(
        cnts, highest_levels, max_hierarchy_level
    )
    highest_hierarchy_contours = sorted(
        highest_hierarchy_contours, key=lambda x: cv2.boundingRect(x)[0]
    )

    for c in highest_hierarchy_contours:
        x, y, w, h = cv2.boundingRect(c)

        if (field_height - h_marge < h < field_height + h_marge) and (
            field_width - w_marge < w < field_width + w_marge
        ):
            ag_take_region_screenshot((x, y, w, h), f"{element_searched}{i}")

            i += 1
            count += 1

    return count


def check_elements(
    field_width,
    field_height,
    w_marge=None,
    h_marge=None,
    seconds=0,
    project="check_element",
    save=False,
):
    """
    affiche les résultats (bounding boxes)
    :param field_width: largeur de l'élément recherché
    :param field_height: hauteur
    :param w_marge: marge de largeur
    :param h_marge: marge de hauteur
    :param seconds: temps d'affichage (infini par défaut)
    :param project: dossier dans lequel il sera stocké (puis supprimé)
    :param save: sauvegarde des résultats (bouding boxes)
    :return: nombre d'éléments trouvés
    """

    if w_marge is None:
        w_marge = field_width * 0.1

    if h_marge is None:
        h_marge = field_height * 0.1

    count = 0
    i = 0
    valid_results = (36, 255, 12)  # rgb
    false_results = (220, 220, 220)

    initialize(project)
    screencast_path = ag_take_screenshot(project)
    actual_screen = cv2.imread(screencast_path)
    os.remove(screencast_path)

    gray = cv2.cvtColor(actual_screen, cv2.COLOR_BGR2GRAY)
    # display_full_screen(gray, "Elements grises", seconds)

    thicked = thick_font(gray, 8)
    # display_full_screen(thicked, "Elements rendus gras", seconds)

    blurred = cv2.GaussianBlur(thicked, (9, 1), 0)
    # display_full_screen(blurred, "Elements floutes", seconds)

    threshed = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_OTSU)[1]
    # threshed = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_OTSU, 11, 2)[1]
    # display_full_screen(threshed, "Elements threshed", seconds)

    cnts, hierarchy = cv2.findContours(
        threshed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    hierarchy = hierarchy[0]

    highest_levels = find_highest_hierarchy_level(hierarchy)
    max_hierarchy_level = max(highest_levels)
    highest_hierarchy_contours = extract_highest_level_contours(
        cnts, highest_levels, max_hierarchy_level
    )
    highest_hierarchy_contours = sorted(
        highest_hierarchy_contours, key=lambda x: cv2.boundingRect(x)[0]
    )

    # with open("points.csv", "w") as f:
    #     f.write("")
    #     # f.write("I;X;Y;W;H\n")
    for c in highest_hierarchy_contours:
        x, y, w, h = cv2.boundingRect(c)

        write_in_file(f"{screencast_path}_points.csv", f"{i};{x};{y};{w};{h}\n")

        if w < 10 or h < 10:
            continue

        cv2.rectangle(actual_screen, (x, y), (x + w, y + h), false_results, 2)
        i += 1

        cv2.putText(
            actual_screen,
            str(i),
            (x + int(w / 2), y + int(h / 2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
        )

        if (field_height - h_marge < h < field_height + h_marge) and (
            field_width - w_marge < w < field_width + w_marge
        ):
            cv2.rectangle(actual_screen, (x, y), (x + w, y + h), valid_results, 2)

            count += 1

    display_full_screen(actual_screen, "Elements trouves", seconds)

    if save:
        ag_take_screenshot(screencast_path, save_format="file")

    return count


def display_full_screen(image, window_name="FullScreenWindow", wait_time=0):
    """
    ouvre l'image en plein écran
    :param image: image
    :param window_name: descriptif
    :param wait_time: temps d'affichage (infini par défaut)
    :return:
    !! utilisé pour imshow()
    """
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, image)
    cv2.waitKey(wait_time * 1000)
    cv2.destroyAllWindows()


def check_elements_bg_inv(
    field_width, field_height, w_marge=None, h_marge=None, seconds=0, project="check"
):
    """
    affiche les résultats (bounding boxes)
    :param field_width: largeur de l'élément recherché
    :param field_height: hauteur
    :param w_marge: marge de largeur
    :param h_marge: marge de hauteur
    :param seconds: temps d'affichage (infini par défaut)
    :return: nombre d'éléments trouvés
    /!\ EN TEST /!\
    ?? Ajusté pour fond sombre
    """

    if w_marge is None:
        w_marge = field_width * 0.1

    if h_marge is None:
        h_marge = field_height * 0.1

    initialize(project)
    screencast_path = ag_take_screenshot("check")
    actual_screen = cv2.imread(screencast_path)
    os.remove(screencast_path)

    count = 0
    valid_results = (36, 255, 12)  # rgb
    false_results = (220, 220, 220)

    gray = cv2.cvtColor(actual_screen, cv2.COLOR_BGR2GRAY)
    # gray = cv2.medianBlur(actual_screen, 5)
    display_full_screen(gray, "Page grisee", seconds)

    invert = cv2.bitwise_not(gray)
    display_full_screen(invert, "Couleurs inversees", seconds)

    thicked = thick_font(invert, 8)
    display_full_screen(thicked, "Elements rendus gras", seconds)

    blurred = cv2.GaussianBlur(thicked, (9, 1), 0)
    # blurred = cv2.medianBlur(thicked, 5)
    display_full_screen(blurred, "Elements floutes", seconds)

    # threshed = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2)
    threshed = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    display_full_screen(threshed, "Elements threshed", seconds * 5)

    cnts, hierarchy = cv2.findContours(
        threshed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    hierarchy = hierarchy[0]

    highest_levels = find_highest_hierarchy_level(hierarchy)
    max_hierarchy_level = max(highest_levels)
    highest_hierarchy_contours = extract_highest_level_contours(
        cnts, highest_levels, max_hierarchy_level
    )
    highest_hierarchy_contours = sorted(
        highest_hierarchy_contours, key=lambda x: cv2.boundingRect(x)[0]
    )

    for c in highest_hierarchy_contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(actual_screen, (x, y), (x + w, y + h), false_results, 2)

        if (field_height - h_marge < h < field_height + h_marge) and (
            field_width - w_marge < w < field_width + w_marge
        ):
            cv2.rectangle(actual_screen, (x, y), (x + w, y + h), valid_results, 2)

            count += 1

    display_full_screen(actual_screen, "Elements trouves", seconds * 5)

    return count


def check_text(
    text, place=-1, sensitivy=False, seconds=0, project="check_text", save=False
):
    """
    affiche les occurences (bouding boxes)
    :param text: caractères cherchés
    :param place: i-ème occurence (les affiche toutes par défaut)
    :param sensitivy: sensibilité à la casse
    :param seconds: temps d'affichage (infini par défaut)
    :param project: dossier dans lequel il sera stocké (puis supprimé)
    :param save: sauvegarde des résultats (bouding boxes)
    :return: nombre d'occurences trouvées
    """

    initialize(project)
    screencast_path = ag_take_screenshot(project)
    actual_screen = cv2.imread(screencast_path)


def write_in_file(file, text):
    """
    stocke les coordonnées des bounding boxes
    :param file: fichier
    :param text: texte à écrire
    """
    with open(file, "a") as f:
        f.write(text)


def identificate_the_current_page(name):
    """
    identifie le nom de la page courante en accédant à l'url
    par exemple: https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList
    retournera : web/index.php/pim/viewEmployeeList
    utiliser du regex afin de ne pas avoir à modifier la fonction à chaque fois, ne gardant que ce qui se trouve après .com
    :return: l'identifiant de la page actuelle
    """
    return name
