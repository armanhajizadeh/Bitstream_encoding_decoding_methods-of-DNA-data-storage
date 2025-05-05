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