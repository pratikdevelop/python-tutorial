from setuptools import setup

setup(
    name='api',
    version='0.1',
    description='Your API Description',
    packages=['api'],  # Package name without __init__.py
    include_package_data=True,
    install_requires=[
        'pyramid',
        'pyramid_jinja2',
        'mongoengine',
        'bcrypt',
        'pyjwt',
        'waitress',
        'hupper',
    ],
    entry_points={
        'paste.app_factory': [
            'main = api:main',  # Directly reference the main function in index.py
        ],
    },
)
