import redis
import os


# Redis configurations
redis_server = os.environ['REDIS']

# Redis Connection
try:
    if "REDIS_PWD" in os.environ:
        rd_oci = redis.StrictRedis(host=redis_server,
                                   port=6379,
                                   password=os.environ['REDIS_PWD'])
    else:
        rd_oci = redis.Redis(redis_server)
    rd_oci.ping()
except redis.ConnectionError:
    exit('Failed to connect to Redis, terminating.')

rd_aws_ip = ""
rd_azure_ip = ""
rd_gcp_ip = ""

rd_aws = redis.StrictRedis(host='rd_aws_ip', port=6379, db=0)
rd_azure = redis.StrictRedis(host='rd_azure_ip', port=6379, db=0)
rd_gcp = redis.StrictRedis(host='rd_gcp_ip', port=6379, db=0)
