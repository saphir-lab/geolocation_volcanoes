import logging
import os
from utils import Console

# Some interresting path
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CUR_DIR,"data")
LOG_DIR = os.path.join(CUR_DIR,"log")
# LOGFILE = os.path.join(LOG_DIR,"main.log")
OUT_DIR = os.path.join(CUR_DIR,"out")

# Other Constants
BANNER = True
CONSOLE = Console(colored=True)
LOGLEVEL_SUCCESS = 25
LOGLEVEL_DISABLE = 99999
LOGLEVEL_CONSOLE = LOGLEVEL_SUCCESS
# LOGLEVEL_CONSOLE = logging.DEBUG
LOGLEVEL_FILE = LOGLEVEL_DISABLE
LOGLEVEL_FILE = logging.DEBUG

# Constant speficic to this program
CSV_DELIMITER = ","
DATA_FILE = os.path.join(DATA_DIR,"volcanoes_worldwide.csv")
MAP_COLORS=("blue", "orange", "green", "purple", "red", "black", "lightgray", "beige")
OUT_FILE = os.path.join(OUT_DIR,"volcanoes.html")



# To generate Banner, visit https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
banner_lst = [
r"""

 ██▒   █▓ ▒█████   ██▓     ▄████▄   ▄▄▄       ███▄    █  ▒█████  ▓█████   ██████ 
▓██░   █▒▒██▒  ██▒▓██▒    ▒██▀ ▀█  ▒████▄     ██ ▀█   █ ▒██▒  ██▒▓█   ▀ ▒██    ▒ 
 ▓██  █▒░▒██░  ██▒▒██░    ▒▓█    ▄ ▒██  ▀█▄  ▓██  ▀█ ██▒▒██░  ██▒▒███   ░ ▓██▄   
  ▒██ █░░▒██   ██░▒██░    ▒▓▓▄ ▄██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒▒██   ██░▒▓█  ▄   ▒   ██▒
   ▒▀█░  ░ ████▓▒░░██████▒▒ ▓███▀ ░ ▓█   ▓██▒▒██░   ▓██░░ ████▓▒░░▒████▒▒██████▒▒
   ░ ▐░  ░ ▒░▒░▒░ ░ ▒░▓  ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░░ ▒░ ░▒ ▒▓▒ ▒ ░
   ░ ░░    ░ ▒ ▒░ ░ ░ ▒  ░  ░  ▒     ▒   ▒▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░  ░ ░  ░░ ░▒  ░ ░
     ░░  ░ ░ ░ ▒    ░ ░   ░          ░   ▒      ░   ░ ░ ░ ░ ░ ▒     ░   ░  ░  ░  
      ░      ░ ░      ░  ░░ ░            ░  ░         ░     ░ ░     ░  ░      ░  
     ░                    ░                                                           
""",
r"""
 ▌ ▐·      ▄▄▌   ▄▄·  ▄▄▄·  ▐ ▄       ▄▄▄ ..▄▄ · 
▪█·█▌▪     ██•  ▐█ ▌▪▐█ ▀█ •█▌▐█▪     ▀▄.▀·▐█ ▀. 
▐█▐█• ▄█▀▄ ██▪  ██ ▄▄▄█▀▀█ ▐█▐▐▌ ▄█▀▄ ▐▀▀▪▄▄▀▀▀█▄
 ███ ▐█▌.▐▌▐█▌▐▌▐███▌▐█ ▪▐▌██▐█▌▐█▌.▐▌▐█▄▄▌▐█▄▪▐█
. ▀   ▀█▄▀▪.▀▀▀ ·▀▀▀  ▀  ▀ ▀▀ █▪ ▀█▄▀▪ ▀▀▀  ▀▀▀▀ 
""",
r"""                                                                                        
@@@  @@@   @@@@@@   @@@        @@@@@@@   @@@@@@   @@@  @@@   @@@@@@   @@@@@@@@   @@@@@@   
@@@  @@@  @@@@@@@@  @@@       @@@@@@@@  @@@@@@@@  @@@@ @@@  @@@@@@@@  @@@@@@@@  @@@@@@@   
@@!  @@@  @@!  @@@  @@!       !@@       @@!  @@@  @@!@!@@@  @@!  @@@  @@!       !@@       
!@!  @!@  !@!  @!@  !@!       !@!       !@!  @!@  !@!!@!@!  !@!  @!@  !@!       !@!       
@!@  !@!  @!@  !@!  @!!       !@!       @!@!@!@!  @!@ !!@!  @!@  !@!  @!!!:!    !!@@!!    
!@!  !!!  !@!  !!!  !!!       !!!       !!!@!!!!  !@!  !!!  !@!  !!!  !!!!!:     !!@!!!   
:!:  !!:  !!:  !!!  !!:       :!!       !!:  !!!  !!:  !!!  !!:  !!!  !!:            !:!  
 ::!!:!   :!:  !:!   :!:      :!:       :!:  !:!  :!:  !:!  :!:  !:!  :!:           !:!   
  ::::    ::::: ::   :: ::::   ::: :::  ::   :::   ::   ::  ::::: ::   :: ::::  :::: ::   
   :       : :  :   : :: : :   :: :: :   :   : :  ::    :    : :  :   : :: ::   :: : :                              
""",
r"""
@@@  @@@  @@@@@@  @@@       @@@@@@@  @@@@@@  @@@  @@@  @@@@@@  @@@@@@@@  @@@@@@ 
@@!  @@@ @@!  @@@ @@!      !@@      @@!  @@@ @@!@!@@@ @@!  @@@ @@!      !@@     
@!@  !@! @!@  !@! @!!      !@!      @!@!@!@! @!@@!!@! @!@  !@! @!!!:!    !@@!!  
 !: .:!  !!:  !!! !!:      :!!      !!:  !!! !!:  !!! !!:  !!! !!:          !:! 
   ::     : :. :  : ::.: :  :: :: :  :   : : ::    :   : :. :  : :: ::  ::.: :  
""",
r"""
            (                                  
 (   (      )\         )                (      
 )\  )\ (  ((_) (   ( /(   (      (    ))\ (   
((_)((_))\  _   )\  )(_))  )\ )   )\  /((_))\  
\ \ / /((_)| | ((_)((_)_  _(_/(  ((_)(_)) ((_) 
 \ V // _ \| |/ _| / _` || ' \))/ _ \/ -_)(_-< 
  \_/ \___/|_|\__| \__,_||_||_| \___/\___|/__/ 
"""
]


if __name__ == "__main__":  
    CONSOLE.clear_screen()
    if BANNER:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=banner_lst))

    print(f"- CUR_DIR: '{CUR_DIR}'")
    print(f"- DATA_DIR:'{DATA_DIR}'")
    print(f"- LOG_DIR: '{LOG_DIR}'")
    print(f"- OUT_DIR: '{OUT_DIR}'")
