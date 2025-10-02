#!/usr/bin/env python3
from typing import List
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import numpy as np
from fastmcp import FastMCP

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

mcp = FastMCP("calculator")

@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate mathematical expressions. Supports +, -, *, /, %, parentheses. Example: '(100 + 50) * 2'
    
    Args:
        expression: Mathematical expression to evaluate
    """
    allowed_chars = set('0123456789+-*/().% ')
    if not all(c in allowed_chars for c in expression):
        return f"Error: Expression contains invalid characters"
    
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {float(result)}\n\nExpression: {expression}"
    except Exception as e:
        return f"Error: Invalid expression: {str(e)}"

@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between units. Supports length (m, km, mile, foot, inch), weight (kg, g, lb, oz), time (second, minute, hour, day), data (byte, kb, mb, gb), and rate (requests/second, requests/minute, requests/hour).
    
    Args:
        value: Value to convert
        from_unit: Source unit
        to_unit: Target unit
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    for category, units in UNIT_CONVERSIONS.items():
        if from_unit in units and to_unit in units:
            base_value = value * units[from_unit]
            result = base_value / units[to_unit]
            return f"Conversion Result: {result:.4f} {to_unit}\n\nFrom: {value} {from_unit}"
    
    return f"Error: Cannot convert from {from_unit} to {to_unit}"

@mcp.tool()
def statistics(numbers: List[float], operation: str) -> str:
    """Calculate statistics on a list of numbers. Operations: mean, median, std, variance, min, max, sum.
    
    Args:
        numbers: List of numbers to analyze
        operation: Statistical operation to perform (mean, median, std, variance, min, max, sum)
    """
    if not numbers:
        return "Error: Numbers list cannot be empty"
    
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
        return f"Error: Unknown operation: {operation}. Available: {', '.join(operations.keys())}"
    
    result = float(operations[operation](arr))
    return f"Statistical Result ({operation}): {result:.4f}\n\nData: {numbers}\nCount: {len(numbers)}"

@mcp.tool()
def date_calculator(date1: str, operation: str, date2: str = "", days: int = 0) -> str:
    """Perform date calculations. Operations: 'difference' (days between dates), 'add_days' (add days to date), 'subtract_days' (subtract days from date).
    
    Args:
        date1: First date in YYYY-MM-DD format or relative like 'today', '2024-12-15'
        operation: Operation to perform (difference, add_days, subtract_days)
        date2: Second date (for 'difference') or leave empty
        days: Number of days (for add_days/subtract_days operations)
    """
    try:
        date1_str = date1.lower()
        if date1_str == "today":
            date1_parsed = datetime.now()
        else:
            date1_parsed = date_parser.parse(date1_str)
        
        if operation == "difference":
            date2_str = date2.lower()
            if date2_str == "today":
                date2_parsed = datetime.now()
            else:
                date2_parsed = date_parser.parse(date2_str)
            
            difference = abs((date2_parsed - date1_parsed).days)
            return f"Date Difference: {difference} days\n\nFrom: {date1_parsed.strftime('%Y-%m-%d')}\nTo: {date2_parsed.strftime('%Y-%m-%d')}"
        
        elif operation == "add_days":
            result_date = date1_parsed + timedelta(days=days)
            return f"Result Date: {result_date.strftime('%Y-%m-%d')}\n\nStarting Date: {date1_parsed.strftime('%Y-%m-%d')}\nAdded: {days} days"
        
        elif operation == "subtract_days":
            result_date = date1_parsed - timedelta(days=days)
            return f"Result Date: {result_date.strftime('%Y-%m-%d')}\n\nStarting Date: {date1_parsed.strftime('%Y-%m-%d')}\nSubtracted: {days} days"
        
        return f"Error: Unknown operation: {operation}"
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
