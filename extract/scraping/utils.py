import numpy


def random_wait(mean):
    done = False
    while done is False:
        length = numpy.random.normal(
            mean, mean / 5
        )
        if length > 0:
            done = True
    return length
