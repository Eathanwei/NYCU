import cv2
import os
import glob
import numpy as np

def median_downsample(image, factor=2):
    """
    使用中值濾波進行降採樣：將圖片縮小為原圖的 1/factor
    :param image: 原始圖像 (np.ndarray)
    :param factor: 縮小倍數（預設 2，即縮成原來的 1/4）
    :return: 中值縮小後的圖像
    """
    h, w = image.shape[:2]
    h_new = h // factor
    w_new = w // factor

    # 修正維度為 factor 倍數
    image = image[:h_new * factor, :w_new * factor]

    # 將圖像分成 (factor x factor) 小區塊，取中位數
    downsampled = np.zeros((h_new, w_new, image.shape[2]), dtype=np.uint8)
    for y in range(h_new):
        for x in range(w_new):
            patch = image[y*factor:(y+1)*factor, x*factor:(x+1)*factor, :]
            downsampled[y, x, :] = np.median(patch.reshape(-1, 3), axis=0)
    return downsampled


def batch_median_downsample(input_folder, output_folder, factor=2):
    os.makedirs(output_folder, exist_ok=True)
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(input_folder, ext)))

    if not image_paths:
        print(f"❌ 找不到圖片於：{input_folder}")
        return

    print(f"🔽 使用 median 縮小圖片尺寸 (1/{factor}×1/{factor})，共 {len(image_paths)} 張：")

    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"⚠️ 讀取失敗：{path}")
            continue

        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        result = median_downsample(img, factor)
        filename = os.path.basename(path)
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, result)
        print(f"✅ 已儲存：{output_path}")

    print("🎉 全部處理完成！")

def apply_median_filter_batch(input_folder, output_folder, ksize=3):
    """
    對 input_folder 中所有圖片應用中值濾波，結果儲存至 output_folder
    :param input_folder: 原始圖片資料夾
    :param output_folder: 輸出資料夾
    :param ksize: 中值濾波器大小（需為奇數）
    """
    os.makedirs(output_folder, exist_ok=True)
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']

    # 搜尋所有圖片
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(input_folder, ext)))

    if not image_paths:
        print(f"❌ 找不到任何圖片於：{input_folder}")
        return

    print(f"🖼️ 共找到 {len(image_paths)} 張圖片，開始處理...")

    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"⚠️ 無法讀取圖片：{path}")
            continue

        filtered = cv2.medianBlur(img, ksize)
        filename = os.path.basename(path)
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, filtered)
        print(f"✅ 已處理並儲存：{output_path}")

    print("🎉 所有圖片處理完畢！")

def resize_images_to_quarter(input_folder, output_folder):
    """
    將 input_folder 中所有圖片縮小為原圖寬高的 1/2（即面積為 1/4），儲存到 output_folder
    :param input_folder: 原始圖片資料夾
    :param output_folder: 輸出縮圖資料夾
    """
    os.makedirs(output_folder, exist_ok=True)
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']

    image_paths = []
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(input_folder, ext)))

    if not image_paths:
        print(f"❌ 找不到圖片於：{input_folder}")
        return

    print(f"📦 共找到 {len(image_paths)} 張圖片，開始縮小為 1/16 尺寸...")

    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"⚠️ 無法讀取圖片：{path}")
            continue

        h, w = img.shape[:2]
        resized = cv2.resize(img, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
        filename = os.path.basename(path)
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, resized)
        print(f"✅ 已縮小並儲存：{output_path}")

    print("🎉 所有圖片縮小完成！")

# 🧪 使用範例：
# apply_median_filter_batch('SwinIR', 'output_median_SwinIR', ksize=3)
# apply_median_filter_batch('Restormer', 'output_median_Restormer', ksize=3)
# apply_median_filter_batch('images', 'output_median_images', ksize=3)
# batch_median_downsample('SwinIR', 'output_scale_SwinIR', factor=4)
# batch_median_downsample('SwinIR_Restormer', 'output_scale_SwinIR_Restormer', factor=4)
# batch_median_downsample('Restormer_SwinIR', 'output_scale_Restormer_SwinIR', factor=4)
resize_images_to_quarter('SwinIR', 'quarter_SwinIR')
resize_images_to_quarter('SwinIR_Restormer', 'quarter_SwinIR_Restormer')
resize_images_to_quarter('Restormer_SwinIR', 'quarter_Restormer_SwinIR')