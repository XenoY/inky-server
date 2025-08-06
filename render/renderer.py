import subprocess
from jinja2 import Environment
from jinja2 import FileSystemLoader
from datetime import datetime
import requests
import asyncio
from pyppeteer import launch
from pathlib import Path
import pathlib
from PIL import Image

class Renderer:
    resolution = (1200,800)
    treshold = 87
    
    @property
    def handle(self):
        raise NotImplementedError
    
    @property
    def template_file(self):
        return f"{self.handle}.html"

    @property
    def html_file(self):
        return f"static/{self.handle}/{self.handle}.html"

    @property
    def image_file(self):
        return f"static/{self.handle}/{self.handle}.png"

    @property
    def template_properties(self):
        return {
            "width": self.resolution[0],
            "height": self.resolution[1]
        }

    def build_html(self):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template(self.template_file)
        
        today = datetime.now().strftime("%d.%m.%Y")
        html_out = template.render(**self.template_properties)
        
        html_file = self.html_file
        with open(html_file, 'w') as f:
            f.write(html_out)
        
        print(f'HTML generiert: {html_file}')

    def render_html_to_image(self, html_path, output_path):
        html_path = pathlib.Path(html_path).resolve()  # Absoluter Pfad
        resolution = [
            self.resolution[0],
            self.resolution[1] + self.treshold
        ]
        subprocess.run([
            "/snap/bin/chromium",
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--run-all-compositor-stages-before-draw",
            f"--window-size={','.join(map(str,resolution))}",
            f"--screenshot={output_path}",
            # "--virtual-time-budget=1000",
            f"file://{html_path}"
        ], check=True)

        
    def render_image(self):
        self.build_html()
        self.render_html_to_image(self.html_file, self.image_file)
        image = Image.open(self.image_file)
        image_cropped = image.crop((0, 0, self.resolution[0], self.resolution[1]))
        image_cropped.save(self.image_file)
        # subprocess.run(["python3", "renderer.py", 'static/wortuhr.html', 'static/wortuhr.png'])