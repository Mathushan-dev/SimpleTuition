import os
import sys

# If the project is checked out into a folder with the same name as the repo
# (e.g. /.../TuitionCentreBookingSystem/TuitionCentreBookingSystem), add
# that inner folder to sys.path so `import main` works in CI.
here = os.path.dirname(__file__)
inner = os.path.join(here, os.path.basename(here))
if os.path.isdir(inner) and inner not in sys.path:
    sys.path.insert(0, inner)

# Also ensure repository root is in sys.path
if here not in sys.path:
    sys.path.insert(0, here)
