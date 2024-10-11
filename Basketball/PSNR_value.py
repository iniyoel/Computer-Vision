import cv2
import numpy as np
import os
import pandas as pd

# Menghitung MSE antara dua gambar
def calculate_mse(original, processed):
    mse = np.mean((original - processed) ** 2)
    return mse

# Menghitung PSNR
def calculate_psnr(mse, max_pixel=255.0):
    if mse == 0:
        return float('inf')
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    return psnr

# Menghitung rata-rata PSNR untuk setiap folder (video)
def evaluate_psnr_per_video(original_folder, processed_folder, max_folders=10):
    psnr_per_video = []
    video_names = []

    # Ambil maksimal 10 folder pertama (video)
    subfolders = os.listdir(original_folder)[:max_folders]

    # Loop melalui setiap folder (video)
    for subfolder in subfolders:
        subfolder_path = os.path.join(original_folder, subfolder)

        if os.path.isdir(subfolder_path):
            mse_values = []
            
            # Loop melalui setiap frame dalam folder video
            for frame_filename in os.listdir(subfolder_path):
                if frame_filename.endswith('.png') or frame_filename.endswith('.jpg'):
                    original_frame_path = os.path.join(subfolder_path, frame_filename)
                    processed_frame_path = os.path.join(processed_folder, subfolder, frame_filename)
                    
                    # Periksa file original dan processed ada
                    if not os.path.exists(original_frame_path) or not os.path.exists(processed_frame_path):
                        print(f"File missing: {frame_filename} in {subfolder}")
                        continue

                    original_frame = cv2.imread(original_frame_path, cv2.IMREAD_GRAYSCALE)
                    processed_frame = cv2.imread(processed_frame_path, cv2.IMREAD_GRAYSCALE)

                    if original_frame is None or processed_frame is None:
                        print(f"Error reading frame: {frame_filename} in {subfolder}")
                        continue

                    # Hitung MSE untuk frame ini
                    mse = calculate_mse(original_frame, processed_frame)
                    mse_values.append(mse)

            # Hitung rata-rata MSE untuk video Basketball
            if mse_values:
                avg_mse = np.mean(mse_values)
                avg_psnr = calculate_psnr(avg_mse)
                psnr_per_video.append(avg_psnr)
                video_names.append(subfolder)

    return video_names, psnr_per_video

original_folder = 'output_grayscale_frames'
processed_folder_he = 'output_Gaussian_HE_frames'
processed_folder_cs = 'output_Gaussian_CS_frames'
processed_folder_clahe = 'output_Gaussian_CLAHE_frames'

# Evaluasi PSNR untuk setiap metode pengolahan gambar dengan membatasi ke 10 folder pertama
video_cs, psnr_cs_basketball = evaluate_psnr_per_video(original_folder, processed_folder_cs, max_folders=10)
video_he, psnr_he_basketball = evaluate_psnr_per_video(original_folder, processed_folder_he, max_folders=10)
video_clahe, psnr_clahe_basketball = evaluate_psnr_per_video(original_folder, processed_folder_clahe, max_folders=10)

if video_cs != video_he or video_cs != video_clahe:
    print("Video names do not match across methods!")
else:
    # Membuat tabel hasil PSNR
    data = {
        'Video Name': video_cs,
        'CS + Gaussian Filter': psnr_cs_basketball,
        'HE + Gaussian Filter': psnr_he_basketball,
        'CLAHE + Filter': psnr_clahe_basketball
    }

    df = pd.DataFrame(data)

    # Menambahkan rata-rata di akhir tabel
    avg_psnr_cs = np.mean(psnr_cs_basketball)
    avg_psnr_he = np.mean(psnr_he_basketball)
    avg_psnr_clahe = np.mean(psnr_clahe_basketball)

    # Menambahkan baris rata-rata
    df.loc['Average'] = ['Average', avg_psnr_cs, avg_psnr_he, avg_psnr_clahe]
    print(df)