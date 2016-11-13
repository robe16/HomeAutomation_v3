def _check_tvlistingsqueue(q_tvlistings):
    # Check listings in queue
    if not q_tvlistings.empty():
        temp = q_tvlistings.get()
        q_tvlistings.put(temp)
        return temp
    else:
        return False
