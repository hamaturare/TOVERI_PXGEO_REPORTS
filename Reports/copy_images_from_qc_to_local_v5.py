import os
import cv2

def process_images_and_create_videos(src_folder, dest_folder, condition, specific_dirs_images):
    # Verifica se a pasta de destino existe, senão cria
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    all_images = {}  # Dicionário para armazenar todas as imagens coletadas
    
    # Navega pelo folder padrão
    for root, dirs, files in os.walk(src_folder):
        for dir_name in dirs:
            # Verifica se o nome do diretório começa com 'rcl' e se a parte numérica atende à condição
            if dir_name.startswith('rcl'):
                try:
                    num_part = int(dir_name[3:])
                    if eval(f'{num_part} {condition}'):
                        specific_dir_path = os.path.join(root, dir_name)
                        for spf, spi_list in specific_dirs_images.items():
                            spf_path = os.path.join(specific_dir_path, spf)
                            if os.path.exists(spf_path):
                                if spf not in all_images:
                                    all_images[spf] = {}
                                for spi in spi_list:
                                    if spi not in all_images[spf]:
                                        all_images[spf][spi] = []
                                    for file_name in os.listdir(spf_path):
                                        if spi in file_name and (file_name.endswith('.jpg') or file_name.endswith('.png')):
                                            src_file_path = os.path.join(spf_path, file_name)
                                            all_images[spf][spi].append(src_file_path)
                except ValueError:
                    # Caso o nome após 'rcl' não seja um número válido, ignora este diretório
                    continue
        
        # Evitar entrar em subdiretórios desnecessários
        dirs[:] = [d for d in dirs if d.startswith('rcl') and d[3:].isdigit() and eval(f'{int(d[3:])} {condition}')]

    # Criar vídeos a partir das imagens coletadas
    for spf, spi_images in all_images.items():
        for spi, images in spi_images.items():
            if images:
                dest_spf_dir = os.path.join(dest_folder, spf)
                if not os.path.exists(dest_spf_dir):
                    os.makedirs(dest_spf_dir)
                video_folder = os.path.join(dest_spf_dir, 'video')
                if not os.path.exists(video_folder):
                    os.makedirs(video_folder)
                create_video_from_images(images, video_folder, spi)

def create_video_from_images(images, video_folder, spi, fps=24):
    video_path = os.path.join(video_folder, f'{spi}_video{fps}fps.mp4')
    images.sort()  # Ordena as imagens pelo nome para garantir a sequência correta

    if not images:
        print(f'No images found for {spi}.')
        return

    print(f'Creating video {video_path} from {len(images)} images...')

    # Pega o tamanho da primeira imagem
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    # Define o codec e cria o objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' para .avi
    video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for image in images:
        frame = cv2.imread(image)
        if frame is None:
            print(f'Failed to load image {image}')
            continue
        video.write(frame)
        print(f'Added {image} to video')

    video.release()
    print(f'Video saved to {video_path}')

# Uso do script
src_folder = r'Z:\03_QC\05-Nodes_QC_Reports\02-png'
dest_folder = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\IMAGE_CHECKS\VIDEO_ALL_IMAGES'
condition = '< 1914'  # Pode ser alterado para '< 1888' conforme necessário
specific_dirs_images = {
    'active_rms_full_p': ['_rci1_active_rms_full_p'],
    'active_rms_full_x': ['_rci1_active_rms_full_x'],
    'active_rms_full_y': ['_rci1_active_rms_full_y'],
    'active_rms_full_z': ['_rci1_active_rms_full_z'],
    'passive_spectra_linear': ['_rci1_passive_spectra_linear'],
    'active_spectra_linear': ['rci1_active_spectra_linear'],
    'active_rms_rejection':['_rci1_rms_offset_p', '_rci1_rms_offset_g1', '_rci1_rms_offset_g2', '_rci1_rms_offset_g3'],
    'inline_tx_nmo_p': ['_rci1_inline_tx_nmo_corr_p'],
    'inline_tx_p': ['_rci1_inline_tx_p'],
    'inline_tx_x': ['_rci1_inline_tx_x'],
    'inline_tx_y': ['_rci1_inline_tx_y'],
    'inline_tx_z': ['_rci1_inline_tx_z'],
    'passive_fx_p': ['_rci1_passive_fx_p'],
    'passive_fx_g1': ['_rci1_passive_fx_g1'],
    'passive_fx_g2': ['_rci1_passive_fx_g2'],
    'passive_fx_g3': ['_rci1_passive_fx_g3'],
    'passive_rms': ['_rci1_passive_rms'],
    'vector_fidelity_cart_p': ['_rci1_vector_fidelity_cart_p'],
    'vector_fidelity_cart_r': ['_rci1_vector_fidelity_cart_r'],
    'vector_fidelity_cart_t': ['_rci1_vector_fidelity_cart_t'],
    'vector_fidelity_cart_x': ['_rci1_vector_fidelity_cart_x'],
    'vector_fidelity_cart_y': ['_rci1_vector_fidelity_cart_y'],
    'vector_fidelity_cart_z': ['_rci1_vector_fidelity_cart_z'],
    'vector_fidelity_vert_t': ['_rci1_vector_fidelity_vert_t'],
    'vector_fidelity_vert_r': ['_rci1_vector_fidelity_vert_r'],
    'vector_fidelity_vert_rt': ['_rci1_vector_fidelity_vert_rt'],
    'drift': ['_rci1_drift_res'],
    # Adicione outros pares spf: [lista_de_imagens] conforme necessário
}

process_images_and_create_videos(src_folder, dest_folder, condition, specific_dirs_images)

