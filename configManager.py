from pygame import locals
import re
import typing

class Config():
    def __init__(self, conf: dict):
        assert isinstance(conf["car_maniability"],(int,float)), "Invalid type for car_maniability"
        self.car_maniability: float = conf["car_maniability"]
        assert hasattr(locals,conf["left_key"]) and conf["left_key"].startswith("K_"), "Invalid control for left_key"
        self.left_key = getattr(locals,conf["left_key"])
        assert hasattr(locals,conf["right_key"]) and conf["right_key"].startswith("K_"), "Invalid control for right_key"
        self.right_key = getattr(locals,conf["right_key"])
        assert isinstance(conf["manual_control"], bool), "Invalid type for manual_control"
        self.manual_control: bool = conf["manual_control"]
        assert conf["display_rays"] in ["None", "Ray", "Cross"], "Invalid option for display_rays"
        self.display_rays: typing.Optional[str] = conf["display_rays"]
        if self.display_rays == "None":
            self.display_rays = None
        assert isinstance(conf["cars_number"], int), "Invalid type for cars_number"
        self.cars_number: int = conf["cars_number"]
        assert re.match(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", conf["car_color"]), "Invalid hex code for car_color"
        self.car_color: str = conf["car_color"]
        assert isinstance(conf["screen_size"],list) and len(conf["screen_size"])==2 and all(isinstance(i,int) for i in conf["screen_size"]), "Invalid formar for screen_size"
        self.screen_size: typing.List[int] = conf["screen_size"]
        assert conf["theme"] in ["dark", "light"], "Invalid option for theme"
        self.theme: str = conf["theme"]