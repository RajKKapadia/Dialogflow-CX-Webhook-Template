from fastapi import Depends, FastAPI, HTTPException

from src.actions import some_tag
from src.utils import verify_api_key
from src import logging
from src.schemas import (
    WebhookRequest,
    WebhookResponse,
    FulfillmentResponse,
    Message,
    Text,
)
from src.actions.default_welcome_intent import default_welcome_intent

logger = logging.getLogger(__name__)

app = FastAPI(title="Dialogflow CX Webhook API")


@app.post("/webhook", response_model=WebhookResponse)
async def dialogflow_webhook(
    webhook_request: WebhookRequest, is_verified: bool = Depends(verify_api_key)
):
    try:
        tag = webhook_request.fulfillmentInfo.tag
        if tag == "defaultWelcomeIntent":
            return await default_welcome_intent(webhook_request=webhook_request)
        elif tag == "someTag":
            return await some_tag(webhook_request=webhook_request)
        else:
            return WebhookResponse(
                fulfillmentResponse=FulfillmentResponse(
                    messages=[
                        Message(text=Text(text=[f"No handler for the tag: {tag}"]))
                    ]
                )
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Webhook processing error: {str(e)}"
        )
