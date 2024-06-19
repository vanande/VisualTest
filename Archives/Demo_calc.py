from ..Libs import PyVisualAutomation as va

# Positionne le répertoire des images pour l'application
# sous-dossier du dossier configuré dans PyVisualAutomation.yaml
va.initialize("Calc")
va.switch_to("Calculatrice", False)
va.find_image("Titre", 60)
va.click_on_image("one")
va.click_on_image("plus")
va.click_on_image("two")
va.click_on_image("equal")
va.click_on_image("one")
va.click_on_image("two")
va.click_on_image("one")
va.click_on_image("two")
va.click_on_image("two")
va.click_on_image("equal")
