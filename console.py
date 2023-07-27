#!/usr/bin/python3
"""The console/command interpreter for the AirBnB_clone project
"""
import cmd
from models import storage, storage_type
from models.base_model import BaseModel
from models.user import User

from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity

from models.review import Review
import sys


class HBNBCommand(cmd.Cmd):
    """Defines the HBNBCommand class for AirBnB_clone

    Attributes:
        prompt (str): The command prompt
        classes (tuple): The list of classes that can be created
    """
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def precmd(self, line):
        """Reformats the command line for the advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return line

    def parseline(self, line):
        """Reformats the command line for the advanced command syntax.
        """
        if '(' in line and ')' in line:
            line = line.replace('.', ' ', 1).replace('(', ' ', 1)
            line = line.replace(')', '')
            if '{' in line and ': ' in line and '}' in line:
                #  Update if dictionary is given
                pre_dict, dict_info = line.split(', {', 1)
                pre_dict = pre_dict.split(" ")
                pre_dict[2] = pre_dict[2].replace('"', '')
                line = ' '.join([pre_dict[1], pre_dict[0], pre_dict[2],
                                 '{' + dict_info])
                return super().parseline(line)

            line = line.split()
            if len(line) == 3:
                #  For show and destroy
                line[2] = line[2].replace('"', '')
                line = " ".join([line[1], line[0], line[2]])
            elif len(line) >= 5:
                #  Update if attribute name and value are given
                line[2] = line[2].replace('"', '').replace(',', '')
                line[3] = line[3].replace('"', '').replace(',', '')
                line[4] = line[4].replace('"', '')
                line = " ".join([line[1], line[0], line[2], line[3], line[4]])
            else:
                line = " ".join([line[1], line[0]])

        return super().parseline(line)

    def do_quit(self, arg):
        """Exit the program with the command 'quit'
        """
        return True

    def help_quit(self):
        """Documentation for the quit command
        """
        print("Exits the program")

    def do_EOF(self, arg):
        """Exit the program on receiving the EOF signal
        """
        print()
        return True

    def help_EOF(self):
        """Documentation for the EOF signal
        """
        print("Exits the program on receiving the EOF signal")

    def emptyline(self):
        """Do nothing on receiving an empty line
        """
        return False

    def do_create(self, arg):
        """Create an object of any class with optional parameters

        Usage: create <Class name>
            OR create <Class name> <param1> <param2> <param3> ...
        Param syntax: <key name>=<value>
        Value syntax:
            - String: "<value>"
            - Integer: <number>
            - Float: <unit>.<decimal>
        """
        if not arg:
            print("** class name missing **")
            return
        tokens = arg.split()
        if tokens[0] not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[tokens[0]]()
        if len(tokens) > 1:
            for i in range(1, len(tokens)):
                if "=" in tokens[i]:
                    key, value = tokens[i].split("=")
                    value = value.replace("_", " ").replace('\"', '"')
                    if value[0] == '"' and value[-1] == '"':
                        value = value[1:-1]
                    if key in self.types:
                        value = self.types[key](value)
                    setattr(new_instance, key, value)
        print(new_instance.id)
        new_instance.save()

    def help_create(self):
        """Documentation for the create command"""
        print("Creates a class instance with optional parameters")
        print("[Usage]: create <className> OR")
        print("         create <className> <param1> <param2> <param3> ...")
        print("Param syntax: <key name>=<value>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del storage.all()[key]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arg):
        """Shows all objects, or all objects of a given class
        """
        """Displays the string representation of all instances or
        all instances of a class

        Usage: all <class name> OR <class name>.all() OR all
        """
        output = []
        if not arg:
            for value in storage.all().values():
                if storage_type == 'db':
                    del value.__dict__['_sa_instance_state']
                output.append((value))

        elif arg not in self.classes:
            print("** class doesn't exist **")
        else:
            for key, value in storage.all().items():
                if storage_type == 'db':
                    del value.__dict__['_sa_instance_state']
                if arg == key.split('.')[0]:
                    output.append((value))
        
        print('[', end='')
        for obj in output:
            print(obj, end=', ' if obj != output[-1] else '')
        print(']')

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] != '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
