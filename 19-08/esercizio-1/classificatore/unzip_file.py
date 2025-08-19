import zipfile
import os

def unzip_file(zip_path, extract_to):
    """
    Estrae tutti i file da uno zip nella cartella indicata.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"File estratti in: {extract_to}")
    extract_to = 'dataset'
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    unzip_file(zip_path, extract_to)
