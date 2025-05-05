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

# --- DNA ANIMATION (embedded) ---
dna_animation_html = """
<style>
    html, body, [class*="st-"] {
        font-family: 'Courier New', monospace;
    }

    .main-title {
        font-size: 2.2rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    .subtitle {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-align: center;
        color: #666;
    }

    header {
        visibility: hidden;
    }

    header button:last-child {
        visibility: visible;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    .dna-container {
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 90px;
        perspective: 1200px;
        z-index: 1000;
    }

    .dna-helix {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100%;
        height: 80%;
        transform-style: preserve-3d;
        animation: dna-rotate 20s linear infinite;
    }

    @keyframes dna-rotate {
        0% { transform: translate(-50%, -50%) rotateY(0deg) rotateX(10deg); }
        50% { transform: translate(-50%, -50%) rotateY(180deg) rotateX(-10deg); }
        100% { transform: translate(-50%, -50%) rotateY(360deg) rotateX(10deg); }
    }

    .strand {
        position: absolute;
        width: 8px;
        height: 100%;
        border-radius: 4px;
        box-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
    }

    .strand.left {
        left: 30%;
        background: linear-gradient(to bottom, rgba(0, 120, 215, 0.2), rgba(0, 180, 216, 0.9), rgba(32, 178, 170, 0.8), rgba(0, 180, 216, 0.9), rgba(0, 120, 215, 0.2));
        animation: strand-pulse 4s ease-in-out infinite alternate;
    }

    .strand.right {
        left: 70%;
        background: linear-gradient(to bottom, rgba(0, 120, 215, 0.2), rgba(0, 139, 139, 0.9), rgba(0, 206, 209, 0.8), rgba(0, 139, 139, 0.9), rgba(0, 120, 215, 0.2));
        animation: strand-pulse 4s ease-in-out infinite alternate-reverse;
    }

    @keyframes strand-pulse {
        0% { opacity: 0.8; box-shadow: 0 0 5px rgba(0, 191, 255, 0.5); }
        50% { opacity: 1; box-shadow: 0 0 10px rgba(0, 191, 255, 0.7); }
        100% { opacity: 0.8; box-shadow: 0 0 5px rgba(0, 191, 255, 0.5); }
    }

    .base-pair {
        position: absolute;
        width: 40%;
        height: 3px;
        left: 30%;
        border-radius: 3px;
        transform-style: preserve-3d;
        box-shadow: 0 0 2px rgba(255, 255, 255, 0.7);
    }

    .base-pair.at { background: linear-gradient(to right, #48D1CC, #20B2AA); animation: glow-at 3s infinite alternate; }
    .base-pair.ta { background: linear-gradient(to right, #20B2AA, #48D1CC); animation: glow-ta 3s infinite alternate; }
    .base-pair.gc { background: linear-gradient(to right, #00BFFF, #1E90FF); animation: glow-gc 3s infinite alternate; }
    .base-pair.cg { background: linear-gradient(to right, #1E90FF, #00BFFF); animation: glow-cg 3s infinite alternate; }

    @keyframes glow-at { 0% { box-shadow: 0 0 2px rgba(72, 209, 204, 0.5); } 100% { box-shadow: 0 0 5px rgba(72, 209, 204, 0.8); } }
    @keyframes glow-ta { 0% { box-shadow: 0 0 2px rgba(32, 178, 170, 0.5); } 100% { box-shadow: 0 0 5px rgba(32, 178, 170, 0.8); } }
    @keyframes glow-gc { 0% { box-shadow: 0 0 2px rgba(0, 191, 255, 0.5); } 100% { box-shadow: 0 0 5px rgba(0, 191, 255, 0.8); } }
    @keyframes glow-cg { 0% { box-shadow: 0 0 2px rgba(30, 144, 255, 0.5); } 100% { box-shadow: 0 0 5px rgba(30, 144, 255, 0.8); } }

    .nucleotide {
        position: absolute;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        top: -3px;
        box-shadow: 0 0 3px rgba(255, 255, 255, 0.6);
    }

    .nucleotide.a { background-color: #48D1CC; left: -4px; }
    .nucleotide.t { background-color: #20B2AA; right: -4px; }
    .nucleotide.g { background-color: #00BFFF; left: -4px; }
    .nucleotide.c { background-color: #1E90FF; right: -4px; }

    .main-content { margin-left: 80px; }
</style>
<div class="dna-container"><div class="dna-helix">
<div class="strand left"></div>
<div class="strand right"></div>
"""

# Dynamically generate 30 base pairs
base_pair_types = ['at', 'gc', 'ta', 'cg']
spacing = 100 / 30
for i in range(30):
    bp = base_pair_types[i % 4]
    y = i * spacing
    rot = i * (720 / 30)
    dna_animation_html += f"""
    <div class="base-pair {bp}" style="top: {y}%; transform: rotateY({rot}deg);">
        <div class="nucleotide {bp[0]}"></div>
        <div class="nucleotide {bp[1]}"></div>
    </div>"""

dna_animation_html += "</div></div><div class='main-content'>"
st.markdown(dna_animation_html, unsafe_allow_html=True)

# --- ENCODING LOGIC ---

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
