import cv2
import os

# Fungsi untuk membuat direktori
def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Path ke folder yang berisi video-video
folder_path = 'VolleyballSpiking'  # Ganti dengan path folder video Anda
output_base_folder = 'output_frames'  # Folder untuk menyimpan semua frame

# Buat folder utama untuk menyimpan frame jika belum ada
create_dir(output_base_folder)

# Loop melalui semua file di dalam folder video
for filename in os.listdir(folder_path):
    if filename.endswith('.mp4') or filename.endswith('.avi'):  # Filter video dengan format mp4 atau avi
        video_path = os.path.join(folder_path, filename)
        
        # Baca video
        cap = cv2.VideoCapture(video_path)

        # Buat subfolder untuk setiap video berdasarkan nama file video
        video_name = os.path.splitext(filename)[0]
        output_folder = os.path.join(output_base_folder, video_name)
        create_dir(output_folder)

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()  # Baca frame dari video
            if not ret:
                break
            
            # Simpan frame sebagai gambar
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
            cv2.imwrite(frame_filename, frame)
            frame_count += 1

        cap.release()
        print(f"Frame extraction completed for {filename}! {frame_count} frames extracted.")

print("All videos processed!")
