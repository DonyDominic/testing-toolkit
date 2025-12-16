import builtins 
from toolkit.decorators import test,skip

#injects test decorator into Python global namespace.
setattr(builtins, "test", test)
setattr(builtins, "skip", skip)

