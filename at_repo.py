

def b_at204_read_dev_rev():
    """
        Get device revision
        DevRev command returns a single four-byte word representing the revision number
        of the device. Software should not
        depend on this value as it may change from time to time
    """
    return b'\x77\x30\x00\x00'


def b_at204_empty_8():
    """
        Empty buffer to check if device is present
    """
    return b'\x00\x00\x00\x00\x00\x00\x00\x00'

