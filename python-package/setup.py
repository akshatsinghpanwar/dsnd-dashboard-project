from pathlib import Path
from setuptools import setup, find_packages

cwd = Path(__file__).resolve().parent
requirements = (cwd / 'employee_events' / 'requirements.txt').read_text().splitlines()
requirements = [line.strip() for line in requirements if line.strip() and not line.strip().startswith('#')]

setup_args = dict(
    name='employee_events',
    version='0.0.1',
    description='SQL Query API',
    packages=find_packages(),
    include_package_data=True,
    package_data={'employee_events': ['employee_events.db', 'requirements.txt']},
    install_requires=requirements,
)

if __name__ == "__main__":
    setup(**setup_args)