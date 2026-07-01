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
        # Pass 1-28 to Arduino
        self.send_comm(n)
        
    def ida(self,n):
        if n not in range(1,15):
            raise ValueError('IDA n must be between 1 and 14')
        self.send_comm(n)

    def gen(self,n):
        if n not in range(1,15):
            raise ValueError('Generator n must be between 1 and 14')
        # Maps Gen 1-14 to WE1 channels 1-14
        # Standard Mapping (Gen 1 = Electrode 1)
        self.send_comm(n)

        # NOTE: Noticed that previous MUX8 required generators to be reversed, uncomment line below if it needs it.
        # Reversed Mapping (Gen 1 = Electrode 14), if using reversed make sure to comment out/delete the self.send_comm(n) line!
        # self.send_comm(15-n)

    def coll(self,n):
        if n not in range(1,15):
            raise ValueError('Collector n must be between 1 and 14')
        # Maps Coll 1-14 to WE2 channels 15-28 (14+1=15... 14+14=28)
        self.send_comm(n+14)
        
    def send_comm(self,n):
        self.ser.write(bytes(f'<{n}>', 'utf-8'))
        msg = self.ser.readline()
        if self.verbose == True:
            print(msg.decode('utf-8'))

    def gen_all(self):
        self.send_comm(100) # All WE1
    
    def coll_all(self):
        self.send_comm(200) # All WE2

    def all(self):
        self.send_comm(300) # Everything

    def global_short(self):
        self.send_comm(400) # Everything with bridge relay closed

    def bridge_only(self):
        self.send_comm(90) # Only bridge relay closed

    def clear_all(self):
        self.send_comm(0) # Opens every relay on board
