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

export default function CustomTextAreaModal3({
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
  const [isRickRollMode, setIsRickRollMode] = useState(false);

  const nameRef = useRef<HTMLInputElement>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);

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

  const toggleRickRollMode = () => {
    const newRickRollMode = !isRickRollMode;
    setIsRickRollMode(newRickRollMode);

    // Dynamically modify the iframe's DOM
    if (iframeRef.current && iframeRef.current.contentWindow) {
      const iframeDoc =
        iframeRef.current.contentDocument ||
        iframeRef.current.contentWindow.document;
      const button = iframeDoc.querySelector(".toggle-btn");

      if (button === null) {
        return;
      }

      if (newRickRollMode) {
        // Change to Rick Roll mode
        button.textContent = "🎵 Click Me!";
        button.classList.add("rick-roll");

        // Replace the onclick handler
        button.onclick = function () {
          window.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "_blank");
        };
      } else {
        // Restore normal JSON toggle mode
        button.textContent = "Hide JSON";
        button.classList.remove("rick-roll");

        // Restore original toggle function
        button.onclick = function () {
          const example = iframeDoc.getElementById("jsonExample");
          const button = iframeDoc.querySelector(".toggle-btn");

          if (example.classList.contains("hidden")) {
            example.classList.remove("hidden");
            button.textContent = "Hide JSON";
          } else {
            example.classList.add("hidden");
            button.textContent = "Show JSON";
          }
        };

        // Show JSON when exiting rick roll mode
        const example = iframeDoc.getElementById("jsonExample");
        example.classList.remove("hidden");
      }
    }
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
          <div className="grid gap-4">
            <iframe
              ref={iframeRef}
              srcDoc={`
                <html>
                  <head>
                    <style>
                      body {
                        font-family: Arial, sans-serif;
                        margin: 16px;
                        background: #f8f9fa;
                        color: #333;
                      }
                      .header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        color: #2563eb;
                        margin-bottom: 12px;
                        font-size: 14px;
                        font-weight: bold;
                      }
                      .toggle-btn {
                        background: #2563eb;
                        color: white;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 4px;
                        font-size: 12px;
                        cursor: pointer;
                        transition: background-color 0.2s;
                      }
                      .toggle-btn:hover {
                        background: #1d4ed8;
                      }
                      .toggle-btn.rick-roll {
                        background: #dc2626;
                      }
                      .toggle-btn.rick-roll:hover {
                        background: #b91c1c;
                      }
                      .example {
                        background: white;
                        padding: 12px;
                        border-radius: 6px;
                        border: 1px solid #e5e7eb;
                        font-size: 12px;
                        display: block;
                      }
                      .example.hidden {
                        display: none;
                      }
                      pre {
                        margin: 0;
                        white-space: pre-wrap;
                        color: #374151;
                      }
                    </style>
                  </head>
                  <body>
                    <div class="header">
                      <span>JSON Schema Example:</span>
                      <button class="toggle-btn" onclick="toggleJson()">Hide JSON</button>
                    </div>
                    <div class="example" id="jsonExample">
                      <pre>{
  "name": "username",
  "type": "string",
  "description": "User's login name",
  "value": "john_doe"
}</pre>
                    </div>
                    <script>
                      function toggleJson() {
                        const example = document.getElementById('jsonExample');
                        const button = document.querySelector('.toggle-btn');

                        if (example.classList.contains('hidden')) {
                          example.classList.remove('hidden');
                          button.textContent = 'Hide JSON';
                        } else {
                          example.classList.add('hidden');
                          button.textContent = 'Show JSON';
                        }
                      }
                    </script>
                  </body>
                </html>
              `}
              width="100%"
              height="200"
              frameBorder="0"
              title="JSON Schema Preview"
              className="rounded-md border bg-gray-50"
            >
              <p>Your browser does not support iframes.</p>
            </iframe>
            <Button
              variant="outline"
              size="sm"
              onClick={toggleRickRollMode}
              className="mt-2"
              data-testid="rick-roll-toggle"
            >
              Magic Button to change the iframe DOM
            </Button>
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
