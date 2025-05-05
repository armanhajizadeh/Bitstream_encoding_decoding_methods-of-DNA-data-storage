import streamlit as st

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

# Create reverse mapping
bin7_to_char = {v: k for k, v in char_to_7bit.items()}

# Binary to ACTG mapping
binary_to_dna = {
    '00': 'A',
    '01': 'C',
    '10': 'T',
    '11': 'G'
}

# Create reverse mapping
dna_to_binary = {v: k for k, v in binary_to_dna.items()}

# === HARDCODED 7-bit to 8-bit map (from your previously used CSV) ===
encoding_map = {
    '0000000': '00100011',
    '0000001': '00010011',
    '0000010': '00111011',
    '0000011': '00110010',
    '0000100': '00110100',
    '0000101': '01001100',
    '0000110': '01000011',
    '0000111': '00111110',
    '0001000': '00110001',
    '0001001': '00011100',
    '0001010': '01110011',
    '0001011': '11001101',
    '0001100': '11000111',
    '0001101': '10111100',
    '0001110': '11000100',
    '0001111': '11001000',
    '0010000': '11000001',
    '0010001': '11000010',
    '0010010': '10110011',
    '0010011': '10001100',
    '0010100': '11011100',
    '0010101': '11010011',
    '0010110': '01111100',
    '0010111': '10000011',
    '0011000': '00111101',
    '0011001': '00110111',
    '0011010': '11001110',
    '0011011': '11001011',
    '0011100': '11101100',
    '0011101': '11100011',
    '0011110': '00101101',
    '0011111': '00101110',
    '0100000': '01110010',
    '0100001': '01110100',
    '0100010': '01001110',
    '0100011': '01000111',
    '0100100': '01001000',
    '0100101': '01000100',
    '0100110': '01011110',
    '0100111': '01111111',
    '0101000': '01010100',
    '0101001': '01000101',
    '0101010': '00101111',
    '0101011': '01010101',
    '0101100': '01011010',
    '0101101': '00101010',
    '0101110': '01111101',
    '0101111': '01111011',
    '0110000': '01100001',
    '0110001': '00111111',
    '0110010': '01100011',
    '0110011': '01010001',
    '0110100': '01010010',
    '0110101': '01000000',
    '0110110': '01110110',
    '0110111': '01100100',
    '0111000': '01100101',
    '0111001': '01101100',
    '0111010': '01101001',
    '0111011': '01101101',
    '0111100': '01101110',
    '0111101': '01110000',
    '0111110': '01100110',
    '0111111': '01100111',
    '1000000': '10111000',
    '1000001': '11111000',
    '1000010': '10100111',
    '1000011': '10101000',
    '1000100': '10101001',
    '1000101': '10101010',
    '1000110': '10101100',
    '1000111': '10101101',
    '1001000': '10101110',
    '1001001': '10101111',
    '1001010': '10110000',
    '1001011': '10110001',
    '1001100': '10110010',
    '1001101': '10110100',
    '1001110': '10110101',
    '1001111': '10110110',
    '1010000': '10110111',
    '1010001': '10111001',
    '1010010': '10111010',
    '1010011': '10111011',
    '1010100': '10111101',
    '1010101': '10111110',
    '1010110': '10111111',
    '1010111': '11000000',
    '1011000': '11000011',
    '1011001': '11000101',
    '1011010': '11000110',
    '1011011': '11001001',
    '1011100': '11001010',
    '1011101': '11001011',
    '1011110': '11001100',
    '1011111': '11001111',
    '1100000': '11010000',
    '1100001': '11010001',
    '1100010': '11010010',
    '1100011': '11010100',
    '1100100': '11010101',
    '1100101': '11010110',
    '1100110': '11010111',
    '1100111': '11011000',
    '1101000': '11011001',
    '1101001': '11011010',
    '1101010': '11011011',
    '1101011': '11011101',
    '1101100': '11011110',
    '1101101': '11011111',
    '1101110': '11100000',
    '1101111': '11100001',
    '1110000': '11100010',
    '1110001': '11100100',
    '1110010': '11100101',
    '1110011': '11100110',
    '1110100': '11100111',
    '1110101': '11101000',
    '1110110': '11101001',
    '1110111': '11101010',
    '1111000': '11101011',
    '1111001': '11101101',
    '1111010': '11101110',
    '1111011': '11101111',
    '1111100': '11110000',
    '1111101': '11110001',
    '1111110': '11110010',
    '1111111': '11110011'
}

