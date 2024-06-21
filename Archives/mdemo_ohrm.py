"""
BUT: depuis la page de connexion, se connecte en admin et effectue des changements d'informations sur son profil, puis sauvegarde via le bouton de sauvegarde
DIMENSIONS: 1920, 1080
"""

from ..Libs import PyVisualAutomation as va

va.initialize("Mohrm")
va.set_pause(1)
url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
va.set_image_confidence(0.6)
va.run_chrome(url)
# va.switch_to("OrangeHRM - Google Chrome", True)
va.time.sleep(2)
va.click_on_image("login_username")
va.type_text("Admin")
va.click_on_image("login_password")
va.type_text("admin123")
va.click_on_image("login_login")
va.time.sleep(2)
va.click_on_image("nav_my_info")
va.click_on_image("myinfo_employee_full_name")
va.prev_field()
va.type_text("Zendel", True)
va.next_field()
va.type_text("Dr", True)
va.next_field()
va.type_text("Shington", True)
va.click_on_image("myinfo_marital_status")
va.click_on_image("myinfo_marital_status_married")
va.scroll_down(5)
va.click_on_image("myinfo_save", 0.8)
