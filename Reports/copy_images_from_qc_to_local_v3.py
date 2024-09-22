import os
import shutil
import cv2

def copy_and_process_images(src_folder, dest_folder, specific_dirs_images):
    # Verifica se a pasta de destino existe, senão cria
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # Navega pelo folder padrão
    for root, dirs, files in os.walk(src_folder):
        for dir_name in dirs:
            # Verifica se o nome do diretório começa com 'rcl'
            if dir_name.startswith('rcl'):
                try:
                    num_part = int(dir_name[3:])
                    if eval(f'{num_part} {condition}'):
                        specific_dir_path = os.path.join(root, dir_name)
                        for spf, spi_list in specific_dirs_images.items():
                            spf_path = os.path.join(specific_dir_path, spf)
                            if os.path.exists(spf_path):
                                dest_spf_dir = os.path.join(dest_folder, spf)
                                if not os.path.exists(dest_spf_dir):
                                    os.makedirs(dest_spf_dir)
                                for spi in spi_list:
                                    for file_name in os.listdir(spf_path):
                                        if spi in file_name and (file_name.endswith('.jpg') or file_name.endswith('.png')):
                                            src_file_path = os.path.join(spf_path, file_name)
                                            dest_file_path = os.path.join(dest_spf_dir, file_name)
                                            if not os.path.exists(dest_file_path):
                                                shutil.copy(src_file_path, dest_file_path)
                                                print(f'Copied {src_file_path} to {dest_file_path}')
                                            else:
                                                print(f'Skipped {src_file_path}, already exists in {dest_file_path}')
                                    # Cria um vídeo a partir das imagens copiadas
                                    video_folder = os.path.join(dest_spf_dir, 'video')
                                    if not os.path.exists(video_folder):
                                        os.makedirs(video_folder)
                                    create_video_from_images(dest_spf_dir, video_folder, spi)
                                    
                except ValueError:
                    # Caso o nome após 'rcl' não seja um número válido, ignora este diretório
                    continue

def create_video_from_images(image_folder, video_folder, spi, fps=24):
    video_path = os.path.join(video_folder, f'{spi}_video{fps}fps.mp4')
    images = [img for img in os.listdir(image_folder) if spi in img and (img.endswith('.jpg') or img.endswith('.png'))]
    images.sort()  # Ordena as imagens pelo nome para garantir a sequência correta

    if not images:
        print(f'No images found in the folder for {spi}.')
        return

    # Pega o tamanho da primeira imagem
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Define o codec e cria o objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' para .avi
    video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for image in images:
        frame = cv2.imread(os.path.join(image_folder, image))
        video.write(frame)

    video.release()
    print(f'Video saved to {video_path}')

    # Delete Images after video creation
    delete_images(image_folder, spi)

# Delete Images Function
def delete_images(image_folder, spi):
    images = [img for img in os.listdir(image_folder) if spi in img and (img.endswith('.jpg') or img.endswith('.png'))]
    for image in images:
        os.remove(os.path.join(image_folder, image))
        print(f'Deleted {image}')

# Uso do script
src_folder = r'Z:\03_QC\05-Nodes_QC_Reports\02-png'
dest_folder = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\IMAGE_CHECKS\VIDEO_ALL_IMAGES'
condition = '< 1888'  # Pode ser alterado para '< 1888' conforme necessário
specific_dirs_images_bkp = {
    'active_spectra_linear': ['rci1_active_spectra_linear'],
    'active_rms_full_p': ['_rci1_active_rms_full_p'],
    'active_rms_full_x': ['_rci1_active_rms_full_x'],
    'active_rms_full_y': ['_rci1_active_rms_full_y'],
    'active_rms_full_z': ['_rci1_active_rms_full_z'],
    'passive_spectra_linear': ['_rci1_passive_spectra_linear'],
    'drift': ['_rci1_drift_res'],
    # Adicione outros pares spf: [lista_de_imagens] conforme necessário
}


copy_and_process_images(src_folder, dest_folder, specific_dirs_images)



#DONT USE BELOW
def dontuse():
    specific_dirs_images = {
    'active_spectra_linear': ['rci1_active_spectra_linear'],
    'active_rms_full_p': ['_rci1_active_rms_full_p'],
    'active_rms_full_x': ['_rci1_active_rms_full_x'],
    'active_rms_full_y': ['_rci1_active_rms_full_y'],
    'active_rms_full_z': ['_rci1_active_rms_full_z'],
    'passive_spectra_linear': ['_rci1_passive_spectra_linear'],
    'drift': ['_rci1_drift_res'],
    # Adicione outros pares spf: [lista_de_imagens] conforme necessário
}