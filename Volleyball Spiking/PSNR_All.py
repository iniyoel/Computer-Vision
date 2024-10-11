import cv2
import numpy as np
import os
import pandas as pd

# Fungsi untuk menghitung MSE antara dua gambar (untuk PSNR)
def calculate_mse(original, processed):
    mse = np.mean((original - processed) ** 2)
    return mse

# Fungsi untuk menghitung PSNR berdasarkan MSE
def calculate_psnr(mse, max_pixel=255.0):
    if mse == 0:  # Jika tidak ada error, PSNR tidak terhingga
        return float('inf')
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    return psnr

# Fungsi untuk menghitung PSNR untuk semua video dan semua frame
def evaluate_psnr_all_videos(original_folder, processed_folder):
    psnr_values = []
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

                    # Hitung MSE dan PSNR untuk frame ini
                    mse = calculate_mse(original_frame, processed_frame)
                    psnr = calculate_psnr(mse)

                    psnr_values.append(psnr)
                    frame_names.append(f"{subfolder}/{frame_filename}")

    return frame_names, psnr_values

# Folder path untuk gambar asli dan yang diproses
original_folder = 'output_grayscale_frames'
processed_folder_he = 'output_Gaussian_HE_frames'
processed_folder_cs = 'output_Gaussian_CS_frames'
processed_folder_clahe = 'output_Gaussian_CLAHE_frames'

# Evaluasi PSNR untuk semua folder video dan semua frame
frames_cs, psnr_cs = evaluate_psnr_all_videos(original_folder, processed_folder_cs)
frames_he, psnr_he = evaluate_psnr_all_videos(original_folder, processed_folder_he)
frames_clahe, psnr_clahe = evaluate_psnr_all_videos(original_folder, processed_folder_clahe)

# Membuat tabel hasil PSNR
if frames_cs == frames_he == frames_clahe:  # Pastikan nama frame konsisten
    data = {
        'Image(jpg)': frames_cs,
        'PSNR CS + Median Filter': psnr_cs,
        'PSNR HE + Median Filter': psnr_he,
        'PSNR CLAHE + Filter': psnr_clahe
    }

    df = pd.DataFrame(data)

    # Tambahkan rata-rata di akhir tabel
    avg_psnr_cs = np.mean(psnr_cs)
    avg_psnr_he = np.mean(psnr_he)
    avg_psnr_clahe = np.mean(psnr_clahe)

    # Menambahkan baris rata-rata
    df.loc['Average'] = ['Average', avg_psnr_cs, avg_psnr_he, avg_psnr_clahe]

    # Cetak hasil PSNR
    print(df)

    # Jika ingin menyimpan ke file CSV
    # df.to_csv('psnr_results_all_videos.csv', index=False)
