import IconComponent from "@/components/common/genericIconComponent";
import {Button} from "@/components/ui/button";
import BaseModal from "@/modals/baseModal";
import React, {ReactNode, useEffect, useRef, useState} from "react";
import IframeJsonForm from "./iframeJsonForm"; // Import the new iframe component

interface CustomTextAreaModalProps {
    value: string;
    setValue: (value: string) => void;
    children: ReactNode;
    disabled?: boolean;
    readonly?: boolean;
    onCloseModal?: () => void;
    modal: string | undefined;
}

// For security, specify the origin of the iframe's content.
// If served from the same domain, this is correct. For external domains,
// use the specific origin (e.g., "https://forms.example.com").
const IFRAME_ORIGIN = window.location.origin;

/*
  IMPORTANT: The page hosted at IFRAME_SRC (`/json-form-page.html`) needs to
  implement the other side of this communication channel.

  The iframe's JavaScript should:
  1. Listen for messages from this parent window.
     window.addEventListener('message', (event) => {
       // Verify the message is from the expected parent origin
       if (event.origin !== IFRAME_ORIGIN) return;

       const { type, payload } = event.data;
       if (type === 'load') {
         // Use payload to populate the form fields
         // e.g., document.getElementById('name').value = payload.name;
       } else if (type === 'reset') {
         // Clear all form fields
       }
     });

  2. Send messages back to the parent window.
     // After its own scripts have loaded, tell the parent it's ready
     window.parent.postMessage({ type: 'ready' }, IFRAME_ORIGIN);

     // On save, send the form data
     const formData = { name: '...', type: '...', description: '...', value: '...' };
     window.parent.postMessage({ type: 'save', payload: formData }, IFRAME_ORIGIN);

     // On cancel, just notify the parent
     window.parent.postMessage({ type: 'cancel' }, IFRAME_ORIGIN);
*/

export default function CustomTextAreaModal({
                                                value,
                                                setValue,
                                                children,
                                                disabled = false,
                                                readonly = false,
                                                onCloseModal,
                                                modal,
                                            }: CustomTextAreaModalProps): React.ReactElement {
    const [modalOpen, setModalOpen] = useState(false);
    const [isIframeReady, setIsIframeReady] = useState(false);
    const iframeRef = useRef<HTMLIFrameElement>(null);

    // Effect to handle messages received from the iframe
    useEffect(() => {
        const handleMessage = (event: MessageEvent) => {
            if (event.origin !== IFRAME_ORIGIN) return;

            const data = event.data;
            if (!data || typeof data.type !== "string") return;

            switch (data.type) {
                case "ready":
                    setIsIframeReady(true);
                    break;
                case "save":
                    handleSave(data.payload);
                    break;
                case "cancel":
                    setModalOpen(false);
                    break;
            }
        };

        if (modalOpen) {
            window.addEventListener("message", handleMessage);
        }

        return () => {
            window.removeEventListener("message", handleMessage);
            setIsIframeReady(false); // Reset on close
        };
    }, [modalOpen]);

    // Effect to send the initial data to the iframe once it's ready
    useEffect(() => {
        if (modalOpen && isIframeReady && iframeRef.current?.contentWindow) {
            try {
                const initialData = value && value.trim() ? JSON.parse(value) : {};
                iframeRef.current.contentWindow.postMessage(
                    {type: "load", payload: initialData},
                    IFRAME_ORIGIN,
                );
            } catch (e) {
                console.error("Failed to parse initial value for iframe:", e);
                iframeRef.current.contentWindow.postMessage(
                    {type: "load", payload: {}},
                    IFRAME_ORIGIN,
                );
            }
        }
    }, [modalOpen, isIframeReady, value]);

    useEffect(() => {
        if (!modalOpen) {
            onCloseModal?.();
        }
    }, [modalOpen, onCloseModal]);

    const handleSave = (formData: any) => {
        const jsonOutput = JSON.stringify(formData, null, 2); // Pretty-print JSON
        setValue(jsonOutput);
        setModalOpen(false);
    };

    const handleReset = () => {
        if (iframeRef.current?.contentWindow) {
            iframeRef.current.contentWindow.postMessage(
                {type: "reset"},
                IFRAME_ORIGIN,
            );
        }
    };

    return (
        <BaseModal
            onChangeOpenModal={() => {
            }}
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
              Configure Input
            </span>
                    </div>
                </div>
            </BaseModal.Header>
            <BaseModal.Content>
                <IframeJsonForm ref={iframeRef} modal={modal}/>
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
                            onClick={() =>
                                iframeRef.current?.contentWindow?.postMessage(
                                    {type: "requestSave"}, // Ask iframe to save
                                    IFRAME_ORIGIN,
                                )
                            }
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