# Copyright (c) 2003-2015, Xively. All rights reserved.
# This is part of Xively Python library.

import os
import sys

class XivelyResourceTypes:

    RESOURCETYPE_BEGIN = 0
    CERTIFICATE_STORE = RESOURCETYPE_BEGIN
    CERTIFICATE = 2
    CREDENTIALS = 3
    BACKOFF_LUT = 4
    DECAY_LUT = 5
    DOMAIN_NAMES = 6
    RESOURCETYPE_END = 7

    def __init__(self):
        pass


class XivelyResourceManager:

    MODE_READ = "rb"
    MODE_WRITE = "wb"

    EXTENSIONS = ["cert_store","certificate","credentials","backoff_lut","decay_lut","domain_names"]

    def __init__(self):
        pass

    @staticmethod
    def stat(resource_type, filename):

        assert resource_type < XivelyResourceTypes.RESOURCETYPE_END
        assert resource_type >= XivelyResourceTypes.RESOURCETYPE_BEGIN

        absolute = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "resources", filename + "." + XivelyResourceManager.EXTENSIONS[resource_type])

        exists = os.path.exists(absolute)
        isfile = os.path.isfile(absolute)
        filesize = 0
        if isfile:
            filesize = os.path.getsize(absolute)
        return exists and isfile, filesize

    @staticmethod
    def open(resource_type, filename, mode):

        assert resource_type < XivelyResourceTypes.RESOURCETYPE_END
        assert resource_type >= XivelyResourceTypes.RESOURCETYPE_BEGIN
        assert mode == XivelyResourceManager.MODE_READ or mode == XivelyResourceManager.MODE_WRITE

        absolute = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "resources")

        if not os.path.exists(absolute) and mode is XivelyResourceManager.MODE_WRITE:
            try:
                os.makedirs(absolute,exist_ok=True)
            except Exception as error:
                return False, None

        try:
            absolute = os.path.join(absolute, filename + "." + XivelyResourceManager.EXTENSIONS[resource_type])
            handle = open(absolute, mode)
            return True, handle
        except IOError as error:
            return False, error
        except Exception as error:
            return False, error

    @staticmethod
    def close(resource_handle):

        assert resource_handle is not None

        try:
            resource_handle.close()
            return True, None
        except IOError as error:
            return False, error

    @staticmethod
    def read(resource_handle):

        assert resource_handle is not None

        try:
            data = resource_handle.read()
            return True, data
        except IOError as error:
            return False, error

    @staticmethod
    def write(resource_handle, data):

        assert resource_handle is not None

        try:
            resource_handle.write(data)
            return True, None
        except IOError as error:
            return False, error

    @staticmethod
    def remove(resource_type, filename):

        assert resource_type < XivelyResourceTypes.RESOURCETYPE_END
        assert resource_type >= XivelyResourceTypes.RESOURCETYPE_BEGIN

        absolute = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "resources", filename + "." + XivelyResourceManager.EXTENSIONS[resource_type])

        exists = os.path.exists(absolute)

        if not exists:
            return True

        try:
            os.remove(absolute)
            return True, None
        except IOError as error:
            return False, error
