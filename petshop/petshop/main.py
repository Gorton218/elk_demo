import random
from os import environ
from time import sleep

from petshop import get_logger
from petshop.ai import AI
from petshop.database_manager import DatabaseConnector
from petshop.identity_manager import IdentityManager
from petshop.request_handler import RequestHandler


def execution_loop(actions):
    rnd = random.Random()
    rnd.seed()
    while True:
        try:
            rnd.choice(actions)()
        except Exception as e:
            logger.exception(e)
        sleep(0.1)


def stable_app():
    identity_manager = IdentityManager()
    database_connector = DatabaseConnector()
    request_handler = RequestHandler()

    actions = []
    actions.extend([identity_manager.scenario_failed_login] * 1)
    actions.extend([identity_manager.scenario_successful_login] * 5)
    actions.extend([database_connector.scenario_query_executed] * 20)
    actions.extend([request_handler.scenario_handle_200] * 20)
    actions.extend([request_handler.scenario_handle_404] * 3)
    execution_loop(actions)


def brutforced_app():
    identity_manager = IdentityManager()
    database_connector = DatabaseConnector()
    request_handler = RequestHandler()

    actions = []
    actions.extend([identity_manager.scenario_brutforce] * 3)
    actions.extend([identity_manager.scenario_failed_login] * 1)
    actions.extend([identity_manager.scenario_successful_login] * 5)
    actions.extend([database_connector.scenario_query_executed] * 20)
    actions.extend([request_handler.scenario_handle_200] * 20)
    actions.extend([request_handler.scenario_handle_404] * 3)
    execution_loop(actions)


def ai_powered():
    identity_manager = IdentityManager()
    database_connector = DatabaseConnector()
    request_handler = RequestHandler()
    ai = AI()

    actions = []
    actions.extend([identity_manager.scenario_failed_login] * 1)
    actions.extend([identity_manager.scenario_successful_login] * 5)
    actions.extend([database_connector.scenario_query_executed] * 20)
    actions.extend([request_handler.scenario_handle_200] * 20)
    actions.extend([request_handler.scenario_handle_404] * 3)
    actions.extend([ai.scenario_failed] * 1)
    execution_loop(actions)


def handler_broken():
    request_handler = RequestHandler()

    actions = []
    actions.extend([request_handler.scenario_handle_500] * 1)
    execution_loop(actions)


if __name__ == '__main__':
    logger = get_logger('main')
    app_ver = environ.get('APP_VER')
    versions = {
        '1.0': brutforced_app,
        '2.0': ai_powered,
        '3.0': handler_broken,
    }
    if app_ver in versions:
        versions.get(app_ver)()
    else:
        stable_app()
