# OpenF1 Professional Analysis Tool

Applicazione Python da riga di comando per l'analisi dei dati di Formula 1 tramite le [API OpenF1](https://openf1.org/). Questo strumento fornisce informazioni dettagliate su sessioni, piloti, tempi sul giro e risultati di gara.

## Funzionalità

- 📅 **Elenco Sessioni**: Visualizza tutte le sessioni F1 per anno
- 👥 **Lista Piloti**: Mostra tutti i piloti che partecipano a una sessione specifica
- 📊 **Analisi Giri**: Analizza i tempi sul giro con statistiche e visualizzazioni (solo sessioni di gara)
- 🗺️ **Mappa Circuito**: Visualizza il layout del circuito tramite dati di telemetria
- 🏁 **Risultati Gara**: Visualizza l'ordine di arrivo con i gap dal leader

## Requisiti

- Python 3.7+
- pip package manager

## Installazione

1. Clona la repository:
```bash
git clone https://github.com/alecappe-boss/openf1-analysis-tool.git
cd openf1-analysis-tool
```

2. Installa le dipendenze necessarie:
```bash
pip install requests pandas matplotlib tabulate
```

## Utilizzo

Avvia l'applicazione:
```bash
python main.py
```

### Opzioni del Menu Principale

1. **Elenco sessioni per anno**: Sfoglia tutte le sessioni F1 disponibili per un anno specifico
2. **Elenco piloti di una sessione**: Visualizza tutti i piloti che partecipano a una sessione
3. **Analisi giri pilota**: Ottieni un'analisi dettagliata dei tempi sul giro con grafici (solo gare)
4. **Mappa circuito**: Visualizza il layout del circuito
6. **Ordine di arrivo + gap leader**: Visualizza i risultati di gara con i distacchi dal leader
0. **Esci**: Chiudi l'applicazione

### Esempio di Utilizzo

1. Avvia l'applicazione
2. Seleziona l'opzione `1` per elencare le sessioni del 2025
3. Annota la `session_key` della sessione desiderata
4. Seleziona l'opzione `2` e inserisci la session key per visualizzare i piloti
5. Seleziona l'opzione `3` per analizzare i tempi sul giro di un pilota specifico
6. Visualizza le statistiche e il grafico dei tempi
7. Esporta i dati in CSV se desiderato

## Esportazione Dati

Tutti i file CSV esportati vengono salvati nella directory `exports/`, che viene creata automaticamente all'avvio dell'applicazione.

## Riferimento API

Questo strumento utilizza le [API OpenF1](https://openf1.org/), che forniscono accesso gratuito a dati di Formula 1 in tempo reale e storici.

## Struttura del Progetto

```
.
├── main.py           # File principale dell'applicazione
├── exports/          # Directory per i file CSV esportati
└── README.md         # Questo file
```

## Componenti Principali

- **OpenF1Client**: Gestisce tutte le richieste API
- **DriversService**: Gestisce le query relative ai piloti
- **SessionsService**: Gestisce le informazioni sulle sessioni
- **LapsService**: Recupera i dati dei tempi sul giro
- **TelemetryService**: Recupera i dati di telemetria e posizione
- **ResultsService**: Elabora i risultati di gara e le posizioni finali

## Contribuire

I contributi sono benvenuti! Sentiti libero di inviare una Pull Request.

## Licenza

Questo progetto è open source e disponibile sotto licenza MIT.

## Riconoscimenti

- Dati forniti dalle [API OpenF1](https://openf1.org/)
- Realizzato per gli appassionati di F1 e gli analisti di dati

## Risoluzione Problemi

**Nessun dato restituito**: Assicurati di utilizzare una session key valida di sessioni F1 recenti

**Timeout API**: Il timeout predefinito è di 15 secondi. Controlla la tua connessione internet se le richieste falliscono

**Grafico non visualizzato**: Assicurati che matplotlib sia installato correttamente e che il tuo sistema supporti i display GUI

## Sviluppi Futuri

- [ ] Integrazione dati meteo
- [ ] Analisi strategia gomme
- [ ] Analisi comparativa tra piloti
- [ ] Dashboard interattiva
- [ ] Analisi trend storici

---

Realizzato con ❤️ per gli appassionati di Formula 1
