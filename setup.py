from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('requirements-test.txt') as f:
    requirements_test = f.read().splitlines()

setup(
    name='delivery_system',
    version='1.0.0',
    author="Varvara Minkina",
    description="Simple version of delivery system",
    url="https://github.com/Varenique/Delivery_system",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={'test': requirements_test}
)
