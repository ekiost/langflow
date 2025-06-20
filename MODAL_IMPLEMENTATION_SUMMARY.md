# Custom Modal Implementation Summary

## Overview

This document summarizes the implementation of the `ModalMixin` feature that allows specifying different modal
components for `CustomInput` fields in Langflow. This enables creating different modals in the frontend and lets users
specify which modal component to use for enhanced text editing experiences.

## Files Modified/Created

### Backend Changes

#### 1. `langflow/src/backend/base/langflow/inputs/input_mixin.py`

- **Added**: `ModalMixin` class with `modal` field

```python
class ModalMixin(BaseModel):
    modal: str | None = Field(default=None)
    """Specifies which modal component to use. Defaults to None."""
```

#### 2. `langflow/src/backend/base/langflow/inputs/inputs.py`

- **Modified**: Added `ModalMixin` to imports
- **Modified**: Updated `CustomInput` class to inherit from `ModalMixin`

```python
from .input_mixin import (
    # ... existing imports
    ModalMixin,
    # ... other imports
)


class CustomInput(BaseInputMixin, MultilineMixin, MetadataTraceMixin, ModalMixin):
    """Represents a textarea input field that duplicates TEXT field type behavior.

    This class uses the TEXTAREA field type which has the same "str" value as TEXT,
    but allows for different frontend handling if needed.

    Attributes:
        field_type (SerializableFieldTypes): The type of the field. Defaults to FieldTypes.TEXT.
        multiline (CoalesceBool): Indicates whether the input field should support multiple lines. Defaults to True.
        modal (str | None): Specifies which modal component to use. Defaults to None.
    """

    field_type: SerializableFieldTypes = FieldTypes.TEXT
    multiline: CoalesceBool = True
    copy_field: CoalesceBool = False
```

#### 3. `langflow/src/backend/base/langflow/inputs/__init__.py`

- **Added**: `CustomInput` to imports and exports

```python
from .inputs import (
    # ... existing imports
    CustomInput,
    # ... other imports
)

__all__ = [
    # ... existing imports
    "CustomInput",
    # ... other imports
]
```

### Frontend Changes

#### 1. `langflow/src/frontend/src/components/core/parameterRenderComponent/types.ts`

- **Added**: `modal` property to `StrRenderComponentType`
- **Added**: `modal` property to `TextAreaComponentType`

```typescript
export type StrRenderComponentType = {
    // ... existing properties
    modal?: string;
};

export type TextAreaComponentType = {
    // ... existing properties
    modal?: string;
};
```

#### 2. `langflow/src/frontend/src/components/core/parameterRenderComponent/index.tsx`

- **Modified**: Changed CustomInput detection from `_input_type` check to modal property presence
- **Modified**: Added `modal` property to `StrCustomComponent` call

```typescript
// Check for modal property presence and route to StrCustomComponent
if (templateData.modal !== undefined) {
    return (
        <StrCustomComponent
            // ... existing props
            modal = {templateData.modal}
    />
)
    ;
}
```

#### 3. `langflow/src/frontend/src/components/core/parameterRenderComponent/components/strCustomComponent/`

- **Added**: Complete directory structure for custom components:
    - `index.tsx` - Main StrCustomComponent that routes to CustomTextAreaComponent
    - `customTextAreaComponent.tsx` - Component that handles modal selection and rendering
    - `customTextAreaModal.tsx` - Default modal with JSON configuration features

## Implementation Details

### Adding New Modal
To add a new modal component to the system, follow these steps:

#### Step 1: Create the Modal Component

Create a new modal component file in the `strCustomComponent` directory:

```typescript
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import BaseModal from "@/modals/baseModal";
import { ReactNode, useEffect, useState } from "react";

interface CustomTextAreaModal3Props {
  children: ReactNode;
  value: string;
  setValue: (value: string) => void;
  disabled?: boolean;
  readonly?: boolean;
}

export default function CustomTextAreaModal3({
  children,
  value,
  setValue,
  disabled = false,
  readonly = false,
}: CustomTextAreaModal3Props) {
  const [isOpen, setIsOpen] = useState(false);
  const [tempValue, setTempValue] = useState(value || "");

  useEffect(() => {
    if (isOpen) {
      setTempValue(value || "");
    }
  }, [value, isOpen]);

  const handleSubmit = () => {
    setValue(tempValue);
    setIsOpen(false);
  };

  return (
    <BaseModal open={isOpen} setOpen={setIsOpen} size="medium">
      <BaseModal.Trigger disable={disabled} asChild>
        {children}
      </BaseModal.Trigger>

      <BaseModal.Header description="Your custom modal description">
        <div className="flex w-full items-center justify-between">
          <span>Your Custom Modal Title</span>
          <Badge variant="secondary" className="text-xs">
            Modal Type: CustomTextAreaModal3
          </Badge>
        </div>
      </BaseModal.Header>

      <BaseModal.Content>
        {/* Your custom modal content here */}
        <Textarea
          value={tempValue}
          onChange={(e) => setTempValue(e.target.value)}
          placeholder="Enter your text here..."
          className="min-h-[200px] resize-none"
          disabled={disabled}
          readOnly={readonly}
        />
      </BaseModal.Content>

      <BaseModal.Footer
        submit={{
          label: "Save",
          disabled: disabled,
          onClick: handleSubmit,
        }}
      />
    </BaseModal>
  );
}
```

#### Step 2: Update the Modal Selection Logic

Update the `getModalComponent` function in `customTextAreaComponent.tsx`:

```typescript
// Update the switch statement to include your new modal
const getModalComponent = () => {
  switch (modal) {
    case "CustomTextAreaModal1":
      return CustomTextAreaModal1;
    case "CustomTextAreaModal2":
      return CustomTextAreaModal2;
    case "CustomTextAreaModal3":
      return CustomTextAreaModal3;
    default:
      return CustomTextAreaModal;
  }
};
```

#### Step 3: Use the New Modal in Your Component

Use the new modal in your backend component:

```python
from langflow.custom import Component
from langflow.inputs import CustomInput
from langflow.io import Output

class MyComponent(Component):
    display_name = "My Component"
    description = "Component with custom modal"

    inputs = [
        CustomInput(
            name="my_input",
            display_name="My Input",
            info="Input with custom modal",
            modal="CustomTextAreaModal3"  # Specify your modal name
        )
    ]

    outputs = [
        Output(display_name="Output", name="output", method="process")
    ]

    def process(self):
        return self.my_input
```
