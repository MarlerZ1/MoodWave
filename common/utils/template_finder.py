import os


def find_templates_dirs(apps_base):
    templates_dirs = []
    for app in os.listdir(apps_base):
        app_path = apps_base / app

        potential_templates_dir = app_path / 'web' / 'templates'
        if potential_templates_dir.exists():
            templates_dirs.append(str(potential_templates_dir))
    return templates_dirs