import cv2
import numpy as np
import os
import pandas as pd

# Fungsi untuk menghitung MSE antara dua gambar
def calculate_mse(original, processed):
    mse = np.mean((original - processed) ** 2)
    return mse

# Fungsi untuk menghitung PSNR
def calculate_psnr(mse, max_pixel=255.0):
    if mse == 0:  # Jika tidak ada error, PSNR tidak terhingga
        return float('inf')
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    return psnr

# Fungsi untuk menghitung rata-rata PSNR untuk setiap folder (video)
def evaluate_psnr_per_video(original_folder, processed_folder, max_folders=10):
    psnr_per_video = []
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
                avg_psnr = calculate_psnr(avg_mse)  # Hitung PSNR berdasarkan MSE
                psnr_per_video.append(avg_psnr)
                video_names.append(subfolder)

    return video_names, psnr_per_video

# Folder path untuk gambar asli dan yang diproses
original_folder = 'output_grayscale_frames'
processed_folder_he = 'output_Gaussian_HE_frames'
processed_folder_cs = 'output_Gaussian_CS_frames'
processed_folder_clahe = 'output_Gaussian_CLAHE_frames'

# Evaluasi PSNR untuk setiap metode pengolahan gambar, batasi ke 10 folder pertama
video_cs, psnr_cs_volleyball = evaluate_psnr_per_video(original_folder, processed_folder_cs, max_folders=10)
video_he, psnr_he_volleyball = evaluate_psnr_per_video(original_folder, processed_folder_he, max_folders=10)
video_clahe, psnr_clahe_volleyball = evaluate_psnr_per_video(original_folder, processed_folder_clahe, max_folders=10)

# Pastikan nama video konsisten di setiap metode
if video_cs != video_he or video_cs != video_clahe:
    print("Video names do not match across methods!")
else:
    # Membuat tabel hasil PSNR
    data = {
        'Video Name': video_cs,
        'CS + Median Filter': psnr_cs_volleyball,
        'HE + Median Filter': psnr_he_volleyball,
        'CLAHE + Filter': psnr_clahe_volleyball
    }

    df = pd.DataFrame(data)

    # Tambahkan rata-rata di akhir tabel
    avg_psnr_cs = np.mean(psnr_cs_volleyball)
    avg_psnr_he = np.mean(psnr_he_volleyball)
    avg_psnr_clahe = np.mean(psnr_clahe_volleyball)

    # Menambahkan baris rata-rata
    df.loc['Average'] = ['Average', avg_psnr_cs, avg_psnr_he, avg_psnr_clahe]

    # Cetak hasil PSNR per video
    print(df)

    # Jika ingin menyimpan ke file CSV
    # df.to_csv('psnr_results_volleyball_per_video.csv', index=False)
