from typing import Dict, List
from loguru import logger

from langflow.helpers.flow import run_flow
from langflow.base.flow_processing.utils import build_data_from_run_outputs
import requests


class FlowAPI

class Flow:
    """
    Flow class manages the execution and results of a single flow instance.
    """

    def __init__(self, flow_name: str, inputs: str, user_id: str, session_id: str):
        """
        Initialize a new Flow instance.

        Args:
            flow_name (str): The name of the flow to run.
            inputs (str): The input string to pass to the flow.
            user_id (str): Identifier for the user running the flow.
            session_id (int): Identifier for the session.
        """
        self._flow_name: str = flow_name
        self._inputs: str = inputs
        self._results: Dict = {}
        self._retries: int = 0
        self._user_id: str = user_id
        self._session_id: str = session_id
        self._is_completed: bool = False

    def set_retries(self, no_of_retries: int):
        """
        Set the number of retries allowed if the flow fails.

        Args:
            no_of_retries (int): The number of retry attempts.
        """
        self._retries = max(0, no_of_retries)

    async def run_flow(self):
        """
        Executes the flow asynchronously and stores the result.
        """
        tweaks = {}  # No tweaks applied
        try:
            self._results = await run_flow(
                inputs={"input_value": self._inputs},
                output_type="all",
                flow_id=None,
                flow_name=self._flow_name,
                tweaks=tweaks,
                user_id=str(self._user_id),
                session_id=self._session_id,
            )
            self._is_completed = True
        except Exception as e:
            logger.exception("Oof!" + str(e))
            raise RuntimeError("Oof!" + str(e)) from e

    async def run_flow_with_retries(self):
        """
        Placeholder for running the flow with retry logic.
        To be implemented.
        """
        pass

    def collect_result_as_string(self) -> str:
        """
        Converts the flow output into a concatenated string.

        Returns:
            str: Concatenated string of all text results.
        """
        output = ""
        data = []
        if isinstance(self._results, list):
            for result in self._results:
                if result:
                    data.extend(build_data_from_run_outputs(result))

        for datum in data:
            output += datum.data.get("text", "")

        return output

    def collect_result_as_dict(self) -> Dict:
        """
        Converts the flow output into a merged dictionary.

        Returns:
            dict: A dictionary containing merged data from all outputs.
        """
        output = {}
        data = []
        if isinstance(self._results, list):
            for result in self._results:
                if result:
                    data.extend(build_data_from_run_outputs(result))

        for datum in data:
            text_data = datum.data.get("text", "")
            print(f"This is data ******************\n{text_data}")
            output = self.merge_string_to_dict(text_data, output)

        return output

    def get_flow_name(self) -> str:
        """
        Returns the name of the flow.

        Returns:
            str: Flow name.
        """
        return self._flow_name

    def clear_state_and_results(self):
        """
        Resets the flow's completion status and clears results.
        """
        self._is_completed = False
        self._results = {}

    def is_completed(self) -> bool:
        """
        Returns whether the flow execution has completed.

        Returns:
            bool: True if completed, False otherwise.
        """
        return self._is_completed
    
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
            msg = f"Error converting string input to dict: " + string
            logger.exception(msg + "string:" + string)
            raise RuntimeError(msg) from e

        # merge dicts
        dict = string_dict | dict
        return dict


class FlowManager:
    """
    Manages a list of Flow instances for execution.
    """

    def __init__(self):
        """
        Initializes the flow manager with an empty flow list.
        """
        self._flows: List[Flow] = []

    def add_flow_to_run(self, flow: Flow):
        """
        Adds a flow to the manager's execution list.

        Args:
            flow (Flow): The flow instance to add.
        """
        self._flows.append(flow)

    def remove_flow_to_run(self, flow: Flow):
        """
        Removes a flow from the manager's execution list.

        Args:
            flow (Flow): The flow instance to remove.
        """
        if flow in self._flows:
            self._flows.remove(flow)
