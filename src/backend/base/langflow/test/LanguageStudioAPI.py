import requests
import json

class LanguageStudioAPI:
    """
    A class to interact with the Language Studio API to retrieve flow profile details.
    """

    def __init__(self, base_url="http://devdemo.languagestudio.com:4000"):
        """
        Initializes the LanguageStudioAPI with a base URL.

        Args:
            base_url (str): The base URL of the API endpoint.
        """
        self._base_url = base_url
        self._getflowprofile_endpoint = f"{self._base_url}/lsrestapi/v6/genai/getflowprofile"
        self._response = None
        self._result = None

    def _set_getflowprofile_endpoint(self, endpoint: str):
        """
        Sets the endpoint for the getflowprofile API with the specified flow ID.

        Args:
            flow_id (str): The ID of the flow to retrieve details for.
        """
        if not endpoint:
            raise ValueError("Endpoint cannot be empty.")
        
        endpoint = endpoint.strip('/')
        self._getflowprofile_endpoint = f"{self.base_url}/{endpoint}"


    def _get_flow_profile_details(self, flow_id, detail: bool = 0) -> bool:
        """
        Calls the getflowprofile API for a given flow ID and extracts
        the 'name', 'guid', and 'id' from the 'result' field of the response.

        Args:
            flow_id (str): The ID of the flow to retrieve details for.
            base_url (str): The base URL of the API endpoint.

        Returns:
            dict: A dictionary containing 'name', 'guid', and 'id' if successful,
                otherwise a dictionary with an 'error' key.
        """
        params = {
            'id': flow_id,
            'detail': detail
        }
        
        #flush results and response
        self._response = None
        self._result = None
        
        try:
            # Make the GET request to the API
            response = requests.get(self._getflowprofile_endpoint, params=params)
            # Raise an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()  
            self._response = data  # Store the response for potential debugging
            
            self._result = self._get_results_from_response()
            
            if self._result:
                return True
            else:
                print("No valid result found in the response.")
                return False

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - Response text: {response.text}")
            
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err} - Could not connect to the API.")
            
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err} - The request timed out.")
            
        except requests.exceptions.RequestException as req_err:
            print(f"An unexpected request error occurred: {req_err}")
            
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error: {json_err} - Response text: {response.text}")
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
        return False
    
    def _get_results_from_response(self) -> dict:
        """
        Extracts the 'result' field from the API response.

        Returns:
            dict: The 'result' field if it exists, otherwise an empty dictionary.
        """
        if self._response and 'result' in self._response:
            return self._response['result']
        return {}
    
    def get_flow_profile_id(self, flow_id: str) -> str:
        """
        Retrieves the flow profile ID for a given flow ID.

        Args:
            flow_id (str): The ID of the flow to retrieve details for.

        Returns:
            str: The flow profile ID if successful, otherwise an error message.
        """
        if not self._result:
            success = self._get_flow_profile_details(flow_id)
            if not success:
                return "Failed to retrieve flow profile details."
            
        if self._result and 'id' in self._result:
            return self._result['id']
        return "Flow profile ID {flow_id} not found in the response."
    
    def get_flow_profile_name(self, flow_id: str) -> str:
        """
        Retrieves the flow profile name for a given flow ID.

        Args:
            flow_id (str): The ID of the flow to retrieve details for.

        Returns:
            str: The flow profile name if successful, otherwise an error message.
        """
        if not self._result:
            success = self._get_flow_profile_details(flow_id)
            if not success:
                return "Failed to retrieve flow profile details."
            
        if self._result and 'name' in self._result:
            return self._result['name']
        return f"Flow profile name {flow_id} not found in the response."

    def get_flow_profile_guid(self, flow_id: str) -> str:
        """
        Retrieves the flow profile GUID for a given flow ID.

        Args:
            flow_id (str): The ID of the flow to retrieve details for.

        Returns:
            str: The flow profile GUID if successful, otherwise an error message.
        """
        if not self._result:
            success = self._get_flow_profile_details(flow_id)
            if not success:
                return "Failed to retrieve flow profile details."
            
        if self._result and 'guid' in self._result:
            return self._result['guid']
        return f"Flow profile GUID {flow_id} not found in the response."
        
# Example usage:
flow_id_to_query = "551"
query = LanguageStudioAPI()

print(f"Flow Profile ID: {query.get_flow_profile_id(flow_id_to_query)}")
print(f"Flow Profile Name: {query.get_flow_profile_name(flow_id_to_query)}")
print(f"Flow Profile GUID: {query.get_flow_profile_guid(flow_id_to_query)}")




# You can also print the entire dictionary
# print("\nFull extracted dictionary:")
# print(profile_details)
