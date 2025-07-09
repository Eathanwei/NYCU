from PIL import Image
import os

input_folder = "D:\\學校\\三下四上四下講義\\影像處理概論\\project\\SwinIR-main\\results\\swinir_color_dn_noise15\\M"       # 原圖資料夾
output_folder = "M_256" # 縮圖儲存資料夾

# 建立輸出資料夾（如果尚未存在）
os.makedirs(output_folder, exist_ok=True)

# 處理所有圖片檔案
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        img = Image.open(input_path)
        img_resized = img.resize((256, 256), Image.LANCZOS)
        img_resized.save(output_path)

print("✅ 所有圖片已使用 PIL 縮圖完成！")
