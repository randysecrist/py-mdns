
class servicegroup:
    def __init__(self, replace_wildcards=False):
        self.__name = None
        self.__services = None
        self.__replace_wildcards = replace_wildcards

class service:
    def __init__(self, svc_type, svc_port, svc_name, sysname, state):
        # Required
        self.__type = svc_type
        self.__port = svc_port
        self.__localized_name = svc_name
        self.__sysname = sysname
        self.__state = state
        
        # Optional
        self.__protocol = 'ipv4'
        self.__domain_name = None
        self.__host_name = None
        self.__subtypes = None
        self.__txt = {}
        
    def __str__(self) :
        return str(self.__dict__)

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
    
    def __hash__(self):
        return hash((self.__type,
                     self.__port,
                     self.__localized_name,
                     self.__sysname,
                     self.__state))
            
    @property
    def type(self):
        return self.__type;

    @property
    def type_full(self):
        return (self.__type, self.__localized_name);

    @property
    def port(self):
        return self.__port;
    
    @property
    def protocol(self):
        return self.__protocol;
    
    @property
    def domain_name(self):
        return self.__domain_name;
    
    @property
    def host_name(self):
        return self.__host_name;

    @property
    def subtypes(self):
        return self.__subtypes;
    
    @property
    def txt(self):
        return self.__txt;
    
    @property
    def localized_name(self):
        return self.__localized_name
    
    @property
    def sysname(self):
        return self.__sysname;

    @property
    def state(self):
        return self.__state;
