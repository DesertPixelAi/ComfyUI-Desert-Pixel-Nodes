class DP_Switch_Controller:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Mode_Settings": (["Txt2Image", "Img2Img"], {"default": "Txt2Image"}),
                "IPadapter_Mode": (["IPadapter_OFF", "IPadapter_ON"], {"default": "IPadapter_OFF"}),
                "ControlNet_mode": (["Controlnet_OFF", "Controlnet_ON"], {"default": "Controlnet_OFF"}),
            }
        }

    RETURN_TYPES = ("SWITCH_SETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, Mode_Settings, IPadapter_Mode, ControlNet_mode):
        settings = (Mode_Settings, IPadapter_Mode, ControlNet_mode)
        return (settings,) 

