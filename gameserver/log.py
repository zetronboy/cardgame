"""import this to your modules to centralize logging
call startlogging() from __main__ and then use
debug log error warn methods
logs to stdout and log_file_name
makes a backup of the log before starting a fresh one"""
import logging
log_file_name = 'current.log'
backup_file_name = 'last.log'
log_format = '%(asctime)s %(levelname)s %(message)s'
logger = None

def backup_log(log_name, backup_log_name): #and create backup
	"""writes last log to backup.log """
	content = ''
	try:
		with open(log_name, 'r') as f:
			content = f.readlines()
	except:
		pass  # ok np if no log yet
	try:
		with open(backup_log_name, 'w') as f:
			f.writelines(content)
	except Exception as e:
		error('backup_log '+ e)


def debug(message):
	print("DEBUG",message)
	if not logger: startlogging()
	logger.debug(message)


def log(message):
	print(message)
	if not logger: startlogging()
	logger.info(message)


def warn(message):
	print("WARN", message)
	if not logger: startlogging()
	logger.warning(message)


def error(message):
	print("ERROR", message)
	if not logger: startlogging()
	logger.error(message)


def startlogging():
	backup_log(log_file_name, backup_file_name)
	try:
		logging.basicConfig(filename=log_file_name,
							level=logging.DEBUG,
							filemode='w',
							format=log_format,
							datefmt='%H:%M:%S'
							)
		global logger
		logger = logging.getLogger()
		print('logging started', log_file_name)
	except Exception as e:
		print("logging error", e)

if __name__ == '__main__':
	startlogging()
	debug('debug')
	warn('warn')
	error('error')
	log('log')