# Copyright (c) 2010 ShootQ Inc. <development [at] shootq [dot] com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""An IOSTAT plugin for ServerDensity that displays nice data for 
every device

     The output of this iostat plugin ncludes  the  following
     information (most of the information found in the iostat
     man page):

     device    name of the disk

     r/s       reads per second

     w/s       writes per second

     kr/s      kilobytes read per second

     kw/s      kilobytes written per second

     wait      average number of transactions waiting for service
               (queue length)

     actv      average number of transactions actively being ser-
               viced  (removed  from  the  queue but not yet com-
               pleted)

     svc_t     average  response  time  of  transactions, in mil-
               liseconds

     %w        percent of time there are transactions waiting for
               service (queue non-empty)

     %b        percent of time the disk is busy (transactions  in
               progress)

"""



from subprocess         import Popen, PIPE


class Iostat(object):

    def __init__(self, agentConfig, checksLogger, rawConfig):
	    self.agentConfig = agentConfig
	    self.checksLogger = checksLogger
	    self.rawConfig = rawConfig
		
    def iostat(self):
        """Run the iostat command with the parameters we need
        and return them in a nice dictionary"""
        command = Popen("iostat -x", shell=True, stdout=PIPE, close_fds=True).communicate()[0]
        stats = {}
        for i in command.split('\n'):
            if i.startswith('device') or 'extend' in i: continue
            foo = i.split()
            if len(foo) < 1: continue
            device = foo[0]
            device_stats = {
                    "r/s"   : foo[1],
                    "w/s"   : foo[2],
                    "kr/s"  : foo[3],
                    "kw/s"  : foo[4],
                    "wait"  : foo[5],
                    "actv"  : foo[6],
                    "svc_t" : foo[7],
                    "%w"    : foo[8],
                    "%b"    : foo[9]
                    }
            stats[device] = device_stats
        return stats



    def run(self):
        """Get called by the SD Agent"""
        return self.iostat()
    
