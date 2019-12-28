import time

def clock(func):
	def clocked(*args):
		t0 = time.perf_counter()
		result = func(*args)
		elapsed = time.perf_counter() - t0
		arg_str = ", ".join(repr(arg) for arg in args)
		print("[%0.8fs %s(%s) -> %r" % (elapsed,func.__name__,arg_str,result))
		return result
	return clocked