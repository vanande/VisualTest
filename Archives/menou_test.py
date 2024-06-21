from ..Libs import PyVisualAutomation as va

print(va.gw.getAllTitles())
va.set_active_app("Notion")
va.initialize("Notion")
va.run_application("calc.exe")
va.time.sleep(1)
# # va.switch_to("adi – menou_test.py", True)
# va.type_text("1")
# va.clear_input()
va.click_on_image("one")
va.press("+")
va.click_on_image("two")
va.click_on_image("egal")
