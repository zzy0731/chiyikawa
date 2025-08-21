from PIL import Image
img = Image.open("assets/mouse.png")

# 重新調整尺寸，例如 64x72
resized_img = img.resize((50, 50), Image.LANCZOS)

# 儲存為新的檔案
resized_img.save("assets/mouse_resize.png")