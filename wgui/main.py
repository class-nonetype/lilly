
import os
import getpass
import socket
import asyncio
import requests
import json





global user
global execution
global session
global struct
global logo



logo = str('''

.__  .__.__  .__         
|  | |__|  | |  | ___.__.
|  | |  |  | |  |<   |  |
|  |_|  |  |_|  |_\___  |
|____/__|____/____/ ____|
                  \/   
                 terminal

''')

execution_path = os.path.dirname(os.path.realpath(__file__))
storage_path = os.path.join(execution_path, 'storage')

struct = {
    'path' : {
        'execution' : execution_path,
        'storage' : storage_path,
    }
}

user = getpass.getuser()
execution = True
session = socket.gethostname() + '@' + user




async def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


async def command(operation):
    
    
    commands = {
        'cls'   : clear,
        'clear' : clear,
        
        'request' : request
    }
    
    
    operation = operation.split(' ')

    
    if operation[0] in commands.keys():
        if len(operation) == 1:
            await commands[str(operation[0])]()
        
        elif len(operation) == 2:
            await commands[str(operation[0])](operation[1])

        elif len(operation) == 3:
            await commands[str(operation[0])](operation[1], operation[2])

        else:
            pass




async def output(data : dict, file_name : str):

    if not os.path.exists(struct['path']['storage']):
        os.mkdir(struct['path']['storage'])
    
    json_file_name = file_name + '.json'
    json_file_path = os.path.join(struct['path']['storage'], json_file_name)
        
    with open(json_file_path, 'w') as output_file:
        output_file.write(json.dumps(data, indent = 4))
    output_file.close()
    


async def request(url : str, file_name : str) -> dict:
    
    try:
    
        if url is not None:
            
            response = requests.get(url)
                
            if response.status_code == 200:
                data = json.loads(response.text)
                
                await output(data, file_name)
                
                return data
                
            else:
                return None
    except KeyboardInterrupt:
        pass
    





async def main():
    
    os.system('mode con: cols=100 lines=20')
    
    print(logo)
        
    while execution:
        operation = str(input(f'{session}\t'))
            
        await command(operation)


if __name__ == '__main__':
    asyncio.run(main())
