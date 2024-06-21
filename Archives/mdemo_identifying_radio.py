"""
identifier les boutons radios avec des bounding boxes
"""
# import cv2
from ..Libs import PyVisualAutomation as va

image = va.cv2.imread("Images/Pytesseract/myinfo.png")
field_width = 20
field_height = 20
w_marge = 500
h_marge = 500

# va.cv2.imshow("image de base", image)
gray = va.cv2.cvtColor(image, va.cv2.COLOR_BGR2GRAY)
# va.cv2.imshow("image grisée", gray)
thicked = va.thick_font(gray, 8)
blurred = va.cv2.GaussianBlur(thicked, (9,1), 0)
# va.cv2.imshow("image floutee", blurred)
threshed = va.cv2.threshold(blurred, 0, 255, va.cv2.THRESH_OTSU + va.cv2.THRESH_OTSU)[1]
# va.cv2.imshow("image threshed", threshed)
# kernal = va.cv2.getStructuringElement(cv2.MORPH_RECT, (16, 1))
# # va.cv2.imshow("kernel", kernal)
# dilated = va.cv2.dilate(threshed, kernal, iterations=1)
# va.cv2.imshow("image dilated", dilated)
cnts, hierarchy = va.cv2.findContours(threshed, va.cv2.RETR_CCOMP, va.cv2.CHAIN_APPROX_SIMPLE)
hierarchy = hierarchy[0]

highest_levels = va.find_highest_hierarchy_level(hierarchy)
max_hierarchy_level = max(highest_levels)
highest_hierarchy_contours = va.extract_highest_level_contours(cnts, highest_levels, max_hierarchy_level)
highest_hierarchy_contours = sorted(highest_hierarchy_contours, key=lambda x: va.cv2.boundingRect(x)[0])


for c in highest_hierarchy_contours:
    x, y, w, h = va.cv2.boundingRect(c)
    if (field_height - h_marge < h < field_height + h_marge) and (field_width - w_marge < w < field_width + w_marge):
        roi = image[y:y+h, x+h]
        va.cv2.imwrite("Images/Pytesseract/test_fields.png", roi)
        va.cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)


bbox = va.cv2.imread("Images/Pytesseract/test_fields.png")
# va.cv2.imshow("bounded image", bbox)
va.cv2.imshow("bboxed", image)
va.cv2.waitKey(7000)

