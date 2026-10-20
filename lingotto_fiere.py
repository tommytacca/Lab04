import csv


class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.disponibile = True
        self.espositore = None

    def prezzo_finale(self):
        return self.prezzo_base

    def __lt__(self, other):
        return self.prezzo_finale() < other.prezzo_finale()

    def __str__(self):
        if self.disponibile:
            stato = "Disponibile"
        else:
            stato = "Non disponibile"

        return (f"{self.codice}: Standard | {self.superficie:g} mq - "
                f"Padiglione {self.padiglione} - "
                f"Prezzo {self.prezzo_finale():.2f}€ - {stato}")


class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.numero_prese = int(numero_prese)

    def prezzo_finale(self):
        return self.prezzo_base * (1 + 0.07 * self.numero_prese)

    def __str__(self):
        if self.disponibile:
            stato = "Disponibile"
        else:
            stato = "Non disponibile"

        return (f"{self.codice}: Prese Extra | {self.superficie:g} mq - "
                f"Padiglione {self.padiglione} - "
                f"Prezzo {self.prezzo_finale():.2f}€ - "
                f"Prese aggiuntive: {self.numero_prese} - {stato}")


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def prezzo_finale(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        if self.disponibile:
            stato = "Disponibile"
        else:
            stato = "Non disponibile"

        return (f"{self.codice}: Premium | {self.superficie:g} mq - "
                f"Padiglione {self.padiglione} - "
                f"Prezzo {self.prezzo_finale():.2f}€ - "
                f"Posizione: {self.posizione} - {stato}")


class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __eq__(self, other):
        if not isinstance(other, Espositore):
            return False
        return self.codice == other.codice

    def __str__(self):
        if self.stand is None:
            return f"{self.codice}: {self.nome} {self.cognome} - Nessuno stand assegnato"
        return f"{self.codice}: {self.nome} {self.cognome} - Stand assegnato: {self.stand.codice}"


class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.stand = {}
        self.espositori = {}

    def get_nome(self):
        return self.nome

    def set_nome(self, nuovo_nome):
        self.nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            lettore = csv.reader(file)

            for riga in lettore:
                if len(riga) == 0:
                    continue

                codice = riga[0].strip()

                if codice.startswith("ST"):
                    superficie = riga[1]
                    padiglione = riga[2]
                    prezzo_base = riga[3]

                    if len(riga) == 4:
                        stand = Stand(codice, superficie, padiglione, prezzo_base)
                    elif riga[4].strip().isdigit():
                        stand = StandPreseExtra(
                            codice, superficie, padiglione, prezzo_base, riga[4]
                        )
                    else:
                        stand = StandPremium(
                            codice, superficie, padiglione, prezzo_base, riga[4].strip()
                        )

                    self.stand[codice] = stand
                elif codice.startswith("ES"):
                    espositore = Espositore(codice, riga[1].strip(), riga[2].strip())
                    self.espositori[codice] = espositore

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        if codice_stand not in self.stand:
            raise Exception("Lo stand non esiste.")

        if codice_espositore not in self.espositori:
            raise Exception("L'espositore non esiste.")

        stand = self.stand[codice_stand]
        espositore = self.espositori[codice_espositore]

        if not stand.disponibile:
            raise Exception("Lo stand non è disponibile.")

        if espositore.stand is not None:
            raise Exception("L'espositore ha già uno stand assegnato.")

        stand.disponibile = False
        stand.espositore = espositore
        espositore.stand = stand

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for espositore in self.espositori.values():
            print(espositore)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand.values())
