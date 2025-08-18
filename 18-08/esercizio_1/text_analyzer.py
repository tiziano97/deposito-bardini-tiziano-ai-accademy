# apri file di test

def open_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File non trovato"
    except Exception as e:
        return "Errore: " + str(e)

# funzione conteggio righe

def conta_righe(testo):
    righe = testo.split('\n')
    return len(righe)

#funzione conteggio parole

def conta_parole(testo):
    parole = testo.split()
    return len(parole)




def analizza_testo(file_path):
    testo = open_file(file_path)

    n_totale_righe = cona_righe(testo)
    n_totale_parole = conta_parole(testo)
    top_5_parole = trova_top_5_parole(testo)

    print("numero totale righe: " + str(n_totale_righe))
    print("numero totale parole: " + str(n_totale_parole))
    print("top 5 parole: " + str(top_5_parole))