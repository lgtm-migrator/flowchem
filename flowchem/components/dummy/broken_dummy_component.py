from flowchem.components.dummy import Dummy


class BrokenDummyComponent(Dummy):
    """
    A fake component, used internally for testing. Its `_update()` method always returns `True` during a dry run but always returns `False` in a real run.

    ::: danger
    Using this component during real protocol execution will result in a failure.
    :::

    Arguments:
    - `name`: The name of the component.

    Attributes:
    - `active`: Whether the component is active. This doesn't actually mean anything.
    """

    def __init__(self, name=None):
        super().__init__(name=name)

    async def _update(self) -> None:
        if self.active:
            raise RuntimeError

    def _validate(self, dry_run):
        return True
