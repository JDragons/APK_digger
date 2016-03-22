#coding:utf8



from .. import *
from VulnerabilityVector import VulnerabilityVector



class URLs_check(VulnerabilityVector):

       def __init__(self,context):

            self.context = context




       def  analyze(self):


            regexGerneralRestricted = ".*(config|setting|constant).*";
            regexSecurityRestricted = ".*(encrypt|decrypt|encod|decod|aes|sha1|sha256|sha512|md5).*"  #No need to add "sha1" and "des"
            #show the user which package is excluded

            prog = re.compile(regexGerneralRestricted, re.I)
            prog_sec = re.compile(regexSecurityRestricted, re.I)

            # Security methods finding:

            if self.context.args.extra == 2:  #The output may be too verbose, so make it an option

                list_security_related_methods = []

                for method in self.context.d.get_methods():
                    if prog.match(method.get_name()) or prog_sec.match(method.get_name()):
                        if self.context.filteringEngine.is_class_name_not_in_exclusion(method.get_class_name()):
                            # Need to exclude "onConfigurationChanged (Landroid/content/res/Configuration;)V"
                            if (method.get_name() != 'onConfigurationChanged') and (
                                        method.get_descriptor() != '(Landroid/content/res/Configuration;)V'):
                                list_security_related_methods.append(method)

                if list_security_related_methods:
                    self.context.startWriter("Security_Methods", LEVEL_NOTICE, "Security Methods Checking",
                                       "Find some security-related method names:")
                    for method in list_security_related_methods:
                        self.context.write(method.get_class_name() + "->" + method.get_name() + method.get_descriptor())
                else:
                    self.context.startWriter("Security_Methods", LEVEL_INFO, "Security Methods Checking",
                                       "Did not detect method names containing security related string.")



            if self.context.args.extra == 2:  #The output may be too verbose, so make it an option
                list_security_related_classes = []

                for current_class in self.context.d.get_classes():
                    if prog.match(current_class.get_name()) or prog_sec.match(current_class.get_name()):
                        if self.context.filteringEngine.is_class_name_not_in_exclusion(current_class.get_name()):
                            list_security_related_classes.append(current_class)

                if list_security_related_classes:
                    self.context.writer.startWriter("Security_Classes", LEVEL_NOTICE, "Security Classes Checking",
                                       "Find some security-related class names:")

                    for current_class in list_security_related_classes:
                        self.context.writer.write(current_class.get_name())
                else:
                    self.context.writer.startWriter("Security_Classes", LEVEL_INFO, "Security Classes Checking",
                                       "Did not detect class names containing security related string.")
