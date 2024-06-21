from ..Libs import PyVisualAutomation as va

img_file = "../Images/Pytesseract/triple_menu.png"
img = va.Image.open(img_file)

ocr_result = va.pytesseract.image_to_string(img)
print(ocr_result)