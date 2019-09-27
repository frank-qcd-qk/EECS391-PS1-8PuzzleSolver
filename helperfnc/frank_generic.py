class frank_function:
    """
    Frank's collection of helper functions
    """
    
    def __init__(self):
        pass

    def customPrint(input_str, level=0,DEBUG=False,MINIMAL=True):
        """
        Parameters
        ----------
        input_str : str
            The text string you want to print it out. It must be a string.

        level : int
            The information level of the string.
        """
        message = str(input_str)
        if level == 0:
            if DEBUG:
                print("[DEBUG]"+message)
        elif level == 1:
            if not MINIMAL:
                print("[INFO]"+message)
        elif level == 2:
            print("[WARNING]"+message)
        elif level == 3:
            print("[ERROR]"+message)
        elif level == 4:
            print("[CRITICAL]"+message)
        elif level == 5:
            print("[FATAL]"+message)
        else:
            print(message)
