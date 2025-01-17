import time

def check_for_more(chunk:str):
    """ 
    Check for pagination prompt '--More--'
    """
    if "--More--" in chunk:
        return True
    elif "#" in chunk or ">" in chunk:  # Adjust prompt detection as needed for more types
        return False
    
    raise Exception("Problem occured with recieved chunk -- check newline symbol")

def is_timed_out(start_time, timeout):
    """
    Check if the elapsed time since start_time has exceeded the timeout value.
    """
    return time.time() - start_time >= timeout