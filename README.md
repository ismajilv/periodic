# Periodic

**Periodic** is periodically checking website availability over the network, producing metrics about this and passes these events through an
Kafka instance into an PostgreSQL database. For this purpose, there is Kafka producer which periodically checks the target websites
(could be many) and sends the check results to a Kafka topic, and a Kafka consumer storing the data to an PostgreSQL database. 
The website checker can perform the checks periodically and collect the HTTP  response time, status code returned, as well as 
optionally checking the returned page contents for a regexp pattern thatis expected to be found on the page.

[Table of Contents](#table-of-contents)
 - [Development](#development)
 - [Example usage](#example-usage)
 - [API Reference](#api-reference)
 - [DB Schema](#db-schema)
 - [Kafka Schema](#kafka-schema)
 - [License](#license)
 - [Feature requests and bugs](#feature-requests-and-bugs)


<a name="quickstart"></a>
## Development
- [x] There are unit, integration and e2e tests. They use real db and kafka instances running in docker containers. Github actions are integrated to run all these tests on every push to main branch. Other than that with GitHub actions code formatting and linting is also tested. 
- [x] There is a Makefile to use with GitHub actions and to setup the development environment.
- [x] All the main components are decoupled and can be run separately. DB writer uses single connection to write bulk data to the database.

Before running the code on your local machine please follow the steps below:
```python
make install_dependencies
make create_test_environment
make db_migration

# optionally
make test_unittest
make test_integration
make test_e2e

make delete_test_environment
```

### To run in production environment
Copy the .env.example file to .env and fill in the required values

<a name="example-usage"></a>
## Example usage
Example is also given in the root folder of the project. [example.py](example.py)

```python
import asyncio

from src.periodic import PeriodicChecker
from src.entities import PeriodicCheckerInput


async def main():
    inputs_ = [
        PeriodicCheckerInput(
            site='http://www.google.com',
            period=60
        )
    ]
    
    await PeriodicChecker().start(periodic_checker_inputs=inputs_)


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
```
**Logs**

```python
INFO:src.producer.uptime_checker:Checking https://www.google.com
INFO:aiokafka.consumer.group_coordinator:Metadata for topic has changed from {} to {'mytopic': 1}. 
INFO:src.producer.uptime_checker:Site https://www.google.com is up
INFO:src.producer.kafka_producer:Producing b'{"site": "https://www.google.com", "up": true, "downtime_reason": null, "response_duration": 0.37, "checked_at": "2022-12-27T21:24:09.922928"}' to mytopic
INFO:src.consumer.kafka_consumer:Consuming message ConsumerRecord(topic='mytopic', partition=0, offset=43, timestamp=1672176249923, timestamp_type=0, key=None, value=b'{"site": "https://www.google.com", "up": true, "downtime_reason": null, "response_duration": 0.37, "checked_at": "2022-12-27T21:24:09.922928"}', checksum=None, serialized_key_size=-1, serialized_value_size=142, headers=()) from Kafka
INFO:src.consumer.db_writer:Successfully inserted all messages from queue to DB
```

<a name="api-reference"></a>
## API reference
```text
src.periodic.PeriodicChecker(site: str, regexp: Optional[str] = None, status_code: Optional[str] = None, period: Optional[int] = 10)
Arguments:
    site (str): The website to check
    regexp (Optional[str]): The regexp pattern to search for on the page
    status_code (Optional[str]): The expected HTTP status code
    period (Optional[int]): The period in seconds to check the website
```

<a name="db-schema"></a>
## DB schema
```text
periodic (
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("site", sa.String(255), nullable=False),
    sa.Column("up", sa.BOOLEAN, nullable=True),
    sa.Column("downtime_reason", sa.String, nullable=True),
    sa.Column("response_duration", sa.Float, nullable=True),
    sa.Column("checked_at", sa.DateTime, nullable=False),
);
```

<a name="kafka-schema"></a>
## Kafka schema
```text
{
    "site": "http://www.google.com",
    "up": true,
    "downtime_reason": null,
    "response_duration": 0.123,
    "checked_at": "2021-05-01 12:00:00"
}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)


<a name="feature-requests-and-bugs"></a>
## Feature requests and bugs
- Periodic jobs might be not too precisely periodic due to asyncio nature
- Create interface to have each DB client implementing its own interface
- Postgres is hardcoded in the alembic uri. Make it configurable
- Make logging level configurable
- Improve this documentation so that it is more enjoyable to read
