"""
Tests d'utilisation

project : projet (nom du dossier principal)
element_searched = éléments recherchés (nom du sous-dossier)
fields = largeur et hauteur des éléments recherchés
marges = marges acceptées

"""

import Libs.PyVisualAutomation as va

project = "Practicing_2"

va.initialize(project)


# Affiche les éléments correspondants aux dimensions/marges données
# elements_found = va.check_elements(field_width, field_height, w_marge, h_marge, 2, element_searched, save=True, show_process=False)

# Login
current_page = "Login"
# va.check_elements(element_searched=current_page)
va.wait_page(current_page)
va.click_on_id(9, current_page)
va.type_text("Admin")
va.click_on_id(8, current_page)
va.type_text("admin123")
va.click_on_id(7, current_page)

# Dashboard
current_page = "Dashboard"
# va.check_elements(element_searched=current_page)
va.wait_page("Login")
va.click_on_id(23, current_page)

# PIM
current_page = "PIM"
# va.check_elements(element_searched=current_page)
va.wait_page(current_page)
va.click_on_id(15, current_page)

# Claim
current_page = "Claim"
# va.check_elements(element_searched=current_page)
va.wait_page(current_page)
va.click_on_id(60, current_page)
va.type_text("123123")
va.click_on_id(96, current_page)

# Sauvegarde les éléments correspondants dans le dossier principal
# elements_found = va.store_elements(project, element_searched, field_width, field_height, w_marge, h_marge)

# Affiche les éléments correspondants sur fond sombre /!\ EN TEST /!\
# elements_found = print(va.check_elements_bg_inv(field_width, field_height, w_marge, h_marge, 1))

