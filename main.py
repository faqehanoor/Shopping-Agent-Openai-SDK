import chainlit as cl
import requests

API_URL = "https://hackathon-apis.vercel.app/api/products"

def fetch_products(query: str) -> str:
    try:
        response = requests.get(API_URL)
        data = response.json()

        matched = [p for p in data if query.lower() in p["name"].lower()]
        if not matched:
            return f"❌ No products found for '**{query}**'. Try a different keyword."

        result = ""
        for product in matched[:5]:
            result += f"""
### 🛒 {product['name']}

💰 **Price:** ${int(product['price']):,}  
![{product['name']}]({product['image']})  
---
"""

        return result

    except Exception as e:
        return f"🚨 Error fetching products: {str(e)}"

@cl.on_chat_start
async def greet():
    await cl.Message(
        content="""
👋 **Welcome to the AI Shopping Agent!**

Just type what you're looking for, like:

- The Poplar suede sofa
- Chair
- The Lucky Lamp

I'll fetch real-time products with images for you. 🛍️
"""
    ).send()

@cl.on_message
async def handle_message(msg: cl.Message):
    user_query = msg.content.strip()
    
    if not user_query:
        await cl.Message(content="❗ Please type a product name to search.").send()
        return

    await cl.Message(content="🔎 Searching for products...").send()

    result = fetch_products(user_query)
    await cl.Message(content=result).send()
