\\ End - to End Flow Reads
try:
    return cosmos.read(id)
except NotFound:
    row = table.get(partition="billing", rowKey=id)
    blob_bytes = blob.download_blob( row["Uri"] )
    return json.loads(gzip.decompress(blob_bytes))
