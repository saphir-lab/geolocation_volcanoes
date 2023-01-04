'''
Author : Philippe Saint-Amand
Date : 2022-11-30

Description:
    Goal of this script is to have possibility of :
    - standard python logging with extra level (SUCCESS)
    - colored console logging
    - Logging to file
    - Possibility to log on both conosle & file but using different formatter for console and log file
'''
import colorama as c
import json
import logging
import os

def get_formatter_definition(fmt_obj) -> str:
    fmt = str(fmt_obj._fmt)
    module_name = str(fmt_obj.__class__.__module__)
    class_name = str(fmt_obj.__class__.__name__)
    result = class_name + "('" + fmt + "')"
    if not module_name == "__main__" : 
        result = module_name + "." + result
    return result

class ColorFormatter(logging.Formatter):
    c.init(autoreset=True)
    color_reset = c.Style.RESET_ALL
    # Change this dictionary to suit your coloring needs!
    COLORS = {
        "DEBUG": c.Fore.MAGENTA,
        "INFO": c.Fore.BLUE,
        "SUCCESS": c.Fore.GREEN,   # This is a custom level
        "WARNING": c.Fore.YELLOW,
        "ERROR": c.Fore.RED,
        "CRITICAL": c.Fore.RED + c.Back.WHITE
    }
    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        if color:           
            record.levelname = color + record.levelname
            record.msg = record.msg  + self.color_reset 
        return logging.Formatter.format(self, record)

class ColorLoggerOptions():
    def __init__(self, 
                console=True, 
                console_formatter = ColorFormatter("%(levelname)s - %(message)s"), 
                console_logging_level = logging.WARNING,
                logfile_name = "",
                logfile_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                logfile_logging_level = logging.DEBUG
                ):
        self.console = console
        self.console_formatter = console_formatter
        self.console_logging_level = console_logging_level
        self.logfile_name = logfile_name
        self.logfile_formatter = logfile_formatter
        self.logfile_logging_level = logfile_logging_level
    
    def to_json(self, indent:int=None):
        result = {
            "console": self.console,
            # "console_formatter":  "ColorFormatter('%(levelname)s - %(message)s')", 
            "console_formatter":  get_formatter_definition(self.console_formatter),
            "console_logging_level": self.console_logging_level,
            "logfile_name": str(self.logfile_name),
            # "logfile_formatter": "logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')",
            "logfile_formatter": get_formatter_definition(self.logfile_formatter),
            "logfile_logging_level": self.logfile_logging_level
        }
        return json.dumps(result, indent=indent)

class ColorLogger(logging.getLoggerClass()):
    def __init__(self, name="default", options=ColorLoggerOptions()):
        logging.Logger.__init__(self, name, logging.DEBUG)
        
        # Will log to a logfile
        if options.logfile_name:
            path = os.path.dirname(os.path.abspath(options.logfile_name))
            if path and not os.path.exists(path):
                try:
                    os.makedirs(path)                   #create logging directory if not exists
                except Exception as e:
                    print(f"Unable to create log directory '{path}'")
                    print(f"Reason: {str(e)}")
                    print(f"Logging to file is disabled")
                else:
                    print(f"Logging directory created '{path}'")
            if os.path.exists(path): 
                fh = logging.FileHandler(options.logfile_name, encoding='utf-8')
                fh.setLevel(options.logfile_logging_level)
                fh.setFormatter(options.logfile_formatter)
                self.addHandler(fh)

        # Put the console handler as last otherwise message is modified with color and appear as well in the file
        if options.console:
            ch = logging.StreamHandler()
            ch.setLevel(options.console_logging_level)
            ch.setFormatter(options.console_formatter)
            self.addHandler(ch)

if __name__ == "__main__":
    # Some usefull variables 
    SUCCESS = 25
    APPNAME, _ = os.path.splitext(os.path.basename(__file__))
    CUR_DIR=os.path.dirname(os.path.abspath(__file__))
    LOG_DIR=os.path.join(CUR_DIR,"log")
    LOGFILE = os.path.join(LOG_DIR,APPNAME+".log")

    # Sample logging creation with logging entries
    logging.addLevelName(SUCCESS, 'SUCCESS')
    log_options = ColorLoggerOptions(logfile_name=LOGFILE, console_logging_level=SUCCESS)
    print(log_options.to_json(indent=4))

    # Uncomment some other options here below to change behavior
    # log_options.logfile_logging_level=logging.INFO
    # log_options.logfile_formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # log_options.console_formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    logger = ColorLogger(name=APPNAME, options=log_options)
    logger.debug('This message should go to the log file')
    logger.info('So should this')
    logger.warning('And this, too')
    logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
    logger.critical('Try a critical message')
    logger.log(SUCCESS, 'Then success level that is a custom level')