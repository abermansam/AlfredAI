from setuptools import setup, find_packages

setup(
    name="alfredAI",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'google-api-python-client',
        'google-auth',
        'google-auth-oauthlib',
        'openpyxl',
        'xlwings',
        'requests',
        'beautifulsoup4',
        'pandas',
        'loguru',
        'PyYAML',
        'pytest',
        'pytest-mock',
        'ollama',
        'openai',
    ],
) 