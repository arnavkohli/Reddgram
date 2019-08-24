import os

class Cleaner:

	@staticmethod
	def clean(path=os.getcwd()):
		"""
			Removes all files which do not have
			a .py extension.
		"""

		l = os.listdir(path)
		to_delete = []

		for item in l:
			if ('.' in item and 'html' not in item) or os.path.isdir(path + '/{}'.format(item)):
				pass
			else:
				to_delete.append(item)

		for d in to_delete:
			print ('Deleting: {}'.format(d))
			os.remove(d)
		print ('Cleaner finished.')