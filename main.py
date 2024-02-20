import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

# Creating Tkinter Window and Label
window = Tk()
window.geometry("800x1000")
window.bind('<Escape>', lambda e: window.quit())
video = Label(window)
video.pack()
video.place(relx=0.5, rely=0.3, anchor=CENTER)
# Getting video from webcam
cap = cv2.VideoCapture(0)

def empty(x):
    pass

# window for Saturation and Value to adjust depending on the current light
cv2.namedWindow("Threshold")
cv2.resizeWindow("Threshold", 300, 200)
cv2.createTrackbar("Lower S", "Threshold", 50, 255, empty)
cv2.createTrackbar("Lower V", "Threshold", 61, 255, empty)
cv2.createTrackbar("Upper S", "Threshold", 255, 255, empty)
cv2.createTrackbar("Upper V", "Threshold", 150, 255, empty)

# #color intervals
# # hue
# # red 0-10 & 171-180
lower_red1 = 0
upper_red1 = 11
lower_red2 = 171
upper_red2 = 180
# # orange 11-20
lower_orange = 10
upper_orange = 20
# # yellow 21-35
lower_yellow = 21
upper_yellow = 35
# # green 36-80
lower_green = 36
upper_green = 80
# # cyan 81-100
lower_cyan = 81
upper_cyan = 100
# # blue 101-130
lower_blue = 101
upper_blue = 130
# # purple 131-150
lower_purple = 131
upper_purple = 150
# # magenta 151-170
lower_magenta = 151
upper_magenta = 180

# buttons setters commands
btnred = 0
def btnred_pressed():
    global btnred
    if btnred == 0:
        btnred = 1

    elif btnred == 1:
        btnred = 0
    print(btnred)

btn_red = Button(window, text="Red", bg = '#FF0000', command=btnred_pressed)
btn_red.pack()
btn_red.place(relx=0.2, rely=0.8, anchor=CENTER)

btnorg = 0
def btnorg_pressed():
    global btnorg
    if btnorg == 0:
        btnorg = 1
    elif btnorg == 1:
        btnorg = 0
    print(btnorg)

btn_org = Button(window, text="Orange", bg = '#FF7D00', command=btnorg_pressed)
btn_org.pack()
btn_org.place(relx=0.4, rely=0.8, anchor=CENTER)

btnylw = 0
def btnylw_pressed():
    global btnylw
    if btnylw == 0:
        btnylw = 1
    elif btnylw == 1:
        btnylw = 0
    print(btnylw)

btn_ylw = Button(window, text="Yellow", bg = '#FFFF00', command=btnylw_pressed)
btn_ylw.pack()
btn_ylw.place(relx=0.6, rely=0.8, anchor=CENTER)

btngrn = 0
def btngrn_pressed():
    global btngrn
    if btngrn == 0:
        btngrn = 1
    elif btngrn == 1:
        btngrn = 0
    print(btngrn)

btn_grn = Button(window, text="Green", bg = '#00FF00', command=btngrn_pressed)
btn_grn.pack()
btn_grn.place(relx=0.8, rely=0.8, anchor=CENTER)

btncyn = 0
def btncyn_pressed():
    global btncyn
    if btncyn == 0:
        btncyn = 1
    elif btncyn == 1:
        btncyn = 0
    print(btncyn)

btn_cyn = Button(window, text="Cyan", bg='#00FFFF', command=btncyn_pressed)
btn_cyn.pack()
btn_cyn.place(relx=0.2, rely=0.9, anchor=CENTER)

btnblue = 0
def btnblue_pressed():
    global btnblue
    if btnblue == 0:
        btnblue = 1
    elif btnblue == 1:
        btnblue = 0
    print(btnblue)

btn_blue = Button(window, text="Blue", bg='#0000FF', command=btnblue_pressed)
btn_blue.pack()
btn_blue.place(relx=0.4, rely=0.9, anchor=CENTER)

btnprp = 0
def btnprp_pressed():
    global btnprp
    if btnprp == 0:
        btnprp = 1
    elif btnprp == 1:
        btnprp = 0
    print(btnprp)

btn_prp = Button(window, text="Purple", bg = '#7D00FF', command=btnprp_pressed)
btn_prp.pack()
btn_prp.place(relx=0.6, rely=0.9, anchor=CENTER)

btnmag = 0
def btnmag_pressed():
    global btnmag
    if btnmag == 0:
        btnmag = 1
    elif btnmag == 1:
        btnmag = 0
    print(btnmag)

btn_mag = Button(window, text="Magenta", bg='#FF00FF', command=btnmag_pressed)
btn_mag.pack()
btn_mag.place(relx=0.8, rely=0.9, anchor=CENTER)


# create mask with color values
def createFinalMask(img, l, u):
    lower = l[0]
    upper = u[0]
    if btnred == 1:
        lower = lower_red1
        upper = upper_red1
    if btnorg == 1:
        lower = lower_orange
        upper = upper_orange
    if btnylw == 1:
        lower = lower_yellow
        upper = upper_yellow
    if btngrn == 1:
        lower = lower_green
        upper = upper_green
    if btncyn == 1:
        lower = lower_cyan
        upper = upper_cyan
    if btnblue == 1:
        lower = lower_blue
        upper = upper_blue
    if btnprp == 1:
        lower = lower_purple
        upper = upper_purple
    if btnmag == 1:
        lower = lower_magenta
        upper = upper_magenta
    l[0] = lower
    u[0] = upper
    maskdef = cv2.inRange(img, l, u)
    mask = maskdef
    return mask

# detect contours + circles using compactity
def detectCircles(img_cntrs, result):
    contours, h = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 300:
            #cv2.drawContours(img_cntrs, cnt, -1, (255, 0, 255), 3)
            aprx_cont = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            perim_cnt = cv2.arcLength(aprx_cont, True)
            area_cnt = cv2.contourArea(aprx_cont)
            if area_cnt:
                compct = (perim_cnt * perim_cnt) / area_cnt
                if compct > 12.4 and compct < 13: # compactity for circle is aprox. 12.56
                    (x, y), radius = cv2.minEnclosingCircle(aprx_cont)
                    center = (int(x), int(y))
                    radius = int(radius)
                    cv2.circle(img_cntrs, center, radius, (0, 255, 0), 4)


while (True):
    Ls = cv2.getTrackbarPos("Lower S", "Threshold")
    Lv = cv2.getTrackbarPos("Lower V", "Threshold")
    Us = cv2.getTrackbarPos("Upper S", "Threshold")
    Uv = cv2.getTrackbarPos("Upper V", "Threshold")

    lw = np.array([0, Ls, Lv])
    up = np.array([180, Us, Uv])

    _, im = cap.read()
    #im = cv2.imread('shapes.png')

    img = cv2.bilateralFilter(im, 7, 90, 90)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    img_mask = createFinalMask(img_hsv, lw, up)

    result = cv2.bitwise_and(img, img, mask=img_mask)

    img_cntrs = img.copy()

    detectCircles(img_cntrs, img_mask)

    cv2image = cv2.cvtColor(img_cntrs, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video.config(image=imgtk)


    #cv2.imshow("hsv", img_hsv)
    cv2.imshow("hsv + mask", result)

    window.update()

    if cv2.waitKey(1) == 27: # press Esc to close window
        break

cap.release()
cv2.destroyAllWindows()
window.mainloop()


