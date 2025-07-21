from PIL import Image
img = Image.open("assets/heart.png")

# 重新調整尺寸，例如 64x72
resized_img = img.resize((32, 32), Image.LANCZOS)

# 儲存為新的檔案
resized_img.save("assets/heart_resize.png")