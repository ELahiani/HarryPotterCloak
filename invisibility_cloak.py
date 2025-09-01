#modes:
#0: invis
#1: cartoon
#2: glow
#c: quit
#by eya lahiani

import cv2
import numpy as np
import time

# ----------------== cartoon effect ===----------------
def cartoonify(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)

    color = cv2.bilateralFilter(image, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# ----------------=== live video ===----------------
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(3)

for i in range(60):
    _, background = video.read()
background = np.flip(background, axis=1)

# default effect is invisible cloak
effect_mode = 0

while video.isOpened():
    check, img = video.read()
    if not check:
        break

    img = np.flip(img, axis=1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # detecting blue cloak, you can change the values to detect other cloak colors, try for example: 
    #lower_red = np.array([0,120,50])
    #upper_red = np.array([10,255,255])
    lower_blue = np.array([94, 80, 2])
    upper_blue = np.array([126, 255, 255])
    mask1 = cv2.inRange(hsv, lower_blue, upper_blue)

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask2 = cv2.bitwise_not(mask1)

    cloak_region = cv2.bitwise_and(img, img, mask=mask1)
    rest_region = cv2.bitwise_and(img, img, mask=mask2)

    # ----------------=== effects ===----------------
    if effect_mode == 0:  
        bg_region = cv2.bitwise_and(background, background, mask=mask1)
        final = cv2.addWeighted(rest_region, 1, bg_region, 1, 0)

    elif effect_mode == 1:  
        cartoon_cloak = cartoonify(cloak_region)
        final = cv2.addWeighted(rest_region, 1, cartoon_cloak, 1, 0)

    elif effect_mode == 2:  
        glow = cv2.GaussianBlur(cloak_region, (25, 25), 30)
        glowing_cloak = cv2.addWeighted(cloak_region, 1.0, glow, 0.7, 0)
        final = cv2.addWeighted(rest_region, 1, glowing_cloak, 1, 0)

    cv2.imshow("Magic Cloak", final)

    # ----------------=== controls ===----------------
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):   #quit
        break
    elif key == ord('0'): 
        effect_mode = 0
        print("Switched to: Invisible Cloak")
    elif key == ord('1'): 
        effect_mode = 1
        print("Switched to: Cartoon Cloak")
    elif key == ord('2'): 
        effect_mode = 2
        print("Switched to: Glowing Cloak")

video.release()
cv2.destroyAllWindows()