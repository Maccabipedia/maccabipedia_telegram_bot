from setuptools import setup, find_packages

__version__ = "0.14.4"

setup(
    name='maccabipediabot',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='MaccabiPedia telegram bot for Maccabi Tel-Aviv fans.',
    long_description="MaccabiPedia telegram bot for Maccabi Tel-Aviv fans, including statistics and crawling from maccabipedia.co.il.",
    long_description_content_type='text/markdown',
    python_requires='>=3',
)
