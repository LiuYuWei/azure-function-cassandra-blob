# azure-function-cassandra-blob
Use azure function to query the data and store into the azure blob.

# How to use this?
```dockerfile
docker build -t="cassandra_azure_blob_function" .
docker run -d -p 8080:80 -it cassandra_azure_blob_function
```