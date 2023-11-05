import cv2
import imutils

# load the image into an RGB nd-array
raw = cv2.imread('.lab/raw.jpg')
image = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)

# convert to gray scale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# find threshold
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# find contours
contours = cv2.findContours(thresh,
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# extract photos
for i, contour in enumerate(contours[:4]):
    # Get the bounding rectangle for the contour
    x, y, w, h = cv2.boundingRect(contour)

    # save the sub-images
    cropped = image[y:y+h, x:x+w]
    image_out = cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f".lab/IMG_{i+1}.jpg", image_out)
