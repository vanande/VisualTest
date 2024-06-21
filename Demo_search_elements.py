"""
Tests d'utilisation

project : projet (nom du dossier principal)
element_searched = éléments recherchés (nom du sous-dossier)
fields = largeur et hauteur des éléments recherchés
marges = marges acceptées

"""

import Libs.PyVisualAutomation as va

project = "Practicing_2"
element_searched = "Login"
field_width = 32
field_height = 32
w_marge = 8
h_marge = 8

va.initialize(project)

# Affiche les éléments correspondants aux dimensions/marges données
elements_found = va.check_elements(field_width, field_height, w_marge, h_marge, 2, element_searched, save=True, show_process=False)

# Login
element_searched = "Login"



# Dashboard
element_searched = "Dashboard"




# Sauvegarde les éléments correspondants dans le dossier principal
# elements_found = va.store_elements(project, element_searched, field_width, field_height, w_marge, h_marge)

# Affiche les éléments correspondants sur fond sombre /!\ EN TEST /!\
# elements_found = print(va.check_elements_bg_inv(field_width, field_height, w_marge, h_marge, 1))

