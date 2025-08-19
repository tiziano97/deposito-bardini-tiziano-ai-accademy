import pandas as pd
import numpy as np

def leggi_csv(percorso_csv):
    """
    Legge il file e restituisce un DataFrame.
    
    Parametri
    ----------
    percorso_csv : str
        Percorso del file CSV.
    
    Restituisce
    ----------
    pandas.DataFrame
        DataFrame con colonne 'timestamp' e 'consumo'.
    """
    df = pd.read_csv(percorso_csv)
    # Trova la colonna consumo dinamicamente (es: 'COMED_MW')
    consumo_col = [col for col in df.columns if col.endswith('_MW')]
    if not consumo_col:
        raise ValueError("Colonna consumo non trovata (deve terminare con '_MW').")
    consumo_col = consumo_col[0]
    # Trova la colonna timestamp (es: 'Datetime')
    timestamp_col = [col for col in df.columns if 'time' in col.lower()]
    if not timestamp_col:
        raise ValueError("Colonna timestamp non trovata (deve contenere 'time').")
    timestamp_col = timestamp_col[0]
    df = df.rename(columns={timestamp_col: 'timestamp', consumo_col: 'consumo'})
    return df

def classifica_consumo(df, livello='giornaliero'):
    """
    Classifica ogni ora come 'alto consumo' o 'basso consumo' rispetto alla media.
    
    Parametri
    ----------
    df : pandas.DataFrame
        DataFrame con almeno una colonna 'timestamp' (datetime) e 'consumo' (float).
    livello : str, opzionale
        Livello di confronto: 'giornaliero', 'settimanale', 'globale'.
    
    Restituisce
    ----------
    pandas.DataFrame
        DataFrame originale con una nuova colonna 'classificazione_<livello>'.
    """
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    if livello == 'giornaliero':
        # Calcola la media giornaliera
        df['media_giornaliera'] = df.groupby(df['timestamp'].dt.date)['consumo'].transform('mean')
        df['classificazione_giornaliera'] = np.where(df['consumo'] > df['media_giornaliera'], 'alto consumo', 'basso consumo')
        df.drop(columns=['media_giornaliera'], inplace=True)
    elif livello == 'settimanale':
        # Calcola la media settimanale
        df['settimana'] = df['timestamp'].dt.isocalendar().week
        df['anno'] = df['timestamp'].dt.year
        df['media_settimanale'] = df.groupby(['anno', 'settimana'])['consumo'].transform('mean')
        df['classificazione_settimanale'] = np.where(df['consumo'] > df['media_settimanale'], 'alto consumo', 'basso consumo')
        df.drop(columns=['media_settimanale', 'settimana', 'anno'], inplace=True)
    elif livello == 'globale':
        # Calcola la media globale
        media_globale = df['consumo'].mean()
        df['classificazione_globale'] = np.where(df['consumo'] > media_globale, 'alto consumo', 'basso consumo')
    else:
        raise ValueError("Livello non valido. Scegli tra 'giornaliero', 'settimanale', 'globale'.")
    return df


