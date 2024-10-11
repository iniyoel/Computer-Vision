import cv2
import numpy as np
import os
import pandas as pd

# Fungsi untuk menghitung MSE antara dua gambar
def calculate_mse(original, processed):
    mse = np.mean((original - processed) ** 2)
    return mse

# Fungsi untuk menghitung rata-rata MSE untuk setiap folder (video)
def evaluate_mse_per_video(original_folder, processed_folder, max_folders=10):
    mse_per_video = []
    video_names = []

    # Ambil maksimal 10 folder pertama (video)
    subfolders = os.listdir(original_folder)[:max_folders]

    # Loop melalui setiap folder (video)
    for subfolder in subfolders:
        subfolder_path = os.path.join(original_folder, subfolder)

        if os.path.isdir(subfolder_path):  # Pastikan itu adalah folder
            mse_values = []
            
            # Loop melalui setiap frame dalam folder video
            for frame_filename in os.listdir(subfolder_path):
                if frame_filename.endswith('.png') or frame_filename.endswith('.jpg'):
                    original_frame_path = os.path.join(subfolder_path, frame_filename)
                    processed_frame_path = os.path.join(processed_folder, subfolder, frame_filename)
                    
                    # Periksa apakah file original dan processed ada
                    if not os.path.exists(original_frame_path) or not os.path.exists(processed_frame_path):
                        print(f"File missing: {frame_filename} in {subfolder}")
                        continue

                    # Baca gambar asli dan yang diproses
                    original_frame = cv2.imread(original_frame_path, cv2.IMREAD_GRAYSCALE)
                    processed_frame = cv2.imread(processed_frame_path, cv2.IMREAD_GRAYSCALE)

                    # Cek apakah pembacaan berhasil
                    if original_frame is None or processed_frame is None:
                        print(f"Error reading frame: {frame_filename} in {subfolder}")
                        continue

                    # Hitung MSE untuk frame ini
                    mse = calculate_mse(original_frame, processed_frame)
                    mse_values.append(mse)

            # Hitung rata-rata MSE untuk video ini (folder)
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

# Evaluasi MSE untuk setiap metode pengolahan gambar, batasi ke 10 folder pertama
video_cs, mse_cs_volleyball = evaluate_mse_per_video(original_folder, processed_folder_cs, max_folders=10)
video_he, mse_he_volleyball = evaluate_mse_per_video(original_folder, processed_folder_he, max_folders=10)
video_clahe, mse_clahe_volleyball = evaluate_mse_per_video(original_folder, processed_folder_clahe, max_folders=10)

# Pastikan nama video konsisten di setiap metode
if video_cs != video_he or video_cs != video_clahe:
    print("Video names do not match across methods!")
else:
    # Membuat tabel hasil MSE
    data = {
        'Video Name': video_cs,
        'CS + Median Filter': mse_cs_volleyball,
        'HE + Median Filter': mse_he_volleyball,
        'CLAHE + Filter': mse_clahe_volleyball
    }

    df = pd.DataFrame(data)

    # Tambahkan rata-rata di akhir tabel
    avg_mse_cs = np.mean(mse_cs_volleyball)
    avg_mse_he = np.mean(mse_he_volleyball)
    avg_mse_clahe = np.mean(mse_clahe_volleyball)

    # Menambahkan baris rata-rata
    df.loc['Average'] = ['Average', avg_mse_cs, avg_mse_he, avg_mse_clahe]

    # Cetak hasil MSE per video
    print(df)

    # Jika ingin menyimpan ke file CSV
    # df.to_csv('mse_results_volleyball_per_video.csv', index=False)
