while ! cqlsh -e 'describe cluster' cassandra 9042; do
    echo 'Waiting for Cassandra to be available...'
    sleep 2
done
echo "Cassandra is up! Initializing keyspace and tables..."
cqlsh -f /opt/cassandra-init/init.cql cassandra 9042
