import React, { forwardRef } from "react";
import iframeSources from "/home/victor/Programming/dev_langflow/langflow/src/frontend/public/iframeSources.json"; // Import the sources for the iframes

interface IframeJsonFormProps {
  ref: React.Ref<HTMLIFrameElement>;
  modal?: string | undefined;
  setIsIframeLoading?: (loading: boolean) => void;
}

/**
 * A simple component that renders an iframe and forwards a ref to it.
 * It is styled to fit within the modal content area.
 */
const IframeJsonForm = forwardRef<HTMLIFrameElement, IframeJsonFormProps>(
  (props, ref) => {
    const get_iframe_source = () => {
      // Create switch statements depending on what the user defined
      // switch (props.modal) {
      //     case "website-1":
      //         return "/json-form-page.html";
      //     case "website-2":
      //         return "/json-form-page-2.html";
      //     default:
      //         return props.modal;
      // }
      // Use mapping from JSON, fallback to props.modal if not found
      return props.modal && iframeSources[props.modal]
        ? iframeSources[props.modal]
        : props.modal;
    };

    return (
      <iframe
        ref={ref}
        src={get_iframe_source()}
        title="JSON Configuration Form"
        style={{
          width: "100%",
          height: "100%",
        }}
        onLoad={() => {
          // console.log("Iframe loaded");
          props.setIsIframeLoading?.(false);
        }}
      />
    );
  },
);

IframeJsonForm.displayName = "IframeJsonForm";

export default IframeJsonForm;
