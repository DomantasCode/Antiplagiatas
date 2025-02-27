import re
import hashlib
from collections import deque

# Winnowing parameters (adjustable)
KGRAM_SIZE = 5  # Size of the k-grams (code chunks)
WINDOW_SIZE = 4  # Size of the rolling window


def preprocess_code(file_path):
    """ Read and preprocess source code (remove comments, normalize spaces). """
    with open(file_path, 'r', encoding="utf-8") as file:
        code = file.read()

    # Remove C++ comments
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.S)
    code = re.sub(r'\s+', ' ', code).strip()  # Normalize spaces
    return code


def generate_kgrams(text, k):
    """ Generate k-grams from the input text. """
    return [text[i:i + k] for i in range(len(text) - k + 1)]


def hash_kgram(kgram):
    """ Hash function for k-grams (returns a fingerprint). """
    return hashlib.md5(kgram.encode()).hexdigest()[-6:]  # Take last 6 hex digits


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


def compute_similarity(file1, file2):
    """ Compare two files using Moss-like winnowing technique. """
    text1 = preprocess_code(file1)
    text2 = preprocess_code(file2)

    kgrams1 = generate_kgrams(text1, KGRAM_SIZE)
    kgrams2 = generate_kgrams(text2, KGRAM_SIZE)

    hashes1 = [hash_kgram(kgram) for kgram in kgrams1]
    hashes2 = [hash_kgram(kgram) for kgram in kgrams2]

    fingerprints1 = winnow_hashes(hashes1, WINDOW_SIZE)
    fingerprints2 = winnow_hashes(hashes2, WINDOW_SIZE)

    common_hashes = fingerprints1.intersection(fingerprints2)
    similarity = (len(common_hashes) / max(len(fingerprints1), len(fingerprints2))) * 100

    return similarity


# Example usage
file1 = "test1.cpp"
file2 = "test2.cpp"

similarity_score = compute_similarity(file1, file2)
print(f"Code Similarity: {similarity_score:.2f}%")
