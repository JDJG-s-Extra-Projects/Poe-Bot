import os

from poe_api_wrapper import PoeApi, api

token = os.environ["API_TOKEN"]
client = PoeApi(token)

bots = client.get_available_bots()

free_bots = sorted(filter(lambda b: not bots[b]["bot"]["isLimitedAccess"], bots))
loose_bots = sorted(
    filter(lambda b: bots[b]["bot"]["isLimitedAccess"] and bots[b]["bot"]["limitedAccessType"] == "soft_limit", bots)
)
restricted_bots = sorted(
    filter(lambda b: bots[b]["bot"]["isLimitedAccess"] and bots[b]["bot"]["limitedAccessType"] == "hard_limit", bots)
)


# api.BOT_CREATION_MODELS
# (may be useful later, who knows)

# for chunk in client.send_message("ChatGPT", "Test"):
# print(chunk["response"])
