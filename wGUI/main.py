import asyncio
import pip
import time
import requests
import json
import os
import socket
import getpass
import sqlite3


try:
    import colorama

except ImportError:
    pip.main(['install', 'colorama'])

try:
    from pygments import highlight
    from pygments.formatters.terminal import TerminalFormatter
    from pygments.lexers.web import JsonLexer

except ImportError:
    pip.main(['install', 'pygments'])


colorama.init()





global session

global execution_path
global storage_path
global database_path


session = str(
    colorama.Fore.LIGHTMAGENTA_EX + socket.gethostname() +
    colorama.Fore.LIGHTCYAN_EX + '@' +
    colorama.Fore.LIGHTBLUE_EX + getpass.getuser()
)


def get_path_format(path : str) -> str:
    path = os.path.normpath(path)
    
    return path



execution_path = get_path_format(os.path.dirname(os.path.abspath(__file__)))
storage_path = get_path_format(os.path.join(execution_path, 'storage'))
database_path = get_path_format(os.path.join(storage_path, 'database'))




'''

classes

'''

class CursorEnvironment(object):
    
    
    def __init__(self):
        
        super(CursorEnvironment, self).__init__()
        
        self.status = False
        self.role = str(
            '\n' +
            colorama.Fore.RESET +
            colorama.Style.BRIGHT +
            colorama.Fore.LIGHTBLUE_EX + '[ cursor ] ' +
            colorama.Fore.RESET +
            
            session +
            
            colorama.Fore.LIGHTWHITE_EX +
            '\t> ' +
            colorama.Fore.RESET
        )
        
        self.__commands = {
            'start' : {
                'scanner' : start_scanner
            }
        }


    async def init(self):
        
        self.status = True
        
        while self.status:
            self.command = input(self.role)
            
            if self.command == 'exit':
                await goodbye_message()
                break
            
            else:
                
                self.command = self.command.split(' ')
                
                try:
                    if len(self.command) == 1:
                        await self.__commands[str(self.command[0])]()
                        
                    elif len(self.command) == 2:
                        await self.__commands[str(self.command[0])](self.command[1])

                    elif len(self.command) == 3:
                        await self.__commands[str(self.command[0])][str(self.command[1])](self.command[2])

                except Exception as e:
                    print(e)
                    pass


class DatabaseEnvironment(object):
    
    
    
    def __init__(self):
        
        super(DatabaseEnvironment, self).__init__()
        
        self.status = False
        self.role = str(
            '\n' +
            colorama.Fore.RESET +
            colorama.Style.BRIGHT +
            colorama.Fore.LIGHTYELLOW_EX + '[ database ] ' +
            colorama.Fore.RESET +
            
            session +
            
            colorama.Fore.LIGHTWHITE_EX +
            '\t> ' +
            colorama.Fore.RESET
        )
        self.__commands = {
            'start' : {
                'database' : start_database
            },
            
            'create' : {
                'database' : create_database,
                'script' : None
            },
            
            'execute' : {
                'sentence' : None,
                'script' : None
            }
        }



    async def init(self):
        
        self.status = True
        
        while self.status:
            self.command = input(self.role)
            
            if self.command == 'exit':
                await goodbye_message()
                break
            
            else:
                
                self.command = self.command.split(' ')
                
                try:
                    if len(self.command) == 1:
                        await self.__commands[str(self.command[0])]()
                        
                    elif len(self.command) == 2:
                        await self.__commands[str(self.command[0])](self.command[1])

                    elif len(self.command) == 3:
                        await self.__commands[str(self.command[0])][str(self.command[1])](self.command[2])

                except Exception as e:
                    print(e)
                    pass
                
                
class OperatorEnvironment(object):
    
    
    def __init__(self):
        
        super(OperatorEnvironment, self).__init__()
        
        self.status = False
        self.role = str(
            '\n' +
            colorama.Fore.RESET +
            colorama.Style.BRIGHT +
            
            session +
            
            colorama.Fore.LIGHTWHITE_EX +
            '\t> ' +
            colorama.Fore.RESET
        )
        

    async def init(self):
        
        self.status = True
        
        while self.status:
            self.command = input(self.role)
            
            if self.command == 'exit':
                await goodbye_message()
                break
            
            else:
                await execute_command(self.command)
                
                
                



'''

functions

'''







