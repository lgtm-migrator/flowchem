import random
from typing import Optional

from flowchem.components.properties import Sensor


class DummySensor(Sensor):
    """A dummy sensor returning the number of times it has been read.

    ::: danger
    Don't use this in a real apparatus! It doesn't return real data.
    :::

    Attributes:
    - `name`: The component's name.
    - `rate`: Data collection rate in Hz as a `pint.Quantity`. A rate of 0 Hz corresponds to the sensor being off.
    """

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)
        self._unit = "Dimensionless"
        self.counter = 0.0

    async def _read(self) -> float:
        """Collect the data."""
        self.counter += (random.random() * 2) - 1
        return self.counter
