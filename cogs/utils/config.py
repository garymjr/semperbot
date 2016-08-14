import json
import os

class Config:
	def __init__(self, file):
		self.file = 'data/' + file
		if os.path.exists(self.file):
			with open(self.file) as f:
				self.config = json.load(f)
		else:
			with open(self.file, 'w') as f:
				self.config = {}
				f.write(json.dumps(self.config))

	def get(self, key):
		if key in self.config.keys():
			return self.config[key]
		return None

	def set(self, key, setting):
		with open(self.file, 'w') as f:
			self.config[key] = setting
			f.write(json.dumps(self.config))