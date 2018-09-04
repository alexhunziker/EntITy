__author__ = "Alex Hunziker"
__email__ = "alexhunziker@sunrise.ch"
__licence__ = "GPL v3"

class EntITyElement(object):
    """ Parent class of all EnITy Elements """
    ent_id = 0
    # Will contain the reference to the EntITy Element
    entITy = None

    # Probably unnecessary?
    FLOW_CONTINUE = -1
    FLOW_RETURN = -2

    @classmethod
    def get_id(cls):
        """ A counter that increments and returns the current value each time invoked """
        this_id = str(cls.ent_id)
        cls.ent_id += 1
        return this_id

# The following 4 classes are subclasses of EntITyElement
class EntITyBlock(EntITyElement):
    def __init__(self):
        """ Generate an empty code block """
        self.name = "Block_" + EntITyElement.get_id()
        self.code = "pass"
        self.jump_after = "None" # This is like Goto. So probably a bad idea

    def getLabels(self):
        """ Returns the labels for a Block Element """
        return ["Block-Duck", "Name", "Code", None, None, "Jump After"]

    def getValues(self):
        """ Returns the properties of a Block Element """
        return [self.name, self.code, None, None, self.jump_after]

    def storeValues(self, name, code, filler1, filler2, jump_after):
        """ Stores the properties of a block element """
		# A check weather the jump is existent could be added
        if EntITyElement.entITy.name_is_unique(name) and True:
            self.name = name
            self.code = code
            self.jump_after = jump_after
            return True
        return False

    def generate_code(self, indent):
        """ Generates the code of a block element """
        commands = self.code.split("\n")
        code = ""
        for command in commands:
            code += " "*indent + command + "\n"
        return [code, self.jump_after]

class EntITyLoop(EntITyElement):
    def __init__(self):
        """ Initializes a loop element """
        self.name = "Loop_" + EntITyElement.get_id()
        self.condition = "False"
        self.jump_if = "None"
        # self.init = ""
        # self.increment = ""

    def getLabels(self):
        """ Returns the property labels of a loop element """
        return ["Loop-Duck", "Name", "Loop Condition", "IF jump", "For-Loop Init", "For-Loop increment"]

    def getValues(self):
        """ Returns the properties of a loop element """
        return [self.name, self.condition, self.jump_if, None, None]

    def storeValues(self, name, condition, jump_if, filler_1, filler_2):
        """ Stores the properties of a loop element """
		# A check weather the jumps exist could be added
        if EntITyElement.entITy.name_is_unique(name) and True and True:
            self.name = name
            self.jump_if = jump_if
            self.condition = condition
            return True
        return False

    def generate_code(self, indent):
        """ Generates the code of a loop element """
        code = " "*indent + "while " + self.condition + ":\n" + \
                EntITyElement.entITy.generate_code(indent+4, name=self.jump_if) + "\n"
        return [code, "None"]

class EntITyControl(EntITyElement):
    def __init__(self):
        """ Initializes a control element """
        self.name = "Control_" + EntITyElement.get_id()
        self.condition = "True"
        self.jump_if = "Ente"
        self.jump_else = "None"

    def getLabels(self):
        """ Returns the property labels of a control element """
        return ["Control-Duck", "Name", "Condition", "IF Jump", "ELSE Jump", None]

    def getValues(self):
        """ Returns the properties of a control element """
        return [self.name, self.condition, self.jump_if, self.jump_else, None]

    def storeValues(self, name, condition, jump_if, jump_else, filler_1):
        """ Stores the properties of a control element """
        # Extention: verify jumps (& condition)
        if EntITyElement.entITy.name_is_unique(name) and True and True and True:
            self.name = name
            self.condition = condition
            self.jump_if = jump_if
            self.jump_else = jump_else
            return True
        return False

    def generate_code(self, indent):
        """ Generates the code of a control element """
        code = " "*indent + "if " + self.condition + ":\n" + \
                EntITyElement.entITy.generate_code(indent+4, name=self.jump_if) + \
                " "*indent + "else:\n" + \
                EntITyElement.entITy.generate_code(indent+4, name=self.jump_else) + "\n"
        return [code, "None"]

class EntITyEnd(EntITyElement):
    def __init__(self):
        """ Initializes an end element """
        self.name = "Ente_" + EntITyElement.get_id()

    def getLabels(self):
        """ Returns the property labels of an end element """
        return ["End-Duck", "Name", None, None, None, None]

    def getValues(self):
        """ Returns the properties of an end element """
        return [self.name, "", "", "", None]

    def storeValues(self, filler_1, filler_2, filler_3, filler_4, filler_5):
        """ Stores the properties of an end element """
        # Nothing can be changed. Name could be changed, but it is pointless from a logical view
        return True

    def generate_code(self, indent):
        """ Generates the code of an end element """
        return ["", "Stop"]
