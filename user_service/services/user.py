import typing as tp

import numpy as np
from omegaconf import OmegaConf


class User:
    
    """
    Environment class for imitating user's behavior.
    
    Args:
        preferences (tp.Union[OmegaConf, str]): 
            User's preferences represented as dict, where key is widget's id.
            Parameter could be passed as a path to config or dict.
    """
    
    def __init__(
        self,
        preferences: tp.Union[OmegaConf, str],
    ) -> None:
        self.preferences = read_config(preferences)

    def watch_widgets(
            self,
            widgets: tp.List[str],
            separate_return: bool=True,
    ) -> tp.Union[tp.List[float], float]:
        """
        Give time which user have spent for interacting with widgets.

        Args:
            widgets (tp.List[str]): list of widgets
        
        Returns:
            tp.Union[tp.List[float], float]: list of time spent for interacting with each widget.
        """
        watch_time = [self._watch(widget_id) for widget_id in widgets]
        
        return watch_time

    def _watch(self, widget_id: str) -> float:
        """
        Sampling value from lognormal distribution for provided widget using user's preferences.

        Args:
            widget_key (str): widget's key from preferences dict

        Returns:
            float: random value from lognormal distribution
        """
        watch_time = np.random.lognormal(
            mean=self.preferences[widget_id]['mean'],
            sigma=self.preferences[widget_id]['sigma'],
        )
        return watch_time
    

def read_config(config: tp.Union[dict, str]) -> dict:
    """Managing how preferences config was passed and give it to user. 

    Args:
        config (tp.Union[dict, str]):
            path to config or dict object, where key is widget's id.

    Returns:
        dict: user's preferences as dict.
    """
    if isinstance(config, str):
        return OmegaConf.load(config)
    return config

