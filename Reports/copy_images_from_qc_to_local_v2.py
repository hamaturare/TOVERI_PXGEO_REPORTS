import os
import shutil
import cv2

def copy_and_process_images(src_folder, dest_folder, condition, specific_dirs_images):
    # Verifica se a pasta de destino existe, senão cria
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Navega pelo folder padrão
    for root, dirs, files in os.walk(src_folder):
        for dir_name in dirs:
            # Verifica se o nome do diretório começa com 'rcl' e se a parte numérica atende à condição
            if dir_name.startswith('rcl'):
                try:
                    num_part = int(dir_name[3:])
                    if eval(f'{num_part} {condition}'):
                        for specific_dir, image_names in specific_dirs_images.items():
                            specific_dir_path = os.path.join(root, dir_name, specific_dir)
                            if os.path.exists(specific_dir_path):
                                for image_name in image_names:
                                    # Cria o diretório de destino com a estrutura dir_name/specific_dir/image_name
                                    dest_specific_dir = os.path.join(dest_folder, dir_name, specific_dir, image_name)
                                    if not os.path.exists(dest_specific_dir):
                                        os.makedirs(dest_specific_dir)
                                    for file_name in os.listdir(specific_dir_path):
                                        if image_name in file_name:  # Verifica se o nome da imagem contém 'spi'
                                            image_path = os.path.join(specific_dir_path, file_name)
                                            dest_image_path = os.path.join(dest_specific_dir, file_name)
                                            if not os.path.exists(dest_image_path):
                                                shutil.copy(image_path, dest_image_path)
                                                print(f'Copied {image_path} to {dest_image_path}')
                                            else:
                                                print(f'Skipped {image_path}, already exists in {dest_image_path}')
                                    # Cria um vídeo a partir das imagens copiadas
                                    video_folder = os.path.join(dest_specific_dir, 'video')
                                    if not os.path.exists(video_folder):
                                        os.makedirs(video_folder)
                                    create_video_from_images(dest_specific_dir, video_folder, image_name)
                except ValueError:
                    # Caso o nome após 'rcl' não seja um número válido, ignora este diretório
                    continue
        
        # Evitar entrar em subdiretórios desnecessários
        dirs[:] = [d for d in dirs if d.startswith('rcl') and d[3:].isdigit() and eval(f'int(d[3:]) {condition}')]

def create_video_from_images(image_folder, video_folder, image_name, fps=24):
    video_path = os.path.join(video_folder, f'{image_name}_video{fps}fps.mp4')
    images = [img for img in os.listdir(image_folder) if image_name in img and (img.endswith(".jpg") or img.endswith(".png"))]
    images.sort()  # Ordena as imagens pelo nome para garantir a sequência correta

    if not images:
        print(f"No images found in the folder for {image_name}.")
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

# Uso do script
src_folder = r'Z:\03_QC\05-Nodes_QC_Reports\02-png'
dest_folder = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\IMAGE_CHECKS'
condition = '< 1888'  # Pode ser alterado para '< 1888' conforme necessário
specific_dirs_images_bkp= {
    'active_rms_full_p': ['_rci1_active_rms_full_p'],
    'active_rms_full_x': ['_rci1_active_rms_full_x'],
    'active_rms_full_y': ['_rci1_active_rms_full_y'],
    'active_rms_full_z': ['_rci1_active_rms_full_z'],
    'passive_spectra_linear': ['_rci1_passive_spectra_linear'],
    'drift': ['_rci1_drift_res'],
    'active_spectra_linear': ['rci1_active_spectra_linear'],

    

    # Adicione outros pares spf: [lista_de_imagens] conforme necessário
}

copy_and_process_images(src_folder, dest_folder, condition, specific_dirs_images)
