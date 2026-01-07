import requests
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os
from tabulate import tabulate

# =========================
# CONFIG
# =========================
BASE_URL = "https://api.openf1.org/v1"
EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================
# API CLIENT
# =========================
class OpenF1Client:
    def fetch(self, endpoint, params=None) -> pd.DataFrame:
        try:
            r = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=15)
            r.raise_for_status()
            return pd.DataFrame(r.json())
        except Exception as e:
            logging.error(f"API error on {endpoint}: {e}")
            return pd.DataFrame()

# =========================
# SERVICES
# =========================
class DriversService:
    def __init__(self, client):
        self.client = client

    def list_by_session(self, session_key):
        df = self.client.fetch("drivers", {"session_key": session_key})
        if df.empty:
            return df
        return (
            df[["driver_number", "full_name", "team_name"]]
            .drop_duplicates()
            .sort_values("driver_number")
        )

    def get_any_driver_number(self, session_key):
        df = self.client.fetch("drivers", {"session_key": session_key})
        if df.empty:
            return None
        return df.iloc[0]["driver_number"]

class SessionsService:
    def __init__(self, client):
        self.client = client

    def list_by_year(self, year):
        df = self.client.fetch("sessions", {"year": year})
        if df.empty:
            return df
        return df[["session_key", "country_name", "session_name", "date_start"]]

    def get_session(self, session_key):
        df = self.client.fetch("sessions", {"session_key": session_key})
        if df.empty:
            return None
        return df.iloc[0]

class LapsService:
    def __init__(self, client):
        self.client = client

    def laps_for_driver(self, session_key, driver_number):
        return self.client.fetch(
            "laps",
            {"session_key": session_key, "driver_number": driver_number}
        )

class TelemetryService:
    def __init__(self, client):
        self.client = client

    def location(self, session_key, driver_number):
        return self.client.fetch(
            "location",
            {"session_key": session_key, "driver_number": driver_number}
        )

class ResultsService:
    def __init__(self, client, drivers_service):
        self.client = client
        self.drivers_service = drivers_service

    def finishing_order(self, session_key):
        pos = self.client.fetch("position", {"session_key": session_key})
        drv = self.drivers_service.list_by_session(session_key)

        if pos.empty:
            return pos

        pos = pos[pos["position"].notna()]

        # Ordine temporale
        if "date" in pos.columns:
            pos = pos.sort_values("date")
        elif "lap_number" in pos.columns:
            pos = pos.sort_values("lap_number")

        # Ultima posizione per pilota
        pos = pos.groupby("driver_number", as_index=False).last()
        pos = pos.sort_values("position")

        # JOIN con drivers
        df = pos.merge(drv, on="driver_number", how="left")

        # Gap handling
        if "gap" in df.columns:
            gap_col = "gap"
        elif "interval" in df.columns:
            gap_col = "interval"
        else:
            gap_col = None

        def format_gap(row):
            if row["position"] == 1:
                return "Leader"
            if gap_col is None or pd.isna(row[gap_col]):
                return "N/A"
            return row[gap_col]

        df["gap_to_leader"] = df.apply(format_gap, axis=1)

        return df[
            [
                "position",
                "driver_number",
                "full_name",
                "team_name",
                "gap_to_leader",
            ]
        ]

# =========================
# UTILITIES
# =========================
def export_csv(df, filename):
    path = os.path.join(EXPORT_DIR, filename)
    df.to_csv(path, index=False)
    logging.info(f"File esportato: {path}")

def print_table(df):
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

def safe_input_int(prompt):
    while True:
        val = input(prompt).strip()
        if not val:
            print("Input vuoto! Riprova.")
            continue
        try:
            return int(val)
        except ValueError:
            print("Inserisci un numero valido!")

def safe_input_str(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Input vuoto! Riprova.")

# =========================
# UI / MENU
# =========================
class MenuApp:
    def __init__(self):
        self.client = OpenF1Client()
        self.drivers = DriversService(self.client)
        self.sessions = SessionsService(self.client)
        self.laps = LapsService(self.client)
        self.telemetry = TelemetryService(self.client)
        self.results = ResultsService(self.client, self.drivers)

    def run(self):
        while True:
            print("""
=====================================
 OPENF1 PROFESSIONAL ANALYSIS TOOL
=====================================
1. Elenco sessioni per anno
2. Elenco piloti di una sessione
3. Analisi giri pilota (SOLO GARA)
4. Mappa circuito
6. Ordine di arrivo + gap leader
0. Esci
""")
            choice = safe_input_str("Seleziona opzione: ")

            if choice == "1":
                self.show_sessions()
            elif choice == "2":
                self.show_drivers()
            elif choice == "3":
                self.analyze_laps()
            elif choice == "4":
                self.show_track()
            elif choice == "6":
                self.show_results()
            elif choice == "0":
                break
            else:
                print("Scelta non valida")

    # =========================
    # MENU FUNCTIONS
    # =========================
    def show_sessions(self):
        year = safe_input_int("Anno (es. 2025): ")
        df = self.sessions.list_by_year(year)
        if df.empty:
            print("Nessuna sessione trovata per l'anno selezionato")
        else:
            print_table(df)

    def show_drivers(self):
        session_key = safe_input_str("Session key: ")
        df = self.drivers.list_by_session(session_key)
        if df.empty:
            print("Nessun pilota trovato per questa sessione")
        else:
            print_table(df)

    def analyze_laps(self):
        sk = safe_input_str("Session key: ")
        session = self.sessions.get_session(sk)

        if session is None or "Race" not in session["session_name"]:
            print("❌ Solo sessioni di gara")
            return

        dn = safe_input_int("Numero pilota: ")
        df = self.laps.laps_for_driver(sk, dn)

        if df.empty or "lap_duration" not in df.columns:
            print("Nessun dato disponibile")
            return

        print("\nStatistiche tempi sul giro:")
        print(df["lap_duration"].describe())

        # GRAFICO
        plt.figure(figsize=(10, 5))
        plt.plot(df["lap_number"], df["lap_duration"], marker="o", linewidth=1)
        plt.xlabel("Lap")
        plt.ylabel("Lap Time (s)")
        plt.title(f"Lap Times – Driver {dn}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        if safe_input_str("Esportare CSV? (s/n): ").lower() == "s":
            export_csv(df, f"laps_{dn}_{sk}.csv")

    def show_track(self):
        sk = safe_input_str("Session key: ")
        dn = self.drivers.get_any_driver_number(sk)
        if dn is None:
            print("Nessun pilota trovato")
            return

        df = self.telemetry.location(sk, dn)
        df = df[(df["x"] != 0) | (df["y"] != 0)].dropna(subset=["x", "y"])

        plt.figure(figsize=(8, 6))
        plt.scatter(df["x"], df["y"], s=1)
        plt.axis("equal")
        plt.title("Track Map")
        plt.show()

    def show_results(self):
        sk = safe_input_str("Session key: ")
        df = self.results.finishing_order(sk)
        if df.empty:
            print("Nessun risultato disponibile")
        else:
            print_table(df)

# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    MenuApp().run()
