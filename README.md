# mado - a window view into your systems

## Quick Start

Install dependencies
```bash
brew install python-tk
pyenv install 3.12
pip install -r requirements.txt
```
To run:
```bash
python main.py
```

To build into macOS App:

```bash
python setup.py py2app
```

You can run this compiled app like so:

```bash
open dist/Mado.app
```
Alternatively you can run in a debug mode with console logging like so:

```bash
open dist/Mado.app/Contents/MacOS/Mado
```
