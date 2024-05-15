from app import start_forum
from app.config import DeploymentConfig

forum = start_forum(DeploymentConfig)

#This line allows import of main.py without running forum automatically
if __name__ == '__main__':
    forum.run(debug=True)