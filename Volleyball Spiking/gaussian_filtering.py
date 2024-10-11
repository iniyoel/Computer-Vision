import cv2
import os

# Fungsi untuk membuat direktori
def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Folder input untuk masing-masing metode
input_folder_HE = 'output_HE_frames'
input_folder_CS = 'output_CS_frames'
input_folder_CLAHE = 'output_CLAHE_frames'

# Folder output untuk hasil Gaussian Filtering
output_folder_Gaussian_HE = 'output_Gaussian_HE_frames'
output_folder_Gaussian_CS = 'output_Gaussian_CS_frames'
output_folder_Gaussian_CLAHE = 'output_Gaussian_CLAHE_frames'

# Buat folder output untuk Gaussian Filtering
create_dir(output_folder_Gaussian_HE)
create_dir(output_folder_Gaussian_CS)
create_dir(output_folder_Gaussian_CLAHE)

# Loop untuk masing-masing folder input
for subfolder in os.listdir(input_folder_HE):
    subfolder_HE_path = os.path.join(input_folder_HE, subfolder)
    subfolder_CS_path = os.path.join(input_folder_CS, subfolder)
    subfolder_CLAHE_path = os.path.join(input_folder_CLAHE, subfolder)

    # Pastikan hanya memproses subfolder (bukan file)
    if os.path.isdir(subfolder_HE_path):
        # Buat subfolder untuk hasil Gaussian Filtering
        gaussian_HE_subfolder = os.path.join(output_folder_Gaussian_HE, subfolder)
        gaussian_CS_subfolder = os.path.join(output_folder_Gaussian_CS, subfolder)
        gaussian_CLAHE_subfolder = os.path.join(output_folder_Gaussian_CLAHE, subfolder)
        
        create_dir(gaussian_HE_subfolder)
        create_dir(gaussian_CS_subfolder)
        create_dir(gaussian_CLAHE_subfolder)
        
        # Loop untuk semua frame di dalam subfolder saat ini
        for frame_filename in os.listdir(subfolder_HE_path):
            if frame_filename.endswith('.png') or frame_filename.endswith('.jpg'):
                # Path untuk masing-masing frame
                frame_HE_path = os.path.join(subfolder_HE_path, frame_filename)
                frame_CS_path = os.path.join(subfolder_CS_path, frame_filename)
                frame_CLAHE_path = os.path.join(subfolder_CLAHE_path, frame_filename)

                # Baca gambar/frame
                he_frame = cv2.imread(frame_HE_path)
                cs_frame = cv2.imread(frame_CS_path)
                clahe_frame = cv2.imread(frame_CLAHE_path)

                # Lakukan Gaussian Filtering
                gaussian_HE_frame = cv2.GaussianBlur(he_frame, (5, 5), 0)  # Kernel size (5, 5)
                gaussian_CS_frame = cv2.GaussianBlur(cs_frame, (5, 5), 0)  # Kernel size (5, 5)
                gaussian_CLAHE_frame = cv2.GaussianBlur(clahe_frame, (5, 5), 0)  # Kernel size (5, 5)

                # Simpan gambar hasil Gaussian Filtering
                gaussian_HE_output_path = os.path.join(gaussian_HE_subfolder, frame_filename)
                gaussian_CS_output_path = os.path.join(gaussian_CS_subfolder, frame_filename)
                gaussian_CLAHE_output_path = os.path.join(gaussian_CLAHE_subfolder, frame_filename)

                cv2.imwrite(gaussian_HE_output_path, gaussian_HE_frame)
                cv2.imwrite(gaussian_CS_output_path, gaussian_CS_frame)
                cv2.imwrite(gaussian_CLAHE_output_path, gaussian_CLAHE_frame)

        print(f"Gaussian filtering completed for {subfolder}.")

print("Gaussian filtering has been applied to all frames in HE, CS, and CLAHE folders.")
