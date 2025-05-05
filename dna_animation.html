import streamlit as st
import csv
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="DNA Encoder",
    page_icon="🧬",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# --- LOAD ANIMATION HTML ---
try:
    with open("dna_animation.html", "r") as f:
        dna_animation_html = f.read()
    st.markdown(dna_animation_html, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("DNA animation file not found. Please ensure 'dna_animation.html' is in the project folder.")

# --- DNA ENCODING LOGIC ---
char_to_7bit = {
    'A': '1000001', 'B': '1000010', 'C': '1000011', 'D': '1000100',
    'E': '1000101', 'F': '1000110', 'G': '1000111', 'H': '1001000',
    'I': '1001001', 'J': '1001010', 'K': '1001011', 'L': '1001100',
    'M': '1001101', 'N': '1001110', 'O': '1001111', 'P': '1010000',
    'Q': '1010001', 'R': '1010010', 'S': '1010011', 'T': '1010100',
    'U': '1010101', 'V': '1010110', 'W': '1010111', 'X': '1011000',
    'Y': '1011001', 'Z': '1011010', ' ': '0100000'
}

binary_to_dna = {
    '00': 'A',
    '01': 'C',
    '10': 'T',
    '11': 'G'
}

def load_7bit_to_8bit_mapping(csv_file):
    mapping = {}
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    mapping[row[0]] = row[1]
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
    return mapping

def binary_to_actg(binary_str):
    if len(binary_str) % 2 != 0:
        binary_str += '0'
    return ''.join(binary_to_dna.get(binary_str[i:i+2], 'A') for i in range(0, len(binary_str), 2))

def text_to_actg(text, mapping):
    binary_7bit = ''.join(char_to_7bit.get(char, '') for char in text)
    binary_8bit = ''
    for i in range(0, len(binary_7bit), 7):
        chunk = binary_7bit[i:i+7].ljust(7, '0')
        binary_8bit += mapping.get(chunk, '00000000')
    return binary_to_actg(binary_8bit)

def gc_content(seq):
    return (seq.count('G') + seq.count('C')) / len(seq) * 100 if seq else 0

# --- UI ---
st.markdown('<h1 class="main-title">Have you ever wondered how your name would be stored on a biological hard disk?</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter text below to encode it into DNA (ACTG) sequences</p>', unsafe_allow_html=True)

user_input = st.text_area("Enter your text to encode:", height=150)
csv_file_path = "7to8.csv"

col1, col2 = st.columns([1, 3])
with col1:
    encode_button = st.button("Encode to DNA")

if encode_button:
    if not user_input:
        st.warning("Please enter text.")
    else:
        if not os.path.exists(csv_file_path):
            st.error("7to8.csv not found.")
        else:
            mapping = load_7bit_to_8bit_mapping(csv_file_path)
            try:
                dna_seq = text_to_actg(user_input.upper(), mapping)
                st.markdown('<h2>Encoded DNA Sequence</h2>', unsafe_allow_html=True)
                st.code(dna_seq)
                st.metric("GC Content", f"{gc_content(dna_seq):.2f}%")
                st.markdown('<p>This is how your data could be stored in DNA!</p>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Encoding error: {str(e)}")

st.markdown("---")
st.markdown('<p style="text-align:center; color:#888; font-size:0.8rem;">DNA Encoding Tool - Powered by molecules & code</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
