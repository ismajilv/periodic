# Periodic

**Periodic** is periodically checking website availability over the network, producing metrics about this and passes these events through an
Kafka instance into an PostgreSQL database. For this purpose, there is Kafka producer which periodically checks the target websites
(could be many) and sends the check results to a Kafka topic, and a Kafka consumer storing the data to an PostgreSQL database. 
The website checker can perform the checks periodically and collect the HTTP  response time, status code returned, as well as 
optionally checking the returned page contents for a regexp pattern thatis expected to be found on the page.

[Table of Contents](#table-of-contents)
 - [Example usage](#example-usage)
 - [API Reference](#api-reference)

<a name="example-usage"></a>
## Example usage
Example is also given in the root folder of the project. [example.py](example.py)

```python

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



