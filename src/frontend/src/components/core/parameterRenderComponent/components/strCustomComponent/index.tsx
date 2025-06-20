import { InputProps, StrRenderComponentType } from "../../types";
import CustomTextAreaComponent from "./customTextAreaComponent";

export function StrCustomComponent({
  templateData,
  name,
  display_name,
  placeholder,
  nodeId,
  nodeClass,
  handleNodeClass,
  modal,
  ...baseInputProps
}: InputProps<string, StrRenderComponentType>) {
  const { handleOnNewValue, id, isToolMode } = baseInputProps;

  return (
    <CustomTextAreaComponent
      {...baseInputProps}
      updateVisibility={() => {
        if (templateData.password !== undefined) {
          handleOnNewValue(
            { password: !templateData.password },
            { skipSnapshot: true },
          );
        }
      }}
      id={`textarea_${id}`}
      isToolMode={isToolMode}
      modal={modal}
    />
  );
}
