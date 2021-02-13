import threading
import os

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self.stopped = False

    def run(self):
        os.system("python -m start")
        # subprocess.call(["python","-m","start"]) 

    def stop(self):
        self.stopped = True

jeu = StoppableThread()
jeu.start()
jeu.stop()
jeu.join()
