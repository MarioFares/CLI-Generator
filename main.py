"""
A command line interpreter for building command line interpreters.

This application is built using the cmd2 module primarily and it is a command line BASH like interpreter.

Welcome to CLI Generator.
This command line interface program was designed for programmers who rely heavily on using
CLI applications and who would like to generate a quick interactive shell with a CLI.

This application is geared towards simplicity trying to make generating such applications
as swift and easy as possible.

Note that this application will generate code for your CLI application using the cmd2 library
or even the almost compatible Python Native cmd library which like cmd2, is very easy to use.

You will be able to generate the basic structure of the application but as for the algorithms
of your commands, you must do the coding yourself in the Python file that will be generated with
code by this application.

You also have the ability to save your information in a JSON file and load information from that
file later on if you need it.

You are able to use ? symbol before any command to learn more about that command, its arguments,
and what it does. You may also use that symbol in the beginning to see the list of commands
available to you inside this application.
"""


from cmd2 import with_argparser_and_unknown_args
from cmd2 import Cmd
import argparse
import pprint
import json
import os


import_argparser = argparse.ArgumentParser()
import_argparser.add_argument('-ap', '--addpackage', action='store_true',
                              help='Add import statement with certain package.')
import_argparser.add_argument('-am', '--addmodule', action='store_true',
                              help='Add import statement with entire module.')

open_argparser = argparse.ArgumentParser()
open_argparser.add_argument('-file', '--file', action='store_true',
                            help='Open the .py file where your code is.')
open_argparser.add_argument('-json', '--json', action='store_true',
                            help='Open the .json file where your config is.')


