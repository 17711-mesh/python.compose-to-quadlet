import logging

def configure_logging(level:str="INFO"):
    logging.basicConfig(level=getattr(logging, level), force=True)
