from abc import ABC, abstractmethod
from typing import List


class Extract(ABC):

    @abstractmethod
    def extract_data(self) -> List[dict]:
        pass
