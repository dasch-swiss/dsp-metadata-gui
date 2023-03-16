
from pathlib import Path
from tinydb import TinyDB

from models import Project


db_path: Path = Path.home() / ".dsp-meta" / "db.json"
db = TinyDB(db_path)
print(db.all())
p = Project(shortcode="0123", name="test2", description="lorem ipsum")
print(p.__dict__)
db.insert(p.__dict__)
print(db.all())
pp = db.all()
p1 = pp.pop()
print(Project(**p1))
