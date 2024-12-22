class DP_Switch_Controller:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Mode_Settings": (["Txt2Image", "Img2Img"], {"default": "Txt2Image"}),
                "Model_mode": (["Model_Dry", "Model_Lora", "Model_Ip_Adapter"], {"default": "Model_Dry"}),
                "ControlNet_mode": (["Controlnet_OFF", "Controlnet_ON"], {"default": "Controlnet_OFF"}),
            }
        }

    RETURN_TYPES = ("SWITCH_SETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, Mode_Settings, Model_mode, ControlNet_mode):
        settings = (Mode_Settings, Model_mode, ControlNet_mode)
        return (settings,) 

