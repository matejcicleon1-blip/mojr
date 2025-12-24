import collections

class AlfastreetPredictor:
    def __init__(self):
        # Fizički raspored brojeva na europskom kolu (u smjeru kazaljke na satu)
        self.wheel = [
            0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 
            5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
        ]
        self.history = []
        self.deltas = []
        self.mode_memory = 10  # Koliko zadnjih bacanja analizira za trend

    def get_index(self, number):
        """Vraća indeks broja na fizičkom kolu (0-36)."""
        return self.wheel.index(number)

    def calculate_delta(self, n1, n2):
        """Izračunava koliko je polja kuglica prešla (pomak)."""
        idx1 = self.get_index(n1)
        idx2 = self.get_index(n2)
        return (idx2 - idx1) % 37

    def update(self, new_number):
        """Unos novog broja i ažuriranje mehaničke memorije."""
        if self.history:
            delta = self.calculate_delta(self.history[-1], new_number)
            self.deltas.append(delta)
        self.history.append(new_number)
        
        if len(self.deltas) > self.mode_memory:
            self.deltas.pop(0)

    def get_top_16(self):
        """Glavni algoritam za izračun sljedećih 16 favorita."""
        if len(self.history) < 2:
            return "Nedovoljno podataka. Unesite barem 2 broja."

        # 1. Pronalaženje najčešćeg pomaka (Modalna Delta)
        # Gledamo koji se razmak najviše ponavlja (mehanički potpis)
        if not self.deltas:
            return []
            
        most_common_delta = collections.Counter(self.deltas).most_common(1)[0][0]
        
        # 2. Analiza trenda (da li se Delta povećava ili smanjuje - usporavanje rotora)
        trend = 0
        if len(self.deltas) >= 3:
            avg_recent = sum(self.deltas[-3:]) / 3
            trend = round(avg_recent - most_common_delta)

        # 3. Predviđanje baze (Zadnji indeks + najvjerojatniji pomak + trend)
        last_index = self.get_index(self.history[-1])
        predicted_center = (last_index + most_common_delta + trend) % 37

        # 4. Generiranje Top 16 (8 lijevo i 8 desno od predviđenog centra)
        # Ovime stvaramo "neprobojni" štit oko najvjerojatnije točke pada
        top_16_indices = []
        for i in range(-8, 8):
            top_16_indices.append((predicted_center + i) % 37)

        # Pretvaranje indeksa natrag u brojeve ruleta
        top_16_numbers = [self.wheel[idx] for idx in top_16_indices]
        
        return top_16_numbers

# --- PRIMJER KORIŠTENJA ---
predictor = AlfastreetPredictor()

def igraj(broj):
    predictor.update(broj)
    favoriti = predictor.get_top_16()
    print(f"Nakon broja {broj}, tvojih Top 16 za idući krug su:")
    print(favoriti)
    print("-" * 30)

# Simulacija unosa brojeva (zamijeni sa stvarnim brojevima s aparata)
igraj(32)
igraj(15)
igraj(21)
igraj(30)
