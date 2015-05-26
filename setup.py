from setuptools import setup, find_packages

setup(
    name         = 'mongorpc',
    version      = '0.1',
    packages     = find_packages(),
    test_suite   = "mongorpc.tests",
)
