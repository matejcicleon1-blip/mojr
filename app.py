import numpy as np
from scipy.fft import fft

class UltraAlfastreetEngine:
    def __init__(self):
        self.wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 
                      5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        self.history = []
        self.index_history = []
        self.weights = np.zeros(37)

    def spectral_rhythm(self):
        """Analizira frekvenciju ponavljanja sektora."""
        if len(self.index_history) < 8: return 0
        
        # Pretvaranje povijesti indeksa u frekvencijski domenu
        sig = np.array(self.index_history[-16:])
        fourier = np.abs(fft(sig))
        # Dominantna frekvencija nam govori koliki je 'skok' najvjerojatniji
        dom_freq_offset = int(np.argmax(fourier) % 37)
        return dom_freq_offset

    def apply_density_bias(self):
        """Pojačava težinu brojevima koji se fizički grupiraju (Bias)."""
        if len(self.index_history) < 5: return
        
        counts = np.bincount(self.index_history[-20:], minlength=37)
        for i in range(37):
            # Ako je broj izašao više od prosjeka, dobiva 'Bias' bonus
            if counts[i] > 1:
                self.weights[i] *= 1.2 

    def update_weights(self, last_num):
        idx = self.wheel.index(last_num)
        self.history.append(last_num)
        self.index_history.append(idx)
        
        # Reset i decay težina
        self.weights = np.full(37, 0.1)
        
        # 1. Balistički pomak (Delta)
        if len(self.index_history) >= 2:
            delta = (self.index_history[-1] - self.index_history[-2]) % 37
            pred_idx = (idx + delta) % 37
            for i in range(-5, 6):
                self.weights[(pred_idx + i) % 37] += 1.0 / (abs(i) + 1)

        # 2. Spektralni pomak (Fourier)
        f_offset = self.spectral_rhythm()
        self.weights[(idx + f_offset) % 37] += 0.8
        
        # 3. Bias/Density korekcija
        self.apply_density_bias()

    def get_top_16(self):
        top_indices = np.argsort(self.weights)[-16:]
        return [self.wheel[i] for i in top_indices]

# Inicijalizacija
engine = UltraAlfastreetEngine()

def unos_broja(n):
    engine.update_weights(n)
    print(f"NOVI TOP 16: {engine.get_top_16()}")
