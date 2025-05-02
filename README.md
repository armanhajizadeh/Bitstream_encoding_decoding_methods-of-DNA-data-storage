# Bitstream_encoding_decoding_methods-of-DNA-data-storage

Q: How can we encode and decode information with DNA under these constraints?

No triple A, C, T, or G.

GC content must be between 25% and 75%.

In the first step, we encode 7-bit ASCII (128 combinations) into an 8-bit binary format (256 combinations) while enforcing the constraints. We filter out any of the 256 binary states that contain triple A/C/T/G, and also exclude those starting or ending with two identical nucleotides to prevent triple repetition when characters are joined. Next, we calculate the GC content and keep only the binary codes with GC content between 25% and 75%. This results in 130 valid 8-bit binary states that meet all constraints.

<h1><img src="https://github.com/armanhajizadeh/Bitstream_encoding_decoding_methods-of-DNA-data-storage/blob/main/Screenshot%202025-05-02%20at%2018.44.46.png"
></h1>

Future: Can this bitstream encoding be implemented using logic circuits with full combinatorics (AND, OR, NOT, XOR)?

