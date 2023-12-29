#!/usr/bin/python3
'''
    Implementing the console for the HBnB project.
'''
import cmd
import json
import shlex
import models
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    '''
        Contains the entry point of the CLI.
    '''
    prompt = ("(hbnb) ")

    def do_quit(self, args):
        '''
            Quit command to exit the program.
        '''
        return True

    def do_EOF(self, args):
        '''
            Exits after receiving the EOF signal.
        '''
        return True

    def do_create(self, args):
        '''
            Create a new obj of class BaseModel.
        '''
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            args = shlex.split(args)
            new_object = eval(args[0])()
            for i in args[1:]:
                try:
                    key = i.split("=")[0]
                    value = i.split("=")[1]
                    if hasattr(new_object, key) is True:
                        value = value.replace("_", " ")
                        try:
                            value = eval(value)
                        except:
                            pass
                        setattr(new_object, key, value)
                except (ValueError, IndexError):
                    pass
            new_object.save()
            print(new_object.id)
        except:
            print("** class doesn't exist **")
            return

    def do_show(self, args):
        '''
            Print the string representation of an instance.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_dict = storage.all(args[0])
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        try:
            value = obj_dict[key]
            print(value)
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        '''
            Deletes an instance.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        cls_name = args[0]
        cls_id = args[1]
        storage.reload()
        obj_dic = storage.all()
        try:
            eval(cls_name)
        except NameError:
            print("** class doesn't exist **")
            return
        key = cls_name + "." + cls_id
        try:
            del obj_dic[key]
        except KeyError:
            print("** no instance found **")
        storage.save()

    def do_all(self, args):
        '''
            Prints all instances
        '''
        args = args.split(" ")
        obj_l = []
        objs = storage.all(args[0])
        try:
            if args[0] != "":
                models.classes[args[0]]
        except (KeyError, NameError):
            print("** class doesn't exist **")
            return
        try:
            for key, value in objs.items():
                obj_l.append(value)
        except:
            pass
        print(obj_l)

    def do_update(self, args):
        '''
            Update an instance based on the class name and id
        '''
        storage.reload()
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        k = args[0] + "." + args[1]
        obj_dic = storage.all()
        try:
            obj_value = obj_dic[k]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_value, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass
        setattr(obj_value, args[2], args[3])
        obj_value.save()

    def emptyline(self):
        '''
        Prints nothing when an empty line is passed.
        '''
        pass

    def do_count(self, args):
        '''
            Get the nums of instances.
        '''
        obj_list = []
        storage.reload()
        objects = storage.all()
        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, value in objects.items():
            if len(args) != 0:
                if type(value) is eval(args):
                    obj_list.append(value)
            else:
                obj_list.append(value)
        print(len(obj_list))

    def default(self, args):
        '''
            Handle all the function prototypes that are not expicitly defined.
        '''
        funcs = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy, "update": self.do_update}
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            cmd_arg = args[0] + " " + args[2]
            f = funcs[args[1]]
            f(cmd_arg)
        except:
            print("*** Unknown syntax:", args[0])

if __name__ == "__main__":
    HBNBCommand().cmdloop()
