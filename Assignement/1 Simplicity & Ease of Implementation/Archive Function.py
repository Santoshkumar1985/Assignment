
\\Archive Function  ( Tmer Trigger )
blob.upload(f"{id}.json.gz", gzip(json.dumps(data)))
table.upsert({ PartitionKey: "billing", RowKey: id, Uri: blobUrl })
cosmos.delete(id)
