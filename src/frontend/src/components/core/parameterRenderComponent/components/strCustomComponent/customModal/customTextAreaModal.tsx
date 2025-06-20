import IconComponent from "@/components/common/genericIconComponent";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import BaseModal from "@/modals/baseModal";
import { classNames } from "@/utils/utils";
import React, { ReactNode, useEffect, useRef, useState } from "react";

interface CustomTextAreaModalProps {
  value: string;
  setValue: (value: string) => void;
  children: ReactNode;
  disabled?: boolean;
  readonly?: boolean;
  onCloseModal?: () => void;
}

interface FormData {
  name: string;
  type: string;
  description: string;
  value: string;
}

const FIELD_TYPES = [
  { value: "string", label: "String" },
  { value: "number", label: "Number" },
  {
    value: "boolean",
    label: "Boolean",
  },
  { value: "array", label: "Array" },
  { value: "object", label: "Object" },
];

export default function CustomTextAreaModal({
  value,
  setValue,
  children,
  disabled = false,
  readonly = false,
  onCloseModal,
}: CustomTextAreaModalProps): React.ReactElement {
  const [modalOpen, setModalOpen] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    name: "",
    type: "string",
    description: "",
    value: "",
  });

  const nameRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (modalOpen) {
      // Try to parse an existing value if it's JSON
      try {
        if (value && value.trim()) {
          const parsed = JSON.parse(value);
          if (typeof parsed === "object" && parsed !== null) {
            setFormData({
              name: parsed.name || "",
              type: parsed.type || "string",
              description: parsed.description || "",
              value: parsed.value || "",
            });
          }
        }
      } catch {
        // If not valid JSON, reset to default
        setFormData({
          name: "",
          type: "string",
          description: "",
          value: "",
        });
      }
    }
  }, [value, modalOpen]);

  useEffect(() => {
    if (!modalOpen) {
      onCloseModal?.();
    }
  }, [modalOpen, onCloseModal]);

  const handleInputChange = (field: keyof FormData, newValue: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: newValue,
    }));
  };

  const handleSave = () => {
    const jsonOutput = JSON.stringify(formData);
    setValue(jsonOutput);
    setModalOpen(false);
  };

  const handleReset = () => {
    setFormData({
      name: "",
      type: "string",
      description: "",
      value: "",
    });
  };

  return (
    <BaseModal
      onChangeOpenModal={() => {}}
      open={modalOpen}
      setOpen={setModalOpen}
      size="large"
    >
      <BaseModal.Trigger disable={disabled} asChild>
        {children}
      </BaseModal.Trigger>
      <BaseModal.Header>
        <div className="flex w-full items-start gap-3">
          <div className="flex">
            <IconComponent
              name="Settings"
              className="h-6 w-6 pr-1 text-primary"
              aria-hidden="true"
            />
            <span className="pl-2" data-testid="custom-modal-title">
              Configure JSON Input
            </span>
          </div>
        </div>
      </BaseModal.Header>
      <BaseModal.Content>
        <div className="flex h-full w-full flex-col gap-4 p-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="field-name">Field Name</Label>
              <Input
                id="field-name"
                ref={nameRef}
                placeholder="Enter field name"
                value={formData.name}
                onChange={(e) => handleInputChange("name", e.target.value)}
                disabled={readonly}
                data-testid="field-name-input"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="field-type">Field Type</Label>
              <Select
                value={formData.type}
                onValueChange={(value) => handleInputChange("type", value)}
                disabled={readonly}
              >
                <SelectTrigger id="field-type" data-testid="field-type-select">
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  {FIELD_TYPES.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="field-description">Description</Label>
            <Input
              id="field-description"
              placeholder="Enter field description"
              value={formData.description}
              onChange={(e) => handleInputChange("description", e.target.value)}
              disabled={readonly}
              data-testid="field-description-input"
            />
          </div>

          <div className="flex-1 space-y-2">
            <Label htmlFor="field-value">Value</Label>
            <Textarea
              id="field-value"
              className={classNames(
                "h-full min-h-[200px] resize-none",
                "focus-visible:ring-1",
              )}
              placeholder="Enter field value"
              value={formData.value}
              onChange={(e) => handleInputChange("value", e.target.value)}
              readOnly={readonly}
              data-testid="field-value-textarea"
            />
          </div>

          <div className="rounded-md bg-muted p-3">
            <Label className="text-sm font-medium">Preview JSON:</Label>
            <pre className="mt-2 text-xs text-muted-foreground">
              {JSON.stringify(formData, null, 2)}
            </pre>
          </div>
        </div>
      </BaseModal.Content>
      <BaseModal.Footer>
        <div className="flex w-full shrink-0 items-end justify-between">
          <Button
            variant="outline"
            onClick={handleReset}
            disabled={readonly}
            data-testid="reset-button"
          >
            Reset
          </Button>
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => setModalOpen(false)}
              data-testid="cancel-button"
            >
              Cancel
            </Button>
            <Button
              onClick={handleSave}
              disabled={readonly}
              data-testid="save-button"
            >
              Save JSON
            </Button>
          </div>
        </div>
      </BaseModal.Footer>
    </BaseModal>
  );
}
