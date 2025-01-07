from dotenv import load_dotenv
import os
from dataclasses import dataclass
load_dotenv()
@dataclass
class ConfiguracionDB:
    DIR_EMAIL :str
    PASS_EMAIL : str


mail=os.getenv('mail')
mailpass=os.getenv('app_pass')

configuracion=ConfiguracionDB(
                               DIR_EMAIL=mail,
                               PASS_EMAIL=mailpass
                              
                               )
   