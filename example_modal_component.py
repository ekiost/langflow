from langflow.custom import Component
from langflow.io import Output
from langflow.inputs import CustomInput
from langflow.schema import Data


class ModalExampleComponent(Component):
    """Example component demonstrating how to use CustomInput with different modal types."""

    display_name = "Modal Example Component"
    description = "Demonstrates using CustomInput with different modal components for various text editing needs"
    icon = "textarea"
    name = "ModalExample"

    inputs = [
        CustomInput(
            name="basic_text",
            display_name="Basic Text Input",
            info="Uses the default CustomTextAreaModal for simple text editing",
            placeholder="Enter your basic text here...",
            value="",
            helper_text="This uses the standard modal with basic editing features"
        ),
        CustomInput(
            name="enhanced_text",
            display_name="Enhanced Text Input",
            info="Uses CustomTextAreaModal1 with text statistics and formatting tools",
            placeholder="Enter text for enhanced editing...",
            value="",
            modal="CustomTextAreaModal1",
            helper_text="This modal provides word count, character count, and quick formatting options"
        ),
        CustomInput(
            name="advanced_text",
            display_name="Advanced Text Input",
            info="Uses CustomTextAreaModal2 with advanced editing features",
            placeholder="Enter text for advanced editing...",
            value="",
            modal="CustomTextAreaModal2",
            helper_text="This modal includes find/replace, format validation, and detailed text analysis"
        ),
        CustomInput(
            name="json_data",
            display_name="JSON Data",
            info="Perfect for JSON editing with CustomTextAreaModal2's format validation",
            placeholder='{"example": "JSON data"}',
            value='{\n  "name": "example",\n  "type": "json",\n  "valid": true\n}',
            modal="CustomTextAreaModal2",
            helper_text="Use the Format tab to validate and prettify JSON"
        ),
        CustomInput(
            name="content_writing",
            display_name="Content Writing",
            info="Ideal for content creation with CustomTextAreaModal1's text statistics",
            placeholder="Write your content here...",
            value="",
            modal="CustomTextAreaModal1",
            helper_text="Track word count and reading time while writing"
        )
    ]

    outputs = [
        Output(display_name="Processed Output", name="output", method="process_texts"),
        Output(display_name="Text Analysis", name="analysis", method="analyze_texts"),
        Output(display_name="Combined Text", name="combined", method="combine_texts"),
    ]

    def process_texts(self) -> Data:
        """Process all text inputs and return structured data."""

        basic = self.basic_text or ""
        enhanced = self.enhanced_text or ""
        advanced = self.advanced_text or ""
        json_data = self.json_data or ""
        content = self.content_writing or ""

        # Try to parse JSON if provided
        parsed_json = None
        try:
            import json
            if json_data.strip():
                parsed_json = json.loads(json_data)
        except json.JSONDecodeError:
            parsed_json = {"error": "Invalid JSON format"}

        result_data = {
            "basic_text": basic,
            "enhanced_text": enhanced,
            "advanced_text": advanced,
            "json_data": parsed_json,
            "content_writing": content,
            "processing_timestamp": self._get_current_timestamp(),
            "modal_types_used": {
                "basic_text": "default",
                "enhanced_text": "CustomTextAreaModal1",
                "advanced_text": "CustomTextAreaModal2",
                "json_data": "CustomTextAreaModal2",
                "content_writing": "CustomTextAreaModal1"
            }
        }

        return Data(
            data=result_data,
            text=f"Processed {len([t for t in [basic, enhanced, advanced, json_data, content] if t])} text inputs"
        )

    def analyze_texts(self) -> Data:
        """Analyze all text inputs and provide statistics."""

        texts = {
            "basic": self.basic_text or "",
            "enhanced": self.enhanced_text or "",
            "advanced": self.advanced_text or "",
            "json_data": self.json_data or "",
            "content": self.content_writing or ""
        }

        analysis = {}
        total_stats = {"words": 0, "characters": 0, "lines": 0}

        for name, text in texts.items():
            if text:
                words = len(text.split()) if text.strip() else 0
                characters = len(text)
                lines = len(text.split('\n'))

                analysis[name] = {
                    "words": words,
                    "characters": characters,
                    "lines": lines,
                    "has_content": bool(text.strip())
                }

                total_stats["words"] += words
                total_stats["characters"] += characters
                total_stats["lines"] += lines

        analysis["total"] = total_stats
        analysis["reading_time_minutes"] = max(1, total_stats["words"] // 200)
        analysis["speaking_time_minutes"] = max(1, total_stats["words"] // 150)

        return Data(
            data=analysis,
            text=f"Analysis: {total_stats['words']} words, {total_stats['characters']} characters across {len([t for t in texts.values() if t])} inputs"
        )

    def combine_texts(self) -> Data:
        """Combine all text inputs into a single formatted output."""

        sections = []

        if self.basic_text:
            sections.append(f"=== BASIC TEXT ===\n{self.basic_text}")

        if self.enhanced_text:
            sections.append(f"=== ENHANCED TEXT ===\n{self.enhanced_text}")

        if self.advanced_text:
            sections.append(f"=== ADVANCED TEXT ===\n{self.advanced_text}")

        if self.json_data:
            sections.append(f"=== JSON DATA ===\n{self.json_data}")

        if self.content_writing:
            sections.append(f"=== CONTENT WRITING ===\n{self.content_writing}")

        combined_text = "\n\n".join(sections) if sections else "No text inputs provided"

        return Data(
            data={"combined_content": combined_text, "section_count": len(sections)},
            text=combined_text
        )

    def _get_current_timestamp(self) -> str:
        """Get current timestamp for processing metadata."""
        from datetime import datetime
        return datetime.now().isoformat()


# Example of how to create a specialized component for specific use cases
class JSONEditorComponent(Component):
    """Specialized component for JSON editing using the advanced modal."""

    display_name = "JSON Editor"
    description = "Specialized JSON editor with validation and formatting"
    icon = "braces"
    name = "JSONEditor"

    inputs = [
        CustomInput(
            name="json_input",
            display_name="JSON Data",
            info="JSON editor with validation and formatting tools",
            placeholder='{\n  "key": "value"\n}',
            value='{\n  "example": "data",\n  "array": [1, 2, 3],\n  "nested": {\n    "property": true\n  }\n}',
            modal="CustomTextAreaModal2",
            helper_text="Use the Format tab to validate and prettify JSON. The Tools tab provides find/replace functionality."
        )
    ]

    outputs = [
        Output(display_name="Validated JSON", name="output", method="validate_json"),
        Output(display_name="JSON Info", name="info", method="get_json_info"),
    ]

    def validate_json(self) -> Data:
        """Validate and return the JSON data."""
        import json

        json_text = self.json_input or ""

        try:
            if not json_text.strip():
                return Data(data=None, text="No JSON data provided")

            parsed = json.loads(json_text)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)

            return Data(
                data=parsed,
                text=formatted
            )
        except json.JSONDecodeError as e:
            return Data(
                data={"error": f"Invalid JSON: {str(e)}"},
                text=f"JSON Validation Error: {str(e)}"
            )

    def get_json_info(self) -> Data:
        """Get information about the JSON structure."""
        import json

        json_text = self.json_input or ""

        try:
            if not json_text.strip():
                return Data(data={"info": "No JSON data"}, text="No JSON data provided")

            parsed = json.loads(json_text)

            def analyze_json(obj, path=""):
                """Recursively analyze JSON structure."""
                info = {"type": type(obj).__name__, "path": path}

                if isinstance(obj, dict):
                    info["keys"] = list(obj.keys())
                    info["key_count"] = len(obj)
                elif isinstance(obj, list):
                    info["length"] = len(obj)
                    info["item_types"] = list(set(type(item).__name__ for item in obj))
                elif isinstance(obj, str):
                    info["length"] = len(obj)

                return info

            structure_info = analyze_json(parsed)

            return Data(
                data={
                    "structure": structure_info,
                    "is_valid": True,
                    "character_count": len(json_text),
                    "formatted_size": len(json.dumps(parsed, indent=2))
                },
                text=f"Valid JSON with {structure_info.get('key_count', 'N/A')} top-level keys"
            )

        except json.JSONDecodeError as e:
            return Data(
                data={
                    "structure": None,
                    "is_valid": False,
                    "error": str(e),
                    "character_count": len(json_text)
                },
                text=f"Invalid JSON: {str(e)}"
            )
