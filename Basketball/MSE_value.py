import cv2
import numpy as np
import os
import pandas as pd

# Menghitung MSE antara dua gambar
def calculate_mse(original, processed):
    mse = np.mean((original - processed) ** 2)
    return mse

# Menghitung rata-rata MSE untuk setiap folder (video)
def evaluate_mse_per_video(original_folder, processed_folder, max_folders=10):
    mse_per_video = []
    video_names = []

    # Mengambil maksimal 10 folder pertama (video)
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
                    
                    # Memeriksa file original dan processed ada
                    if not os.path.exists(original_frame_path) or not os.path.exists(processed_frame_path):
                        print(f"File missing: {frame_filename} in {subfolder}")
                        continue

                    # Baca gambar asli dan yang diproses
                    original_frame = cv2.imread(original_frame_path, cv2.IMREAD_GRAYSCALE)
                    processed_frame = cv2.imread(processed_frame_path, cv2.IMREAD_GRAYSCALE)

                    if original_frame is None or processed_frame is None:
                        print(f"Error reading frame: {frame_filename} in {subfolder}")
                        continue

                    # Hitung MSE untuk frame ini
                    mse = calculate_mse(original_frame, processed_frame)
                    mse_values.append(mse)

            # Menghitung rata-rata MSE untuk video ini (folder)
            if mse_values:
                avg_mse = np.mean(mse_values)
                mse_per_video.append(avg_mse)
                video_names.append(subfolder)

    return video_names, mse_per_video

# Folder path untuk gambar asli dan yang diproses
original_folder = 'output_grayscale_frames'
processed_folder_he = 'output_Gaussian_HE_frames'
processed_folder_cs = 'output_Gaussian_CS_frames'
processed_folder_clahe = 'output_Gaussian_CLAHE_frames'

# Evaluasi MSE untuk setiap metode pengolahan gambar dengan membatasi ke 10 folder pertama
video_cs, mse_cs_basketball = evaluate_mse_per_video(original_folder, processed_folder_cs, max_folders=10)
video_he, mse_he_basketball = evaluate_mse_per_video(original_folder, processed_folder_he, max_folders=10)
video_clahe, mse_clahe_basketball = evaluate_mse_per_video(original_folder, processed_folder_clahe, max_folders=10)

if video_cs != video_he or video_cs != video_clahe:
    print("Video names do not match across methods!")
else:
    # Membuat tabel hasil MSE
    data = {
        'Video Name': video_cs,
        'CS + Gaussian Filter': mse_cs_basketball,
        'HE + Gaussian Filter': mse_he_basketball,
        'CLAHE + Filter': mse_clahe_basketball
    }

    df = pd.DataFrame(data)

    # Menambahkan rata-rata di akhir tabel
    avg_mse_cs = np.mean(mse_cs_basketball)
    avg_mse_he = np.mean(mse_he_basketball)
    avg_mse_clahe = np.mean(mse_clahe_basketball)

    # Menambahkan baris rata-rata
    df.loc['Average'] = ['Average', avg_mse_cs, avg_mse_he, avg_mse_clahe]
    print(df)