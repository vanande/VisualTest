import Libs.PyVisualAutomation as va

url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

va.initialize("Practicing_OHRM")

va.run_nav(url)
va.switch_to("OrangeHRM - Google Chrome", True)

va.click_on_element("Login_inputs", "username", 0.5) # Seuil de confiance réduit
va.type_text("Admin", True)
# va.click_on_element("Login_inputs", "password")
va.next_field() # navigue via "tab"
va.type_text("admin123")
va.click_on_element("Login_inputs", "login_button")
va.click_on_element("Navbars_icons", "my_info")
va.click_on_element("Myinfo_regular_fields", "drivers_license_number")
va.type_text("81236", True)
va.scroll(3)
va.click_on_element("Myinfo_save", "save")
va.close_existing_window()