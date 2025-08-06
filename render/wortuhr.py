from render.renderer import Renderer

class Wortuhr(Renderer):
    handle = "wortuhr"


    
    @property
    def template_properties(self) -> dict:
        properties = super().template_properties
        properties.update(background="rgb(5, 114, 113)")
        return properties

