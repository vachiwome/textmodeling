import matplotlib.pyplot as plt

def plot_vector(vec):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	x_points = xrange(0,len(vec))
	p = ax.plot(x_points, vec, 'b')
	ax.set_xlabel('x-points')
	ax.set_ylabel('y-points')
	ax.set_title('Simple XY point plot')
	fig.show()