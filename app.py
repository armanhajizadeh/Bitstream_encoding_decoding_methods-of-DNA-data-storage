import streamlit as st
import csv
import os
import base64

# Set page configuration - with minimal menu items
st.set_page_config(
    page_title="DNA Encoder",
    page_icon="🧬",
    layout="wide",
    menu_items={
        'Get help': None,
        'Report a bug': None,
        'About': None
    }
)

# Apply Courier New font styling and hide GitHub and edit buttons
st.markdown("""
<style>
    /* Set Courier New as the default font for the entire app */
    html, body, [class*="st-"] {
        font-family: 'Courier New', monospace;
    }
    .main-title {
        font-size: 2.2rem;
        margin-bottom: 1rem;
        text-align: center;
        font-family: 'Courier New', monospace;
    }
    .subtitle {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-align: center;
        color: #666;
        font-family: 'Courier New', monospace;
    }
    /* Hide most of the default header */
    header {
        visibility: hidden;
    }
    /* Keep only the "Share" button visible */
    header button:last-child {
        visibility: visible;
    }
    /* Hide hamburger menu */
    section[data-testid="stSidebar"] {
        display: none;
    }
    /* Hide GitHub icon and edit buttons */
    .viewerBadge_link__1S137, .viewerBadge_container__1QSob,
    footer, #MainMenu, .stActionButton {
        display: none !important;
    }
    /* Hide deploy and GitHub buttons */
    .css-1rs6os {
        visibility: hidden;
    }
    .stDeployButton {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

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

# Binary to ACTG mapping
binary_to_dna = {
    '00': 'A',
    '01': 'C',
    '10': 'T',
    '11': 'G'
}

# Embed the 7to8.csv data directly
# This is a placeholder - replace with your actual CSV content
embedded_csv_data = """7-bit,8-bit
0000000,00100011
0000001,00010011
0000010,00111011
0000011,00110010
0000100,00110100
0000101,01001100
0000110,01000011
0000111,00111110
0001000,00110001
0001001,00011100
0001010,01110011
0001011,11001101
0001100,11000111
0001101,10111100
0001110,11000100
0001111,11001000
0010000,11000001
0010001,11000010
0010010,10110011
0010011,10001100
0010100,11011100
0010101,11010011
0010110,01111100
0010111,10000011
0011000,00111101
0011001,00110111
0011010,11001110
0011011,11001011
0011100,11101100
0011101,11100011
0011110,00101101
0011111,00101110
0100000,01110010
0100001,01110100
0100010,01001110
0100011,01000111
0100100,01001000
0100101,01000100
0100110,01011110
0100111,01111111
0101000,01010100
0101001,01000101
0101010,00101111
0101011,01010101
0101100,01011010
0101101,00101010
0101110,01111101
0101111,01111011
0110000,01100001
0110001,00111111
0110010,01100011
0110011,01010001
0110100,01010010
0110101,01000000
0110110,01110110
0110111,01100100
0111000,01100101
0111001,01101100
0111010,01101001
0111011,01101101
0111100,01101110
0111101,01110000
0111110,01100110
0111111,01100111
1000000,10111000
1000001,11111000
1000010,10100111
1000011,10101000
1000100,10101001
1000101,10101010
1000110,10101100
1000111,10101101
1001000,10101110
1001001,10101111
1001010,10110000
1001011,10110001
1001100,10110010
1001101,10110100
1001110,10110101
1001111,10110110
1010000,10110111
1010001,10111001
1010010,10111010
1010011,10111011
1010100,10111101
1010101,10111110
1010110,10111111
1010111,11000000
1011000,11000011
1011001,11000101
1011010,11000110
1011011,11001001
1011100,11001010
1011101,11001011
1011110,11001100
1011111,11001111
1100000,11010000
1100001,11010001
1100010,11010010
1100011,11010100
1100100,11010101
1100101,11010110
1100110,11010111
1100111,11011000
1101000,11011001
1101001,11011010
1101010,11011011
1101011,11011101
1101100,11011110
1101101,11011111
1101110,11100000
1101111,11100001
1110000,11100010
1110001,11100100
1110010,11100101
1110011,11100110
1110100,11100111
1110101,11101000
1110110,11101001
1110111,11101010
1111000,11101011
1111001,11101101
1111010,11101110
1111011,11101111
1111100,11110000
1111101,11110001
1111110,11110010
1111111,11110011"""

def load_embedded_mapping():
    """
    Loads the 7-bit to 8-bit mapping from the embedded CSV data.
    Returns the mapping as a dictionary.
    """
    encoding_map = {}
    try:
        # Split the CSV data into lines
        lines = embedded_csv_data.strip().split('\n')
        
        # Parse the CSV data
        for i, line in enumerate(lines):
            if i == 0:  # Skip header
                continue
                
            values = line.split(',')
            if len(values) >= 2:
                encoding_map[values[0]] = values[1]
    except Exception as e:
        st.error(f"Error parsing embedded CSV data: {str(e)}")
    
    return encoding_map

def binary_to_actg(binary_str):
    """
    Converts a binary string to ACTG format by grouping every 2 bits.
    """
    if len(binary_str) % 2 != 0:
        binary_str += '0'  # Pad with a zero if odd length
    
    dna = ''
    for i in range(0, len(binary_str), 2):
        pair = binary_str[i:i+2]
        dna += binary_to_dna[pair]
    
    return dna

def text_to_actg(text, encoding_map):
    """
    Converts text to ACTG DNA sequence using 7-bit to 8-bit encoding.
    """
    # Convert text to 7-bit binary
    binary_7bit = ''
    for char in text:
        if char not in char_to_7bit:
            raise ValueError(f"Unsupported character: {char}")
        binary_7bit += char_to_7bit[char]
    
    # Convert 7-bit chunks to 8-bit encoded chunks
    binary_8bit = ''
    for i in range(0, len(binary_7bit), 7):
        chunk_7bit = binary_7bit[i:i+7]
        # Handle the last chunk if it's incomplete
        if len(chunk_7bit) < 7:
            chunk_7bit = chunk_7bit.ljust(7, '0')
        
        # Encode 7-bit to 8-bit using the mapping
        if chunk_7bit in encoding_map:
            binary_8bit += encoding_map[chunk_7bit]
        else:
            st.warning(f"Missing mapping for 7-bit chunk: {chunk_7bit}. Using default padding.")
            binary_8bit += '00000000'  # Default padding
    
    # Convert to ACTG (every 2 bits becomes 1 nucleotide)
    actg = binary_to_actg(binary_8bit)
    
    return actg

def gc_content(seq):
    """
    Calculates the GC content percentage of a DNA sequence.
    """
    if not seq:
        return 0.0
    gc = seq.count('G') + seq.count('C')
    return (gc / len(seq)) * 100.0

# Set up the Streamlit interface
st.markdown('<h1 class="main-title">Have you ever wondered how your name would be stored on a biological hard disk?</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter text below to encode it into DNA (ACTG) sequences</p>', unsafe_allow_html=True)

# Text input
user_input = st.text_area("Enter your text to encode:", height=150)

# Create two columns for button and result
col1, col2 = st.columns([1, 3])

with col1:
    encode_button = st.button("Encode to DNA")

if encode_button:
    if not user_input:
        st.warning("Please enter some text to encode.")
    else:
        try:
            # Load the mapping from embedded data instead of file
            encoding_map = load_embedded_mapping()
            
            # Check if mapping loaded successfully
            if not encoding_map:
                st.error("Could not load mapping data. Please try again.")
            else:
                # Encode the text
                actg_sequence = text_to_actg(user_input, encoding_map)
                
                # Display results
                st.markdown('<h2>Encoded DNA Sequence</h2>', unsafe_allow_html=True)
                st.code(actg_sequence)
                
                # Calculate and display GC content
                gc = gc_content(actg_sequence)
                st.metric("GC Content", f"{gc:.2f}%")
                
                # Additional explanation
                st.markdown('<p>This sequence represents how your text would be stored in a DNA-based storage system!</p>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer without links
st.markdown("---")
st.markdown('<p style="text-align:center; color:#888; font-size:0.8rem;">DNA Encoding Tool - Using biological molecules to store digital information</p>', unsafe_allow_html=True)