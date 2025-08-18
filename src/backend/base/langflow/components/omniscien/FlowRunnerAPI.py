import ast
from typing import List, Any, Dict
from loguru import logger

from langflow.custom import Component
from langflow.graph.graph.base import Graph
from langflow.helpers.flow import get_flow_inputs

from langflow.inputs.inputs import (
    DropdownInput,
    MessageTextInput,
    CustomInput,
    IntInput,
    DictInput,
    BoolInput,
    MultilineInput
)
from langflow.schema import Data, dotdict
from langflow.template import Output

from langflow.test.FlowAPI import FlowAPI
from langflow.helpers.flow import run_flow
from langflow.base.flow_processing.utils import build_data_from_run_outputs
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

def merge_string_to_dict(string: str | Dict, dict: Dict) -> Dict:
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
        if (isinstance(string,str)):
        # Cast to string
            string_dict = {"Result": string}
        
        elif (isinstance(string, Dict)):
            string_dict = string
        else: 
            string_dict= {}
    # merge dicts
    dict = string_dict | dict
    return dict


class FlowRunnerAPIComponent(Component):
    display_name = "Flow Runner API(Upgraded)"
    description = "Component to run multiple flows sequentially."
    documentation: str = "https://docs.langflow.org/components-custom-components"
    name = "FlowRunner"
    icon = "Omniscien"
    
    inputs = [
        BoolInput(
            name="SeqOrParallel",
            display_name="Enable Parallel running?",
            value=False,
            dynamic=True,
            real_time_refresh=True,
        ),
        IntInput(
            name="num_parallel_workers",
            display_name="Set Max Number of Parallel Requests",
            value=3,
            show=False,
            dynamic=True,
            real_time_refresh=True,),
            
        CustomInput(
            name="flows",
            display_name="Select Flows",
            modal="https://devdemo.languagestudio.com/langflow/popup",
            info="Click here to input Flows to run",
            dynamic=True,
            real_time_refresh=True,
            advanced=False
        ),
            
        MessageTextInput(
            name="flows_to_run",
            display_name="Flows to Run",
            info="This is input accepts only valid flows that exist in the LangFlow server. \n Removes inputs that are invalid Flows or duplicate Flows.",
            value=[],
            is_list=True,
            tool_mode=True,
            real_time_refresh=True,
            input_types=[],
            advanced=False,
        ),
        
        DropdownInput(
            name="mode",
            display_name="On Error:",
            options=["Cascade", "Break"],
            value="Cascade",
            dynamic=True,
            advanced=True,
            info="On Error, either continue to cascade the flows or break the flows from running.",
            show= False,
        ),
        
        MultilineInput(
            name="flow_value",
            display_name="Flow Input",
            value="",
            dynamic=True,
            real_time_refresh=True,
            info=".",
            advanced=False
        ),
        
        MessageTextInput(
            name="LangflowAPI",
            display_name="Langflow API key (optional)",
            value="",
            info="API key to use for the Langflow API",
            advanced=True,
            show= False,
        ),
        
        MessageTextInput(
            name="API_URL",
            display_name="URL of the API to call",
            value="https://devdemo.languagestudio.com:3000/",
            info="URL of the Langflow API to call",
            advanced=True,
            show= True,
        ),

        DictInput(
            name="flow_dict",
            display_name="Language Studio Flow Data",
            value={},
            dynamic=True,
            real_time_refresh=True,
            is_list=True,
            advanced=True,
            show=True
        ),
        IntInput(
            name="retries",
            display_name="Number of API call attempts (Minimum: 1)",
            value=1,
            advanced=True,
            show=True,
        ),

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

    async def get_value_from_str_dict(self, str_dict: str, key: str) -> str | None:
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

    async def build_list_of_flows(self, flows_to_run:dict, input_value) -> List:
        list_of_flows = []
        print("flows to run is of type", type(flows_to_run).__name__)
        
        for idx, (flow_name, flow_id) in enumerate(flows_to_run.items()):
            if not flow_name or not flow_id:
                continue  # Skip if either is missing or empty
    
            self.log(flow_name + ": ID : " + str(flow_id), str(idx))
    
            new_flow = FlowAPI(self._attributes.get("API_URL"))
            new_flow.set_flow_name(flow_name)
            new_flow.set_flow_id(flow_id)
            new_flow.add_payload("input_value", input_value)
            new_flow.set_retry_count(int(self._attributes.get("retries")))
            new_flow.prepare_default_payload()
    
            list_of_flows.append(new_flow)
            self.log(flow_name, "Added to flows to run")

        return list_of_flows

    async def run_flows(self, flows: List[FlowAPI]):
        self.log("Running sequentially", "Run Mode")
        for flow in flows:
            if isinstance(flow, FlowAPI):
                success = await flow.send_request()
                self.log(flow.get_flow_name(), "Successful flow run")
            else:
                self.log(flow.get_flow_name(), "Error running flow")
                
    async def run_flows_in_parallel(self, flows: List) -> None:
        self.log("Running in Parallel", "Run Mode")
        tasks = []
        for flow in flows:
            if isinstance(flow, FlowAPI):
                tasks.append(flow.send_request())
            else: 
                self.log("Non-FlowAPI object in flows list")
                
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            flow = flows[i]
            if isinstance(result, Exception):
                self.log(f"Flow {i} failed with error: {result}")
            else:
                self.log(flow.get_flow_name(), f"Flow {i} completed: success = {result}")
                
    async def run_with_futures(self, flows: List, max_workers: int = 5):
        """
        Runs flows in parallel using ThreadPoolExecutor.
        
        Args:
            flows (List): List of FlowAPI instances to run.
            max_workers (int): Maximum number of threads to use.
        """
        
        def run_flow_sync(flow):
        # Create a new event loop in this thread and run the async function
            return asyncio.run(flow.run_with_retries())
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(run_flow_sync, flow): flow for flow in flows}
            for future in as_completed(futures):
                flow = futures[future]
                try:
                    result = future
                except Exception as e:
                    self.log(f"Flow failed with error: {e}", flow.get_flow_name())
                        
    async def collect_results_from_flows_as_dicts(self, flows: List) -> Dict[str, str]:
        results: Dict[str, str] = {}

        for flow in flows:
            if isinstance(flow, FlowAPI):
                if (flow.is_response_ready):
                    print(flow.collect_response())
                    
                    results = merge_string_to_dict(flow.collect_response(), results)
                else:
                    self.log(flow.get_flow_name(), "Is not completed")
            else:
                self.log("Is not an instance of a Flow")

        return results
        # Function to take in Flow inputs as a List and return only Flows that exist in LangFlow without duplicates
    def validate_flows(self, flows_input: List) -> List:
        """
        Filters and returns only valid, unique flow names from the user input.
    
        Args:
            flows_input (List): List of user-specified flow names.
    
        Returns:
            List: Validated list of unique flow names (non-empty, no duplicates).
        """
        validated_flows = []
        seen = set()
    
        for flow in flows_input:
            if flow and flow not in seen:
                validated_flows.append(flow)
                seen.add(flow)
    
        return validated_flows
    
    async def validate_flow(self, flow: str) -> str:
        valid_flows = await self.get_flow_names()
        return flow if flow in valid_flows else ""
        
    def validate_dicts(self, dicts_to_val: list[dict]) -> list[dict]:
        return [
            d for d in dicts_to_val
            if d and not (len(d) == 1 and '' in d and d[''] == '')
        ]

    def flatten_dict(self, l: List) -> dict:
        """
        Flattens a list of dictionaries into a single dictionary. Non-recursive.
    
        Args:
            l (List): List of dictionaries to flatten.
    
        Returns:
            dict: Flattened dictionary.
        """
        result = {}
        if isinstance(l, list):
            for d in l:
                if isinstance(d, dict):
                    result.update(d)
                    
        return result

    def unflatten_dict(self, d: dict) -> List[dict]:
        """
        Converts a flattened dictionary into a list of single-key dictionaries.
    
        Args:
            d (dict): Flattened dictionary.
    
        Returns:
            List[dict]: List of single-key dictionaries.
        """
        if not isinstance(d, dict):
            return []

        return [{k: v} for k, v in d.items()]
        
    def update_flow_data(self, flow_data: dict) -> bool:
        """
        Updates the 'flows_to_run' attribute by removing invalid or duplicate flows.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        flows_to_run = self._attributes.get("flows_to_run", [])
        print(flows_to_run, "Flows to run before update")
    
        list_of_flows = flow_data.keys()
        print("List of flows:", list(list_of_flows))
    
        valid_flows = [flow for flow in flows_to_run if flow in list_of_flows]
          # Filter the original flow_data to only include valid_flows
        valid_flow_data = {key: flow_data[key] for key in valid_flows}
        
        print("Valid Flow Data", valid_flow_data)
        
        return valid_flows, valid_flow_data

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
        print("\n\n=== Updating Build Config === \n")
        print(f"{field_name}: {field_value}")
        
        
        if field_name == "SeqOrParallel":
            build_config["num_parallel_workers"]["show"] = field_value
        
        # Unions flows to run and flows_to_run
        # Removes flows that don't exist in both
        if field_name == "flows_to_run" or field_name == "flow_dict":
            flow_data = self.flatten_dict(build_config["flow_dict"]["value"])
            print("Flow datas:", flow_data)
            updated_flows, updated_flow_data = self.update_flow_data(flow_data)
            
            build_config["flow_dict"]["value"] = self.validate_dicts(self.unflatten_dict(updated_flow_data))
            build_config["flows_to_run"]["value"] = self.validate_flows(updated_flows)
            
            return build_config
            
        #print(build_config["data"]["value"])
        
        # When Flows are updated, validate them
        # if field_name == "flows_to_run":
        #     build_config["flows_to_run"]["value"] = await self.validate_flows(build_config["flows_to_run"]["value"])
        #     return build_config
            
        if field_name == "flows":
            flow_to_add = await self.get_value_from_str_dict(build_config["flows"]["value"], "name")
            uuid_to_add = await self.get_value_from_str_dict(build_config["flows"]["value"], "id")
            print(uuid_to_add)
            
            if not flow_to_add or not uuid_to_add: return build_config
    
            new_flow = { flow_to_add : uuid_to_add }  
            
            
            if flow_to_add: 
                updated_flows = build_config["flows_to_run"]["value"]
                updated_flows.append(flow_to_add)
                flow_dict = build_config["flow_dict"]["value"]
                
                if isinstance(flow_dict, dict):
                    flow_dict = [flow_dict]
                    
                flow_dict.append(new_flow)
                print(flow_dict)
                
                #print(flow_dict)
                
                build_config["flows_to_run"]["value"] = self.validate_flows(updated_flows)
                build_config["flow_dict"]["value"] = self.validate_dicts(flow_dict)
                build_config["flows"]["value"] = ""
                
        return build_config
        
    
    def update_dict(self, dict1: dict, dict2: dict):
        return dict1 | dict2
    

    async def build_output(self) -> Data:
        """
        Orchestrates the complete process of:
        - Running validated flows
        - Merging their results with the input
        - Returning a combined Data output

        Returns:
            Data: Final structured output with results of all processed flows.
        """
        
        
        parallel = self._attributes.get("SeqOrParallel")
        max_workers = self._attributes.get("num_parallel_workers")
        self.log(parallel, "Run Mode: parallel")
        
        flows_selected = self._attributes.get("flows_to_run")
        
        output={}
        
        inputs = self._attributes.get("flow_value")
        self.log(inputs, "inputs")
        dict_input = {"inputs": inputs}
        
        flows_selected = self._attributes.get("flow_dict")
        self.log(flows_selected, "flows_selected")
        #self.log(type(flows_selected).__name__, "flows_selected type")
        
        flows_to_run = await self.build_list_of_flows(flows_selected, inputs)
        #self.log(flows_to_run, "Flows to run")
        
        if parallel:
            await self.run_with_futures(flows_to_run, max_workers=max_workers)
            #await self.run_flows_in_parallel(flows_to_run)
            #await self.run_flows(flows_to_run)
        else: 
            success = await self.run_flows(flows_to_run)
        
        for flow in flows_to_run:
            flow_error = flow.get_error() 
            if flow_error: self.log(f"Error: {flow_error}", flow.get_flow_name())
            else: self.log("Run successfully", flow.get_flow_name())
            
        results = await self.collect_results_from_flows_as_dicts(flows_to_run)
        self.log(results, "Results of flows run")
        
        output = merge_string_to_dict(dict_input, results)
        self.log(output, "output")
        
        return Data(data=output)

