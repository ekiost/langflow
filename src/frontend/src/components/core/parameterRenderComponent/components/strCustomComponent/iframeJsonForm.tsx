import React, {forwardRef} from "react";

interface IframeJsonFormProps {
    ref: React.Ref<HTMLIFrameElement>;
    modal?: string | undefined;
    setIsIframeLoading?: (loading: boolean) => void;
}

/**
 * A simple component that renders an iframe and forwards a ref to it.
 * It is styled to fit within the modal content area.
 */
const IframeJsonForm = forwardRef<HTMLIFrameElement, IframeJsonFormProps>((props, ref) => {
    const get_iframe_source = () => {
        switch (props.modal) {
            default:
                return "/json-form-page.html"
        }
    }

    return (<iframe
        ref={ref}
        src={get_iframe_source()}
        title="JSON Configuration Form"
        style={{
            width: "100%", height: "100%",
        }}
        onLoad={() => {
            // console.log("Iframe loaded");
            props.setIsIframeLoading?.(false);
        }}
    />);
},);

IframeJsonForm.displayName = "IframeJsonForm";

export default IframeJsonForm;