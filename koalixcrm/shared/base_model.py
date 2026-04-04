# -*- coding: utf-8 -*-
"""
Base DTO class for all koalixcrm client-side models.
Ported from qq_workflow_support_webapp_backend pattern.
"""
from typing import Dict, Any


class BaseModel:
    """Base class for all client-side models (DTOs)."""

    def __init__(self, data: Dict[str, Any]):
        self._data = data
        self._populate_from_data(data)

    def _populate_from_data(self, data: Dict[str, Any]):
        """Populate object attributes from data dictionary."""
        for key, value in data.items():
            if key != 'id':
                setattr(self, key, value)

    @property
    def id(self) -> int:
        return self._data.get('id')

    def __str__(self) -> str:
        if hasattr(self, 'name'):
            return self.name
        return f"{self.__class__.__name__}(id={self.id})"

    def _to_dict(self) -> Dict[str, Any]:
        """Recursively convert the object to a dictionary."""
        result = {
            '_class': self.__class__.__name__,
            '_module': self.__class__.__module__
        }
        for key, value in self.__dict__.items():
            if key == '_data':
                result['_data'] = value
                continue
            result[key] = self._convert_value(value)
        return result

    @staticmethod
    def _convert_value(value: Any) -> Any:
        """Recursively convert a value to a serializable form."""
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, list):
            return [BaseModel._convert_value(item) for item in value]
        if isinstance(value, dict):
            return {k: BaseModel._convert_value(v) for k, v in value.items()}
        if isinstance(value, BaseModel):
            return value._to_dict()
        return str(value)

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Recursively create an object from a dictionary."""
        if '_class' not in data or '_module' not in data:
            raise ValueError("Invalid dictionary format: missing '_class' or '_module'")

        class_name = data['_class']
        module_name = data['_module']

        if class_name == cls.__name__ and module_name == cls.__module__:
            instance_data = data.get('_data', {})
            instance = cls(instance_data)
            for key, value in data.items():
                if key not in ('_class', '_module', '_data'):
                    setattr(instance, key, cls._restore_value(value))
            return instance
        else:
            try:
                module = __import__(module_name, fromlist=[class_name])
                target_class = getattr(module, class_name)
                return target_class._from_dict(data)
            except (ImportError, AttributeError) as e:
                raise ValueError(f"Could not import class {class_name} from {module_name}: {e}")

    @classmethod
    def _restore_value(cls, value: Any) -> Any:
        """Recursively restore a value from its serialized form."""
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, list):
            return [cls._restore_value(item) for item in value]
        if isinstance(value, dict):
            if '_class' in value and '_module' in value:
                try:
                    module_name = value['_module']
                    class_name = value['_class']
                    module = __import__(module_name, fromlist=[class_name])
                    target_class = getattr(module, class_name)
                    return target_class._from_dict(value)
                except (ImportError, AttributeError):
                    return value
            else:
                return {k: cls._restore_value(v) for k, v in value.items()}
        return value
