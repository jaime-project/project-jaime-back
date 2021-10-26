#!env/bin/python
from flask.app import Flask

from logic.apps.admin.config.logger import setup_loggers
from logic.apps.admin.config.app import setup_modules, setup_servers_json
from logic.apps.admin.config.rest import setup_rest
from logic.apps.admin.config.variables import Vars, setup_vars
from logic.apps.works.services.garbage_collector import start_garbage_thread
from logic.libs.variables.variables import get_var

app = Flask(__name__)

setup_vars()
setup_loggers()
setup_rest(app)

start_garbage_thread()
setup_modules()
setup_servers_json()

print("\n\n")
print("> Jaimeeehhhh...!!!")
print("""

                          `+yhyo-                           
                     `.-:/NMMMMMMo/:--`                     
                 `-/osyyyhMMMMMMMmyyyyss+:-`                
              `:osyyyyyyydMMMMMMMmyyyyyyyysso:`             
            .+syyyyyyyyyyyMMMMMMMdyyyyyyyyyyyys+.           
          .+syyyyyyyyyyyysmMMMMMN+osyyyyyyyyyyyys+.   `     
         :syyyyyyyyyys+/-:smMMMmy+``.:+syyyyyyyyyys/+oys.   
       `/syyyyyyyyy+::/sdm:`+N/`:Nds+-``-+sso++yyyyyyyyyo`  
      `+yyyyyyyyysyhmNMMMMN:sMo:NMMMMNmdo-```  -oyys+/-.`   
      /yyyyyyyys+mMMMMMMMMMNNMmNMMMMMMMMMN.  `.-/o.`        
     -syyyyyyyy:.NMMMMMMMMMMMMMMMMMMMMMMMM+/oossss/         
     +yyyyyyyy+  hMMMMMMMMMMMMMMMMMMMMMMMMsssssssss.        
    `syyyyyyys. `+MMMMMMMMMMMMMMMMMMMMMMMMsssssssss+        
    .yyyyyyyys+os+NMMMMMMMMMMMMMMMMMMMMMMM+sssssssss.-:+-   
    -so++yyyyyyyy+hMMMMMMMy+hMo+++++sMMMMM/sssosyyyysyyy:   
    ``` .yyyso+/-./MMMMMMM+ oM.     :MMMMm-:-..syyyyyyyy.   
       `.o:-.`    `NMMMMMMy/yM.     :Mmyo.    :yyyyyyyys    
  `.:/+oss-        hdNMMMMMMMM.     :M/      .oyyyyyyyy/    
 -sssssssso`       +:oMMMMMMMM.`````:M/     .oyyyyyyyyo`    
 `osssssssso.      `oNMMMMMMMM..```.:Ms   `:syyyyyyyys.     
  .ssssssssss/.-/+o:.-sMMMMMMM-.```.:Mh `:oyyyyyyyyys-      
   .osssooyyyyyyyyyys++MMMMMMM:.---./hs/syyyyyyyyyyo.       
    `:-.``/syyyyyyyyyysNMMMMMMNNNNNmsyyyyyyyyyyyys/`        
           ./syyyyyyyysdMMMMMMMMMMMmyyyyyyyyyyyo/.          
             `:osyyyyyyyMMMMMMMMMMMdyyyyyyyyso:`            
                .:ossyysMMMMMMMMMMMyyyyysso:.               
                   `.:/+mMMMMMMMMMMoso/:-`                  
                        sMMMMMMMMMd`                        
                        /MMMMMMMMMs                         
                        .MMMMMMMMM:                         
                         mMMMMMMMM`                         
                        -dMMMMMMMN:`                        
                     `/ydddddddddddh+.                      
                                                                                
""")

if __name__ == "__main__":
    flask_host = get_var(Vars.PYTHON_HOST)
    flask_port = int(get_var(Vars.PYTHON_PORT))

    app.run(host=flask_host, port=flask_port, debug=False)
