import inspect
import sys
import types
from warnings import warn
from collections import ChainMap, deque


def _is_class_obj(obj):
	""" A dummy way of telling if an object is a Class Object"""
	return callable(obj) and not hasattr(obj, '__code__')


def get_contained_functions(f):
	""" Given a function object, return a tuple of function names called by f """
	return f.__code__.co_names


def get_source_code(f, locals=None, globals=None):
	""" Get the source code of a function 
	:param f: Can be a function type or String,
		if a string is given, we look into 
		locals and globals to find the definition of f
	:return The function body along with a tuple of function names 
		that will be called by f
	"""

	# In the case we couldn't find the definition of the function
	if f is None:
		return '', ()

	if isinstance(f, types.FunctionType):
		return inspect.getsource(f), get_contained_functions(f)
	elif isinstance(f, str):
		var_map = ChainMap(locals or {}, globals or {})
		return get_source_code(var_map.get(f, None), locals, globals)
	elif isinstance(f, types.ModuleType):
		warn('{} is a Module object. Support for external moduels coming soon.'.format(f))
		return '', ()
	elif _is_class_obj(f):
		warn('Failed to get the code for {}. The support for Class object soon to be added'.format(f))
		return '', ()
	else:
		raise TypeError('{} should either be a function or string.'.format(f))


def get_code(f, newlines=1):

	_globals = f.__globals__

	definitions = list()
	queue = deque([f])
	
	while queue:
		f = queue.popleft()
		code, functions = get_source_code(f, None, _globals)
		if code:
			definitions.append(code)
		queue.extend(functions)

	delimiter = '\n' * newlines
	return delimiter.join(definitions)



