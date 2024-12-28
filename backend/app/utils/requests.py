import httpx

async def make_request(url: str, method: str = 'POST', headers: dict = None, data: dict = None):
    """
    Makes an asynchronous HTTP request using the specified method.

    Args:
        url (str): The URL to which the request is made.
        method (str): The HTTP method to use for the request ('GET' or 'POST'). Defaults to 'POST'.
        headers (dict, optional): A dictionary of HTTP headers to include in the request. Defaults to None.
        data (dict, optional): A dictionary of data to include in the request body for POST requests. Defaults to None.

    Returns:
        httpx.Response: The response object from the HTTP request.

    Raises:
        ValueError: If an unsupported HTTP method is specified.
        httpx.HTTPStatusError: If the HTTP request returns an unsuccessful status code.
    """
    async with httpx.AsyncClient() as client:
        if method == 'GET':
            response = await client.get(url, headers=headers)
        elif method == 'POST':
            response = await client.post(url, headers=headers, json=data)
        else:
            raise ValueError(method)
        response.raise_for_status()
        return response