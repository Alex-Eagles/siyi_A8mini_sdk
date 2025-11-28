from siyiA8mini import siyisdk



siyi=siyisdk.SIYISDK("192.168.144.25",37260,1024)

# siyi.device_restart(0, 1)
# siyi.keep_turn()
# siyi.turn_to(0, -90)
# siyi.get_device_workmode()
siyi.one_click_down()
# siyi.get_config_info()
siyi.close()




