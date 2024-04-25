from app import start_forum

forum = start_forum()

#This line allows import of main.py without running forum automatically
if __name__ == '__main__':
    forum.run(debug=True)