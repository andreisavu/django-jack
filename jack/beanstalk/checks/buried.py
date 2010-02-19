""" Basic check for buried jobs

The max number for buried jobs should not exced 3 and
the max age of buried job should not exced 120 seconds.
"""


def do_check(client):
    current_buried = client.stats()['current-jobs-buried']
    if current_buried >= 3:
        return 'found %d jobs buried.' % current_buried

    max_age, max_jid = 0, 0
    for tube in client.tubes():
        client.use(tube)

        job = client.peek_buried()
        if job is not None:
            age = int(job.stats()['age'])
            if age > max_age:
                max_age, max_jid = age, job.jid

    if max_jid and max_age > 120:
        return 'found old buried job #%d' % max_jid
            

