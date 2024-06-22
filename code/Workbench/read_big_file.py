import gzip

# Define the path to the gzipped GAF file
file_path = '/data_link/servilla/SPOT2/data/goa_uniprot_all.gaf.gz'

# Initialize a counter for annotations
annotation_count = 0


def process_chunk(lines):
    """Process a chunk of lines and return the count of valid annotations."""
    count = 0
    for line in lines:
        if not line.startswith('!'):
            count += 1
    return count


# Read the file in chunks
with gzip.open(file_path, 'rt') as f:
    chunk_size = 100000  # Number of lines per chunk
    while True:
        lines = list(f.readlines(chunk_size))
        if not lines:
            break
        annotation_count += process_chunk(lines)

print(f"Number of annotations: {annotation_count}")
