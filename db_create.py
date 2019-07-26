from project import db
from project.models import BuySheet, SellSheet, DaySheet, BalSheet, LifeSheet

# Create the database and the tables
db.create_all()

# Insert
#db.session.add(BlogPost("Good", "I am Good"))
#db.session.add(BlogPost("Well", "I am Well"))
#db.session.add(BlogPost("postgres", "setting up PGSQL DB"))

# Commit
db.session.commit()
