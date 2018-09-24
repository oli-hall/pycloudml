from setuptools import setup

install_requires = [
    'google-api-python-client==1.7.4',
]

test_requires = [
]

setup(
    name='pycloudml',
    version='0.1.0',
    author='Oli Hall',
    author_email='',
    description="Python wrapper for the Google CloudML client",
    license='MIT',
    url='https://github.com/oli-hall/pycloudml',
    packages=['pycloudml'],
    setup_requires=[],
    install_requires=install_requires,
    tests_require=test_requires,
)
