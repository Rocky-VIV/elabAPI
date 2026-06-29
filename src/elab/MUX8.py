from .main import instrument

class MUX28(instrument):

    def __init__(self, com_port, **kwargs):
        super().__init__(com_port, baud_rate=115200, **kwargs)
        self.model = 'Arduino MUX 28'
        self.type = 'MUX'
        if self.verbose == True:
            print(f'{self.model} connected on {com_port} at {self.baud_rate} bits/s')

    def electrode(self,n):
        if n not in range(1,29):
            raise ValueError('Electrode n must be between 1 and 28')
        self.send_comm(n+100)
        
    def ida(self,n):
        if n not in range(1,15):
            raise ValueError('IDA n must be between 1 and 14')
        self.send_comm(n)

    def gen(self,n):
        if n not in range(1,15):
            raise ValueError('Generator n must be between 1 and 14')
        command = (115-n)
        self.send_comm(command)

    def coll(self,n):
        if n not in range(1,15):
            raise ValueError('Collector n must be between 1 and 14')
        command = (114+n)
        self.send_comm(command)
        
    def send_comm(self,n):
        self.ser.write(bytes(f'<{n}>', 'utf-8'))
        msg = self.ser.readline()
        if self.verbose == True:
            print(msg.decode('utf-8'))

    def gen_all(self):
        self.send_comm(230)
    
    def coll_all(self):
        self.send_comm(220)

    def all(self):
        self.send_comm(240)