# Create reverse mapping for decoding
decoding_map = {v: k for k, v in encoding_map.items()}

def binary_to_actg(binary_str):
    """
    Converts a binary string to ACTG format by grouping every 2 bits.
    """
    if len(binary_str) % 2 != 0:
        raise ValueError("Binary string length must be even for ACTG conversion.")

    dna = ''
    for i in range(0, len(binary_str), 2):
        pair = binary_str[i:i+2]
        dna += binary_to_dna[pair]

    return dna

def actg_to_binary(dna_str):
    """
    Converts an ACTG string back to binary.
    """
    binary = ''
    for nucleotide in dna_str:
        if nucleotide not in dna_to_binary:
            raise ValueError(f"Invalid nucleotide: {nucleotide}")
        binary += dna_to_binary[nucleotide]

    return binary

def text_to_actg(text):
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
            # Pad with zeros to make it 7 bits
            chunk_7bit = chunk_7bit.ljust(7, '0')

        # Encode 7-bit to 8-bit using the hardcoded mapping
        binary_8bit += encoding_map[chunk_7bit]

    # Convert to ACTG (every 2 bits becomes 1 nucleotide)
    actg = binary_to_actg(binary_8bit)

    return actg

def actg_to_text(actg):
    """
    Converts ACTG DNA sequence back to text using 8-bit to 7-bit decoding.
    """
    # Convert ACTG to binary
    binary_8bit = actg_to_binary(actg)

    # Ensure binary length is multiple of 8
    if len(binary_8bit) % 8 != 0:
        raise ValueError("Encoded binary length must be a multiple of 8 bits.")

    # Convert 8-bit chunks to 7-bit chunks
    binary_7bit = ''
    for i in range(0, len(binary_8bit), 8):
        chunk_8bit = binary_8bit[i:i+8]
        if chunk_8bit in decoding_map:
            binary_7bit += decoding_map[chunk_8bit]
        else:
            # Handle invalid 8-bit chunks
            st.warning(f"Invalid 8-bit chunk detected: {chunk_8bit}")
            # Skip this chunk or use a placeholder
            binary_7bit += '0000000'  # Placeholder for invalid chunks

    # Convert 7-bit chunks to characters
    text = ''
    for i in range(0, len(binary_7bit), 7):
        chunk_7bit = binary_7bit[i:i+7]
        if len(chunk_7bit) < 7:
            break  # Incomplete chunk at the end, ignore

        if chunk_7bit in bin7_to_char:
            text += bin7_to_char[chunk_7bit]
        else:
            st.warning(f"Invalid 7-bit chunk detected: {chunk_7bit}")
            text += '?'  # Replace with a question mark

    return text

def gc_content(seq):
    """
    Calculates the GC content percentage of a DNA sequence.
    """
    if not seq:
        return 0.0

    gc_count = seq.count('G') + seq.count('C')
    return (gc_count / len(seq)) * 100.0

def check_triple_nucleotides(seq):
    """
    Checks a DNA sequence for the presence of triple nucleotides (AAA, CCC, TTT, GGG).
    Returns a dictionary with counts and positions of each triple nucleotide.
    """
    result = {}
    patterns = ['AAA', 'CCC', 'TTT', 'GGG']

    for pattern in patterns:
        # Find all occurrences of the pattern
        occurrences = []
        start_pos = 0

        while True:
            pos = seq.find(pattern, start_pos)
            if pos == -1:
                break
            occurrences.append(pos)
            start_pos = pos + 1  # Overlap allowed

        result[pattern] = {
            'count': len(occurrences),
            'positions': occurrences
        }

    # Calculate total number of triple nucleotides
    result['total_count'] = sum(result[pattern]['count'] for pattern in patterns)

    return result

