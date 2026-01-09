from dataclasses import dataclass

@dataclass
class Album:
    id : int
    title : str
    duration : str

    def __str__(self):
        return f'- {self.title} ({self.duration:.2f} min)'

    def __hash__(self):
        return hash(self.id)