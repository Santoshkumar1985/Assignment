\\ Read Path

function getBilling(id):
  try:
    return cosmos.read(id)          # hot data
  catch NotFound:
    uri = tableStorage.get("billing", id).Uri
    return deserialize(gunzip(blob.download(uri)))  # cold data
