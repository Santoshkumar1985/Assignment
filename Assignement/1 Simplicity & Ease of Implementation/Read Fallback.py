\\ Read Fallback ( your existing service)

try:
    return cosmos.read(id)
except CosmosResourceNotFoundError:
    uri = table.get("billing", id).Uri
    return json.loads(gzip.decompress(blob.download(id+".json.gz")))
