from typing import Optional

from loguru import logger

from flowchem.components.stdlib import Pump


class DummyPump(Pump):
    """
    A fake pumping device whose primary feature is that it moves fluid, used internally for testing.

    ::: warning
    Users should not instantiate a `DummyPump` for use in a `Protocol` because it is not an actual lab instrument.
    :::

    Arguments:
    - `name`: The name of the pump.

    Attributes:
    - `name` (`str`): The name of the pump.
    - `rate` (`pint.Quantity`): The flow rate of the pump. Must be of the dimensionality of volume/time.
    """

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

    async def _update(self):
        logger.trace(f"Set {self} rate to {self.rate}")
