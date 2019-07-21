from project import db
from project.models import BlogPost

# Create the databse and the tables
db.create_all()

# Insert
db.session.add(BlogPost("Good", "I am Good"))
db.session.add(BlogPost("Well", "I am Well"))
db.session.add(BlogPost("postgres", "setting up PGSQL DB"))

# Commit
db.session.commit()
