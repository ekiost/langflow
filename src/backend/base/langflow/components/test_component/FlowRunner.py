import ast
from typing import List, Any, Dict
from loguru import logger

from langflow.custom import Component
from langflow.graph.graph.base import Graph
from langflow.helpers.flow import get_flow_inputs

from langflow.inputs.inputs import (
    DropdownInput,
    MessageTextInput,
    CustomInput
)
from langflow.schema import Data, dotdict
from langflow.template import Output

from langflow.test.Flow import Flow
from langflow.test.FlowAPI import FlowAPI
from langflow.helpers.flow import run_flow
from langflow.base.flow_processing.utils import build_data_from_run_outputs

def merge_string_to_dict(string: str, dict: Dict) -> Dict:
    """
    Parses a JSON-like string into a dictionary and merges it with another dictionary.

    Args:
    string (str): String to convert into a dictionary.
    dict (Dict): Dictionary to merge into.

    Returns:
    Dict: Merged dictionary.

    Raises:
    RuntimeError: If the string cannot be safely parsed.
    """

    # attempt to convert string into Dictionary structure
    try:
        string_dict = ast.literal_eval(string)
    except Exception as e:
        #msg = f"Error converting string input to dict: " + string
        #logger.exception(msg + "string:" + string)
        
        # Cast to string
        string_dict = {"Response": string}
        # raise RuntimeError(msg) from e

    # merge dicts
    dict = string_dict | dict
    return dict


