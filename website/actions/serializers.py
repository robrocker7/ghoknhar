from rest_framework import serializers

class GoogleActionSerializer(serializers.Serializer):
    """
    {
  "id": "b7cfa4ac-8bcc-444e-918b-405967efd833",
  "timestamp": "2016-12-31T00:27:19.348Z",
  "result": {
    "source": "agent",
    "resolvedQuery": "Add December 3rd to my Work Schedule",
    "action": "calendar.add",
    "actionIncomplete": false,
    "parameters": {
      "date-time": "December 3rd ",
      "workschedule": "workschedule.action"
    },
    "contexts": [],
    "metadata": {
      "intentId": "9cb46c0d-1603-4ffd-8ed1-aaa737ed2c76",
      "webhookUsed": "false",
      "webhookForSlotFillingUsed": "false",
      "intentName": "Add Work Day to Schedule"
    },
    "fulfillment": {
      "speech": "Alright. I've added that to your work schedule.",
      "messages": [
        {
          "type": 0,
          "speech": "Alright. I've added that to your work schedule."
        }
      ]
    },
    "score": 1
  },
  "status": {
    "code": 200,
    "errorType": "success"
  },
  "sessionId": "0e67f6c9-ddd6-4e9b-a7e4-90a2b2a55e2d"
}
    """
    id = serializers.UUIDField()
    session_id = serializers.UUIDField()
    timestamp = serializers.DateTimeField()
    parameters = serializers.CharField()
    status_code = serializers.CharField()
