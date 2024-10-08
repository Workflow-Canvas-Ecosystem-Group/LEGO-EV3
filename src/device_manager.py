import uuid
import json
import os
import sys
import logging
from importlib import import_module
from threading import Lock
from utils import Singleton


class ResourceBlockInfo:
    def __init__(self, author, version, name, description, type):
        self.author = author
        self.version = version
        self.name = name
        self.description = description
        self.type = type


class ModuleManager(metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        self.rbs = {}
        self.modules_root_directory = os.path.join(os.path.dirname(__file__), "modules")
        sys.path.append(os.path.dirname(__file__))
        # load modules
        sys.path.append(self.modules_root_directory)
        for rb in os.listdir(self.modules_root_directory):
            if os.path.isdir(os.path.join(self.modules_root_directory, rb)):
                self.load_modules(rb)

    def load_modules(self, name):
        return self.load(name)

    def load(self, name):
        """
        register device to device manager, the device directory should have already installed to devices directory
        :param name: device name, also the device directory name
        :param category: resource block category, builtin/public
        :return:
        """
        try:
            root_directory = self.modules_root_directory
            # parse info.json
            info_path = os.path.join(root_directory, name, "info.json")
            if not os.path.exists(info_path):
                logging.error("LEGO module [{}] not find info.json".format(name))
                return False
            with open(info_path) as fp:
                info_obj = json.load(fp)
            if not info_obj:
                logging.error("Failed to parse LEGO module [{}] info.json".format(name))
                return False
            rb = ResourceBlockInfo(info_obj["author"],
                                   info_obj["version"],
                                   info_obj["name"],
                                   info_obj["description"],
                                   info_obj["type"])
            self.rbs[name] = rb
        except Exception as e:
            logging.error("Failed to load LEGO module [{}] : {}".format(name, e))
            return False
        logging.info("Load LEGO module [{}] successfully".format(name))
        return True

    def get_rb_entity(self, rb: ResourceBlockInfo):
        root_directory = self.modules_root_directory
        sys.path.append(os.path.join(root_directory, rb.name))
        module = import_module(rb.name + '.' + rb.name.lower(), package=rb.name)
        # RB entity class name should be RB name remove "_"
        entity = rb.name.replace("_", "")
        return getattr(module, entity)

    def get_rb_by_type(self, device_type) -> ResourceBlockInfo:
        for rb in self.rbs:
            for type in self.rbs[rb].type:
                if self.is_type_match(device_type, type):
                    return self.rbs[rb]
        return None

    def get_rb_by_name(self, name) -> ResourceBlockInfo:
        return self.rbs.get(name)

    def is_type_match(self, device_type: str, check_type: str):
        if check_type == device_type:
            return True
        elif check_type.endswith("*"):
            t = check_type[:len(check_type) - 1]
            if device_type.startswith(t):
                return True
        return False

    def has_rb(self, name):
        return self.rbs.get(name) is not None

    def get_all_rbs_names(self):
        """
        get all registered resource block names
        :return:
        """
        rst = []
        for key in self.rbs:
            rst.append(key)
        return rst


DEL_KEYS = ['resource', 'raAddress']


class DeviceManager(metaclass=Singleton):
    """
    Device Manager is a singleton instance, to store the service instances
    """
    def __init__(self, *args, **kwargs):
        self.devices = dict()
        self.run_flag = True
        self.lock = Lock()

    def get_device(self, device_info):
        device_uuid = DeviceManager().generate_device_uuid(device_info)
        if not self.devices.get(device_uuid):
            return self.create_device(device_info)
        return self.devices.get(device_uuid)

    def create_device(self, device_info):
        device_type = device_info.get("type", "")
        rb = ModuleManager().get_rb_by_type(device_type)
        if not rb:
            logging.error("Failed to find LEGO module match [{}]".format(device_type))
        else:
            device_uuid = DeviceManager().generate_device_uuid(device_info)
            entity = ModuleManager().get_rb_entity(rb)
            device = entity(device_info)
            self.devices[device_uuid] = device
            return device

    def destroy_device(self, device_info):
        device_uuid = DeviceManager().generate_device_uuid(device_info)
        if self.devices.get(device_uuid):
            del(self.devices[device_uuid])

    def destroy(self):
        """
        Destroy all the device handlers, will be called when the process is shutdown
        """
        for device in self.devices.values():
            logging.info("In device manager, Do destroy for {}".format(device))
            # device_handler.destroy()
        self.devices.clear()

    @staticmethod
    def generate_device_uuid(device_info):
        """
        Generate uuid by type and parameters, with key and value
        """
        device_type = device_info.get("type")
        device_parameters = DeviceManager().filter_device_parameters(device_info)
        order_device_parameters = sorted(device_parameters.items(), key=lambda d: d[0])
        device_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS,
                                     json.dumps({"type": device_type, "parameters": order_device_parameters})))
        return device_uuid

    @staticmethod
    def filter_device_parameters(parameters):
        del_keys = [k for k in parameters if k.startswith('_') or k in DEL_KEYS]
        return dict([(key, val) for key, val in parameters.items() if key not in del_keys])
