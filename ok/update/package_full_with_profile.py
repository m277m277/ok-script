import sys

import os.path

import json
from ok.logging.Logger import config_logger, get_logger
from ok.update.init_launcher_env import create_app_env
from ok.util.path import delete_if_exists

logger = get_logger(__name__)

if __name__ == "__main__":
    config_logger(name='build')
    try:
        # Get the folder path from the command line arguments
        tag = sys.argv[1]
        profile_index = int(sys.argv[2])
        logger.info(f'Tag: {tag} profile {profile_index}')

        build_dir = os.path.join(os.getcwd(), 'dist')
        repo_dir = os.path.join(build_dir, 'repo', tag)

        logger.info(f'Build directory: {repo_dir}')

        launcher_json = os.path.join(repo_dir, 'launcher.json')
        with open(launcher_json, 'r', encoding='utf-8') as file:
            launch_profiles = json.load(file)
            if not launch_profiles:
                logger.error('not launch profiles')
                sys.exit(1)

        profile = launch_profiles[profile_index]

        delete_if_exists(os.path.join(build_dir, 'python', 'app_env'))

        launcher_config_json = os.path.join(build_dir, 'configs', 'launcher.json')

        with open(launcher_config_json, 'r', encoding='utf-8') as file:
            config = json.load(file)
            config['app_dependencies_installed'] = True
            config['profile_index'] = profile_index

        with open(launcher_config_json, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)

        if not create_app_env(repo_dir, build_dir, profile['install_dependencies']):
            logger.error('not create app env')
            sys.exit(1)

        logger.info(f'installed profile: {profile}')

    except Exception as e:
        logger.info(f'Error: {e}')
        sys.exit(1)
