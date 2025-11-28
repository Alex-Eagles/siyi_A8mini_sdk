import inspect
from .crc16 import CRC16

class CommandLine:
    def __init__(self, STX=[0x55, 0x66], CTRL=[0x01], SEQ=[0x00,0x00], CMD_ID=[], DATA=[]):
        # send_buff construction
        self.STX = STX                                  # Start flag
        self.CTRL = CTRL                                # Whether data packet needs ack, 0 needs, 1 doesn't need
        self.DATA=DATA                                  # Data to send
        self.Data_len= self.calculate_data_len()        # Data byte length to send
        self.SEQ = SEQ                                  # Frame sequence, range (0-65535)
        self.CMD_ID = CMD_ID                            # Command IDmand ID
        
        self.CRC16=self.calculate_crc16()               # CRC checksum
        

    def calculate_data_len(self):
        # Calculate data_len
        data_len = len(self.DATA)
        return [(data_len & 0xFF), (data_len >> 8) & 0xFF]



    def calculate_crc16(self):
        # Calculate CRC16
        data_to_crc = self.STX+self.CTRL+self.Data_len+self.SEQ+self.CMD_ID+self.DATA
        crc_calculator = CRC16()
        crc = crc_calculator.calculate(data_to_crc)  #  CRC16 计算逻辑
        return crc
    
    def create_send_buf(self):
        # Construct send_buff
        return bytes(self.STX) + bytes(self.CTRL) + bytes(self.Data_len) +bytes(self.SEQ)+ bytes(self.CMD_ID)+bytes(self.DATA) + bytes(self.CRC16)
    
    def recv_date_parser(self,recv_data):
        # Parse the received data to corresponding values, automatically corresponds to parsing process based on different calling functions
        caller_function_name = inspect.stack()[1].function # Function name that calls this function
        datelength=int.from_bytes(recv_data[3:4], byteorder='little') # Calculate data length
        date=recv_data[8:8+datelength] # Get data segment
        
        if(caller_function_name=="get_device_hardwareID"):
            ID_dict={0x6B:"ZR10",
                     0x73:"A8 mini",
                     0x75:"A2 mini",
                     0x78:"ZR30",
                     0x82:"ZT6",
                     0x7A:"ZT30"
                     }
            hex_value = int(date[:2].decode(), 16)
            hardware_ID=ID_dict.get(hex(hex_value),"Unknown device")
            print(f"Current device: {hardware_ID}")
            
        elif(caller_function_name=="get_device_workmode"):
            workmode_dict={0x00:"Lock mode",
                           0x01:"Follow mode",
                           0x02:"FPV mode"}
            # Find corresponding mode based on mode byte
            
            mode = workmode_dict.get(int.from_bytes(date, byteorder='little'), "Unknown mode")
            print(f"Current mode: {mode}")
             
        elif(caller_function_name=="get_position"):
            yaw=int.from_bytes(date[:2], byteorder='little')/10
            pitch=int.from_bytes(date[2:4], byteorder='little')/10
            roll=int.from_bytes(date[4:6], byteorder='little')/10
            yaw_velocity=int.from_bytes(date[6:8], byteorder='little')/10
            pitch_velocity=int.from_bytes(date[8:10], byteorder='little')/10
            roll_velocity=int.from_bytes(date[8:10], byteorder='little')/10
            print(f"Yaw: {yaw}; Pitch: {pitch}; Roll: {roll}; Yaw velocity: {yaw_velocity}; Pitch velocity: {pitch_velocity}; Roll velocity: {roll_velocity}")

        elif(caller_function_name=="get_config_info"):
            hdr_dict={0x00:"Off",0x01:"On"}
            record_dict={0x00:"Recording not started",
                         0x01:"Recording started",
                         0x02:"TF card not inserted",
                         0x03:"TF card recording video lost, please check IF card"}
            motion_mode_dict={0x00:"Lock mode",
                              0x01:"Follow mode",
                              0x02:"FPV mode"}
            mounting_dir_dict={0x00:"reseve",
                               0x01:"Normal",
                               0x02:"Inverted"}
            video_mode_dict={0x00:"HDMI output",
                             0x01:"CVBS output"}
            
            hdr=hdr_dict.get(int.from_bytes(date[1:2], byteorder='little'), "Unknown HDR mode")
            record=record_dict.get(int.from_bytes(date[3:4], byteorder='little'), "Unknown recording status")
            motion=motion_mode_dict.get(int.from_bytes(date[4:5], byteorder='little'), "Unknown gimbal mode")
            mounting=mounting_dir_dict.get(int.from_bytes(date[5:6], byteorder='little'), "Unknown gimbal mounting orientation")
            video=video_mode_dict.get(int.from_bytes(date[6:7], byteorder='little'), "Unknown video output mode")
            print(f"HDR mode: {hdr}; Recording status: {record}; Gimbal mode: {motion}; Gimbal mounting orientation: {mounting}; Video output mode: {video}")

        elif(caller_function_name=="get_encode_info"):
            stream_type_dict={0x00:"Recording stream",
                              0x01:"Main stream",
                              0x02:"Sub stream"}
            video_encode_type_dict={0x01:"H264",
                                    0x02:"H265"}
            stream=stream_type_dict.get(int.from_bytes(date[0:1], byteorder='little'), "Unknown stream")
            video_enc_type=video_encode_type_dict.get(int.from_bytes(date[1:2], byteorder='little'), "Unknown encoding format")
            resolution_L=int.from_bytes(date[2:4], byteorder='little')
            resolution_H=int.from_bytes(date[4:6], byteorder='little')
            video_bit_rate=int.from_bytes(date[6:8], byteorder='little')
            video_frame_rate=int.from_bytes(date[8:9], byteorder='little')
            print(f"Current stream: {stream}; Encoding format: {video_enc_type}; Resolution width: {resolution_L}; Resolution height: {resolution_H}; Video bitrate Kbps: {video_bit_rate}; Video frame rate: {video_frame_rate}")
        
        elif(caller_function_name=="format_SDcard"):  
            format_state_dict={0x00:"Format failed",
                               0x01:"Format successful"}
            format_s=format_state_dict.get(int.from_bytes(date[0:1], byteorder='little'), "Unknown format status")
            print(f"Format status: {format_s}")
            
        else:pass

  


 
