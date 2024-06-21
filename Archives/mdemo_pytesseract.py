"""
full tuto:
https://www.youtube.com/watch?v=9FCw1xo_s0I&list=PL2VXyKi-KpYuTAZz__9KVl1jQz74bDG7i&index=8&ab_channel=PythonTutorialsforDigitalHumanities

"""

from ..Libs import PyVisualAutomation as va

original_image = va.cv2.imread("Images/Pytesseract/myinfo.png") 
base_image = original_image.copy() 

image = va.cv2.imread("Images/Pytesseract/myinfo_grayscaled.png") 
image = va.thick_font(image, 20)
gray_image = va.cv2.cvtColor(image, va.cv2.COLOR_BGR2GRAY)
va.cv2.imshow("grayscaled", gray_image)
va.cv2.waitKey(0)
# blur = va.cv2.GaussianBlur(gray_image, (7, 7), 0)
# va.cv2.imwrite("Images/Pytesseract/myinfo_gray_blurred.png", blur)
# thresh = va.cv2.threshold(blur, 0, 255, va.cv2.THRESH_BINARY_INV + va.cv2.THRESH_OTSU)[1]
# va.cv2.imwrite("Images/Pytesseract/myinfo_gray_blurred_threshed.png", thresh)
# kernal = va.cv2.getStructuringElement(va.cv2.MORPH_RECT, (3, 13))
# va.cv2.imwrite("Images/Pytesseract/myinfo_gbt_kernal.png", kernal)
# dilate = va.cv2.dilate(thresh, kernal, iterations=1)
# va.cv2.imwrite("Images/Pytesseract/myinfo_gbtk_dilated.png", dilate)
# cnts = va.cv2.findContours(dilate, va.cv2.RETR_EXTERNAL, va.cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# cnts = sorted(cnts, key=lambda x: va.cv2.boundingRect(x)[0])
# for c in cnts:
#     x, y, w, h = va.cv2.boundingRect(c)
#     if h > 10 and w > 80:
#         roi = original_image[y:y+h, x:x+h]
#         va.cv2.imwrite("Images/Pytesseract/index_roi.png", roi)
#         va.cv2.rectangle(original_image, (x, y), (x+w, y+h), (36, 255, 12), 2) #bounding box

# va.cv2.imwrite("Images/Pytesseract/myinfo_gbtkd_bbox.png", original_image)