from smbus2 import SMBus
from mlx90614 import MLX90614

def temp():
	bus = SMBus(1)
	sensor = MLX90614(bus, address=0x5A)
	
	while True:
		temp_list=[]
		print('ambient : ',sensor.get_ambient())
		print('object : ',sensor.get_object_1()) 
		if int(sensor.get_ambient()) < int(sensor.get_object_1()):
			for i in range(20):
				print( "Ambient Temperature :", sensor.get_ambient())
				temp_list.append(sensor.get_object_1())
			bus.close()
			return sum(temp_list)/len(temp_list)


			
if __name__=='__main__':
	print(temp())
