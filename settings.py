from decouple import config

KAFKA_BOOTSTRAP_SERVERS = config("KAFKA_BOOTSTRAP_SERVERS", default="localhost:29092", cast=str)
KAFKA_TOPIC = config("KAFKA_TOPIC", default="mytopic", cast=str)
DB_DSN = config("DB_DSN", default="postgresql://postgres:postgres@localhost:65432/postgres", cast=str)
