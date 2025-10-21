from collections import OrderedDict
from uuid import uuid4

from pypiper.datamodel import Source, Output


class Pipeline:

    def __init__(self, name:str, source: Source, run_id=None):
        self.id = uuid4()
        self.name = name
        self.source = source
        self.context = OrderedDict([("source", source)])
        self.tasks = []
        self.run_id = run_id
        self.status = status.PENDING
        self.start_time = None
        self.end_time = None
        self.dependencies = []
        self.parameter_map = {}

    @classmethod
    def build(cls, id, run_id, state):
        pass

    @property
    def output(self):
        last_step = next(reversed(self.context))
        output = data[last_step].read()
        return {
            "output" : output,
            "meta" : {
                "pipeline_name" : self.name,
                "pipeline_id": self.id,
                "run_id": self.run_id,
                "start_time": getattr(self, "start_time", None),
                "start_time" : self.start_time,
                "end_time" : self.end_time,
                "execution_time" : self.end_time - self.start_time,
                "steps" : self.tasks
            }
        }

    @property
    def state(self):
        return {
            "pipeline_name" : self.name,
            "pipeline_id": self.id,
            "run_id": self.run_id,
            "start_time": getattr(self, "start_time", None),
            "end_time": getattr(self, "endtime", None),
            "status": self.status,
            "current_task": self.current_task,
            "context": {name: output.content for name, output in self.context.items()},
            "tasks": [task.name for task in self.tasks],
            "task_state": [task.state for task in tasks],
            "progress": f"{self.tasks.index(self.current_task)} / {len(self.tasks)}",
            "dependencies" : self.dependencies,
            "paramter_map" : self.parameter_map
        }

    def run(self):
        # notifiy pipeline process started
        self.start_time = datetime.now()
        if self.run_id is None:
            self.run_id = uuid4()
        error = None
        for task in self.tasks:
            self.current_task = task
            try:
                # notify task started
                parameters = self.get_task_paramters(task)
                result = task.execute(**parameters)
            except Exception as e:
                # notifiy task failed
                error = PipelineException(**{"task" : task.name, "retries" : task.retries, "error_message" : str(e)})
            else:
                # notify task completed
                self.context[task.name] = result
            finally:
                # persist pipeline current state
                pipeline.orm.save(self.state)
                if error:
                    raise error

        self.end_time = datetime.now()
        # notifiy pipeline process completed

    def register_task(task: callable | Task):
        if callable(task):
            task = Task(process=task)
            task.name = task.process.__name__
        task.status = status.PENDING
        task.pipeline_id = self.id
        task.run_id = self.run_id
        if task.retries is None:
            task.retries = config.retries
        self.dependencies.update(self.check_for_task_dependencies(task))
        self.append(task)
        return task

    def check_for_task_dependencies(self, task):
        """
        Inspect the task’s process method for type annotations that declare
        dependencies on other tasks. And updates paramter map.
        """
        # update paramter map
        # return {task.name : [names of task this task depends on]
        pass

    def get_task_parameters(self, task):
        #{"task7" : {"category_list" : "task_2", "content" : "source", "keywords" : "task3"}}
        task_param_map = self.paramter_map.get(task.name)
        parameter = {key : self.data[value].read() for key, value in task_param_map}
        return paramter


