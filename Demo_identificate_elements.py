"""
Tests d'utilisation

project : projet (nom du dossier principal)
element_searched = éléments recherchés (nom du sous-dossier)
fields = largeur et hauteur des éléments recherchés
marges = marges acceptées

"""

import Libs.PyVisualAutomation as va


project = "Identificate_OHRM"
element_searched = va.identificate_the_current_page(f"{va.dt_fr('', '')}")
field_width = 32
field_height = 32
w_marge = 5
h_marge = 5

# Affiche les éléments correspondants aux dimensions/marges données
elements_found = va.check_elements(field_width, field_height, w_marge, h_marge, project=project)

# with open("points.csv", "r") as f:
#     content = f.read().strip()
#     print(content)
#     line = content.split("\n")
#     print(line)
#
#     for l in line:
#         print(l)
#         point = l.split(";")
#         print(point)
#         x = int(point[1])
#         y = int(point[2])
#         w = int(point[3])
#         h = int(point[4])
#         i = int(point[0])
#         va.ag_take_region_screenshot((x, y, w, h), f"id{i}")
#         # if x == 19:
#         #     va.move_mouse_at(x+ w / 2, y+ h / 2)

# Sauvegarde les éléments correspondants dans le dossier principal
# element_found = va.store_elements(project, element_searched, field_width, field_height, w_marge, h_marge)

# Affiche les éléments correspondants
# elements_found = va.check_elements(field_width, field_height, w_marge, h_marge, 1)

print("Elements trouves: ", elements_found)