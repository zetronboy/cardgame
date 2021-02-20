#!/usr/bin/env python3

"""
write to screen and/or file
hook to observable objects
"""
from datetime import datetime
from os import linesep, path, rename, remove, mkdir #for various file operations
from .observerpattern import ObservableBase #for connecting events
from glob import glob #for file searching by pattern
from threading import Lock
import enum 

#todo: __str___ and __repr__

mutex = Lock() #threadsafe file access

class Level(enum.Enum): #use type() to get string of enum
	"Syslog levels"
	EMERG, ALERT, CRIT, ERR, \
	WARNING, NOTICE, INFO, DEBUG, TRACE = range(9)


class Logger():
	"""
	to use:
	instantiate class log = Logger()
	attach a file log.attach_file('logs/current.log')
	"""
	def __init__(self):
		self.prefix_datetime=True
		self.toScreen=True
		self.toFile=False
		self.toSyslog=False
		self.file_path='' 
		self.file_folder='' #pulled for attach to cleanup folder
		self.max_file_size=102400
		self.log_extension='.log' #include the dot
		self.max_file_count = 10
		self.logging_level = Level.DEBUG #message_level <= are logged
		

	def get_current_log_contents(self):
		try:
			with open(self.file_path, 'r') as f:
				content=f.read()
				self.info("returning log content {} bytes ".format(len(content)))
				return content
		except Exception as e:
			self.error("Problem reading log, {}".foramt(e))

	def attach_file(self,file_path:str):
		try:
			if len(file_path) == 0:
				print("attach_file() Error empty file path")
				return -1
			self.toFile=True
			self.file_path=file_path
			file_folder=path.dirname(file_path)
			self.file_folder=file_folder
			print("Logger() folder '{}'".format(file_folder))
			if file_folder and not path.isdir(file_folder):
				mkdir(file_folder)
			print("Logger({}) file attached".format(file_path))
			if len(file_path) > 4 and file_path[-4]=='.':
				self.log_extension = file_path[-4:]#last 4 chars .log
				print("set log ext to {}".format(self.log_extension))
			else:
				print("!bad ext "+ file_path[-4])

		except Exception as e:
			self.error("attachFile({}) {}".format(file_path,e))


	def update(self,message:str): #observed object callback
		self.log(message)
	def warn(self,message:str):
		self.log(message,Level.WARNING)
	def info(self,message:str):
		self.log(message,Level.INFO)
	def debug(self,message:str):
		self.log(message,Level.DEBUG)
	def error(self,message:str):
		print("logger error {}".format(message))
		self.log(message,Level.ERR)
	def log(self,message:str,message_level=Level.INFO):
		with mutex:
			if self.needs_rollover(): 
				self.archive_current()
				self.cleanup_logs()
			optional_date = ''
			if self.prefix_datetime:
				optional_date = datetime.now().strftime("%b%d %H:%M:%S") + " "

			stamped_message = optional_date + str(message_level) +' '+ message + linesep
			if self.toScreen:
				print(stamped_message)
			if self.toFile and self.file_path:
				try:
					with open( self.file_path, 'a') as file:
						#print("Writing to file")
						file.write(stamped_message)
				except Exception as e:
					print("Error writing to disk. {}".format(e))


	def needs_rollover(self):
		"""test for log filesize and calls archive_current()
		if too many archived then purge oldest"""
		logSize = 0
		try:
			if path.exists(self.file_path):
				logSize = path.getsize(self.file_path)
				if logSize > self.max_file_size:
					print("log {}/{} needs rollover".format(logSize,self.max_file_size))
		except Exception as e:
			self.error("Logger.needs_rollover() Error {}".format(e))
		return logSize > self.max_file_size

	def archive_current(self):
		"""called if log rollover is needed
		backs up log with datetime and creates new
		"""
		dated_log=self.file_folder+'/'+datetime.now().strftime("%d%b%y-%H%M%S")+ self.log_extension
		print("logger.archive_current to {}".format(dated_log))
		try:
			rename(self.file_path , dated_log)
		except Exception as e:
			self.error("Logger.archive_current() Error {}".format(e))

	def cleanup_logs(self):
		"""called if log rollover is needed
		if logcount exceeds max it removes the oldest log
		"""
		try:
			print("cleanup_logs")
			logFolder=path.dirname(self.file_path)
			print("basename {} - {}".format(self.file_path,logFolder))
			logFiles= glob(logFolder+'/*'+ self.log_extension)
			logCount= len(logFiles)
			print("cleanup_logs '"+ logFolder+'/*'+ self.log_extension +"' {}/{}".format(logCount,self.max_file_count))
			if logCount > self.max_file_count:				
				oldest_file = min(logFiles, key=path.getctime)
				print("logger.cleanup_logs count {}/{} deleting {}".format(logCount,self.max_file_count,oldest_file))
				remove(oldest_file) # os.remove

		except Exception as e:
			self.error("Error cleaning up logs. {}".format(e))
		
		
	def zip(self):
		"""zip all logs and delete all but current"""
		print("zip NOTIMPLIMENTED")
		#todo
		#

	def trace(self, func):
		"""
		marks entry and exit of a function wrapped in this decorator @log.trace
		logs to disk and console
		:param func:
		:return:
		"""
		def inner(*args, **kwargs):
			message = func.__name__ + str(args)
			self.log('>' + message, Level.TRACE)
			result = func(*args, **kwargs)
			self.log('<' + result, Level.TRACE)
			return result
		return inner

if __name__ == '__main__':
	l=Logger()
	l.max_file_size = 100
	l.max_file_count = 3
	l.attachFile("logs/current.log")
	l.attachSyslog("localhost")
	l.info("logger self test")
	l.warn("logger self test")
	l.error("logger self test")

	@l.trace
	def hello(msg):
		return "decorator hello "+msg

	hello("logger decorator self test")