from datetime import datetime

from google.genai import types


async def process_agent_response(event):
    """Process and display agent response events."""
    print(f"Event ID: {event.id}, Author: {event.author}")

    # Check for specific parts first
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"  Text: '{part.text.strip()}'")

    # Check for final response after specific parts
    final_response = None
    if not has_specific_part and event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            # Use colors and formatting to make the final response stand out
            print(
                "╔══ AGENT RESPONSE ═════════════════════════════════════════"
            )
            print("final_response")
            print(
              "╚═════════════════════════════════════════════════════════════\n"
            )
        else:
            print(
                f"==> Final Agent Response: [No text content in final event]\n"
            )

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"--- Running Query: {query} ---"
    )
    final_response_text = None
    agent_name = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
          
            if event.author:
                agent_name = event.author

            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"ERROR during agent run: {e}")
    print(f"{'-' * 30}")
    return final_response_text