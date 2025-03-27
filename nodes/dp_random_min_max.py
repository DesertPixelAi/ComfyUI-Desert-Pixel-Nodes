import random


class DP_random_min_max:
    """Generate random numbers between min and max with specified step size"""

    def __init__(self):
        self.step_options = {
            "int_1": 1,
            "float_0.1": 0.1,
            "float_0.01": 0.01,
            "float_0.001": 0.001,
        }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "min": (
                    "FLOAT",
                    {"default": 0.0, "min": -10000.0, "max": 10000.0, "step": 0.1},
                ),
                "max": (
                    "FLOAT",
                    {"default": 1.0, "min": -10000.0, "max": 10000.0, "step": 0.1},
                ),
                "step": (list(cls().step_options.keys()),),
            }
        }

    RETURN_TYPES = ("FLOAT", "FLOAT", "INT", "INT")
    RETURN_NAMES = ("random_float_1", "random_float_2", "random_int_1", "random_int_2")
    FUNCTION = "generate_random"
    CATEGORY = "DP/utils"

    # Add this flag to force re-execution every time
    IS_CHANGED = True

    def generate_random(self, min, max, step):
        if max <= min:
            raise ValueError("Max value must be greater than min value")

        step_value = self.step_options[step]

        # Validate step size
        if step_value > (max - min):
            raise ValueError(
                f"Step size {step_value} is too large for range {min} to {max}"
            )

        try:
            # Get decimal precision based on step
            if step.startswith("float"):
                decimal_places = len(str(self.step_options[step]).split(".")[-1])
            else:
                decimal_places = 0

            # Generate floats
            if step.startswith("float"):
                steps = int((max - min) / step_value)
                # Format to maintain proper decimal places
                random_float_1 = format(
                    round(
                        min + (random.randint(0, steps) * step_value), decimal_places
                    ),
                    f".{decimal_places}f",
                )
                random_float_2 = format(
                    round(
                        min + (random.randint(0, steps) * step_value), decimal_places
                    ),
                    f".{decimal_places}f",
                )

                # Convert formatted strings back to float
                random_float_1 = float(random_float_1)
                random_float_2 = float(random_float_2)

                # For integers, we'll round the random floats
                random_int_1 = round(min + (random.randint(0, steps) * step_value))
                random_int_2 = round(min + (random.randint(0, steps) * step_value))
            else:  # int_1
                # For integers, we'll use randint directly
                random_int_1 = random.randint(int(min), int(max))
                random_int_2 = random.randint(int(min), int(max))

                # For floats, we'll use the same integers as float values
                random_float_1 = float(random_int_1)
                random_float_2 = float(random_int_2)

            return (random_float_1, random_float_2, random_int_1, random_int_2)

        except Exception as e:
            raise RuntimeError(f"Error generating random numbers: {str(e)}")
