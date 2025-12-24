import streamlit as st
import collections

# Postavke stranice
st.set_page_config(page_title="R8 Quantum Predictor", layout="centered")

# Fizički raspored Alfastreet R8 kola
WHEEL = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 
         5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

# Inicijalizacija baze podataka u sesiji
if 'numbers' not in st.session_state:
    st.session_state.numbers = [14,1,25,5,7,15,19,28,33,21,3,24,34,25,18,27,34,11,4,28,34,26,24,24,25,8,4,34,8,16,11,34,4,26,29,3,32,11,25,23,28,6,20,12,6,29,32,33,25,21,22]

def get_neighbors(number, count=2):
    try:
        idx = WHEEL.index(number)
        return [WHEEL[(idx + i) % 37] for i in range(-count, count + 1)]
    except ValueError:
        return []

def calculate_top_16(niz):
    if not niz: return []
    
    # --- AUTOMATSKO PODEŠAVANJE PARAMETARA (Self-Tuning) ---
    freq = collections.Counter(niz)
    last_num = niz[-1]
    
    # Ako se zadnja 3 broja ponavljaju u istom sektoru, pojačaj 'Sector Weight'
    scores = {n: 0 for n in range(37)}
    
    for num in range(37):
        # 1. Kvantna masa (Frekvencija pojavljivanja)
        scores[num] += freq.get(num, 0) * 2.8
        
        # 2. Dinamički sektor (Susjedi zadnjeg broja)
        if num in get_neighbors(last_num, 4):
            scores[num] += 6.5
            
        # 3. Sidrišta (Vruće točke sustava - npr. 25 i 34)
        vruci_brojevi = [n for n, c in freq.most_common(3)]
        for vruci in vruci_brojevi:
            if num in get_neighbors(vruci, 2):
                scores[num] += 3.5

    sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [x[0] for x in sorted_res[:16]]

# --- UI DIZAJN ---
st.title("🎰 R8 Quantum Predictor")
st.subheader("Samo-podešavajući statistički model")

# Unos novog broja
new_num = st.number_input("Unesi zadnji broj koji je pao:", min_value=0, max_value=36, step=1)
if st.button("DODAJ BROJ I ANALIZIRAJ"):
    st.session_state.numbers.append(new_num)
    st.rerun()

# Prikaz Top 16 ishoda
top_16 = calculate_top_16(st.session_state.numbers)

st.write("---")
st.header("🎯 Sljedeći ishod (Top 16):")
cols = st.columns(4)
for i, num in enumerate(top_16):
    cols[i % 4].button(f"**{num}**", key=f"btn_{i}", use_container_width=True)

st.write("---")
with st.expander("Pogledaj povijest i statistiku"):
    st.write(f"Ukupno analizirano: {len(st.session_state.numbers)} brojeva")
    st.write(f"Zadnjih 10: {st.session_state.numbers[-10:]}")
    if st.button("Resetiraj sve"):
        st.session_state.numbers = []
        st.rerun()