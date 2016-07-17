from distutils.core import setup

long_desc = None
with open('readme.md') as f:
    long_desc = f.read()

setup(
    name='pyhooked',
    packages=['pyhooked'],
    version='1.0.0',
    description='Pure Python hotkey hook, with thanks to pyHook and pyhk',
    long_description=long_desc,
    author='Ethan Smith',
    author_email='mr.smittye@gmail.com',
    url='https://github.com/ethanhs/hooked',
    download_url="https://github.com/ethanhs/pyhooked/archive/master.zip",
    keywords=['hotkey', 'shortcut', 'windows', 'keyboard', 'hooks', 'hook'],
    classifiers=[],
)
