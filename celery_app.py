from celery import Celery

app = Celery(
    'tasks',
    broker='redis://default:redispw@localhost:32768',
    backend='redis://default:redispw@localhost:32768',
    include=['tasks']
)

if __name__ == '__main__':
    app.start()
