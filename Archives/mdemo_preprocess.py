from ..Libs import PyVisualAutomation as va

image_file = "../Images/Pytesseract/myinfo.png"
img = va.cv2.imread(image_file)
# va.cv2.imshow("my info page", img)
# va.cv2.waitKey(2000)

inverted_img = va.cv2.bitwise_not(img)
# va.cv2.imwrite("./Images/Pytesseract/myinfo_inverted.png", inverted_img)
# va.cv2.imshow("inverted image", inverted_img)

gray_image = va.grayscale(img)
# va.cv2.imwrite("./Images/Pytesseract/myinfo_grayscaled.png", gray_image)
# va.cv2.imshow("grayscaled image", gray_image)

thresh, img_bw = va.cv2.threshold(gray_image, 200, 230, va.cv2.THRESH_BINARY)
# va.cv2.imwrite("./Images/Pytesseract/myinfo_bw.png", img_bw)
# va.cv2.imshow("black and white image", img_bw)

no_noise = va.noise_removal(img_bw)
# va.cv2.imwrite("./Images/Pytesseract/myinfo_nonoise.png", no_noise)
# va.cv2.imshow("no noised image", no_noise)

eroded_image = va.thin_font(no_noise, 1)
va.cv2.imwrite("./Images/Images/Pytesseract/myinfo_eroded.png", eroded_image)
# va.cv2.imshow("eroded image", eroded_image)

# va.cv2.waitKey(5000)

for _ in range(10):
    va.cv2.imshow("original image", img)
    va.cv2.waitKey(4000)
    va.cv2.destroyAllWindows()
    #
    # va.cv2.imshow("inverted image", inverted_img)
    # va.cv2.waitKey(4000)
    # va.cv2.destroyAllWindows()

    va.cv2.imshow("grayscaled image", gray_image)
    va.cv2.waitKey(4000)
    va.cv2.destroyAllWindows()

    va.cv2.imshow("black and white image", img_bw)
    va.cv2.waitKey(4000)
    va.cv2.destroyAllWindows()
    #
    # va.cv2.imshow("no noised image", no_noise)
    # va.cv2.waitKey(4000)
    # va.cv2.destroyAllWindows()
    #
    # va.cv2.imshow("eroded image", eroded_image)
    # va.cv2.waitKey(4000)
    # va.cv2.destroyAllWindows()

#
# img_file = "./Images/Pytesseract/myinfo_nonoise.png"
# img = va.Image.open(img_file)
# ocr_result = va.pytesseract.image_to_string(img)
# print(ocr_result)