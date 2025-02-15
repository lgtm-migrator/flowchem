from typing import Optional

from flowchem.components.properties import ActiveComponent


class Dummy(ActiveComponent):
    """
    A fake component, used internally for testing.

    ::: warning
    This component *can* be used in a non-dry run protocol execution. It does not do anything.
    :::

    Arguments:
    - `name`: The component's name.

    Attributes:
    - `name`: The component's name.
    - `active`: Whether the component is active. This doesn't actually mean anything.
    """

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)
        self.active = False

        self._base_state = dict(active=False)

    async def _update(self) -> None:
        if self.active:
            print("Active!")
        else:
            print("Inactive.")
