#!/usr/bin/env python3
import asyncio
import sys
from typing import Any, List
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import numpy as np
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

app = Server("calculator")

UNIT_CONVERSIONS = {
    "length": {
        "m": 1.0,
        "km": 1000.0,
        "cm": 0.01,
        "mm": 0.001,
        "mile": 1609.34,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254
    },
    "weight": {
        "kg": 1.0,
        "g": 0.001,
        "mg": 0.000001,
        "lb": 0.453592,
        "oz": 0.0283495
    },
    "time": {
        "second": 1.0,
        "minute": 60.0,
        "hour": 3600.0,
        "day": 86400.0,
        "week": 604800.0
    },
    "data": {
        "byte": 1.0,
        "kb": 1024.0,
        "mb": 1048576.0,
        "gb": 1073741824.0,
        "tb": 1099511627776.0
    },
    "rate": {
        "requests/second": 1.0,
        "requests/minute": 1/60.0,
        "requests/hour": 1/3600.0
    }
}

def safe_eval(expression: str) -> float:
    allowed_chars = set('0123456789+-*/().% ')
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Expression contains invalid characters")
    
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

def convert_unit(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    for category, units in UNIT_CONVERSIONS.items():
        if from_unit in units and to_unit in units:
            base_value = value * units[from_unit]
            return base_value / units[to_unit]
    
    raise ValueError(f"Cannot convert from {from_unit} to {to_unit}")

def calculate_statistics(numbers: List[float], operation: str) -> float:
    arr = np.array(numbers)
    
    operations = {
        "mean": np.mean,
        "median": np.median,
        "std": np.std,
        "variance": np.var,
        "min": np.min,
        "max": np.max,
        "sum": np.sum
    }
    
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}. Available: {', '.join(operations.keys())}")
    
    return float(operations[operation](arr))

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="calculate",
            description="Evaluate mathematical expressions. Supports +, -, *, /, %, parentheses. Example: '(100 + 50) * 2'",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="convert_units",
            description="Convert between units. Supports length (m, km, mile, foot, inch), weight (kg, g, lb, oz), time (second, minute, hour, day), data (byte, kb, mb, gb), and rate (requests/second, requests/minute, requests/hour).",
            inputSchema={
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "Value to convert"
                    },
                    "from_unit": {
                        "type": "string",
                        "description": "Source unit"
                    },
                    "to_unit": {
                        "type": "string",
                        "description": "Target unit"
                    }
                },
                "required": ["value", "from_unit", "to_unit"]
            }
        ),
        Tool(
            name="statistics",
            description="Calculate statistics on a list of numbers. Operations: mean, median, std, variance, min, max, sum.",
            inputSchema={
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of numbers to analyze"
                    },
                    "operation": {
                        "type": "string",
                        "description": "Statistical operation to perform",
                        "enum": ["mean", "median", "std", "variance", "min", "max", "sum"]
                    }
                },
                "required": ["numbers", "operation"]
            }
        ),
        Tool(
            name="date_calculator",
            description="Perform date calculations. Operations: 'difference' (days between dates), 'add_days' (add days to date), 'subtract_days' (subtract days from date).",
            inputSchema={
                "type": "object",
                "properties": {
                    "date1": {
                        "type": "string",
                        "description": "First date in YYYY-MM-DD format or relative like 'today', '2024-12-15'"
                    },
                    "date2": {
                        "type": "string",
                        "description": "Second date (for 'difference') or leave empty"
                    },
                    "operation": {
                        "type": "string",
                        "description": "Operation to perform",
                        "enum": ["difference", "add_days", "subtract_days"]
                    },
                    "days": {
                        "type": "number",
                        "description": "Number of days (for add_days/subtract_days operations)"
                    }
                },
                "required": ["date1", "operation"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    try:
        if name == "calculate":
            expression = arguments.get("expression", "")
            result = safe_eval(expression)
            return [TextContent(
                type="text",
                text=f"Result: {result}\n\nExpression: {expression}"
            )]
        
        elif name == "convert_units":
            value = float(arguments.get("value"))
            from_unit = arguments.get("from_unit")
            to_unit = arguments.get("to_unit")
            
            result = convert_unit(value, from_unit, to_unit)
            return [TextContent(
                type="text",
                text=f"Conversion Result: {result:.4f} {to_unit}\n\nFrom: {value} {from_unit}"
            )]
        
        elif name == "statistics":
            numbers = [float(x) for x in arguments.get("numbers", [])]
            operation = arguments.get("operation")
            
            if not numbers:
                raise ValueError("Numbers list cannot be empty")
            
            result = calculate_statistics(numbers, operation)
            return [TextContent(
                type="text",
                text=f"Statistical Result ({operation}): {result:.4f}\n\nData: {numbers}\nCount: {len(numbers)}"
            )]
        
        elif name == "date_calculator":
            date1_str = arguments.get("date1", "").lower()
            operation = arguments.get("operation")
            
            if date1_str == "today":
                date1 = datetime.now()
            else:
                date1 = date_parser.parse(date1_str)
            
            if operation == "difference":
                date2_str = arguments.get("date2", "").lower()
                if date2_str == "today":
                    date2 = datetime.now()
                else:
                    date2 = date_parser.parse(date2_str)
                
                difference = abs((date2 - date1).days)
                return [TextContent(
                    type="text",
                    text=f"Date Difference: {difference} days\n\nFrom: {date1.strftime('%Y-%m-%d')}\nTo: {date2.strftime('%Y-%m-%d')}"
                )]
            
            elif operation == "add_days":
                days = int(arguments.get("days", 0))
                result_date = date1 + timedelta(days=days)
                return [TextContent(
                    type="text",
                    text=f"Result Date: {result_date.strftime('%Y-%m-%d')}\n\nStarting Date: {date1.strftime('%Y-%m-%d')}\nAdded: {days} days"
                )]
            
            elif operation == "subtract_days":
                days = int(arguments.get("days", 0))
                result_date = date1 - timedelta(days=days)
                return [TextContent(
                    type="text",
                    text=f"Result Date: {result_date.strftime('%Y-%m-%d')}\n\nStarting Date: {date1.strftime('%Y-%m-%d')}\nSubtracted: {days} days"
                )]
        
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
