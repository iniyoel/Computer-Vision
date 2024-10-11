import cv2
import os

# Fungsi untuk membuat direktori
def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Folder input (folder frame asli) dan folder output (untuk hasil grayscale)
input_folder = 'output_frames'
output_folder = 'output_grayscale_frames'

# Buat folder utama untuk menyimpan frame grayscale jika belum ada
create_dir(output_folder)

# Loop melalui semua subfolder di dalam output_frames
for subfolder in os.listdir(input_folder):
    subfolder_path = os.path.join(input_folder, subfolder)
    
    # Memastikan hanya memproses subfolder
    if os.path.isdir(subfolder_path):
        # Membuat subfolder baru di dalam output_grayscale_frames
        grayscale_subfolder = os.path.join(output_folder, subfolder)
        create_dir(grayscale_subfolder)
        
        # Loop melalui semua frame di dalam subfolder
        for frame_filename in os.listdir(subfolder_path):
            if frame_filename.endswith('.png') or frame_filename.endswith('.jpg'):
                frame_path = os.path.join(subfolder_path, frame_filename)
                
                # Baca gambar/frame
                frame = cv2.imread(frame_path)
                
                # Konversi ke grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Simpan gambar grayscale di subfolder yang sesuai
                output_frame_path = os.path.join(grayscale_subfolder, frame_filename)
                cv2.imwrite(output_frame_path, gray_frame)
                
        print(f"Grayscale conversion completed for {subfolder}.")

print("All frames have been converted to grayscale and saved in the output folder.")
