class DP_txt_img2img_Switch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["Text_To_Image_Empty_Latent", 
                         "Img2Img_Image_01", 
                         "Img2Img_Image_02", 
                         "Img2Img_Image_03", 
                         "Img2Img_Image_04"], 
                        {"default": "Text_To_Image_Empty_Latent"})
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("mode_setting",)
    FUNCTION = "switch"
    CATEGORY = "DP/utils"

    def switch(self, mode):
        mode_map = {
            "Text_To_Image_Empty_Latent": 0,
            "Img2Img_Image_01": 1,
            "Img2Img_Image_02": 2,
            "Img2Img_Image_03": 3,
            "Img2Img_Image_04": 4
        }
        return (mode_map[mode],)

NODE_CLASS_MAPPINGS = {
    "DP_txt_img2img_Switch": DP_txt_img2img_Switch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_txt_img2img_Switch": "DP Text/Img2Img Switch"
}
