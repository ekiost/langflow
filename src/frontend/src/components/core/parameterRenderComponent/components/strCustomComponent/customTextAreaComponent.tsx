import { GRADIENT_CLASS } from "@/constants/constants";
import { cn } from "@/utils/utils";
import React, { ChangeEvent, useMemo, useRef, useState } from "react";
import IconComponent from "../../../../common/genericIconComponent";
import { Input } from "../../../../ui/input";
import { getPlaceholder } from "../../helpers/get-placeholder-disabled";
import { InputProps, TextAreaComponentType } from "../../types";
import { getIconName } from "../inputComponent/components/helpers/get-icon-name";
import CustomTextAreaModal from "./customTextAreaModal";

const inputClasses = {
  base: ({ isFocused, password }: { isFocused: boolean; password: boolean }) =>
    `w-full ${isFocused ? "" : "pr-3"} ${password ? "pr-16" : ""}`,
  editNode: "input-edit-node",
  normal: ({ isFocused }: { isFocused: boolean }) =>
    `primary-input ${isFocused ? "text-primary" : "text-muted-foreground"}`,
  disabled: "disabled-state",
  password: "password",
};

const externalLinkIconClasses = {
  gradient: ({
    disabled,
    editNode,
    password,
  }: {
    disabled: boolean;
    editNode: boolean;
    password: boolean;
  }) =>
    disabled || password
      ? ""
      : editNode
        ? "gradient-fade-input-edit-node"
        : "gradient-fade-input",
  background: ({
    disabled,
    editNode,
  }: {
    disabled: boolean;
    editNode: boolean;
  }) =>
    disabled
      ? ""
      : editNode
        ? "background-fade-input-edit-node"
        : "background-fade-input",
  icon: "icons-parameters-comp absolute right-3 h-4 w-4 shrink-0",
  editNodeTop: "top-[-1.4rem] h-5",
  normalTop: "top-[-2.1rem] h-7",
  iconTop: "top-[-1.7rem]",
};

export default function CustomTextAreaComponent({
  value,
  disabled,
  handleOnNewValue,
  editNode = false,
  id = "",
  password,
  placeholder,
  isToolMode = false,
  modal,
}: InputProps<
  string,
  TextAreaComponentType & {
    modal?: string;
  }
>): React.ReactElement {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isFocused, setIsFocused] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);

  const displayValue = useMemo(() => {
    return value || "";
  }, [value]);

  const getInputClassName = () => {
    return cn(
      inputClasses.base({
        isFocused,
        password: password!,
      }),
      editNode ? inputClasses.editNode : inputClasses.normal({ isFocused }),
      disabled && inputClasses.disabled,
      password && !passwordVisible && "text-clip",
      isFocused && "pr-10",
    );
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    handleOnNewValue({ value: e.target.value });
  };

  // Function to get the appropriate modal component based on the modal prop
  const getModalComponent = () => {
    switch (modal) {
      default:
        return CustomTextAreaModal;
    }
  };

  const ModalComponent = getModalComponent();

  const renderIcon = () => (
    <div>
      {!disabled && !isFocused && (
        <div
          className={cn(
            externalLinkIconClasses.gradient({
              disabled,
              editNode,
              password: password!,
            }),
            editNode
              ? externalLinkIconClasses.editNodeTop
              : externalLinkIconClasses.normalTop,
          )}
          style={{
            pointerEvents: "none",
            background: isFocused
              ? undefined
              : disabled
                ? "bg-background"
                : GRADIENT_CLASS,
          }}
          aria-hidden="true"
        />
      )}

      <IconComponent
        dataTestId={`button_open_json_modal_${id}${editNode ? "_advanced" : ""}`}
        name={getIconName(disabled, "", "", false, isToolMode) || "Settings"}
        className={cn(
          "cursor-pointer bg-background",
          externalLinkIconClasses.icon,
          editNode
            ? externalLinkIconClasses.editNodeTop
            : externalLinkIconClasses.iconTop,
          disabled
            ? "bg-muted text-placeholder-foreground"
            : "bg-background text-foreground hover:text-primary",
        )}
      />
    </div>
  );

  return (
    <div className={cn("w-full", disabled && "pointer-events-none")}>
      <Input
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        id={id}
        data-testid={id}
        value={disabled ? "" : displayValue}
        onChange={handleInputChange}
        disabled={disabled}
        className={getInputClassName()}
        placeholder={getPlaceholder(
          disabled,
          placeholder || "Enter JSON string",
        )}
        aria-label={disabled ? displayValue : undefined}
        ref={inputRef}
        type={password ? (passwordVisible ? "text" : "password") : "text"}
        readOnly={false}
      />

      <ModalComponent
        value={value}
        setValue={(newValue) => handleOnNewValue({ value: newValue })}
        disabled={disabled}
        readonly={false}
      >
        <div className="relative w-full">{renderIcon()}</div>
      </ModalComponent>

      {password && !isFocused && (
        <div
          onClick={() => {
            setPasswordVisible(!passwordVisible);
          }}
        >
          <IconComponent
            name={passwordVisible ? "eye" : "eye-off"}
            className={cn(
              externalLinkIconClasses.icon,
              editNode ? "top-[5px]" : "top-[13px]",
              disabled
                ? "text-placeholder"
                : "text-placeholder-foreground hover:text-foreground",
              "right-10",
            )}
          />
        </div>
      )}
    </div>
  );
}