# Streamlit UI
st.title("Text to DNA (ACTG) Encoder/Decoder")

# Create tabs for encoding and decoding
tab1, tab2 = st.tabs(["Encode Text to DNA", "Decode DNA to Text"])

with tab1:
    st.header("Text to DNA Conversion")
    
    # Text input for encoding
    user_input = st.text_area("Enter your text to encode:", height=150)
    
    if st.button("Encode to DNA"):
        if user_input:
            try:
                # Encode the text to ACTG
                actg_sequence = text_to_actg(user_input)
                
                # Display the encoded DNA sequence
                st.subheader("Encoded DNA Sequence")
                st.code(actg_sequence)
                
                # Display sequence length
                st.info(f"Sequence length: {len(actg_sequence)} nucleotides")
                
                # Calculate and display GC content
                gc = gc_content(actg_sequence)
                st.metric("GC Content", f"{gc:.2f}%")
                
                # Check for triple nucleotides
                triple_check = check_triple_nucleotides(actg_sequence)
                
                st.subheader("Triple Nucleotide Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Triple Repeats", triple_check['total_count'])
                    
                with col2:
                    # Create a simple bar chart for triple nucleotide counts
                    import matplotlib.pyplot as plt
                    import numpy as np
                    
                    patterns = ['AAA', 'CCC', 'TTT', 'GGG']
                    counts = [triple_check[p]['count'] for p in patterns]
                    
                    fig, ax = plt.subplots()
                    bars = ax.bar(patterns, counts)
                    
                    # Add count labels on top of bars
                    for bar, count in zip(bars, counts):
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                str(count), ha='center', va='bottom')
                    
                    ax.set_ylabel('Count')
                    ax.set_title('Triple Nucleotide Distribution')
                    
                    st.pyplot(fig)
                
                # Display detailed positions of triple nucleotides if any were found
                if triple_check['total_count'] > 0:
                    st.subheader("Detailed Triple Nucleotide Positions")
                    for pattern in patterns:
                        count = triple_check[pattern]['count']
                        positions = triple_check[pattern]['positions']
                        
                        if count > 0:
                            with st.expander(f"{pattern}: {count} occurrences"):
                                st.write(f"Positions: {positions}")
                
            except ValueError as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter some text to encode.")

with tab2:
    st.header("DNA to Text Conversion")
    
    # DNA input for decoding
    dna_input = st.text_area("Enter DNA sequence to decode (ACTG only):", height=150)
    
    if st.button("Decode to Text"):
        if dna_input:
            # Validate input (only ACTG allowed)
            if not all(n in 'ACTG' for n in dna_input):
                st.error("Invalid DNA sequence. Only characters A, C, T, and G are allowed.")
            else:
                try:
                    # Decode the DNA to text
                    decoded_text = actg_to_text(dna_input)
                    
                    # Display the decoded text
                    st.subheader("Decoded Text")
                    st.text_area("Decoded result:", value=decoded_text, height=150, disabled=True)
                    
                except ValueError as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a DNA sequence to decode.")

# Add an "About" section
with st.expander("About this App"):
    st.write("""
    This app converts text to DNA sequences and vice versa using a specialized encoding technique:
    
    1. **Text to 7-bit Binary**: Each character is converted to a 7-bit binary representation.
    2. **7-bit to 8-bit Conversion**: The 7-bit sequences are encoded to 8-bit sequences using a specialized mapping.
    3. **Binary to DNA**: Every 2 bits are converted to a DNA nucleotide (A, C, T, G).
    
    The encoding is designed to optimize for DNA storage properties such as balanced GC content
    and minimized homopolymer runs (AAA, CCC, TTT, GGG).
    
    To use the app:
    - Enter text in the "Encode" tab to convert it to a DNA sequence
    - Enter a DNA sequence (ACTG only) in the "Decode" tab to convert it back to text
    
    Note: Special characters outside the supported character set cannot be encoded.
    """)