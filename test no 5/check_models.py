from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key="sk_d5c0c41bba86b98c87a9fdcfc47a5598b35ad75f07f754dc"
)

response = client.conversational_ai.agents.create(
    name="agent_3201kdcj40n4etm9sbd2f28hfh3t",
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": "You are a helpful assistant that can answer questions and help with tasks.", 
            }
        }
    }
)

print(response)