async def time_message():
    message = str(
        colorama.Fore.RESET  + ' ' * 2 + '∟ ' +
        colorama.Fore.BLUE + f'[ {time.asctime()} ]\t' +
        colorama.Fore.RESET
    )
    
    print(message)



async def status_message(status : int):
    
    if status == 0:
        status_message = str(
            colorama.Fore.RESET + 
            colorama.Fore.BLUE + '[ * ]\t' +
            colorama.Fore.RESET
        )
    
    elif status == 1:
        status_message = str(
            colorama.Fore.RESET + 
            colorama.Fore.GREEN + '[ + ]\t' +
            colorama.Fore.RESET
        )
        
    elif status == 2:
        status_message = str(
            colorama.Fore.RESET + 
            colorama.Fore.RED + '[ ! ]\t' +
            colorama.Fore.RESET
            
        )
    
    return status_message




async def output_directory_message(status : int, path : str):
    
    if status == 0:
        message = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            await status_message(status) +
            colorama.Fore.YELLOW + 'Checking for existence of storage directory ' +
            colorama.Fore.RESET + path
        )

    elif status == 1:
        message = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            await status_message(status) +
            colorama.Fore.LIGHTGREEN_EX + 'Directory created! ' +
            colorama.Fore.RESET + path
        )
    
    print(message)


async def output_file_message(status : int, file_name : str, file_path : str):
    
    if status == 0:
        message = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            await status_message(status) +
            colorama.Fore.YELLOW + 'Creating file ' +
            colorama.Fore.RESET + file_name +
            colorama.Fore.LIGHTYELLOW_EX + ' on ' +
            colorama.Fore.RESET + file_path
        )

    elif status == 1:
        message = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            await status_message(status) +
            colorama.Fore.LIGHTGREEN_EX + 'File created! ' +
            colorama.Fore.RESET + file_name +
            colorama.Fore.LIGHTYELLOW_EX + ' on ' +
            colorama.Fore.RESET + file_path
        )
    
    print(message)



async def search_message(status : int, file_name : str, file_path : str):
    
    if status == 0:
        message = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            await status_message(status) +
            colorama.Fore.YELLOW + 'Searching ' +
            colorama.Fore.RESET +
            colorama.Fore.LIGHTYELLOW_EX + ' on ' +
            colorama.Fore.RESET + file_path
        )

    elif status == 1:
        message = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            await status_message(status) +
            colorama.Fore.LIGHTGREEN_EX + 'Found ' +
            colorama.Fore.RESET + file_name +
            colorama.Fore.LIGHTYELLOW_EX + ' on ' +
            colorama.Fore.RESET + file_path
        )
    
    print(message)



async def request_message(status : int, url : str):
    
    if status == 0:
        message = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            await status_message(status) +
            colorama.Fore.YELLOW + 'Requesting ' +
            colorama.Fore.RESET + url
        )

    elif status == 1:
        message = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            await status_message(status) +
            colorama.Fore.LIGHTGREEN_EX + 'Request completed! ' +
            colorama.Fore.RESET + url
        )
    
    elif status == 2:
        exception = url
        message = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            await status_message(status) +
            colorama.Fore.LIGHTRED_EX + f'Exception : {exception}' +
            colorama.Fore.RESET
        )
    
    print(message)

async def goodbye_message():
    message = str(
        colorama.Fore.RESET +
        colorama.Fore.LIGHTYELLOW_EX + 'Goodbye ' +
        colorama.Fore.RESET
    )
    
    print(message, end = '\n')
    

async def exception_message(exception : str):
    message = str(
        colorama.Fore.RESET +
        colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
        await status_message(2) +
        colorama.Fore.LIGHTRED_EX + f'Exception : {exception}' +
        colorama.Fore.RESET
    )
    print(message, end = '\n\n')




async def start_scanner(path : str):
    
    
    for root, directories, files in os.walk(path):
        
        root = get_path_format(root)
        
        root = str(
            colorama.Fore.RESET +
            colorama.Fore.LIGHTMAGENTA_EX + ' ' * 2 + '∟ ' +
            root)
        
        print(root)
        
        
        for directory in directories:
            directories = str(
                colorama.Fore.RESET +
                colorama.Fore.LIGHTMAGENTA_EX + ' ' * 4 + '∟ ' +
                colorama.Fore.YELLOW + 'Directories     ' + colorama.Fore.RESET + str(directory))

            print(directories)
        for file in files:
            files = str(
                colorama.Fore.RESET +
                colorama.Fore.LIGHTMAGENTA_EX + ' ' * 4 + '∟ ' +
                colorama.Fore.YELLOW + 'Files           ' + colorama.Fore.RESET + str(file)
            )
            print(files)
        print('\n\n')
        
        time.sleep(0.3)




