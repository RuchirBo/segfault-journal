import jwt
import sys
print("Imported jwt from:", getattr(jwt, '__file__', 'No __file__ attribute'))
print(jwt.__file__)
print(sys.path)
print("jwt.__spec__:", jwt.__spec__)
