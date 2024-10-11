import cv2
import os
import numpy as np

# Membuat direktori
def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Folder input (grayscale frames)
input_folder = 'output_grayscale_frames'

# Folder output untuk masing-masing metode
output_folder_HE = 'output_HE_frames'
output_folder_CS = 'output_CS_frames'
output_folder_CLAHE = 'output_CLAHE_frames'

# Membuat folder output untuk HE, CS, dan CLAHE
create_dir(output_folder_HE)
create_dir(output_folder_CS)
create_dir(output_folder_CLAHE)

# Fungsi untuk melakukan contrast stretching
def contrast_stretching(image):
    # Mencari nilai minimum dan maksimum dari pixel
    min_val = np.min(image)
    max_val = np.max(image)
    
    # Melakukan normalisasi (stretching)
    stretched_image = (image - min_val) * (255 / (max_val - min_val))
    return stretched_image.astype(np.uint8)

# CLAHE setup
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

# Loop melalui semua subfolder di dalam output_grayscale_frames
for subfolder in os.listdir(input_folder):
    subfolder_path = os.path.join(input_folder, subfolder)
    
    # Memastikan hanya memproses subfolder
    if os.path.isdir(subfolder_path):
        he_subfolder = os.path.join(output_folder_HE, subfolder)
        cs_subfolder = os.path.join(output_folder_CS, subfolder)
        clahe_subfolder = os.path.join(output_folder_CLAHE, subfolder)
        
        create_dir(he_subfolder)
        create_dir(cs_subfolder)
        create_dir(clahe_subfolder)
        
        # Loop melalui semua frame di dalam subfolder saat ini
        for frame_filename in os.listdir(subfolder_path):
            if frame_filename.endswith('.png') or frame_filename.endswith('.jpg'):
                frame_path = os.path.join(subfolder_path, frame_filename)
                
                # Baca gambar/frame grayscale
                gray_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
                
                ### 1. Histogram Equalization (HE) ###
                he_frame = cv2.equalizeHist(gray_frame)
                he_output_path = os.path.join(he_subfolder, frame_filename)
                cv2.imwrite(he_output_path, he_frame)
                
                ### 2. Contrast Stretching (CS) ###
                cs_frame = contrast_stretching(gray_frame)
                cs_output_path = os.path.join(cs_subfolder, frame_filename)
                cv2.imwrite(cs_output_path, cs_frame)
                
                ### 3. CLAHE ###
                clahe_frame = clahe.apply(gray_frame)
                clahe_output_path = os.path.join(clahe_subfolder, frame_filename)
                cv2.imwrite(clahe_output_path, clahe_frame)
                
        print(f"Processing completed for {subfolder}.")

print("All frames have been processed with HE, CS, and CLAHE and saved to respective folders.")
