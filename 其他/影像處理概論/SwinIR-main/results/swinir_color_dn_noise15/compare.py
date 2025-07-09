import os
from PIL import Image
import matplotlib.pyplot as plt

# 資料夾設定（順序會對應）
folder1 = r"D:\學校\三下四上四下講義\影像處理概論\project\SwinIR-main\results\swinir_color_dn_noise15\images"
folder2 = r"D:\學校\三下四上四下講義\影像處理概論\project\SwinIR-main\results\swinir_color_dn_noise15\M_dn_256"
folder3 = r"D:\學校\三下四上四下講義\影像處理概論\project\SwinIR-main\results\swinir_color_dn_noise15\M_dn_256_dn"

# 儲存合併結果（可選）
save_combined = True
output_folder = "combined_comparisons"
os.makedirs(output_folder, exist_ok=True)

# 讀取檔案並排序（按檔名字典順序）
files1 = sorted([f for f in os.listdir(folder1) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
files2 = sorted([f for f in os.listdir(folder2) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
files3 = sorted([f for f in os.listdir(folder3) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

# 檢查數量一致
assert len(files1) == len(files2) == len(files3), "❌ 三個資料夾中的圖像數量不一致！"

# 逐張比對（不管檔名，只用索引）
for i in range(len(files1)):
    path1 = os.path.join(folder1, files1[i])
    path2 = os.path.join(folder2, files2[i])
    path3 = os.path.join(folder3, files3[i])

    try:
        img1 = Image.open(path1)
        img2 = Image.open(path2)
        img3 = Image.open(path3)

        # 合併圖片
        combined_width = img1.width + img2.width + img3.width
        combined_img = Image.new('RGB', (combined_width, img1.height))

        combined_img.paste(img1, (0, 0))
        combined_img.paste(img2, (img1.width, 0))
        combined_img.paste(img3, (img1.width + img2.width, 0))

        # 顯示
        plt.figure(figsize=(12, 4))
        plt.imshow(combined_img)
        plt.title(f"Image {i+1} Comparison")
        plt.axis('off')
        plt.show()

        # 儲存
        if save_combined:
            out_path = os.path.join(output_folder, f"comparison_{i+1:03d}.jpg")
            combined_img.save(out_path)

    except Exception as e:
        print(f"⚠️ 發生錯誤於第 {i+1} 張圖片: {e}")

print("✅ 所有圖片比對完成！")

