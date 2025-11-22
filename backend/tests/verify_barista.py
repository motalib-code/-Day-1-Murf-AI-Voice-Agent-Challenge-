import asyncio
import os
import json
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from agent import Assistant

async def main():
    print("Verifying Barista Agent...")

    # Mock context
    ctx = None

    # Test incomplete order
    print("\nTesting incomplete order submission...")
    agent_incomplete = Assistant()
    result = await agent_incomplete.submit_order(ctx)
    print("Result:", result)
    assert "Cannot submit order" in result

    # Test complete flow
    agent = Assistant()
    print("\nTesting complete flow...")
    print("Initial state:", agent.order_state)

    # Test update_order
    print("Testing update_order...")
    await agent.update_order(ctx, drink_type="Latte", size="Medium")
    print("State after update:", agent.order_state)
    assert agent.order_state["drinkType"] == "Latte"
    assert agent.order_state["size"] == "Medium"

    await agent.update_order(ctx, milk="Oat", name="Jules")
    print("State after 2nd update:", agent.order_state)
    assert agent.order_state["milk"] == "Oat"
    assert agent.order_state["name"] == "Jules"

    await agent.update_order(ctx, extras=["Sugar", "Cinnamon"])
    print("State after extras update:", agent.order_state)
    assert "Sugar" in agent.order_state["extras"]

    # Test submit_order
    print("Testing submit_order...")
    # Verify it creates the file
    if os.path.exists("order.json"):
        os.remove("order.json")

    result = await agent.submit_order(ctx)
    print("Submit result:", result)

    if os.path.exists("order.json"):
        print("order.json created successfully.")
        with open("order.json", "r") as f:
            content = json.load(f)
            print("order.json content:", content)
            assert content == agent.order_state
    else:
        print("Error: order.json not created.")
        exit(1)

    print("\nVerification passed!")

if __name__ == "__main__":
    asyncio.run(main())
