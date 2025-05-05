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

# Define DNA animation HTML - enhanced with more realistic features
dna_animation_html = """
<style>
    /* Base styling */
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
    
    /* Enhanced realistic DNA styling */
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
        0% {
            transform: translate(-50%, -50%) rotateY(0deg) rotateX(10deg);
        }
        50% {
            transform: translate(-50%, -50%) rotateY(180deg) rotateX(-10deg);
        }
        100% {
            transform: translate(-50%, -50%) rotateY(360deg) rotateX(10deg);
        }
    }
    
    /* Create the backbone strands with more depth */
    .strand {
        position: absolute;
        width: 8px;
        height: 100%;
        border-radius: 4px;
        box-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
    }
    
    .strand.left {
        left: 30%;
        background: linear-gradient(to bottom, 
            rgba(0, 120, 215, 0.2), 
            rgba(0, 180, 216, 0.9) 10%, 
            rgba(32, 178, 170, 0.8) 50%, 
            rgba(0, 180, 216, 0.9) 90%, 
            rgba(0, 120, 215, 0.2));
        transform-origin: center;
        animation: strand-pulse 4s ease-in-out infinite alternate;
    }
    
    .strand.right {
        left: 70%;
        background: linear-gradient(to bottom, 
            rgba(0, 120, 215, 0.2), 
            rgba(0, 139, 139, 0.9) 10%, 
            rgba(0, 206, 209, 0.8) 50%, 
            rgba(0, 139, 139, 0.9) 90%, 
            rgba(0, 120, 215, 0.2));
        transform-origin: center;
        animation: strand-pulse 4s ease-in-out infinite alternate-reverse;
    }
    
    @keyframes strand-pulse {
        0% {
            opacity: 0.8;
            box-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
        }
        50% {
            opacity: 1;
            box-shadow: 0 0 10px rgba(0, 191, 255, 0.7);
        }
        100% {
            opacity: 0.8;
            box-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
        }
    }
    
    /* Base pairs with improved styling */
    .base-pair {
        position: absolute;
        width: 40%;
        height: 3px;
        left: 30%;
        border-radius: 3px;
        transform-style: preserve-3d;
        box-shadow: 0 0 2px rgba(255, 255, 255, 0.7);
    }
    
    /* Different base pair types with scientific color coding */
    .base-pair.at {
        background: linear-gradient(to right, #48D1CC, #20B2AA);
        animation: glow-at 3s infinite alternate;
    }
    
    .base-pair.ta {
        background: linear-gradient(to right, #20B2AA, #48D1CC);
        animation: glow-ta 3s infinite alternate;
    }
    
    .base-pair.gc {
        background: linear-gradient(to right, #00BFFF, #1E90FF);
        animation: glow-gc 3s infinite alternate;
    }
    
    .base-pair.cg {
        background: linear-gradient(to right, #1E90FF, #00BFFF);
        animation: glow-cg 3s infinite alternate;
    }
    
    @keyframes glow-at {
        0% { box-shadow: 0 0 2px rgba(72, 209, 204, 0.5); }
        100% { box-shadow: 0 0 5px rgba(72, 209, 204, 0.8); }
    }
    
    @keyframes glow-ta {
        0% { box-shadow: 0 0 2px rgba(32, 178, 170, 0.5); }
        100% { box-shadow: 0 0 5px rgba(32, 178, 170, 0.8); }
    }
    
    @keyframes glow-gc {
        0% { box-shadow: 0 0 2px rgba(0, 191, 255, 0.5); }
        100% { box-shadow: 0 0 5px rgba(0, 191, 255, 0.8); }
    }
    
    @keyframes glow-cg {
        0% { box-shadow: 0 0 2px rgba(30, 144, 255, 0.5); }
        100% { box-shadow: 0 0 5px rgba(30, 144, 255, 0.8); }
    }
    
    /* Nucleotide bases with enhanced style */
    .nucleotide {
        position: absolute;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        top: -3px;
        box-shadow: 0 0 3px rgba(255, 255, 255, 0.6);
    }
    
    .nucleotide.a {
        background-color: #48D1CC;
        left: -4px;
    }
    
    .nucleotide.t {
        background-color: #20B2AA;
        right: -4px;
    }
    
    .nucleotide.g {
        background-color: #00BFFF;
        left: -4px;
    }
    
    .nucleotide.c {
        background-color: #1E90FF;
        right: -4px;
    }
    
    /* Add small particle effect to simulate water molecules */
    .water-particle {
        position: absolute;
        width: 2px;
        height: 2px;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        pointer-events: none;
    }
    
    /* Add padding to main content to avoid overlap with DNA */
    .main-content {
        margin-left: 80px;
    }
</style>

<div class="dna-container">
    <div class="dna-helix">
        <div class="strand left"></div>
        <div class="strand right"></div>
"""

# Generate 30 base pairs with alternating types (AT and GC)
types = ['at', 'gc', 'ta', 'cg']
num_base_pairs = 30
spacing = 100 / num_base_pairs

for i in range(num_base_pairs):
    pair_type = types[i % 4]
    y_pos = i * spacing
    rotation = i * (720 / num_base_pairs)  # 720 degrees = 2 full turns for helix effect
    
    if pair_type == 'at':
        dna_animation_html += f'''
        <div class="base-pair at" style="top: {y_pos}%; transform: rotateY({rotation}deg);">
            <div class="nucleotide a"></div>
            <div class="nucleotide t"></div>
        </div>
        '''
    elif pair_type == 'ta':
        dna_animation_html += f'''
        <div class="base-pair ta" style="top: {y_pos}%; transform: rotateY({rotation}deg);">
            <div class="nucleotide t"></div>
            <div class="nucleotide a"></div>
        </div>
        '''
    elif pair_type == 'gc':
        dna_animation_html += f'''
        <div class="base-pair gc" style="top: {y_pos}%; transform: rotateY({rotation}deg);">
            <div class="nucleotide g"></div>
            <div class="nucleotide c"></div>
        </div>
        '''
    elif pair_type == 'cg':
        dna_animation_html += f'''
        <div class="base-pair cg" style="top: {y_pos}%; transform: rotateY({rotation}deg);">
            <div class="nucleotide c"></div>
            <div class="nucleotide g"></div>
        </div>
        '''

# Add 20 water particles for ambient effect
for i in range(20):
    x = 10 + (i % 7) * 10
    y = (i * 5) % 100
    delay = (i * 0.5) % 5
    duration = 3 + (i % 3)
    
    dna_animation_html += f'''
    <div class="water-particle" style="left: {x}%; top: {y}%; 
        animation: float-particle {duration}s ease-in-out {delay}s infinite alternate;"></div>
    '''

dna_animation_html += '''
    </div>
</div>

<style>
@keyframes float-particle {
    0% {
        transform: translate(0, 0) scale(1);
        opacity: 0.2;
    }
    50% {
        transform: translate(5px, -5px) scale(1.5);
        opacity: 0.5;
    }
    100% {
        transform: translate(0, -10px) scale(1);
        opacity: 0.2;
    }
}
</style>

<div class="main-content">
'''

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