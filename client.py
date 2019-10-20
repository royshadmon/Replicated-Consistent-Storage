import socket
import sys
import logging

connected_servers = []

def which_server(message):
	server_num = message.split(' ')[0]
	try:
		server_num = int(server_num) - 1
		if server_num in range(0, len(connected_servers)):
			print('success')
			return server_num
		else:
			logging.warning('Server at index %d in connected_servers list does not exist', server_num)
			return False
	except:
		logging.warning('Server at index %s in connected_servers list does not exist', server_num)
		return False				
	


def prepare_server_message(server_num):
	client_socket = connected_servers[server_num]
	return client_socket

def clean_message(message):
	message = message.lower().strip()
	return message

def client_program(num_servers):
	host = socket.gethostname()  # as both code is running on same pc
	dns_addr = socket.gethostbyname(host)
	port = 12345  # socket server port number

	for i in range(0, num_servers):
		try:
			client_socket = socket.socket()  # instantiate
			client_socket.connect((dns_addr, port))  # connect to the server
			connected_servers.append(client_socket)
		except Exception as e:
			logging.warning('No server running on port: %s', port)
			logging.warning('Exception message: %s', e)
			# we start servers on +1 ports
			break
		port += 1
	
	while True:
		message = clean_message(input(" -> "))  # take input
		if message.startswith('bye'):
			break
		server_num = which_server(message)
		if server_num is False:
			continue
		client_socket = prepare_server_message(server_num)
		client_socket.send(message.encode())  # send message
		
		data = client_socket.recv(1024).decode()  # receive response

		print('Received from server: ' + data)  # show in terminal


	client_socket.close()  # close the connection


if __name__ == '__main__':
	# two argumets, filename and number of servers
	if len(sys.argv) == 2:
		num_servers = int(sys.argv[1])
		client_program(num_servers)
	else:
		logging.warning('Specify number of servers to run.', 'Ex run: python3 client.py [num_servers]')