import json
import time
import typing as tp

import requests
from omegaconf import OmegaConf
from src.bandits import UCB, EpsilonGreedy
from src.base import Bandit


class BanditAgent:
    """Multi-armed bandits for widget recommendation.

    A general class for interacting with the User class
    using multi-armed bandits to provide widget recommendations.

    Args:
        bandit_conf (tp.Union[str, OmegaConf]): config for bandit.
        bandit_name (str): bandit strategy. Could be [epsilon_greedy, ucb]
        host_address (str): address for requesting widgest's timespent.
    """

    def __init__(
        self,
        bandit_conf: dict,
        bandit_name: str,
        host_address: str,
    ) -> None:

        self.bandit: Bandit = init_bandit(bandit_name, bandit_conf)
        self.host_address = host_address

    def request_timespent_from_user(
        self,
        widget_set: tp.List[int],
    ) -> tp.List[float]:
        """Request watch time for a widget set.

        Args:
            widget_set (tp.List[int]): set of widgets.

        Returns:
            tp.List[float]: list of time spent for watching widgets.
        """
        try:
            widgets = {
                'widgets': widget_set,
            }
            payload = json.dumps(widgets)
            headers = {'Content-Type': 'application/json'}
            response = requests.get(
                url='{0}{1}'.format(self.host_address, 'watch'),
                data=payload,
                headers=headers,
                timeout=1,
            )

            if response.status_code == 200:
                return response.json()['timespent']
            else:
                print(
                    'Something went wrong, but server is runnig!\n'
                    + 'Please, check request parameters.',
                )
        except requests.exceptions.RequestException as exc:
            print(f'Host is not avalaible! Wait for 1 sec.')
            time.sleep(1)

    def form_recommendation(self) -> tp.List[int]:
        """Process information gained from user to from recommendations.

        Returns:
            tp.List[int]: list of widgets
        """
        chosen_arms = self.bandit.choose_arms()
        timespent_set = self.request_timespent_from_user(chosen_arms)
        if timespent_set:
            self.bandit.update_values(chosen_arms, timespent_set)


def bandit_mapper(bandit_name: str) -> Bandit:
    """Process string of bandit name for getting it's object.

    Args:
        bandit_name (str): bandit name

    Raises:
        AttributeError: If passed parameter is not str or unknown value.

    Returns:
        Bandit: requested bandit class object.
    """
    if isinstance(bandit_name, str):
        if bandit_name == 'epsilon_greedy':
            return EpsilonGreedy
        if bandit_name == 'ucb':
            return UCB
    else:
        raise AttributeError(
            'Please pass the valid bandit_name as str!\n'
            + f'Got <{type(bandit_name)}> instead.\n'
            + 'Please, use one of these: [epsilon_greedy, UPB]',
        )


def init_bandit(
    bandit_name: str,
    bandit_conf: tp.Union[str, OmegaConf]
) -> Bandit:

    """Initialize bandit class using parameters from config file.

    Args:
        bandit_name (str): bandit name.
        bandit_conf (tp.Union[str, OmegaConf]): config with bandit's parameters.

    Returns:
        Bandit: initialized bandit class.
    """
    bandit_name = bandit_name.lower()
    bandit_conf = read_config(bandit_conf)
    bandit_obj = bandit_mapper(bandit_name)
    return bandit_obj(**bandit_conf[bandit_name])


def read_config(config: tp.Union[dict, str]) -> dict:
    """Managing how preferences config was passed and give it to user. 

    Args:
        config (tp.Union[dict, str]): path to config or dict object, where key is widget's id.

    Returns:
        dict: user's preferences as dict.
    """
    if isinstance(config, str):
        return OmegaConf.load(config)
    return config
