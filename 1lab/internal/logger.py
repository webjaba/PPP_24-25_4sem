import logging
import sys

def set_up_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(name)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
