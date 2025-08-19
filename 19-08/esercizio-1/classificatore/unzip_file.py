import zipfile
import os

def unzip_file(zip_path, extract_to):
    """
    Estrae tutti i file da uno zip nella cartella indicata.

    Parametri
    ----------
    zip_path : str
        Percorso del file zip da estrarre.
    extract_to : str
        Cartella di destinazione dove estrarre i file.

    Returns
    -------
    None
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"File estratti in: {extract_to}")