class FlowRunner(Component):
    display_name = "Flow Runner (Upgraded)"
    description = "Component to run multiple flows sequentially.\n Removes invalid and duplicate flows to run."
    documentation: str = "https://docs.langflow.org/components-custom-components"
    icon = "code"
    name = "CustomComponent"
    flow_name_selected = ""
    validated_flows: List[str] = []
    icon = "FAISS"
    
    class DemoClass():
        def something(self):
            return True
    
    
    demo = DemoClass()
    
    inputs = [
        MessageTextInput(
            name="input_value",
            display_name="Flows to Run",
            info="This is input accepts only valid flows that exist in the LangFlow server. \n Removes inputs that are invalid Flows or duplicate Flows.",
            value=["Test Flow"],
            is_list=True,
            tool_mode=True,
            real_time_refresh=True,
            input_types=[],
        ),
        DropdownInput(
            name="mode",
            display_name="On Error:",
            options=["Cascade", "Break"],
            value="Cascade",
            dynamic=True,
            advanced=True,
            info="On Error, either continue to cascade the flows or break the flows from running."
        ),
        MessageTextInput(
            name="flow_value",
            display_name="Flow Input",
            value="",
            dynamic=True,
            real_time_refresh=True,
            info="."
        ),
        MessageTextInput(
            name="retries",
            display_name="Retry Count",
            value=["0"],
            dynamic=True,
            is_list=True,
            info=".",
            advanced=True,
        ),
        CustomInput(
            name="flows",
            display_name="Popup Form",
            modal="json-form-page.html",
            info="Click here to input Flows to run",
            dynamic=True,
            real_time_refresh=True)
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    
    async def get_flow_names(self) -> list[str]:
        """
        Retrieves the list of all available flow names on the Langflow server.

        Returns:
            list[str]: A list of flow names.
        """
        flow_data = await self.alist_flows()
        return [flow_data.data["name"] for flow_data in flow_data]
        

    async def get_flow(self, flow_name_selected: str) -> Data | None:
        """
        Fetches a specific flow's data by name.

        Args:
            flow_name_selected (str): The name of the flow.

        Returns:
            Data | None: The flow's data if found, otherwise None.
        """
        flow_datas = await self.alist_flows()
        for flow_data in flow_datas:
            if flow_data.data["name"] == flow_name_selected:
                self.log(flow_data, "Flow Data:")
                return flow_data
                
        return None


    # Function to take in Flow inputs as a List and return only Flows that exist in LangFlow without duplicates
    async def validate_flows(self, flows_input: List):
        """
       Filters and returns only valid, unique flow names from the user input.

       Args:
       flows_input (List): List of user-specified flow names.

       Returns:
       List: Validated list of unique flow names.
       """
        validated_flows = []
        valid_flows = await self.get_flow_names()

        # If the flow input is valid or still empty
        for i, flow in enumerate(flows_input):
            is_last = i == len(flows_input) -1
            
            if (flow in valid_flows) and (flow not in validated_flows):
                # if the flow input is not already in the validated_flows
                validated_flows.append(flow)
            #if flow == "" and is_last:
            #    validated_flows.append("")
    
        return validated_flows
    
    async def validate_flow(self, flow: str) -> str:
        valid_flows = await self.get_flow_names()
        return flow if flow in valid_flows else ""
        
    async def get_value_from_str_dict(self, str_dict: str, key: str) -> str:
        parsed_dict = None
        try:
            # Convert the string to a dictionary
            if isinstance(str_dict, str):
                self.log("Is string")
                parsed_dict = ast.literal_eval(str_dict)
            elif isinstance(str_dict, dict):    
                parsed_dict = str_dict
            else:
                self.log(f"Unsupported input type: {type(str_dict)}", "Popup input")
                return ""
            
        except Exception as e:
            self.log(str(e), "Exception while parsing string to dict:")
            return ""

        # Check if it's a dictionary and contains the key
        if (key in parsed_dict):
            self.log(f"Key '{key}' found in parsed dict")
            return parsed_dict[key]
        else: return ""

    async def build_list_of_flows(self, flows_to_run: List, input_value) -> List:
        list_of_flows = []

        for flow_name_selected in flows_to_run:
            if flow_name_selected == "" or flow_name_selected is None: continue

            new_flow = Flow(flow_name_selected, input_value, self.user_id, "1")
            list_of_flows.append(new_flow)

            self.log(flow_name_selected, "Added to flows to run")

        return list_of_flows

    async def run_flows(self, flows: List):
        for flow in flows:
            if isinstance(flow, Flow):
                await flow.run_flow()
                self.log(flow.get_flow_name(), "Successful flow run")
            else:
                self.log(flow.get_flow_name(), "Error running flow")
                

    async def collect_results_from_flows_as_dicts(self, flows: List) -> Dict[str, str]:
        results: Dict[str, str] = {}

        for flow in flows:
            if isinstance(flow, Flow):
                if (flow.is_completed()):
                    results = merge_string_to_dict(flow.collect_result_as_string(), results)
                else:
                    self.log(flow.get_flow_name(), "Is not completed")
            else:
                self.log("Is not an instance of a Flow")

        return results


    async def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None):
        """
        Updates the component's config when a field value is changed (especially 'input_value').

        Args:
            build_config (dotdict): Current configuration.
            field_value (Any): New field value.
            field_name (str | None): Name of the field being updated.

        Returns:
            dotdict: Updated configuration.
        """
        
        # When Flows are updated, validate them
        if field_name == "input_value":
            build_config["input_value"]["value"] = await self.validate_flows(build_config["input_value"]["value"])
            return build_config
            
        if field_name == "flows":
            flow_to_add = await self.get_value_from_str_dict(build_config["flows"]["value"], "name")

            
            if flow_to_add: 
                updated_flows = build_config["input_value"]["value"]
                updated_flows.append(flow_to_add)
                build_config["input_value"]["value"] = await self.validate_flows(updated_flows)
                build_config["flows"]["value"] = ""
                
        return build_config

        
    async def build_output(self) -> Data:
        """
        Orchestrates the complete process of:
        - Running validated flows
        - Merging their results with the input
        - Returning a combined Data output

        Returns:
            Data: Final structured output with results of all processed flows.
        """
        flow = FlowAPI("http://langflow.languagestudio.com:3001", "run", "v1")
        
        flows_selected = self._attributes.get("input_value")
        self.log(flows_selected, "Flows selected")
        
        await self.get_flow(flows_selected[0])
        
        inputs = self._attributes.get("flow_value")
        self.log(inputs, "inputs")
        
        flows_to_run = await self.build_list_of_flows(flows_selected, inputs)
        self.log(type(flows_to_run).__name__, "Flows to run type")

        await self.run_flows(flows_to_run)
        results = await self.collect_results_from_flows_as_dicts(flows_to_run)
        
        #output = merge_string_to_dict(inputs, results)
        output = results
        self.log(output, "output")
        
        print(self.demo.something())
        # output = {}
        
        # output["Output"] = await self.get_value_from_str_dict(self.flows, "name")
        
        return Data(data=output)


