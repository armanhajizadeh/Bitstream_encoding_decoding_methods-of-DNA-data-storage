import streamlit as st
import csv
import os

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

# Define DNA animation HTML - this is a simpler animation that will definitely display
dna_animation_html = """
<style>
    /* DNA animation container */
    .dna-animation-container {
        position: fixed;
        left: 0;
        top: 0;
        bottom: 0;
        width: 100px;
        overflow: hidden;
        z-index: 1000;
    }
    
    /* DNA strand styling */
    .dna-strand {
        position: absolute;
        left: 40px;
        top: 10px;
        bottom: 10px;
        width: 20px;
        animation: dna-float 10s infinite linear;
    }
    
    /* Basepair styling */
    .base-pair {
        position: absolute;
        width: 60px;
        height: 5px;
        background: linear-gradient(to right, #00CED1, #20B2AA);
        left: -20px;
        border-radius: 10px;
        opacity: 0.8;
    }
    
    /* Left nucleotide */
    .base-pair::before {
        content: "";
        position: absolute;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #20B2AA;
        left: -5px;
        top: -3px;
    }
    
    /* Right nucleotide */
    .base-pair::after {
        content: "";
        position: absolute;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #008B8B;
        right: -5px;
        top: -3px;
    }
    
    /* Alternate base pairs */
    .base-pair:nth-child(even) {
        transform: rotate(30deg);
    }
    
    .base-pair:nth-child(odd) {
        transform: rotate(-30deg);
    }
    
    /* Animation keyframes */
    @keyframes dna-float {
        0% {
            transform: translateY(0) rotate(0deg);
        }
        100% {
            transform: translateY(-50%) rotate(360deg);
        }
    }
    
    /* Offset for main content */
    .main-content {
        margin-left: 80px;
    }
    
    /* Ensure Courier New as the default font */
    html, body, [class*="st-"] {
        font-family: 'Courier New', monospace;
    }
    
    /* Title styling */
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
</style>

<div class="dna-animation-container">
    <div class="dna-strand">
"""

# Generate 40 base pairs for the DNA animation
for i in range(40):
    dna_animation_html += f'<div class="base-pair" style="top: {i * 20}px;"></div>\n'

dna_animation_html += """
    </div>
</div>

<div class="main-content">
"""

# Apply the styles and DNA animation
st.markdown(dna_animation_html, unsafe_allow_html=True)

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

def load_7bit_to_8bit_mapping(csv_filename):
    """
    Loads the 7-bit to 8-bit mapping from the CSV file.
    Returns the mapping as a dictionary.
    """
    encoding_map = {}
    try:
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)  # Skip header if exists
            
            for row in reader:
                if len(row) >= 2:
                    encoding_map[row[0]] = row[1]
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
    
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

# Path to the CSV file in the repository
csv_file_path = "7to8.csv"  # Change this to the actual path of your CSV file

# Create two columns for button and result
col1, col2 = st.columns([1, 3])

with col1:
    encode_button = st.button("Encode to DNA")

if encode_button:
    if not user_input:
        st.warning("Please enter some text to encode.")
    else:
        try:
            # Load the mapping from repository file
            if os.path.exists(csv_file_path):
                encoding_map = load_7bit_to_8bit_mapping(csv_file_path)
            else:
                st.error(f"CSV file not found at path: {csv_file_path}")
                encoding_map = {}
            
            # Check if mapping loaded successfully
            if not encoding_map:
                st.error("Could not load mapping from CSV file. Please check the file format.")
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

# Footer information
st.markdown("---")
st.markdown('<p style="text-align:center; color:#888; font-size:0.8rem;">DNA Encoding Tool - Using biological molecules to store digital information</p>', unsafe_allow_html=True)

# Close the main content div
st.markdown('</div>', unsafe_allow_html=True)