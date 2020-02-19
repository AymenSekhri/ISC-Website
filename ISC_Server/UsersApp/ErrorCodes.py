
class ErrorCodes(object):

    class REGISTER_INPUTS(object):
        NONE = 0
        USEREXISTS = 1
        EMAILEXISTS = 2
        PASSMISSMATCH = 3

    class LOGIN_INPUTS(object):
        NONE = 0
        EMAIL_NOT_FOUND = 1
        PASS_MISMATCH = 2

    class FORGOT_INPUTS(object):
        NONE = 0
        EMAIL_NOT_FOUND = 1
        INVALID_TOKEN = 2

    class EVENT_INPUTS(object):
        NONE = 0
        EVENTEXISTS = 1

    class EVENTENROLMENT_INPUTS(object):
        NONE = 0
        DUPLICATES = 1
        EVENTDOESNOTEXISTS = 2
        MAXNUMBEROFENROLMENTS = 3
        ENROLLMENTDOESNOTEXISTS = 4
        ENROLLMENTPASTDEADLINE = 4

    class EVENTMANAGMENT_INPUTS(object):
        NONE = 0
        EVENTDOESNOTEXISTS = 1

    class SESSIONUSERS(object):
        VALID_USER = 0
        NOT_VALID_USER = 1

    





