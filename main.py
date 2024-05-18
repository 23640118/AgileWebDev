from app import start_forum, db
from app.config import DeploymentConfig
from flask_migrate import Migrate

forum = start_forum(DeploymentConfig)
migrate = Migrate(forum, db)

#This line allows import of main.py without running forum automatically
if __name__ == '__main__':
    forum.run(host='0.0.0.0', debug=True)
