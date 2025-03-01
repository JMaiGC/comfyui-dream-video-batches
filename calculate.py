# -*- coding: utf-8 -*-
import math

from evalidate import Expr, EvalException, base_eval_model

from .categories import *
from .core import *


class DVB_Multiply:
    NODE_NAME = "Multiply"
    ICON = "⦁"
    CATEGORY = NodeCategories.UTILS
    RETURN_TYPES = ("FLOAT", "INT")
    RETURN_NAMES = ("FLOAT", "INT")
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "multiple": ("INT", {"default": 2}),
                "float": ("FLOAT", {"default": 0.0}),
                "int": ("INT", {"default": 0})
            }
        }

    def result(self, multiple, **kwargs):
        f = kwargs.get("float", 0.0)
        i = kwargs.get("int", 0)
        v = f * multiple + i * multiple
        return (v, round(v))


class DVB_Divide:
    NODE_NAME = "Divide"
    ICON = "÷"
    CATEGORY = NodeCategories.UTILS
    RETURN_TYPES = ("FLOAT", "INT")
    RETURN_NAMES = ("FLOAT", "INT")
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "divisor": ("INT", {"default": 2}),
                "float": ("FLOAT", {"default": 0.0}),
                "int": ("INT", {"default": 0})
            }
        }

    def result(self, divisor, **kwargs):
        f = kwargs.get("float", 0.0)
        i = kwargs.get("int", 0)
        v = (f + i) / divisor
        return (v, math.floor(v))


class DVB_Calculation:
    NODE_NAME = "Calculation"
    ICON = "🖩"
    CATEGORY = NodeCategories.UTILS
    RETURN_TYPES = ("FLOAT", "INT")
    RETURN_NAMES = ("FLOAT", "INT")
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "expression": ("STRING", {"default": "a + b + c - (r * s * t)", "multiline": True})
            },
            "optional": {
                "a_int": ("INT", {"default": 0, "multiline": False}),
                "b_int": ("INT", {"default": 0, "multiline": False}),
                "c_int": ("INT", {"default": 0, "multiline": False}),
                "r_float": ("FLOAT", {"default": 0.0, "multiline": False}),
                "s_float": ("FLOAT", {"default": 0.0, "multiline": False}),
                "t_float": ("FLOAT", {"default": 0.0, "multiline": False})
            }
        }

    def _make_model(self):
        funcs = self._make_functions()
        m = base_eval_model.clone()
        m.nodes.append('Mult')
        m.nodes.append('Call')
        for funname in funcs.keys():
            m.allowed_functions.append(funname)
        return (m, funcs)

    def _make_functions(self):
        return {
            "round": round,
            "float": float,
            "int": int,
            "abs": abs,
            "min": min,
            "max": max,
            "tan": math.tan,
            "tanh": math.tanh,
            "sin": math.sin,
            "sinh": math.sinh,
            "cos": math.cos,
            "cosh": math.cosh,
            "pow": math.pow,
            "sqrt": math.sqrt,
            "ceil": math.ceil,
            "floor": math.floor,
            "pi": math.pi,
            "log": math.log,
            "log2": math.log2,
            "acos": math.acos,
            "asin": math.asin,
            "acosh": math.acosh,
            "asinh": math.asinh,
            "atan": math.atan,
            "atanh": math.atanh,
            "exp": math.exp,
            "fmod": math.fmod,
            "factorial": math.factorial,
            "dist": math.dist,
            "atan2": math.atan2,
            "log10": math.log10
        }

    def result(self, expression, **values):
        model, funcs = self._make_model()
        vars = funcs
        for key in ("a_int", "b_int", "c_int", "r_float", "s_float", "t_float"):
            nm = key.split("_")[0]
            v = values.get(key, None)
            if v is not None:
                vars[nm] = v
        try:
            data = Expr(expression, model=model).eval(vars)
            if isinstance(data, (int, float)):
                return float(data), int(round(data))
            else:
                return 0.0, 0
        except EvalException as e:
            on_node_error(DVB_Calculation, str(e))
