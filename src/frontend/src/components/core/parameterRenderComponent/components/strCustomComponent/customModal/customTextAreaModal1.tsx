import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import BaseModal from "@/modals/baseModal";
import { ReactNode, useEffect, useState } from "react";

interface CustomTextAreaModal1Props {
  children: ReactNode;
  value: string;
  setValue: (value: string) => void;
  disabled?: boolean;
  readonly?: boolean;
}

export default function CustomTextAreaModal1({
  children,
  value,
  setValue,
  disabled = false,
  readonly = false,
}: CustomTextAreaModal1Props) {
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

  // Helper function to count words and characters
  const getTextStats = (text: string) => {
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const characters = text.length;
    const lines = text.split("\n").length;
    return { words, characters, lines };
  };

  const stats = getTextStats(tempValue);

  return (
    <BaseModal open={isOpen} setOpen={setIsOpen} size="large">
      <BaseModal.Trigger disable={disabled} asChild>
        {children}
      </BaseModal.Trigger>

      <BaseModal.Header description="Enhanced text editor with statistics and formatting tools">
        <div className="flex w-full items-center justify-between">
          <span>Enhanced Text Editor</span>
          <Badge variant="secondary" className="text-xs">
            Modal Type: CustomTextAreaModal1
          </Badge>
        </div>
      </BaseModal.Header>

      <BaseModal.Content className="gap-4">
        {/* Text Statistics Card */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Text Statistics</CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex gap-4 text-sm text-muted-foreground">
              <span>Words: {stats.words}</span>
              <span>Characters: {stats.characters}</span>
              <span>Lines: {stats.lines}</span>
            </div>
          </CardContent>
        </Card>

        {/* Main Text Area */}
        <div className="flex flex-1 flex-col">
          <Textarea
            value={tempValue}
            onChange={(e) => setTempValue(e.target.value)}
            placeholder="Enter your text here..."
            className="min-h-[300px] flex-1 resize-none font-mono text-sm"
            disabled={disabled}
            readOnly={readonly}
          />
        </div>

        {/* Quick Actions */}
        <div className="flex flex-wrap gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setTempValue(tempValue.toUpperCase())}
            disabled={disabled || readonly}
          >
            TO UPPERCASE
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setTempValue(tempValue.toLowerCase())}
            disabled={disabled || readonly}
          >
            to lowercase
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setTempValue(tempValue.replace(/\s+/g, " ").trim())}
            disabled={disabled || readonly}
          >
            Clean Whitespace
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setTempValue("")}
            disabled={disabled || readonly}
          >
            Clear All
          </Button>
        </div>
      </BaseModal.Content>

      <BaseModal.Footer
        submit={{
          label: "Save Changes",
          disabled: disabled,
          onClick: handleSubmit,
        }}
      />
    </BaseModal>
  );
}
