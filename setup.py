from setuptools import setup, find_packages

__version__ = "0.13.1"

setup(
    name='maccabipediabot',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='MaccabiPedia telegram bot for Maccabi Tel-Aviv fans.',
    long_description="MaccabiPedia telegram bot for Maccabi Tel-Aviv fans, including statistics and crawling of maccabipedia.co.il.",
    long_description_content_type='text/markdown',
    python_requires='>=3',
    install_requires=["python-telegram-bot>=12.4.2, <13",
                      "decorator>=4.4.2, <5",
                      "python-dotenv>=0.12.0, <0.13",
                      "maccabistats>=2.17",
                      "requests>=2.20.0"]
)
