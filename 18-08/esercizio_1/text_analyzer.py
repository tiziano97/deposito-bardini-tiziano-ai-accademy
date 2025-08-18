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

# funzione conteggio parole

def conta_parole(testo):
    parole = testo.split()
    return len(parole)

def rimuovi_punteggiatura(testo):
    testo = testo.replace(".", "").replace(",", "").replace("!", "").replace("?", "")
    return testo

def rimuovi_upper_testo(testo):
    return testo.lower()

def trova_top_5_parole(testo):
    testo = rimuovi_punteggiatura(testo)
    testo = rimuovi_upper_testo(testo)
    parole = testo.split()
    conteggio = {}
    for parola in parole:
        conteggio[parola] = conteggio.get(parola, 0) + 1
    top_5 = sorted(conteggio.items(), key=lambda x: x[1], reverse=True)[:5]
    return [f"{parola}: {conteggio}" for parola, conteggio in top_5]


def analizza_testo(file_path):
    testo = open_file(file_path)

    n_totale_righe = conta_righe(testo)
    n_totale_parole = conta_parole(testo)
    top_5_parole = trova_top_5_parole(testo)

    print("numero totale righe: " + str(n_totale_righe))
    print("numero totale parole: " + str(n_totale_parole))
    print("top 5 parole: " + str(top_5_parole))

file_path = "18-08/esercizio_1/input.txt"
analizza_testo(file_path)