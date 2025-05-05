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
    # Additional 64 characters for full 7-bit mapping
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

def load_7bit_to_8bit_mapping(csv_filename='7to8.csv'):
    """
    Loads the 7-bit to 8-bit mapping from the CSV file.
    Returns the mapping as a dictionary.
    """
    encoding_map = {}
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            if len(row) == 2:
                encoding_map[row[0]] = row[1]

    return encoding_map

# Create reverse mapping for decoding
def create_8bit_to_7bit_mapping(encoding_map):
    """
    Creates a reverse mapping from 8-bit to 7-bit binary.
    """
    return {v: k for k, v in encoding_map.items()}

# Binary to ACTG conversion function
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

# ACTG to binary conversion function
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

# Encoding pipeline: Text -> 7-bit binary -> 8-bit binary -> ACTG
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
            # Pad with zeros to make it 7 bits
            chunk_7bit = chunk_7bit.ljust(7, '0')

        # Encode 7-bit to 8-bit using the mapping from CSV
        binary_8bit += encoding_map[chunk_7bit]

    # Convert to ACTG (every 2 bits becomes 1 nucleotide)
    actg = binary_to_actg(binary_8bit)

    return actg

# Decoding pipeline: ACTG -> 8-bit binary -> 7-bit binary -> Text
def actg_to_text(actg, decoding_map):
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
            print(f"Warning: Invalid 8-bit chunk detected: {chunk_8bit}")
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
            print(f"Warning: Invalid 7-bit chunk detected: {chunk_7bit}")
            text += '?'  # Replace with a question mark

    return text

# Calculate GC content
def gc_content(seq):
    """
    Calculates the GC content percentage of a DNA sequence.
    """
    if not seq:
        return 0.0

    gc_count = seq.count('G') + seq.count('C')
    return (gc_count / len(seq)) * 100.0

# Split into chunks for analysis
def split_into_chunks(seq, chunk_size):
    """
    Splits a sequence into chunks of specified size.
    """
    return [seq[i:i+chunk_size] for i in range(0, len(seq), chunk_size)]

# Check for triple nucleotides
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

# Main function to demonstrate the encoding/decoding process
def main():
    # Load the 7-bit to 8-bit mapping from the CSV file
    encoding_map = load_7bit_to_8bit_mapping('7to8.csv')
    decoding_map = create_8bit_to_7bit_mapping(encoding_map)

    # Example usage
    input_text = "Hello World! This is a DNA encoding test."
    print(f"Original text: '{input_text}'")

    # Encode text to ACTG
    actg_sequence = text_to_actg(input_text, encoding_map)
    print("\nEncoded ACTG sequence:")
    print(actg_sequence)

    # Analyze GC content
    gc = gc_content(actg_sequence)
    print(f"\nGC content: {gc:.2f}%")

    # Check for triple nucleotides
    triple_check = check_triple_nucleotides(actg_sequence)
    print("\n=== TRIPLE NUCLEOTIDE CHECK ===")
    print(f"Total triple nucleotides found: {triple_check['total_count']}")
    for pattern in ['AAA', 'CCC', 'TTT', 'GGG']:
        count = triple_check[pattern]['count']
        if count > 0:
            positions = triple_check[pattern]['positions']
            print(f"- {pattern}: {count} occurrences at positions {positions}")
        else:
            print(f"- {pattern}: No occurrences")

    # Decode ACTG back to text
    decoded_text = actg_to_text(actg_sequence, decoding_map)
    print(f"\nDecoded text: '{decoded_text}'")

    # Verify if decoding matches the original text
    print(f"Decoding successful: {decoded_text == input_text}")

if __name__ == "__main__":
    main()