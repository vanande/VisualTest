import time
from ..Libs import PyVisualAutomation as va

url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
firstname = "Vanande"
lastname = "KHATCHATRIAN"

def click_wait_visible(image, wait=1):
    while va.click_on_image(image) is None:
        time.sleep(wait)

va.initialize("Ohrm")
va.run_chrome(url)
time.sleep(5)
va.pyautogui.typewrite("Admin")
va.pyautogui.press("tab")
va.pyautogui.typewrite("admin123")
va.pyautogui.press("enter")
click_wait_visible("PIM")
va.wait_vanish("PIM", 5)
click_wait_visible("employee_add")

va.wait_vanish("employee_add", 1)
va.image_type_text("employee_first_name", firstname, False)
time.sleep(0.5)
va.image_type_text("employee_last_name", lastname, False)
print("Click on employee save button")
print(va.click_on_image("employee_save"))
time.sleep(2)
if va.click_on_image("err_employee_exist") is not None:
    print("Error message displayed")
    time.sleep(2)
    print("Trying again... Moving down 20px from employee id")
    # va.image_type_text_offset("employee_id", "1", 0, 10, False)
    va.image_type_text_offset("emplyee_id", "1", False)

va.wait_vanish("employee_save_loading", 10)

click_wait_visible("employee_list")

time.sleep(2)
va.image_type_text("employee_search_name", firstname + " " + lastname, False)

click_wait_visible("employee_search_button")

while va.click_on_image("employee_search_result") is not None:
    time.sleep(1)
    va.click_on_image("employee_search_result_confirm")
    time.sleep(3)

va.click_at(1820, 145, 0)
# va.click_on_image("profile")
click_wait_visible("logout")

time.sleep(2)

if va.click_on_image("page_login") is not None:
    print("Logout successful")
else:
    print("Logout failed")

