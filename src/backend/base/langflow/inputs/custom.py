import warnings
from typing import Any

from pydantic import Field, field_validator, BaseModel

from langflow.inputs.input_mixin import BaseInputMixin, MultilineMixin, MetadataTraceMixin, SerializableFieldTypes, \
    FieldTypes
from langflow.inputs.validators import CoalesceBool


class ModalMixin(BaseModel):
    modal: str | None = Field(default=None)
    """Specifies which modal component to use. Defaults to None."""


class CustomInput(BaseInputMixin, MultilineMixin, MetadataTraceMixin, ModalMixin):
    """Represents a textarea input field that duplicates TEXT field type behavior.

    This class uses the TEXTAREA field type which has the same "str" value as TEXT,
    but allows for different frontend handling if needed.

    Attributes:
        field_type (SerializableFieldTypes): The type of the field. Defaults to FieldTypes.TEXTAREA.
        multiline (CoalesceBool): Indicates whether the input field should support multiple lines. Defaults to True.
    """

    field_type: SerializableFieldTypes = FieldTypes.TEXT
    multiline: CoalesceBool = True
    copy_field: CoalesceBool = False

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: Any, info):
        """Validates the given value and returns the processed value.

        Args:
            v (Any): The value to be validated.
            info: Additional information about the input.

        Returns:
            The processed value.

        Raises:
            ValueError: If the value is not of a valid type.
        """
        if not isinstance(v, str) and v is not None:
            if info.data.get("input_types") and v.__class__.__name__ not in info.data.get("input_types"):
                warnings.warn(f"Invalid value type {type(v)} for input {info.data.get('name')}. "
                              f"Expected types: {info.data.get('input_types')}", stacklevel=4, )
            else:
                warnings.warn(f"Invalid value type {type(v)} for input {info.data.get('name')}.", stacklevel=4, )
        return v
