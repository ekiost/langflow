
import httpx
import asyncio
from typing import Dict, List
from langflow.test.LanguageStudioAPI import APICaller


class FlowAPI:
    def __init__(self, base_url: str, api_to_call: str = "/ruun/", api_version: str = "v1"):
        """
        Initialize the FlowAPI with a base URL.

        Args:
            base_url (str): The base URL for the Flow API.
        """
        self._base_url: str = base_url.rstrip('/')
        self._api_to_call: str = api_version + "/" + api_to_call
        self._flow_UUID: str = ""
        self._flow_name: str = ""

        self._headers: Dict[str, str] = {"Content-Type": "application/json"}
        self._payload: Dict[str, str | Dict] = {}
        self._tweaks: Dict[str, Dict] = {}

        self._method: str = "POST"
        self._timeout = httpx.Timeout(timeout=5000, connect=10.0)
        self._client: httpx.AsyncClient = httpx.AsyncClient(timeout=self._timeout)
        self._output: Dict = {}
        self._error: str = ""
        self._is_successful: bool = False
        self._completed: bool = False
        
    def get_flow_name(self) -> str:
        """
        Get the name of the flow.

        Returns:
            str: The name of the flow.
        """
        if not self._flow_name: return "no name set"
        return self._flow_name
    def set_flow_name(self, flow_name: str):
        """
        Set the name of the flow.

        Args:
            flow_name (str): The name of the flow.
        """
        self._flow_name = flow_name
    
    def set_flow_id(self, flow_UUID: str):
        """
        Set the UUID of the flow to be called.

        Args:
            flow_UUID (str): The UUID of the flow.
        """
        self._flow_UUID = f"<script>{flow_UUID}</script>"

    def map_flowid_to_UUID(self, flow_id: str) -> str:
        """
        Map a flow ID to a UUID.

        Args:
            flow_id (str): The flow ID to map.
        """
        # This method is a placeholder for future implementation
        # Currently, it does not perform any operation 
        query = APICaller()
        resolved_guiid = query.get_flow_profile_guid(flow_id)
        
        if not resolved_guiid:
            print(f"Flow ID {flow_id} could not be resolved to a UUID.")
            return flow_id
        return resolved_guiid 

    def add_Langflow_API_key(self, key: str):
        """
        Add an API key to the headers for authentication.

        Args:
            key (str): The API key to add.
        """
        self._headers["x-api-key"] = key

    def add_payload(self, key: str, value: str):
        """
        Add a key-value pair to the payload for the API request.

        Args:
            key (str): The key for the payload.
            value (str): The value for the payload.
        """
        self._payload[key] = value
    def add_tweaks(self, component: str, field_name: str, field_value: str):
        """
        Adds tweaks into the payload to alter the fields of components within the flow

        Args:
            component(str): The name of the component
            field_name(str): Field of the component to change
            field_value(str): value of the field
        """
        if component not in self._tweaks:
            self._tweaks[component] = {}

        self._tweaks[None][field_name] =  field_value

    def validate_inputs(self) -> bool:
        """
        Check that the fields UUID and Api to call is not empty
        """
        if self._flow_UUID and self._api_to_call and self._payload: return True
        return False
    
    def prepare_default_payload(self):
        """
        Prepare the default payload for the API request.
        This method can be overridden to customize the payload.
        
        By default, it sets the input and output types to "chat".
        It also sets the input_type and output_type to "chat" in the payload.
        """
        pass
        
    def get_error(self) -> str:
        if self._error:
            return self._error
        return "No error occurred."
    
    def _build_payload(self) -> Dict:
        return {**self._payload, "tweaks": self._tweaks}

    def _build_request(self) -> str:
        self._flow_UUID = self.map_flowid_to_UUID(self._flow_UUID)
        url = f"{self._base_url}/api/{self._api_to_call}/{self._flow_UUID}"
        return url

    async def send_request(self) -> bool:
        """        Send a request to the Flow API with the current headers and payload.
        Returns:
            Dict: The JSON response from the API.
        """
        try:
            url = self._build_request()
            final_payload = self._build_payload()
            
            # 🔍 Print full request
            print("===== HTTP REQUEST =====")
            print("METHOD:", self._method)
            print("URL:", url)
            print("HEADERS:", self._headers)
            print("PAYLOAD:", final_payload)
            print("========================")

            response = await self._client.request(
                method=self._method,
                url=url,
                headers=self._headers,
                json=final_payload
            )

            # Check if the response was successful
            response.raise_for_status()
            print(f"Response from {self._api_to_call} received with status code: {response.status_code}", flush=True)
            self._output = response.json()
            
            if response.status_code == 200:
                self._is_successful = True
                self._output = {"outputs": response.json()}
                return True

            self._completed = True

        except httpx.RequestError as e:
            self._error = f"❌ Request error: {e.__class__.__name__} - {e}"
        except httpx.HTTPStatusError as e:
            self._error = f"HTTP error response from {self._api_to_call}: {e}"
        except ValueError as e:
            self._error = f"Error parsing JSON response from {self._api_to_call}: {e}"
        return False

    def is_response_ready(self) -> bool:
        return False

    def collect_response(self) -> str:
        try:
            text = (
                self._output
                .get("outputs", [{}])[0]
                .get("outputs", [{}])[0]
                .get("results", {})
                .get("message", {})
                .get("data", {})
                .get("text", "")
            )
            return ""
        except Exception as e:
            print(f"Error collecting response: {e}")
            return ""

    
    def _extract_output(self) -> str:
        try:
            for item in self._output.get("outputs", []):
                for output in item.get("outputs", []):
                    for result in output.get("results", {}):
                        text= result.get("data", {}).get("text")
                        if text: 
                            return text
        except Exception as e:
            print(f"Failed to extract outputs {e}")
        return ""


    async def close_client(self):
        """
        Close the HTTP client if it is open.
        """
        if self._client:
            await self._client.aclose()
            self._client = None
    
async def main():    
    flow = FlowAPI("https://devdemo.languagestudio.com:3000")
    flow.set_flow_id("189")
    flow.prepare_default_payload()
    flow.add_payload("input_value", "Banana")

    success = await flow.send_request()
    
    if success:
        output = flow.collect_response()
    else: output = "Response not ready. Error" + flow._error 
    print("=== FINAL OUTPUT ===")
    print(output)
    
    await flow.close_client()


if __name__ == "__main__":
    asyncio.run(main())

