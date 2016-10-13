from subprocess import Popen, PIPE
from threading import Thread

import sparkmagic.utils.configuration as conf


class KerberosThread(Thread):
    def __init__(self, event, endpoint, ipython_display):
        Thread.__init__(self)
        self.stopped = event
        self.setDaemon(True)
        self.endpoint = endpoint
        self.ipython_display = ipython_display

    def run(self):
        self.kinit()
        while not self.stopped.wait(conf.kerberos_renew_time_interval_seconds()):
            self.kinit()

    def kinit(self):
        kinit_args = [conf.kinit(), self.endpoint.username]
        kinit = Popen(kinit_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = kinit.communicate(('%s\n' % self.endpoint.password).encode())
        if kinit.wait() is not 0:
            self.ipython_display.html(err.decode(conf.process_output_decoding()))
        kinit.terminate()