async def generate_json_file(data, file_name : str):
    
    
    await output_directory_message(0, storage_path)
    
    
    if not os.path.exists(storage_path):
        await output_directory_message(0, storage_path)
        os.mkdir(storage_path)
        await output_directory_message(1, storage_path)

    
    json_file_name = file_name + '.json'
    json_file_path = os.path.join(storage_path, json_file_name)
    
    await output_file_message(0, json_file_name, storage_path)

        
    with open(json_file_path, 'w') as output_file:
        output_file.write(json.dumps(data, indent = 4))
    output_file.close()
    
    await output_file_message(1, json_file_name, storage_path)
    


async def create_database_directory():
    
    await output_directory_message(0, database_path)
    
    if not os.path.exists(storage_path):
        await output_directory_message(0, storage_path)
        os.mkdir(storage_path)
        await output_directory_message(1, storage_path)


    if not os.path.exists(database_path):
        await output_directory_message(0, database_path)
        os.mkdir(database_path)
        await output_directory_message(1, database_path)



async def clear():
    if os.name == 'nt':
        return os.system('cls')
    else:
        return os.system('clear')


async def create_database(file_name : str):
    
    await create_database_directory()
    
    
    file_path = os.path.join(database_path, file_name)

    
    await output_file_message(0, file_name, file_path)
    connection = sqlite3.connect(file_path)
    
    await output_file_message(1, file_name, file_path)
    
    cursor = connection.cursor()

async def start_database(file_path : str):

    
    if file_path == '' or None:
        for obj in os.scandir(database_path):
            
            
            await search_message(0, obj.name, obj.path)
            
            if str(obj.name).split('.')[-1] == 'sqlite3' or str(obj.name).split('.')[-1] == 'db':
                await search_message(1, obj.name, obj.path)
                
                connection = sqlite3.connect(get_path_format(obj.path))
    else:
        connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    




async def request(url : str, file_name : str = None):
    
    
    
    execution = True
    
    while execution:
        
        if file_name is None:
            await request_message(0, url)
            
            try:
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = json.dumps(response.text, indent = 4, sort_keys = True)
                    data = eval(data)
                    
                    colorful = highlight(
                        data,
                        lexer = JsonLexer(),
                        formatter = TerminalFormatter(),
                    )
                    print(colorful)
                
                await request_message(1, url)
                
            
            except Exception as exception:
                await exception_message(exception)
        
        else:

            await request_message(0, url)
            
            try:
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = json.dumps(response.text, indent = 4, sort_keys = True)
                    data = eval(data)
                    
                    colorful = highlight(
                        data,
                        lexer = JsonLexer(),
                        formatter = TerminalFormatter(),
                    )
                    print(colorful)
                
                await request_message(1, url)
                
                data = dict(content = eval(data))
                await generate_json_file(data, file_name)
            
            except Exception as exception:
                await exception_message(exception)
        
        execution = False
    
    

async def database():
    try:
        await DatabaseEnvironment().init()
    
    except KeyboardInterrupt:
        pass

async def cursor():
    try:
        await CursorEnvironment().init()
    
    except KeyboardInterrupt:
        pass

async def operator():
    try:
        await OperatorEnvironment().init()
    
    except KeyboardInterrupt:
        pass











commands = {
    
    # Functions
    'request' : request,
    
    'time' : time_message,

    'clear' : clear,
    'cls' : clear,
    
    # Environments
    'database' : database,
    'cursor' : cursor,
    'operator' : operator
}

























async def execute_command(operation : str):
    
    operation = operation.split(' ')
    
    try:
        if len(operation) == 1:
            await commands[str(operation[0])]()
            
        elif len(operation) == 2:
            await commands[str(operation[0])](operation[1])

        elif len(operation) == 3:
            await commands[str(operation[0])](operation[1], operation[2])

    except:
        pass






















async def main():
    await OperatorEnvironment().init()

    

if __name__ == "__main__":
    asyncio.run(main())
