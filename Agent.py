from abc import abstractmethod, ABC
class Agent(ABC):
  @abstractmethod
  def move(self,possible_moves):
    pass