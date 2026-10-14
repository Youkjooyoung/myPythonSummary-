import cv2
import matplotlib.pyplot as plt

# 1. 이미지 로드
img = cv2.imread("backg.jpg")

# 2. 이미지 증강
img_bright = cv2.convertScaleAbs(img, alpha=1, beta=50)
img_dark = cv2.convertScaleAbs(img, alpha=1, beta=-50)
img_flip = cv2.flip(img, 1)
# alpha : 픽셀에 곱하는 값
# beta : 더할 밝기(+ 50 = 밝게)

# 색상(Hue) 변경
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img_hsv)
h_shift = (h + 30) % 180
img_hue = cv2.cvtColor(cv2.merge([h_shift, s, v]), cv2.COLOR_HSV2BGR)

# 채도(Saturation) 변경
s_up = cv2.add(s, 80)
img_sat = cv2.cvtColor(cv2.merge([h, s_up, v]), cv2.COLOR_HSV2BGR)

# 3. 이미지 시각화
fig, ax = plt.subplots(2, 3, figsize=(12, 6))

# 3-1 원본 이미지
ax[0,0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ax[0,0].axis('off')
ax[0,0].set_title("Original")

# 3-2 밝기 이미지
ax[0,1].imshow(cv2.cvtColor(img_bright, cv2.COLOR_BGR2RGB))
ax[0,1].axis('off')
ax[0,1].set_title("Bright")

# 3-3 어두운 이미지
ax[0,2].imshow(cv2.cvtColor(img_dark, cv2.COLOR_BGR2RGB))
ax[0,2].axis('off')
ax[0,2].set_title("Dark")

# 3-4 좌우 반전 이미지
ax[1,0].imshow(cv2.cvtColor(img_flip, cv2.COLOR_BGR2RGB))
ax[1,0].axis('off')
ax[1,0].set_title("Flip")

# 3-5 색상 변경 이미지
ax[1,1].imshow(cv2.cvtColor(img_hue, cv2.COLOR_BGR2RGB))
ax[1,1].axis('off')
ax[1,1].set_title("Hue")

# 3-6 채도 변경 이미지
ax[1,2].imshow(cv2.cvtColor(img_sat, cv2.COLOR_BGR2RGB))
ax[1,2].axis('off')
ax[1,2].set_title("Saturation")

# 4. 그림창 띄우기
plt.tight_layout()
# subplot으로 나눴을때 칸 사이의 간격을 자동으로 맞춰주는기능

plt.show()


# 5. 이미지 저장
cv2.imwrite("./bright_img.jpg", img_bright)
cv2.imwrite("./dark_img.jpg", img_dark)
cv2.imwrite("./flip_img.jpg", img_flip)
cv2.imwrite("./hue_img.jpg", img_hue)
cv2.imwrite("./sat_img.jpg", img_sat)