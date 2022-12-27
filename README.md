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
- Improve this documentation so that it is more enjoyable to read
