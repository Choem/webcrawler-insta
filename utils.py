def chunk(data, size):
    chunks = list()
    for i in range(0, len(data), size):
        chunks.append(data[i:i+size])
    return chunks