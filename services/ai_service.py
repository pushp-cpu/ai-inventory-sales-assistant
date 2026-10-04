import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from services.ai_tools import TOOLS

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)


tool_declarations = [
    types.FunctionDeclaration(
        name="get_products",
        description="Returns all products in the inventory, including stock levels and reorder levels.",
        parameters=types.Schema(
            type="OBJECT",
            properties={}
        ),
    ),
    types.FunctionDeclaration(
        name="get_sales",
        description="Returns all recorded sales transactions.",
        parameters=types.Schema(
            type="OBJECT",
            properties={}
        ),
    ),
    types.FunctionDeclaration(
        name="get_low_stock_products",
        description="Returns products whose current stock is at or below their reorder level.",
        parameters=types.Schema(
            type="OBJECT",
            properties={}
        ),
    ),
    types.FunctionDeclaration(
        name="get_total_revenue",
        description="Returns the total revenue generated from all recorded sales.",
        parameters=types.Schema(
            type="OBJECT",
            properties={}
        ),
    ),
    types.FunctionDeclaration(
        name="get_best_selling_products",
        description="Returns products ranked by the total quantity sold.",
        parameters=types.Schema(
            type="OBJECT",
            properties={}
        ),
    ),
]


inventory_tools = types.Tool(
    function_declarations=tool_declarations
)


def ask_gemini(question):

    system_instruction = """
    You are an AI assistant for an inventory and sales management system.

    Help users understand:
    - products
    - inventory
    - sales
    - revenue
    - low-stock products
    - best-selling products

    All monetary values in this system are in Indian Rupees (₹).
    Never convert monetary values to another currency.

    Do not invent inventory or sales data.
    When database information is required, use the available business tools.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[inventory_tools],
            system_instruction=system_instruction,
        ),
    )

    function_calls = response.function_calls

    if not function_calls:
        return response.text

    tool_call = function_calls[0]
    tool_name = tool_call.name

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool requested: {tool_name}")

    tool_function = TOOLS[tool_name]
    tool_result = tool_function()

    final_response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            question,
            response.candidates[0].content,
            types.Part.from_function_response(
                name=tool_name,
                response={
                    "result": tool_result
                },
            ),
        ],
        config=types.GenerateContentConfig(
            tools=[inventory_tools],
            system_instruction=system_instruction,
        ),
    )

    return final_response.text