"""
identifier les champs (ajustable)
/!\ Itère à partir d'en bas à gauche de l'écran, en remontant sur les y, puis déplacement droite sur x
"""
from ..Libs import PyVisualAutomation as va

va.set_pause(1)
va.set_image_confidence(0.6)

"""
"""
# Nom du dossier principal
project = "test_identifying"
# Nom du sous-dossiers
element_searched = "Navbars"
# Largeur/Hauteur de l'élément recherché
field_width = 32
field_height = 32
# Marges acceptées
w_marge = 5
h_marge = 5

i = 0
count = 0
"""
"""

va.initialize(project)
screencast_path = va.ag_take_screenshot(element_searched)
actual_screen = va.cv2.imread(screencast_path)
va.os.remove(screencast_path)

# va.cv2.imshow("image de base", actual_screen)
# va.cv2.waitKey(2000)
gray = va.cv2.cvtColor(actual_screen, va.cv2.COLOR_BGR2GRAY)
# va.cv2.imshow("image grisee", gray)
# va.cv2.waitKey(2000)
thicked = va.thick_font(gray, 8)
blurred = va.cv2.GaussianBlur(thicked, (9,1), 0)
# va.cv2.imshow("image floutee", blurred)
# va.cv2.waitKey(2000)
threshed = va.cv2.threshold(blurred, 0, 255, va.cv2.THRESH_OTSU + va.cv2.THRESH_OTSU)[1]
# va.cv2.imshow("image threshed", threshed)
# va.cv2.waitKey(2000)

cnts, hierarchy = va.cv2.findContours(threshed, va.cv2.RETR_CCOMP, va.cv2.CHAIN_APPROX_SIMPLE)
hierarchy = hierarchy[0]

highest_levels = va.find_highest_hierarchy_level(hierarchy)
max_hierarchy_level = max(highest_levels)
highest_hierarchy_contours = va.extract_highest_level_contours(cnts, highest_levels, max_hierarchy_level)
highest_hierarchy_contours = sorted(highest_hierarchy_contours, key=lambda x: va.cv2.boundingRect(x)[0])

for c in highest_hierarchy_contours:
    x, y, w, h = va.cv2.boundingRect(c)
    va.cv2.rectangle(actual_screen, (x, y), (x + w, y + h), (220, 220, 220), 2)
    if (field_height - h_marge < h < field_height + h_marge) and (field_width - w_marge < w < field_width + w_marge):
        va.ag_take_region_screenshot((x, y, w, h), f"{element_searched}{i}")
        va.cv2.rectangle(actual_screen, (x, y), (x+w, y+h), (36, 255, 12), 2)
        i += 1
        count += 1


va.cv2.imshow("bboxed", actual_screen)
va.cv2.waitKey(5000)

# va.click_on_element(element_searched, "Inputs_fields0")
# va.click_on_element("Inputs_fields", "Inputs_fields1")
#
# va.click_on_element(element_searched, "Navbars0")