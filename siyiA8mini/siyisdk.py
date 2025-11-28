import socket
from .core import *
from .utils import *
import time
from pynput import keyboard

class SIYISDK:
    def __init__(self, SERVER_IP, SERVER_PORT, BUFF_SIZE):
        # UDP initialization: IP, port, buffer size
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.send_addr = (self.SERVER_IP, self.SERVER_PORT)
        self.BUFF_SIZE = BUFF_SIZE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    
    def send_receive_date(self,send_buf):
        """
            Send and receive data
        """
        #print("Send HEX data")
        try:
            self.sock.sendto(send_buf, self.send_addr)
        except Exception as e:
            print(f"sendto error: {e}")
            return

        # Receive return data from gimbal camera
        try:
            recv_buf, recv_addr = self.sock.recvfrom(self.BUFF_SIZE)
            return recv_buf
        except Exception as e:
            print(f"recvfrom error: {e}")
            return
        
        


    def one_click_down(self):
        """ 
        One-click down, directly rotate -90 degrees
        """
        self.turn_to(0,-90)
        """
        # Create command line class, calculate send_buff
        cmd=CommandLine(CMD_ID=[0x0e],DATA=[0x00, 0x00, 0x3e, 0xfe])
        send_buf=cmd.create_send_buf()
        # Send and receive data
        recv_date=self.send_receive_date(send_buf) 

        # Print received data in hexadecimal format
        print("Received HEX data: ", end="")
        print(" ".join(f"{byte:02x}" for byte in recv_date))
        """

    def get_device_hardwareID(self):
        """
        Get gimbal camera hardware ID
        """
        cmd=CommandLine(CMD_ID=[0x02],DATA=[])
        # Create command line class, calculate send_buff
        send_buf=cmd.create_send_buf()
        
        # Send and receive data
        recv_date=self.send_receive_date(send_buf) 
          
         # Print received data in hexadecimal format
        print("Received HEX data: ", end="")
        print(" ".join(f"{byte:02x}" for byte in recv_date))
        # Parse received data
        cmd.recv_date_parser(recv_date);
        
        
        
    def get_device_workmode(self):
        """"
        Get gimbal camera work mode
        """
        cmd=CommandLine(CMD_ID=[0x19],DATA=[])
        # Create command line class, calculate send_buff
        send_buf=cmd.create_send_buf()
        
        # Send and receive data
        recv_date=self.send_receive_date(send_buf) 
          
         # Print received data in hexadecimal format
        print("Received HEX data: ", end="")
        print(" ".join(f"{byte:02x}" for byte in recv_date))
        # Parse received data
        cmd.recv_date_parser(recv_date);

    
    def keep_turn(self):
        """
        Control gimbal continuous rotation
        """
        speed_yaw =50 # Rotation speed, default is 0, range [0-100], 0 means stationary
        speed_pitch=50
        turn=[0,0]# [yaw,pitch]
        last_turn = [0, 0]  # Record the previous turn state
        running = True  # Used to control main loop
         
        # Move the camera
        def camera_move():
            nonlocal last_turn, turn
            if turn != last_turn:
                last_turn = turn.copy()  # Update last_turn value
                # print(f"turn changed: {turn}")
                # Send control signal based on turn valueignal based on turn value
                ut =utils()
                turn_yaw_hex=ut.int_to_hex_array_uint8(turn[0])     # Convert to hexadecimal
                turn_pitch_hex=ut.int_to_hex_array_uint8(turn[1])
                cmd=CommandLine(CMD_ID=[0x07],DATA=turn_yaw_hex+turn_pitch_hex)
                # Create command line class, calculate send_buff
                send_buf=cmd.create_send_buf()
                # Send and receive data
                recv_date=self.send_receive_date(send_buf) 


        # Callback function for key pressnction for key press
        def on_press(key):
            nonlocal speed_yaw, speed_pitch,turn # Declare use of external function's local variables
            try:

                if key ==keyboard.Key.up:# When up arrow is pressed
                    turn[1]= speed_pitch
                if key ==keyboard.Key.down:# When down arrow is pressed
                    turn[1]= speed_pitch*(-1)
                if key ==keyboard.Key.left:# When left arrow is pressed
                    turn[0]= speed_yaw*(-1)
                if key ==keyboard.Key.right:# When right arrow is pressed
                    turn[0]= speed_yaw
                camera_move()
            except AttributeError:
                pass

        # Callback function for key release
        def on_release(key):
            nonlocal speed_yaw, speed_pitch,running
            if key == keyboard.Key.esc:
                print("Esc key pressed, exit listening")
                running = False  # Set control variable to False to terminate main loop
                return False  # Returning False will automatically stop the listener
                
            try:
                if key==keyboard.Key.up:
                    turn[1]=0
                if key ==keyboard.Key.down:
                    turn[1]=0
                if key ==keyboard.Key.left:
                    turn[0]=0
                if key ==keyboard.Key.right:
                    turn[0]=0
                camera_move()
                # Use WSAD to increase/decrease speed, step size is 10
                if key.char =="w":
                    speed_pitch=speed_pitch+10
                    if(speed_pitch>100):
                        speed_pitch=100
                    if(speed_pitch<0):
                        speed_pitch=0
                    print(f"Current pitch speed: {speed_pitch}")
                if key.char =="s":
                    speed_pitch=speed_pitch-10
                    if(speed_pitch>100):
                        speed_pitch=100
                    if(speed_pitch<0):
                        speed_pitch=0
                    print(f"Current pitch speed: {speed_pitch}")
                if key.char =="a":
                    speed_yaw=speed_yaw-10
                    if(speed_yaw>100):
                        speed_yaw=100
                    if(speed_yaw<0):
                        speed_yaw=0
                    print(f"Current yaw speed: {speed_yaw}")
                if key.char =="d":
                    speed_yaw=speed_yaw+10
                    if(speed_yaw>100):
                        speed_yaw=100
                    if(speed_yaw<0):
                        speed_yaw=0
                    print(f"Current yaw speed: {speed_yaw}")
                
            except AttributeError:
                pass
            

        
        # Create and start listener in non-blocking mode
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()  # Start listener (non-blocking)
        print("Enter manual control mode, ↑↓←→ to control camera movement, WSAD to control rotation speed, ESC to exit control mode")
        # listener.join()  # Wait for listener to stop
        # Use control variable to keep main thread running, avoid exit
        while running:
            time.sleep(0.1)
            
            
    

   

    def one_click_back(self):
        """
        One-click center/home
        """
        cmd=CommandLine(CMD_ID=[0x08],DATA=[0x01])
        # Create command line class, calculate send_buff
        send_buf=cmd.create_send_buf()
        
        # Send and receive data
        recv_date=self.send_receive_date(send_buf) 
          
         # Print received data in hexadecimal format
        print("Received HEX data: ", end="")
        print(" ".join(f"{byte:02x}" for byte in recv_date))
        
    def get_position(self):
        """
        Get gimbal attitude/position
        """
        cmd=CommandLine(CMD_ID=[0x0D],DATA=[])
        send_buf=cmd.create_send_buf()
         # Send and receive data
        recv_date=self.send_receive_date(send_buf) 
          
         # Print received data in hexadecimal format
        print("Received HEX data: ", end="")
        print(" ".join(f"{byte:02x}" for byte in recv_date))
        cmd.recv_date_parser(recv_date)
        
    def turn_to(self,yaw,pitch):
        """
        Set gimbal control angle, precision is one decimal place, supports yaw: -135.0 to 135.0; pitch: -90.0 to 25.0
        """
        if((-135<=yaw<=135)&(-90<=pitch<=25.0)):
            turn_yaw=int(yaw*10)     # Round to integer
            turn_pitch=int(pitch*10)
            ut=utils()
            turn_yaw_hex=ut.int_to_hex_array_uint16(turn_yaw)     # Convert to hexadecimal
            turn_pitch_hex=ut.int_to_hex_array_uint16(turn_pitch)
            
            cmd=CommandLine(CMD_ID=[0x0e],DATA=turn_yaw_hex+turn_pitch_hex)
             # Create command line class, calculate send_buff
            send_buf=cmd.create_send_buf()
        
            # Send and receive data
            recv_date=self.send_receive_date(send_buf) 
             # Print received data in hexadecimal format
            print("Received HEX data: ", end="")
            print(" ".join(f"{byte:02x}" for byte in recv_date))
             # Delay one second, wait for action to complete
            time.sleep(1.5)
            
        else:
            print("Incorrect angle setting, supports yaw: -135.0 to 135.0; pitch: -90.0 to 25.0")
            
    def single_turn_to(self,angle,direction):
        """
        Single-axis angle control, angle supports yaw: -135.0 to 135.0; pitch: -90.0 to 25.0; direction: 0: yaw, 1: pitch
        """
        if (direction==0):
            if(-135.0<angle<135.0):
                yaw=int(angle*10)
                ut=utils()
                yaw_hex=ut.int_to_hex_array_uint16(yaw)
                cmd=CommandLine(CMD_ID=[0x41],DATA=yaw_hex+[0x00])
                
                send_buf=cmd.create_send_buf()
                recv_date=self.send_receive_date(send_buf) 
                # Print received data in hexadecimal format
                print("Received HEX data: ", end="")
                print(" ".join(f"{byte:02x}" for byte in recv_date))
                # Delay one second, wait for action to complete
                time.sleep(1.5)
            else:
                print("Incorrect angle setting")


        elif(direction==1):
            if(-90<angle<25):
                pitch=int(angle*10)
                ut=utils()
                pitch_hex=ut.int_to_hex_array_uint16(pitch)
                cmd=CommandLine(CMD_ID=[0x41],DATA=pitch_hex+[0x01])
                
                send_buf=cmd.create_send_buf()
                recv_date=self.send_receive_date(send_buf) 
                # Print received data in hexadecimal format
                print("Received HEX data: ", end="")
                print(" ".join(f"{byte:02x}" for byte in recv_date))
                # Delay one second, wait for action to complete
                time.sleep(1.5)
            else:
                print("Incorrect angle setting")
        else:
            print("Unknown control direction, please enter 0 or 1")

    

    def get_config_info(self):
        """
        Get gimbal configuration information
        """
        cmd=CommandLine(CMD_ID=[0x0A],DATA=[])
        send_buf=cmd.create_send_buf()
         # Send and receive data
        recv_date=self.send_receive_date(send_buf) 
          
         # Print received data in hexadecimal format
        print("Received HEX data: ", end="")
        print(" ".join(f"{byte:02x}" for byte in recv_date))
        # Parse received data
        cmd.recv_date_parser(recv_date);
        

    def get_encode_info(self):
        """
         Get camera encoding parameters
        """
        cmd=CommandLine(CMD_ID=[0x20],DATA=[0x01])
        send_buf=cmd.create_send_buf()
         # Send and receive data
        recv_date=self.send_receive_date(send_buf) 
          
         # Print received data in hexadecimal format
        print("Received HEX data: ", end="")
        print(" ".join(f"{byte:02x}" for byte in recv_date))
        # Parse received data
        cmd.recv_date_parser(recv_date);
        
    def set_encode_info(self):
        """
        Set camera encoding format
        """
        "It is recommended to use SIYI Assistance software for configuration"
        pass

    def format_SDcard(self):
        """
        Format SD card
        """
        cmd=CommandLine(CMD_ID=[0x48],DATA=[])
        send_buf=cmd.create_send_buf()
         # Send and receive data
        recv_date=self.send_receive_date(send_buf) 
          
         # Print received data in hexadecimal format
        print("Received HEX data: ", end="")
        print(" ".join(f"{byte:02x}" for byte in recv_date))
        # Parse received data
        cmd.recv_date_parser(recv_date);

        
    def device_restart(self,camera_restart,gimbal_restart):
        """
        Camera or gimbal restart, 0: no action; 1: restart
        """
        ut=utils()
        if((camera_restart==0)|(camera_restart==1)):
            camera_act=ut.int_to_hex_array_uint8(camera_restart)
        else:
            print("Invalid command, please set 0 (no action) or 1 (restart)")
        
        if((gimbal_restart==0)|(gimbal_restart==1)):
            gimbal_act=ut.int_to_hex_array_uint8(gimbal_restart)
        else:
            print("Invalid command, please set 0 (no action) or 1 (restart)")
        cmd=CommandLine(CMD_ID=[0x80],DATA=camera_act+gimbal_act)
        send_buf=cmd.create_send_buf()
         # Send and receive data
        recv_date=self.send_receive_date(send_buf) 
          
         # Print received data in hexadecimal format
        print("Received HEX data: ", end="")
        print(" ".join(f"{byte:02x}" for byte in recv_date))


    def close(self):
        # Close socket
        self.sock.close()
        
