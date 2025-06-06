"""Test utilities."""


class FakeResponse:
    """Fake response object."""

    def __init__(self, data: str, status_code: int, exc: bool):
        """Fake init method."""
        self.text = data
        self.status_code = status_code
        self.exc = exc

    def raise_for_status(self):
        """Fake raise_for_status method."""
        if self.exc:
            raise RuntimeError()
