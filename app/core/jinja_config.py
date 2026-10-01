from jinja2 import Environment, FileSystemLoader, select_autoescape
from starlette.templating import Jinja2Templates

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"])
)

templates = Jinja2Templates(directory="templates")
templates.env = env

def get_templates():
    return templates
