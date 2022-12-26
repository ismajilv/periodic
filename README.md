producer
* periodic
* kafka producer

consumer
* kafka consumer
* db writer

postgresql
kafka

# API

```python
from periodic import Periodic

checks = [
    PeriodicHTTPCheck(
        site='http://example.com',
        period=60,
        regexp='.*',
        status_code="2**",
    )
]
periodic = Periodic(checks)
periodic._start()
```