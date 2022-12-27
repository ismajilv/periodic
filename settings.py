from decouple import config

KAFKA_BOOTSTRAP_SERVERS = config("KAFKA_BOOTSTRAP_SERVERS", default="localhost:29092", cast=str)
KAFKA_TOPIC = config("KAFKA_TOPIC", default="mytopic", cast=str)
KAFKA_CA_CERT_FULL_PATH = config("KAFKA_CA_CERT_FULL_PATH", default=None, cast=str)
KAFKA_CLIENT_KEY_FULL_PATH = config("KAFKA_CLIENT_KEY_FULL_PATH", default=None, cast=str)
KAFKA_CLIENT_CERT_FULL_PATH = config("KAFKA_CLIENT_CERT_FULL_PATH", default=None, cast=str)
KAFKA_SECURITY_PROTOCOL = config("KAFKA_SECURITY_PROTOCOL", default=None, cast=str)

DB_DSN = config("DB_DSN", default="postgresql://postgres:postgres@localhost:65432/postgres", cast=str)
