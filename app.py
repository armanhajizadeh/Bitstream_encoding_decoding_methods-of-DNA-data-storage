import streamlit as st
import csv

# Character to 7-bit binary mapping
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
    'z': '1011001', '{': '1011010', '}': '1011011', '|': '1011100', '~': '1011101',
    '`': '1011110', '\t': '1011111', '\n': '1100000', '\r': '1100001', '€': '1100010',
    '£': '1100011', '¥': '1100100', '¢': '1100101', '©': '1100110', '®': '1100111',
    '™': '1101000', '§': '1101001', '¶': '1101010', '•': '1101011', '‹': '1101100',
    '›': '1101101', '«': '1101110', '»': '1101111', '↑': '1110000', '↓': '1110001',
    '→': '1110010', '←': '1110011', '↔': '1110100', '↕': '1110101', '⇐': '1110110',
    '⇒': '1110111', '⇑': '1111000', '⇓': '1111001', '★': '1111010', '☆': '1111011',
    '♠': '1111100', '♣': '1111101', '♥': '1111110', '♦': '1111111'
}

bin7_to_char = {v: k for k, v in char_to_7bit.items()}

binary_to_dna = {
    '00': 'A', '01': 'C', '10': 'T', '11': 'G'
}
dna_to_binary = {v: k for k, v in binary_to_dna.items()}

def binary_to_actg(binary_str):
    if len(binary_str) % 2 != 0:
        raise ValueError("Binary string length must be even for ACTG conversion.")
    return ''.join(binary_to_dna[binary_str[i:i+2]] for i in range(0, len(binary_str), 2))

def actg_to_binary(dna_str):
    return ''.join(dna_to_binary[nuc] for nuc in dna_str)

def text_to_actg(text, encoding_map):
    binary_7bit = ''.join(char_to_7bit[char] for char in text if char in char_to_7bit)
    binary_8bit = ''.join(encoding_map[binary_7bit[i:i+7].ljust(7, '0')] for i in range(0, len(binary_7bit), 7))
    return binary_to_actg(binary_8bit)

def actg_to_text(actg, decoding_map):
    binary_8bit = actg_to_binary(actg)
    binary_7bit = ''.join(decoding_map.get(binary_8bit[i:i+8], '0000000') for i in range(0, len(binary_8bit), 8))
    return ''.join(bin7_to_char.get(binary_7bit[i:i+7], '?') for i in range(0, len(binary_7bit), 7))

def gc_content(seq):
    if not seq:
        return 0.0
    gc_count = seq.count('G') + seq.count('C')
    return (gc_count / len(seq)) * 100.0

# === Streamlit UI Starts Here ===

st.title("Text to DNA (ACTG) Encoder")

# Upload CSV file
csv_file = st.file_uploader("Upload 7-to-8 bit mapping CSV (7to8.csv)", type="csv")

if csv_file is not None:
    # Load encoding and decoding maps
    encoding_map = {}
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
        if len(row) == 2:
            encoding_map[row[0]] = row[1]
    decoding_map = {v: k for k, v in encoding_map.items()}

    # Text input
    user_input = st.text_area("Enter text to encode:")

    if user_input:
        try:
            # Encode
            actg_sequence = text_to_actg(user_input, encoding_map)
            gc = gc_content(actg_sequence)

            st.subheader("ACTG Sequence")
            st.code(actg_sequence, language='text')

            st.subheader("GC Content")
            st.write(f"{gc:.2f}%")

        except ValueError as e:
            st.error(f"Encoding Error: {e}")
else:
    st.info("Please upload the required 7to8.csv file to begin.")
