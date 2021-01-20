from setuptools import find_packages, setup

setup(
    name='delivery_system',
    version='1.0.0',
    author="Varvara Minkina",
    description="Simple version of delivery system",
    url="https://github.com/Varenique/Delivery_system",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=1.1.2',
        'Jinja2>=2.11.2',
        'MarkupSafe>=1.1.1',
        'Werkzeug>=1.0.1',
        'python-dotenv>=0.15.0',
        'flasgger>=0.9.5',
        'py>=1.10.0',
        'PyYAML>=5.3.1',
        'pytest>=6.2.1',
        'pytest-mock>=3.5.1'
    ]
)
