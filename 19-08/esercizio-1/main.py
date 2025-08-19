from classificatore.classificatore import leggi_csv, classifica_consumo

def main():
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
