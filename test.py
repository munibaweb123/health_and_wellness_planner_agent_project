import asyncio
from tools.workout_recommender import workout_recommender

async def test():
    result = await workout_recommender.tool(goal="lose 5kg")  # ✅ use `.tool()`
    print(result)

asyncio.run(test())
