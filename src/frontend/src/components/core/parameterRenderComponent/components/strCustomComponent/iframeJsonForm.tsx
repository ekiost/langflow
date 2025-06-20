import React, {forwardRef} from "react";

interface IframeJsonFormProps {
    // The URL of the page to be loaded in the iframe.
    src: string;
}

/**
 * A simple component that renders an iframe and forwards a ref to it.
 * It is styled to fit within the modal content area.
 */
const IframeJsonForm = forwardRef<HTMLIFrameElement, IframeJsonFormProps>(
    ({src}, ref) => {
        return (
            <iframe
                ref={ref}
                src={src}
                title="JSON Configuration Form"
                style={{
                    width: "100%",
                    height: "100%",
                }}
            />
        );
    },
);

IframeJsonForm.displayName = "IframeJsonForm";

export default IframeJsonForm;