import time

import click
from src.agent import BanditAgent

# Running inside docker container 
LOCALHOST = 'http://user_service:8000/'
CONFIG = 'configs/bandits_config.yaml'

# Local runnig
# LOCALHOST = 'http://127.0.0.1:8000/'
# CONFIG = 'configs/agent/bandits_config.yaml'

@click.command()
@click.argument('bandit_name', type=click.STRING)
def main(bandit_name: str) -> None:

    bandit = BanditAgent(
        bandit_conf=CONFIG,
        bandit_name=bandit_name,
        host_address=LOCALHOST,
    )
    while True:
        bandit.form_recommendation()
        time.sleep(0.5)


if __name__ == '__main__':
    main()