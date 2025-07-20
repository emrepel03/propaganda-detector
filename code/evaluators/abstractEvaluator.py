#This class is only to provide the abstract class meant to serve as the base for all the implemented evaluators

from abc import ABC, abstractmethod

class abstractEvaluator(ABC):


    @abstractmethod
    def evaluate(self, text):
        pass