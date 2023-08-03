import typing as tp
from abc import ABC, abstractmethod

import numpy as np


class Bandit(ABC):
    """Abstract class for all bandit types.

    Args:
        n_arms (int): total number of arms.
        n_picks (int): how many arms will be used in a same time.
    """
    def __init__(
        self,
        n_arms: int,
        n_picks: int
    ) -> None:

        self.n_arms: int = n_arms
        self.n_picks: int = n_picks
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)
        
        
        @abstractmethod
        def choose_arms(self) -> tp.List[int]:
            """
            Choose arms according specified strategy. 
            
            Returns:
                tp.List[int]: list of chosen arms.
            """
            pass

        @abstractmethod
        def update_values(
            self,
            chosen_arms: tp.List[int],
            values_set: tp.List[float]
        ):
            """Update arms statistic for learning.

            Args:
                chosen_arms (tp.List[int]): arms to update
                values_set (tp.List[float]): arms's rewards
            """
            pass
