import azure.functions as func
import logging
import requests

app = func.FunctionApp(auth_level=func.AuthLevel.FUNCTION)

@app.route(route="processpdf")
def process_pdf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.method == "POST":
        try:
            req_body = req.get_json()
            pdf_url = req_body.get("pdf_url")  # Get the PDF URL from the request body

            # Call Azure Document Intelligence service
            endpoint = "https://pdf-function-test-qima.cognitiveservices.azure.com/formrecognizer/documentModels/prebuilt-read:analyze"
            key = "b573abdcfa8d470f8d32c5ee47c294a6"
            headers = {
                "Ocp-Apim-Subscription-Key": key,
                "Content-Type": "application/json"
            }
            payload = {
                "url": pdf_url
            }
            response = requests.post(endpoint, headers=headers, json=payload)

            # Return the JSON response from the Document Intelligence service
            if response.status_code == 200:
                return func.HttpResponse(response.json(), status_code=200)
            else:
                return func.HttpResponse("Error processing the PDF", status_code=response.status_code)

        except ValueError:
            return func.HttpResponse("Invalid input", status_code=400)

    else:
        return func.HttpResponse("Method not allowed", status_code=405)