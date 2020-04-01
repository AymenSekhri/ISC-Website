
class ErrorCodes(object):

    class REGISTER_INPUTS(object):
        NONE = 0
        USEREXISTS = 1
        EMAILEXISTS = 1
        PASSMISSMATCH = 3

    class LOGIN_INPUTS(object):
        NONE = 0
        EMAIL_NOT_FOUND = 1
        PASS_MISMATCH = 1

    class FORGOT_INPUTS(object):
        NONE = 0
        EMAIL_NOT_FOUND = 1
        INVALID_TOKEN = 2

    class EVENT_INPUTS(object):
        NONE = 0
        EVENTEXISTS = 1
        INVALIDDATEFORMAT = 2
        EVENTDOESNOTEXISTS = 3

    class EVENTENROLMENT_INPUTS(object):
        NONE = 0
        DUPLICATES = 1
        EVENTDOESNOTEXISTS = 2
        MAXNUMBEROFENROLMENTS = 3
        ENROLLMENTDOESNOTEXISTS = 4
        ENROLLMENTPASTDEADLINE = 5

    class EVENTMANAGMENT_INPUTS(object):
        NONE = 0
        EVENTDOESNOTEXISTS = 1

    class SESSIONUSERS(object):
        VALID_USER = 0
        NOT_VALID_USER = 1
        USER_PRIV_LEVEL0 = 2
        USER_PRIV_LEVEL1 = 3
        USER_PRIV_LEVEL2 = 4
        USER_PRIV_LEVEL3 = 5
        USER_PRIV_LEVEL4 = 6

    class POSTS(object):
        VALID_POST = 0
        INVALID_POST = 1

    class TEAMUSERS(object):
        VALID_USER = 0
        INVALID_USER = 1
        DUPLICATED_USER = 2


    





