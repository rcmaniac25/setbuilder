import os
import sys

# https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
def clear_screen():
	os.system('cls' if os.name=='nt' else 'clear')

def printerr(x):
	clear_screen()
	sys.stderr.write('{0}\n'.format(x))

def handle_command(dataset, cmd, value):
	if cmd == 'a' or cmd == 'add':
		clear_screen()
		if value in dataset:
			print('\'{0}\' exists already'.format(value))
		else:
			dataset.append(value)
			print('\'{0}\' added'.format(value))
	elif cmd == 'r' or cmd == 'remove':
		clear_screen()
		if value in dataset:
			dataset.remove(value)
			print('\'{0}\' removed'.format(value))
		else:
			print('\'{0}\' didn\'t exist'.format(value))
	elif cmd == 'l' or cmd == 'load':
		if value == '':
			printerr('Requires a file name')
		elif not os.path.isfile(value):
			printerr('Cannot find \'{0}\''.format(value))
		else:
			clear_screen()
			with open(value, 'r') as f:
				dataset.clear()
				for line in f:
					clean_line = line.strip()
					if clean_line == '':
						continue
					dataset.append(clean_line)
			print('Loaded set from \'{0}\''.format(value))
	elif cmd == 's' or cmd == 'save':
		if value == '':
			printerr('Requires a file name')
		else:
			clear_screen()
			with open(value, 'w') as f:
				for data in dataset:
					f.write('{0}{1}'.format(data, os.linesep))
			print('Saved set to \'{0}\''.format(value))
	elif cmd == 'sort':
		clear_screen()
		print('Sorted...')
		dataset.sort()
	elif cmd == 'p' or cmd == 'print':
		clear_screen()
		if len(dataset) == 0:
			print('<Empty set>')
		else:
			for x in dataset:
				print(x)
	elif cmd == 'h' or cmd == 'help':
		clear_screen()
		print('Syntax: \'[@@<cmd>] value\'\n')
		print('By default, the \'add\' command is in use')
		print('Doesn\'t support multi-line values\n')
		print('Commands:')
		print('- a|add <value>: adds a value to the set. Will return if added or exists already')
		print('- r|remove <value>: removes a value from the set. Will return if removed or didn\'t exist')
		print('- l|load <file>: clears the existing set and loads a new one from a file. Will skip empty lines')
		print('- s|save <file>: Saves the existing set to a file')
		print('- sort: Sorts the set')
		print('- p|print: Prints the set to screen')
		print('- h|help: Prints help info')
		print('- e|exit: Exits the program')
	elif cmd == 'e' or cmd == 'exit':
		return None
	else:
		printerr('Unknown command: {0}'.format(cmd))
	return dataset

if __name__ == "__main__":
	clear_screen()
	print("Set Builder")
	print("- Type '@@help' for info")

	dataset = []

	while dataset != None:
		sys.stdout.write('\n> ')
		sys.stdout.flush()
		try:
			line = sys.stdin.readline().strip()
		except KeyboardInterrupt:
			break

		if line == '':
			continue

		cmd = 'add'
		if line.startswith('@@'):
			tmp = line[2:]
			if tmp.lower() in ['e', 'exit', 'p', 'print', 'h', 'help', 'sort']:
				cmd = tmp.lower()
			else:
				idx = tmp.find(' ')
				if idx <= 0:
					printerr('Invalid command line: {0}'.format(line))
					continue
				elif tmp[idx+1:].strip() == '':
					printerr('Missing value for command {0}'.format(tmp[:idx]))
					continue
				cmd = tmp[:idx].lower()
				line = tmp[idx+1:].strip()

		dataset = handle_command(dataset, cmd, line)
	