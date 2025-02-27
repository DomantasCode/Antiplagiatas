import re
import hashlib
import ast
import os
from collections import deque
from datasketch import MinHash, MinHashLSH  # MinHash + LSH for faster comparisons

# Winnowing parameters (adjustable)
KGRAM_SIZE = 5  # Size of the k-grams (code chunks)
WINDOW_SIZE = 4  # Size of the rolling window


def preprocess_code(file_path):
    """ Read and preprocess source code (remove comments, normalize spaces). """
    with open(file_path, 'r', encoding="utf-8") as file:
        code = file.read()

    # Remove C++ comments (single-line and multi-line)
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.S)
    code = re.sub(r'\s+', ' ', code).strip()  # Normalize spaces

    return code

int main()
def generate_kgrams(text, k):
    """ Generate k-grams from the input text. """
    return [text[i:i + k] for i in range(len(text) - k + 1)]


def hash_kgram(kgram):
    """ Hash function using SHA-256 (more secure than MD5) """
    return hashlib.sha256(kgram.encode()).hexdigest()[-8:]  # Take last 8 hex digits


def winnow_hashes(hashes, window_size):
    """ Winnowing: Selects representative fingerprints using a sliding window. """
    window = deque()
    fingerprints = set()

    for i, hash_val in enumerate(hashes):
        window.append((hash_val, i))

        # Maintain the window size
        if len(window) > window_size:
            window.popleft()

        # Select the minimum hash in the window
        if len(window) == window_size:
            min_hash = min(window, key=lambda x: x[0])
            fingerprints.add(min_hash[0])  # Store only hash values

    return fingerprints


### **NEW: MinHashing for Large-Scale Comparisons**
def compute_minhash(file_path):
    """ Create a MinHash fingerprint for a file """
    minhash = MinHash(num_perm=128)  # 128 permutations for higher accuracy
    with open(file_path, 'r', encoding="utf-8") as file:
        for word in file.read().split():
            minhash.update(word.encode('utf8'))  # Hashing each word

    return minhash


def compute_minhash_similarity(file1, file2):
    """ Compare two files using MinHash similarity """
    minhash1 = compute_minhash(file1)
    minhash2 = compute_minhash(file2)

    return minhash1.jaccard(minhash2) * 100  # Convert to percentage


### **NEW: LSH for Fast Comparisons**
def lsh_index_files(file_list, threshold=0.8):
    """ Index multiple files into an LSH table for fast similarity checking """
    lsh = MinHashLSH(threshold=threshold, num_perm=128)
    minhashes = {}

    for file in file_list:
        minhash = compute_minhash(file)
        lsh.insert(file, minhash)
        minhashes[file] = minhash

    return lsh, minhashes


def find_similar_files(file_list, threshold=0.8):
    """ Find similar files using LSH """
    lsh, minhashes = lsh_index_files(file_list, threshold)

    similar_pairs = []
    for file in file_list:
        similar_files = lsh.query(minhashes[file])  # Get similar files from LSH
        similar_pairs.append((file, similar_files))

    return similar_pairs


### **AST Parsing for Python**
def extract_ast_structure(file_path):
    """ Convert Python code into an Abstract Syntax Tree (AST) """
    with open(file_path, 'r', encoding="utf-8") as file:
        code = file.read()

    try:
        tree = ast.parse(code)
        return ast.dump(tree)  # Return AST as a string
    except SyntaxError:
        return ""  # If not valid Python code, return empty


def compute_ast_similarity(file1, file2):
    """ Compare AST structures to detect similarity """
    ast1 = extract_ast_structure(file1)
    ast2 = extract_ast_structure(file2)

    set1, set2 = set(ast1.split()), set(ast2.split())
    similarity = len(set1 & set2) / max(len(set1), len(set2)) * 100

    return similarity


def compute_similarity(file1, file2):
    """ Compare two files using MinHash (default), AST for Python, or Winnowing for C++ """
    if file1.endswith(".py") and file2.endswith(".py"):
        return compute_ast_similarity(file1, file2)

    return compute_minhash_similarity(file1, file2)


# Example usage
file1 = "test1.cpp"
file2 = "test2.cpp"

similarity_score = compute_similarity(file1, file2)
print(f"Code Similarity: {similarity_score:.2f}%")

# **Find Similar Files in a Folder**
file_list = ["test1.cpp", "test2.cpp", "test3.cpp"]
similar_files = find_similar_files(file_list)
print("\nSimilar File Groups:")
for file, matches in similar_files:
    print(f"{file} -> {matches}")
