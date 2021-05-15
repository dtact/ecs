from setuptools import setup, find_packages

setup(
    name='ecs',
    version='0.1.0',
    description='Elastic Common Schema',
    author='Remco Verhoef',
    author_email='remco.verhoef@dtact.com',
    packages=find_packages(where='src'),  # Required
    package_dir={'': 'src'},  # Optional
    install_requires=[
        'python-dateutil'
    ]
)
