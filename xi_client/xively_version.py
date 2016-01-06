# Copyright (c) 2003-2015, LogMeIn, Inc. All rights reserved.
# This is part of Xively Python library.

class XivelyClientVersion:
    major = 0
    minor = 7
    revision = 0

    @staticmethod
    def get_version_string():
        return str(XivelyClientVersion.major) \
        + "." + str(XivelyClientVersion.minor) \
        + "." + str(XivelyClientVersion.revision)
