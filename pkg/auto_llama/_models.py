from typing import Any, TypeVar, Type, cast, Callable

T = TypeVar("T")


class _ModelLoader:
    """Add larger ai models and provide them as singleton to reduce RAM/VRAM usage"""

    _models: dict[str, Any] = {}
    _lazy: dict[str, Callable] = {}

    def add(self, name: str, lazy_loader: Callable):
        """Add new model.

        Raises ValueError if model with this name already exists
        """

        if self._lazy.get(name, None):
            raise ValueError(f"Model with name '{name}' already exists")

        self._lazy[name] = lazy_loader

    def get(self, name: str, py_type: Type[T] = Any) -> T:
        """Get the model singleton with the given name.

        Raises KeyError if model doesn't exist.
        """

        if not self._models.get(name, None):
            loader = self._lazy.get(name, None)

            if not loader:
                raise KeyError(f"Model with name '{name}' doesn't exist")

            self._models[name] = loader()

        return cast(py_type, self._models[name])

    def drop(self, name: str, py_type: Type[T] = Any) -> T:
        """Drop the model singleton with the given name.

        Raises KeyError if model doesn't exist.
        """

        loader = self._lazy.pop(name, None)
        model = self._models.pop(name, None)

        if not loader:
            raise KeyError(f"Model with name '{name}' doesn't exist")

        if not model:
            model = loader()

        return cast(py_type, model)


ModelLoader = _ModelLoader()
"""Add larger ai models and provide them as singleton to reduce RAM/VRAM usage"""
