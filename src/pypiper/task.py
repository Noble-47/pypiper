from typing import Optional


class Task:

    def __init__(
        self,
        name: str = None,
        process: Optional[callable] = None,
        retries: Optional[int] = None,
        pipeline_id: Optional[UUID] = None,
        status: Optional[Status] = status.PENDING,
    ):
        self.events = []
        self.retries = retries
        self.status = status
        self.pipeline_id = pipeline_id
        self.run_id = run_id
        self._callable_process = process
        self.extra_context = {}

    @property
    def callable_process(self):
        """Return the function that will be called when the pipeline runs the task."""
        # Used mainly for process inspection when getting task dependencies
        if self._callable_process:
            # if `process` is passed as an initialization argument
            # use it
            return self._callable_process

        elif hasattr(self, 'process'):
            # For Task subclasses, return process method
            # if it was redefined
            return self.process

    @property
    def state(self):
        state = {
            "name" : self.name,
            "pipeline_id" : self.pipeline_id,
            "run_id" : self.run_id,
            "status" : self.status,
            "retries" : self.retries,
        }
        if self.extra_context:
            extra['extra'] = self.extra_context
        return state

    def execute(self, *args, **kwargs):
        # Called by the pipeline
        retries = self.retries
        while retries:
            try:
                output = self.callable_process(*args, **kwargs)
            except Exception as e:
                if retries == 0:
                    raise e
                retries -= 1
            else:
                break
        return output
