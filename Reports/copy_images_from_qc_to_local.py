import shutil
import path
import os
import cv2

image_folders_root = r'Z:\03_QC\05-Nodes_QC_Reports\02-png'
root_name_of_files = '_rec_deltatimepick_aslaid-repo'

def copy_images(src_folder, dest_folder, specific_name):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    for root, dirs, files in os.walk(src_folder):
        for dir_name in dirs:
            if dir_name.startswith('rcl'):
                try:
                    num_part = int(dir_name[3:])
                    if num_part < 1914:
                        specific_dir_path = os.path.join(root, dir_name, 'rec_pos_qc' )
                        if os.path.exists(specific_dir_path):
                            for file_name in os.listdir(specific_dir_path):
                                if specific_name in file_name and (file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.PNG')):
                                    src_file_path = os.path.join(specific_dir_path, file_name)
                                    dest_file_path = os.path.join(dest_folder, file_name)

                                    if not os.path.exists(dest_file_path):

                                        shutil.copy(src_file_path, dest_file_path)
                                        print(f'Copied {src_file_path} to {dest_file_path}')
                except ValueError :
                    continue
        dirs[:] = [d for d in dirs if d.startswith('rcl') and d[3:].isdigit() and int(d[3:]) < 1984]

def create_video_from_images(image_folder, video_path, fps=30):
    images = [img for img in os.listdir(image_folder) if img.endswith('png') or img.endswith('jpg') or img.endswith('PNG')]
    images.sort()

    if not images:
        print("No images found in the folder")
        return
    
    # Pega o tamanho da primeira imagem
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    
    # Define o codec e cria o objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for image in images:
        frame = cv2.imread(os.path.join(image_folder, image))
        video.write(frame)

    video.release()
    print(f'Video saved to {video_path}')

#variaveis do script
src_folder = r'Z:\03_QC\05-Nodes_QC_Reports\02-png'
specific_name = r'_rec_deltatimepick_aslaid-repo'
dest_folder = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\IMAGE_CHECKS\rec_pos_qc_all_nodes'
video_path = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\IMAGE_CHECKS\rec_pos_qc_all_nodes\video\All_rls_rec_deltatimepick_aslaid-repo_video30fps.mp4'


copy_images(src_folder, dest_folder, specific_name)
create_video_from_images(dest_folder, video_path)