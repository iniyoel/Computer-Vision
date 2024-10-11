import cv2
import numpy as np
import os
import pandas as pd

# Fungsi untuk menghitung MSE antara dua gambar
def calculate_mse(original, processed):
    mse = np.mean((original - processed) ** 2)
    return mse

# Fungsi untuk menghitung MSE untuk semua video dan semua frame
def evaluate_mse_all_videos(original_folder, processed_folder):
    mse_values = []
    frame_names = []

    # Loop melalui semua subfolder (video) di folder original
    for subfolder in os.listdir(original_folder):
        subfolder_path = os.path.join(original_folder, subfolder)

        if os.path.isdir(subfolder_path):  # Pastikan itu adalah folder
            # Loop melalui setiap frame dalam subfolder
            for frame_filename in os.listdir(subfolder_path):
                if frame_filename.endswith('.png') or frame_filename.endswith('.jpg'):
                    original_frame_path = os.path.join(subfolder_path, frame_filename)
                    processed_frame_path = os.path.join(processed_folder, subfolder, frame_filename)

                    # Periksa apakah kedua file (original dan processed) ada
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
                    frame_names.append(f"{subfolder}/{frame_filename}")

    return frame_names, mse_values

# Folder path untuk gambar asli dan yang diproses
original_folder = 'output_grayscale_frames'
processed_folder_he = 'output_Gaussian_HE_frames'
processed_folder_cs = 'output_Gaussian_CS_frames'
processed_folder_clahe = 'output_Gaussian_CLAHE_frames'

# Evaluasi MSE untuk semua folder video dan semua frame
frames_cs, mse_cs = evaluate_mse_all_videos(original_folder, processed_folder_cs)
frames_he, mse_he = evaluate_mse_all_videos(original_folder, processed_folder_he)
frames_clahe, mse_clahe = evaluate_mse_all_videos(original_folder, processed_folder_clahe)

# Membuat tabel hasil MSE
if frames_cs == frames_he == frames_clahe:  # Pastikan nama frame konsisten
    data = {
        'Image(jpg)': frames_cs,
        'MSE CS + Median Filter': mse_cs,
        'MSE HE + Median Filter': mse_he,
        'MSE CLAHE + Filter': mse_clahe
    }

    df = pd.DataFrame(data)

    # Tambahkan rata-rata di akhir tabel
    avg_mse_cs = np.mean(mse_cs)
    avg_mse_he = np.mean(mse_he)
    avg_mse_clahe = np.mean(mse_clahe)

    # Menambahkan baris rata-rata
    df.loc['Average'] = ['Average', avg_mse_cs, avg_mse_he, avg_mse_clahe]

    # Cetak hasil MSE
    print(df)

    # Jika ingin menyimpan ke file CSV
    # df.to_csv('mse_results_all_videos.csv', index=False)
