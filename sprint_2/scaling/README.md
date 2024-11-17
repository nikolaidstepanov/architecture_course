# How to:

1. Run containers: `docker compose up -d`
2. Init MongoDB replication:
    - `docker exec -it mongodb1 mongosh`
    - `rs.initiate({_id: "rs0", members: [{_id: 0, host: "mongodb1:27017"},{_id: 1, host: "mongodb2:27018"},{_id: 2, host: "mongodb3:27019"}]})`
3. Run Redis cluster:
    - `docker exec -it redis_1`
    - `echo "yes" | redis-cli --cluster create   173.17.0.2:6379   173.17.0.3:6379   173.17.0.4:6379   173.17.0.5:6379   173.17.0.6:6379   173.17.0.7:6379   --cluster-replicas 1`
    - `redis-cli cluster nodes`
