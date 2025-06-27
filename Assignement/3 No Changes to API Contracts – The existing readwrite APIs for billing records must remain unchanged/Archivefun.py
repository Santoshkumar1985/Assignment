\\ ARCHIVE FUNCTION
cutoff = now() - 90 days
for each record in COSMOS where _ts < cutoff:
  blobName = record.id + ".json.gz"
  upload blobContainer/blobName ← gzip(serialize(record))
  tableStorage.upsert(PartitionKey="billing", RowKey=record.id, Uri=blobUrl)
  cosmos.delete(record.id)        # only after successful blob+index write
