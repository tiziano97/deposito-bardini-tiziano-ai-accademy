from classificatore.classificatore import leggi_csv, classifica_consumo
from classificatore.unzip_file import unzip_file
import os

def main():
    """
    Esegue il processo di estrazione, lettura e classificazione dei dati di consumo.

    Step
    ----
    1. Estrae i file dallo zip 'archive.zip' nella cartella 'dataset'.
    2. Legge il file CSV 'dataset/COMED_hourly.csv' e lo carica in un DataFrame.
    3. Classifica ogni ora come 'alto consumo' o 'basso consumo' rispetto alla media giornaliera, settimanale e globale.
    4. Salva il DataFrame classificato in 'classificato.csv'.

    Returns
    -------
    None
    """
    zip_path = 'archive.zip'
    extract_to = 'dataset'
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    unzip_file(zip_path, extract_to)
    percorso_csv = 'dataset/COMED_hourly.csv'
    df = leggi_csv(percorso_csv)
    # Classifica per tutti i livelli
    df = classifica_consumo(df, livello='giornaliero')
    df = classifica_consumo(df, livello='settimanale')
    df = classifica_consumo(df, livello='globale')
    # Salva il risultato
    output_path = "classificato.csv"
    df.to_csv(output_path, index=False)
    print(f"File classificato salvato in: {output_path}")

if __name__ == "__main__":
    main()
