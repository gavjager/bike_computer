import dbus

bus = dbus.SystemBus()
proxy = bus.get_object(':1.19','/com/example/calculator')
interface = dbus.Interface(proxy, 'com.example.calculator_interface')

all_props = interface.Add(1,2)
print(all_props)

