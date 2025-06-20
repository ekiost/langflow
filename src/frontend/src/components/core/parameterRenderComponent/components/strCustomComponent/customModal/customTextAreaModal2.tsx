import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import BaseModal from "@/modals/baseModal";
import { ReactNode, useEffect, useState } from "react";

interface CustomTextAreaModal2Props {
  children: ReactNode;
  value: string;
  setValue: (value: string) => void;
  disabled?: boolean;
  readonly?: boolean;
}

export default function CustomTextAreaModal2({
  children,
  value,
  setValue,
  disabled = false,
  readonly = false,
}: CustomTextAreaModal2Props) {
  const [isOpen, setIsOpen] = useState(false);
  const [tempValue, setTempValue] = useState(value || "");
  const [activeTab, setActiveTab] = useState("editor");
  const [findText, setFindText] = useState("");
  const [replaceText, setReplaceText] = useState("");

  useEffect(() => {
    if (isOpen) {
      setTempValue(value || "");
    }
  }, [value, isOpen]);

  const handleSubmit = () => {
    setValue(tempValue);
    setIsOpen(false);
  };

  // Advanced text manipulation functions
  const handleFindReplace = () => {
    if (findText) {
      const newValue = tempValue.replaceAll(findText, replaceText);
      setTempValue(newValue);
    }
  };

  const formatAsJSON = () => {
    try {
      const parsed = JSON.parse(tempValue);
      setTempValue(JSON.stringify(parsed, null, 2));
    } catch (error) {
      console.error("Invalid JSON format");
    }
  };

  const formatAsCSV = () => {
    const lines = tempValue.split("\n").filter((line) => line.trim());
    const formatted = lines
      .map((line) =>
        line
          .split(",")
          .map((cell) => cell.trim())
          .join(", "),
      )
      .join("\n");
    setTempValue(formatted);
  };

  const addLineNumbers = () => {
    const lines = tempValue.split("\n");
    const numbered = lines
      .map((line, index) => `${index + 1}. ${line}`)
      .join("\n");
    setTempValue(numbered);
  };

  const removeLineNumbers = () => {
    const lines = tempValue.split("\n");
    const unnumbered = lines
      .map((line) => line.replace(/^\d+\.\s*/, ""))
      .join("\n");
    setTempValue(unnumbered);
  };

  // Text analysis
  const getAdvancedStats = (text: string) => {
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const characters = text.length;
    const charactersNoSpaces = text.replace(/\s/g, "").length;
    const lines = text.split("\n").length;
    const paragraphs = text.split(/\n\s*\n/).filter((p) => p.trim()).length;
    const sentences = text.split(/[.!?]+/).filter((s) => s.trim()).length;

    return {
      words,
      characters,
      charactersNoSpaces,
      lines,
      paragraphs,
      sentences,
    };
  };

  const stats = getAdvancedStats(tempValue);

  return (
    <BaseModal open={isOpen} setOpen={setIsOpen} size="x-large">
      <BaseModal.Trigger disable={disabled} asChild>
        {children}
      </BaseModal.Trigger>

      <BaseModal.Header description="Advanced text editor with comprehensive tools for editing, formatting, and analysis">
        <div className="flex w-full items-center justify-between">
          <span>Advanced Text Editor</span>
          <Badge variant="secondary" className="text-xs">
            Modal Type: CustomTextAreaModal2
          </Badge>
        </div>
      </BaseModal.Header>

      <BaseModal.Content>
        <Tabs
          value={activeTab}
          onValueChange={setActiveTab}
          className="flex flex-1 flex-col"
        >
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="editor">Editor</TabsTrigger>
            <TabsTrigger value="tools">Tools</TabsTrigger>
            <TabsTrigger value="format">Format</TabsTrigger>
            <TabsTrigger value="stats">Statistics</TabsTrigger>
          </TabsList>

          <TabsContent value="editor" className="flex flex-1 flex-col">
            <div className="flex flex-1 flex-col gap-4">
              <Textarea
                value={tempValue}
                onChange={(e) => setTempValue(e.target.value)}
                placeholder="Enter your advanced text here..."
                className="min-h-[400px] flex-1 resize-none font-mono text-sm"
                disabled={disabled}
                readOnly={readonly}
              />
            </div>
          </TabsContent>

          <TabsContent value="tools" className="flex flex-1 flex-col gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Find & Replace</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <Label htmlFor="find">Find</Label>
                    <Input
                      id="find"
                      value={findText}
                      onChange={(e) => setFindText(e.target.value)}
                      placeholder="Text to find..."
                    />
                  </div>
                  <div>
                    <Label htmlFor="replace">Replace with</Label>
                    <Input
                      id="replace"
                      value={replaceText}
                      onChange={(e) => setReplaceText(e.target.value)}
                      placeholder="Replacement text..."
                    />
                  </div>
                </div>
                <Button
                  onClick={handleFindReplace}
                  size="sm"
                  disabled={!findText}
                >
                  Replace All
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Text Transformations</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-2">
                  <Button variant="outline" size="sm" onClick={addLineNumbers}>
                    Add Line Numbers
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={removeLineNumbers}
                  >
                    Remove Line Numbers
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() =>
                      setTempValue(tempValue.split("\n").reverse().join("\n"))
                    }
                  >
                    Reverse Lines
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() =>
                      setTempValue(tempValue.split("\n").sort().join("\n"))
                    }
                  >
                    Sort Lines
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="format" className="flex flex-1 flex-col gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Format Options</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-2">
                  <Button variant="outline" size="sm" onClick={formatAsJSON}>
                    Format as JSON
                  </Button>
                  <Button variant="outline" size="sm" onClick={formatAsCSV}>
                    Format as CSV
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() =>
                      setTempValue(tempValue.replace(/\s+/g, " ").trim())
                    }
                  >
                    Normalize Whitespace
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() =>
                      setTempValue(tempValue.replace(/^\s+|\s+$/gm, ""))
                    }
                  >
                    Trim Lines
                  </Button>
                </div>
              </CardContent>
            </Card>

            <div className="flex-1">
              <Label>Preview</Label>
              <div className="mt-2 max-h-[300px] min-h-[200px] overflow-auto rounded-md border bg-muted/50 p-3">
                <pre className="whitespace-pre-wrap font-mono text-xs">
                  {tempValue}
                </pre>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="stats" className="flex flex-1 flex-col gap-4">
            <div className="grid grid-cols-2 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Basic Statistics</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex justify-between">
                    <span>Words:</span>
                    <Badge variant="outline">{stats.words}</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span>Characters:</span>
                    <Badge variant="outline">{stats.characters}</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span>Characters (no spaces):</span>
                    <Badge variant="outline">{stats.charactersNoSpaces}</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span>Lines:</span>
                    <Badge variant="outline">{stats.lines}</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Advanced Statistics</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex justify-between">
                    <span>Paragraphs:</span>
                    <Badge variant="outline">{stats.paragraphs}</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span>Sentences:</span>
                    <Badge variant="outline">{stats.sentences}</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span>Avg. words/sentence:</span>
                    <Badge variant="outline">
                      {stats.sentences > 0
                        ? Math.round(stats.words / stats.sentences)
                        : 0}
                    </Badge>
                  </div>
                  <div className="flex justify-between">
                    <span>Avg. chars/word:</span>
                    <Badge variant="outline">
                      {stats.words > 0
                        ? Math.round(stats.charactersNoSpaces / stats.words)
                        : 0}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="flex-1">
              <CardHeader>
                <CardTitle className="text-sm">Text Analysis</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  <div>
                    <strong>Reading time:</strong> ~
                    {Math.ceil(stats.words / 200)} minutes
                  </div>
                  <div>
                    <strong>Speaking time:</strong> ~
                    {Math.ceil(stats.words / 150)} minutes
                  </div>
                  <div>
                    <strong>Typing time (40 WPM):</strong> ~
                    {Math.ceil(stats.words / 40)} minutes
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
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
