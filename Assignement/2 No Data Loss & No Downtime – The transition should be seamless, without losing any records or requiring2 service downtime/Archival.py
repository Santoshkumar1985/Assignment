\\ Archival function
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobClient
from azure.data.tables import TableClient
import gzip, json, os

def main(mytimer: func.TimerRequest):
    cosmos = CosmosClient(os.getenv("COSMOS_URI"), os.getenv("COSMOS_KEY"))
    container = cosmos.get_container_client("billing")
    blob_container = BlobClient.from_connection_string(
        os.getenv("STORAGE_CONN"), container_name="billing-archive", blob_name=None
    )
    table = TableClient.from_connection_string(
        os.getenv("STORAGE_CONN"), table_name="BillingIndex"
    )

    cutoff = int((time.time() - 90*24*3600))
    query = f"SELECT c.id, c.data FROM c WHERE c._ts < {cutoff}"
    for item in container.query_items(query, enable_cross_partition_query=True):
        blob_name = f"{item['id']}.json.gz"
        data = gzip.compress(json.dumps(item["data"]).encode())
        blob_container.get_blob_client(blob_name).upload_blob(data, overwrite=True)
        table.upsert_entity({
            "PartitionKey": "billing",
            "RowKey": item["id"],
            "Uri": blob_container.url + "/" + blob_name
        })
        container.delete_item(item["id"], partition_key=item.get("pk", item["id"]))
