import sys
from remote.remote import *

if len(sys.argv) == 1:
    sys.exit(0)

if sys.argv[1] == "create":
    r = create_remote()
    r.create_repository("testing", "bachler-testing-student", private=False)

elif sys.argv[1] == "delete":
    r = create_remote()
    r.delete_repo("testing")

