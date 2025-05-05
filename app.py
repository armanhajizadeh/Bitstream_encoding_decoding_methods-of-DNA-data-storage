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

# --- DNA ANIMATION STYLES ---
with open("dna_animation.html", "r") as f:
    dna_animation_html = f.read()
st.markdown(dna_animation_html, unsafe_allow_html=True)

# --- CHAR TO 7-BIT MAPPING (your long one) ---
char_to_7bit = {
    'Y': '0000000', 'Q': '0000001', 'K': '0000010', '_': '0000011', '7': '0000100',
    'S': '0000101', '1': '0000110', '0': '0000111', '5': '0001000', '!': '0001001',
    '8': '0001010', 'J': '0001011', ' ': '0001100', '"': '0001101', 'I': '0001110',
    '#': '0001111', '$': '0010000', '%': '0010001', '&': '0010010', "'": '0010011',
    'B': '0010100', ']': '0010101', 'W': '0010110', 'V': '0010111', 'A': '0011000',
    'H': '0011001', '(': '0011010', ')': '0011011', 'X': '0011100', '^': '0011101',
    'U': '0011110', 'Z': '0011111', '*': '0100000', '+': '0100001', '4': '0100010',
    '.': '0100011', '3': '0100100', '-': '0100101', '9': '0100110', '?': '0100111',
    'O': '0101000', 'E': '0101001', '/': '0101010', 'F': '0101011', ':': '0101100',
    ';': '0101101', 'P': '0101110', 'C': '0101111', '<': '0110000', '=': '0110001',
    '2': '0110010', '>': '0110011', 'R': '0110100', 'M': '0110101', ',': '0110110',
    'N': '0110111', '@': '0111000', 'L': '0111001', '[': '0111010', '\\': '0111011',
    '6': '0111100', 'T': '0111101', 'D': '0111110', 'G': '0111111',
    'a': '1000000', 'b': '1000001', 'c': '1000010', 'd': '1000011', 'e': '1000100',
    'f': '1000101', 'g': '1000110', 'h': '1000111', 'i': '1001000', 'j': '1001001',
    'k': '1001010', 'l': '1001011', 'm': '1001100', 'n': '1001101', 'o': '1001110',
    'p': '1001111', 'q': '1010000', 'r': '1010001', 's': '1010010', 't': '1010011',
    'u': '1010100', 'v': '1010101', 'w': '1010110', 'x': '1010111', 'y': '1011000',
    'z': '1011001'
}

binary_to_dna = {
    '00': 'A',
    '01': 'C',
    '10': 'T',
    '11': 'G'
}

def load_7bit_to_8bit_mapping(csv_filename):
    encoding_map = {}
    try:
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip header if any
            for row in reader:
                if len(row) >= 2:
                    encoding_map[row[0]] = row[1]
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
    return encoding_map

def binary_to_actg(binary_str):
    if len(binary_str) % 2 != 0:
        binary_str += '0'
    return ''.join(binary_to_dna.get(binary_str[i:i+2], 'A') for i in range(0, len(binary_str), 2))

def text_to_actg(text, encoding_map):
    binary_7bit = ''.join(char_to_7bit.get(char, '') for char in text)
    binary_8bit = ''
    for i in range(0, len(binary_7bit), 7):
        chunk = binary_7bit[i:i+7].ljust(7, '0')
        binary_8bit += encoding_map.get(chunk, '00000000')
    return binary_to_actg(binary_8bit)

def gc_content(seq):
    if not seq:
        return 0.0
    return (seq.count('G') + seq.count('C')) / len(seq) * 100

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
        st.warning("Please enter some text.")
    else:
        encoding_map = load_7bit_to_8bit_mapping(csv_file_path) if os.path.exists(csv_file_path) else {}
        if not encoding_map:
            st.error("Mapping file missing or empty.")
        else:
            try:
                dna_seq = text_to_actg(user_input, encoding_map)
                gc = gc_content(dna_seq)
                st.markdown('<h2>Encoded DNA Sequence</h2>', unsafe_allow_html=True)
                st.code(dna_seq)
                st.metric("GC Content", f"{gc:.2f}%")
                st.markdown('<p>This sequence represents how your text would be stored in a DNA-based storage system!</p>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown('<p style="text-align:center; color:#888; font-size:0.8rem;">DNA Encoding Tool - Powered by molecules & code</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
