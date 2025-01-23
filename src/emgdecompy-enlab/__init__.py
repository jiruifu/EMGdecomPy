from . import preprocessing
from . import contrast
from . import decomposition
from . import viz

# read version from installed package
from importlib.metadata import version
__version__ = version("emgdecompy-wenlab")

__all__ = ['preprocessing', 'contrast', 'decomposition', 'viz']