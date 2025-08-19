import pandas as pd

def load_airquality_dataset(filepath):
    """
    Carica il dataset AirQuality con separatore ';'.

    Parametri
    ---------
    filepath : str
        Percorso del file CSV.

    Restituisce
    -----------
    df : pandas.DataFrame
        DataFrame con i dati caricati.
    """
    return pd.read_csv(filepath, sep=';')

def combine_datetime(df):
    """
    Combina le colonne 'Date' e 'Time' in una singola colonna 'DateTime'.

    Parametri
    ---------
    df : pandas.DataFrame
        DataFrame con le colonne 'Date' e 'Time'.

    Restituisce
    -----------
    df : pandas.DataFrame
        DataFrame con la nuova colonna 'DateTime'.
    """
    df['DateTime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'],
        format='%d/%m/%Y %H.%M.%S',
        errors='coerce'
    )
    return df

def select_and_rename_columns(df):
    """
    Seleziona e rinomina le colonne rilevanti per l'analisi.

    Parametri
    ---------
    df : pandas.DataFrame
        DataFrame con la colonna 'DateTime' e le colonne originali.

    Restituisce
    -----------
    df_parsed : pandas.DataFrame
        DataFrame con colonne selezionate e rinominate.
    """
    df_parsed = df[['DateTime', 'PT08.S5(O3)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)']].rename(
        columns={
            'PT08.S5(O3)': 'O3',
            'PT08.S3(NOx)': 'NOx',
            'NO2(GT)': 'GT',
            'PT08.S4(NO2)': 'NO2'
        }
    )
    return df_parsed

def save_parsed_dataset(df_parsed, output_path):
    """
    Salva il DataFrame pulito in un file CSV.

    Parametri
    ---------
    df_parsed : pandas.DataFrame
        DataFrame da salvare.
    output_path : str
        Percorso del file di output.

    Restituisce
    -----------
    None
    """
    df_parsed.to_csv(output_path, index=False)

df = load_airquality_dataset('AirQuality.csv')
df = combine_datetime(df)
df_parsed = select_and_rename_columns(df)
save_parsed_dataset(df_parsed, 'airquality_parsed.csv')