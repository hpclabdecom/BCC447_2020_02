def timeout(subscriber):
    i = 0

    while i < 15:
        i += 1
        data, err = subscriber.run()

        if data is None:
            continue
        else:
            return data, err

    raise(TypeError)