# noinspection PyUnusedLocal
class App(Cmd):
    """
    This is the main class which will be used to run the interpreter.
    An instance is created below using the cmdloop() function.
    It will repeatedly issue a prompt, wait for a command and its arguments,
    and execute the corresponding function.
    """

    intro = "Welcome to CLI Generator"
    prompt = "|>"
    file = None
    created_app = {
        "name": "",
        "app path": "./code.py",
        "json path": "./config.json",
        "intro": "",
        "prompt": "",
        "file": "None",
        "imports": [],
        "commands": [],
    }

    def do_intro(self, arg):
        """
        Specify CLI introduction -> The first string that will appear when the application is run.
        Argument: any string
        """
        self.created_app["intro"] = arg.args

    def do_prompt(self, arg):
        """
        Specify CLI prompt -> The prompt is a string repeatedly shown which awaits input.
        Argument: any string
        """
        self.created_app["prompt"] = arg.args

    def do_name(self, arg):
        """
        Specify the name of your application.
        Argument: any string
        """
        self.created_app["name"] = arg.args

    def do_path(self, arg):
        """
        Specify the absolute path to the script you want to create.
        - Example: C:/Users/User/Desktop/code.py
        - Default: ./code.py  ->  A Python file will be created in the directory of the script.

        Argument: absolute path to .py file
        """
        self.created_app["app path"] = arg.args

    def do_jsonpath(self, arg):
        """
        Specify path to the JSON path where you want to save application.
        - Example: C:/Users/User/Desktop/config.json
        - Default: ./config.json    ->  A JSON file will be created in the directory of the script.

        Argument: absolute path to .json file
        """
        self.created_app["json path"] = arg.args
           
    def do_save(self, arg):
        """
        Save the application settings to a JSON file.
        Settings you have specified will be saved to the JSON file you specified.

        Argument: no argument
        """
        with open(self.created_app['json path'], 'w+') as file:
            json.dump(self.created_app, file, sort_keys=True, indent=4)
    
    def do_info(self, arg):
        """
        Show the information that has been inputted for the app.
        This includes:
        - The name of the application
        - The path to the Python file to be generated
        - The path to the JSON file to be generated
        - The prompt of your generated application
        - The intro of your generated application
        - The list of commands and their arguments
        - The list of imported modules

        Argument: no argument
        """
        pprint.pprint(self.created_app)
        
    def do_load(self, arg):
        """
        Load application information from JSON file, with the absolute path to that file to be specified.

        Argument: no argument
        """
        try:
            file = input("Path: ")
            with open(file, 'r+') as json_file:
                self.created_app = json.load(json_file)
        except Exception as e:
            print(e)
                
    def do_reset(self, arg):
        # quit and open again the app
        """
        Reset all the values that you have inputted.
        Application information will return to default.

        Argument: no argument
        """
        self.created_app = self.created_app.fromkeys(self.created_app, "")
        self.created_app['app path'] = './code.py'
        self.created_app['json path'] = './config.json'
        self.created_app['file'] = 'None'
        self.do_clear(self)

    @with_argparser_and_unknown_args(open_argparser)
    def do_open(self, opts, arg):
        """
        Open files and folders.

        Argument: absolute path to file/folder
        """
        try:
            if opts.file:
                os.startfile(self.created_app['app path'])
            elif opts.json:
                os.startfile(self.created_app['json path'])
            else:
                os.startfile(arg[0])
        except WindowsError:
            print("The file does not exist. Check path to file or create the file.")

    @staticmethod
    def do_clear(arg):
        """
        Clear the console window.

        Argument: no argument
        """
        try:
            os.system('cls')
        except OSError:
            os.system('clear')

    @staticmethod
    def do_about(arg):
        """
        Learn about this CLI.

        Argument: no argument
        """
        print("""
              Welcome to CLI Generator.
              This command line interface program was designed for programmers who rely heavily on using
              CLI applications and who would like to generate a quick interactive shell with a CLI.
              
              This application is geared towards simplicity trying to make generating such applications
              as swift and easy as possible.
              
              Note that this application will generate code for your CLI application using the cmd2 library
              or even the almost compatible Python Native cmd library which are very easy to use. 
              
              You will be able to generate the basic structure of the application but as for the algorithms 
              of your commands, you must do the coding yourself in the Python file that will be generated with
              code by this application.
              
              You also have the ability to save your information in a JSON file and load information from that
              file later on if you need it.
              
              You are able to use ? symbol before any command to learn more about that command, its arguments,
              and what it does. You may also use that symbol in the beginning to see the list of commands 
              available to you inside this application.
              """)
    
    @with_argparser_and_unknown_args(import_argparser)
    def do_import(self, opts, arg):
        # need a way to verify that name specified is in std
        """
        This will add the modules you want to import to the script.
        """
        if opts.addmodule:
            namespace = input("Would you like to add a namespace?(y/n)")
            if namespace == "y":
                name = input("Namespace: ")
                self.created_app["imports"].append(["namespace", arg[0], name])
            elif namespace == "n":
                self.created_app["imports"].append(arg)
            else:
                self.created_app["imports"].append(arg)
        elif opts.addpackage:
            module = input("What module is this package located in?")
            self.created_app["imports"].append(["package", module, arg[0]])
        else:
            print("You must add a valid argument for the command.")

    def do_add(self, arg):
        """
        Add command to your script.

        Argument: name of the command
        """
        doc = input("Documentation: ")
        args = input("Arguments(csv): ")
        self.created_app["commands"].append([str(arg), doc, args])
        print(arg)

    def do_gen(self, opts):
        """
        This command will generate code in the Python file (absolute path specified in info).

        Argument: no argument
        """
        exception = input("Do you want to feature exception handling in all your functions?(y/n)")
        print("Text Document is being generated.")
        with open(self.created_app["app path"], "a+") as file:
            for i in self.created_app["imports"]:
                if len(i) == 1:
                    file.write(f"\nimport {i[0]}")
                elif i[0] == "namespace":
                    file.write(f"\nimport {i[1]} as {i[2]}")
                elif i[0] == "package":
                    file.write(f"\nfrom {i[1]} import {i[2]}")
                else:
                    continue 
            file.write("\n\n\n\n\n")
            file.write(f"\nclass App(Cmd):") 
            file.write(f"\n    intro = {self.created_app['intro']}")             
            file.write(f"\n    prompt = {self.created_app['prompt']}")
            file.write(f"\n    file = {self.created_app['file']}")
            for c in self.created_app["commands"]:
                file.write(f"\n\n    def do_{c[0]}(self, {c[2]}):")
                file.write(f"\n        \"\"\"{c[1]}\"\"\"")
                if exception == 'y':
                    file.write("\n        try:")
                    file.write("\n            pass")
                    file.write("\n        except Exception as e:")
                    file.write("\n            print(e)")
                else:
                    file.write("\n    pass")
            file.write("\n\n\napp = App()")
            file.write("\napp.cmdloop()")
            print(self.created_app)
            file.close()
 

app = App()
app.cmdloop()
