import typing as tp

import numpy as np
from src.base import Bandit


class EpsilonGreedy(Bandit):
    """Bandit with Epsilon Greedy strategy.
    """
    def __init__(
        self,
        n_arms: int,
        n_picks: int,
        epsilon: float,
    ):
        super().__init__(n_arms, n_picks)
        self.epsilon = epsilon
        
    def choose_arms(self) -> tp.List[int]:
        """
        Choose arms according Epsilon Greedy strategy. 
  
        Returns:
            tp.List[int]: list of chosen arms.
        """
        if np.random.random() < self.epsilon:
            arms = np.random.choice(self.n_arms, size=self.n_picks, replace=False)
        else:
            arms = np.argsort(self.values)[::-1][:self.n_picks]
        return arms.tolist()

    # TODO: Learning from rewards with alpha parameter
    def update_values(
        self,
        chosen_arms: tp.List[int],
        values: tp.List[float]
    ) -> None:
        """Update arms statistic for learning.

        Args:
            chosen_arms (tp.List[int]): arms to update
            values_set (tp.List[float]): arms's rewards
        """
        for arm, value in zip(chosen_arms, values):
            self.counts[arm] += 1
            self.values[arm] += (value - self.values[arm]) / self.counts[arm]


class UCB(Bandit):
    """Bandit with Upper Confident Bound strategy.
    """

    def choose_arms(self) -> tp.List[int]:
        """
        Choose arms according Upper Confidence Bound strategy. 

        Returns:
            tp.List[int]: list of chosen arms.
        """
        zeros_arms = []
        for arm in range(self.n_arms):
            if self.counts[arm] == 0:
                zeros_arms.append(arm)
            if len(zeros_arms) == 3:
                return zeros_arms

        ucb_values = [0. for _ in range(self.n_arms)]
        total_counts = sum(self.counts)

        for arm in range(self.n_arms):
            bonus = np.sqrt((2.0 * np.log(total_counts)) / (float(self.counts[arm]) + 1e-10))
            ucb_values[arm] = self.values[arm] + bonus

        return np.argsort(ucb_values)[::-1][:self.n_picks].tolist()

    def update_values(
        self,
        chosen_arms: tp.List[int],
        values: tp.List[float],
    ) -> None:
        """Update arms statistic for learning.

        Args:
            chosen_arms (tp.List[int]): arms to update
            values_set (tp.List[float]): arms's rewards
        """
        for arm, value in zip(chosen_arms, values):
            self.counts[arm] += 1
            self.values[arm] += (value - self.values[arm]) / self.counts[arm]
