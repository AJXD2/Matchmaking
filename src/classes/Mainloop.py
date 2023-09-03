import threading
import time
import logging


class MainLoop:
    def __init__(self):
        self.tasks = []
        self.lock = threading.Lock()  # Use a lock for thread safety

    def add_task(self, callable_function, temp=False):
        task_id = len(self.tasks)
        self.tasks.append({"id": task_id, "callable": callable_function, "temp": temp})

    def remove_task(self, task_id):
        with self.lock:
            self.tasks = [task for task in self.tasks if task["id"] != task_id]

    def loop(self, on=True):
        pass

    class Thread(threading.Thread):
        def __init__(self, tasks):
            super().__init__()
            self.stop_flag = threading.Event()  # Thread-safe flag
            self.lock = threading.Lock()
            self.tasks = tasks

        def run(self):
            while not self.stop_flag.is_set():
                tasks_to_remove = []
                with self.lock:
                    for task in self.tasks:
                        try:
                            task["callable"]()
                            if task.get("temp", None) == True:
                                print("removed task with id:", task.get("task_id"))
                                tasks_to_remove.append(task)
                        except AttributeError as e:
                            print(e)
                            tasks_to_remove.append(task)
                    for task in tasks_to_remove:
                        self.tasks.remove(task)

        def stop(self):
            # Set the flag to stop the thread
            self.stop_flag.set()

    def start(self):
        self.loop_thread = self.Thread(self.tasks)
        self.loop_thread.daemon = True

        self.loop_thread.start()

    def stop(self):
        self.loop_thread.stop()
        self.loop_thread.join()
