
# SIYISDK

A Python SDK developed for the SIYI A8mini gimbal camera, facilitating easy access to gimbal functions.

## Usage
### Dependency: pynput, used for monitoring keyboard input
```bash
pip install pynput
```

### 1. Use Source Code Directly

Clone the entire project locally, enter the `test.py` file, change the corresponding camera IP address and port, then run:

```bash
python test.py
```

### 2. Install Package with pip (Recommended)

Download `siyiA8mini-0.1.0-py3-none-any.whl` from [release](https://github.com/Percylevent/siyi_A8mini_sdk/releases/tag/v1.0.0) locally, then run:

```bash
pip install siyiA8mini-0.1.0-py3-none-any.whl
```

Then create a new `test.py`, write the example program (Example), and run:

## Example (test.py)

```python
# Import package
from siyiA8mini import siyisdk

# Instantiate
siyi_controler = siyisdk.SIYISDK("192.168.1.25", 37260, 1024)

# Start keyboard control function
siyi_controler.keep_turn()

# End control
siyi_controler.close()
```

## Function

| Function Name                        | Parameters                            | Description                                                                                                                                       |
|-------------------------------|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `one_click_down()`             | None                              | One-click down, camera rotates vertically 90°.                                                                                                               |
| `get_device_hardwareID()`      | None                              | Get device hardware information, printed to console.                                                                                                          |
| `get_device_workmode()`        | None                              | Get device running status, printed to console.                                                                                                          |
| `keep_turn()`                  | None                              | Enter keyboard control camera rotation mode, `↑↓←→` controls camera movement, `WSAD` controls rotation speed, `ESC` exits control mode.                                                |
| `one_click_back()`             | None                              | One-click center, returns camera orientation to home position.                                                                                                                  |
| `get_position()`               | None                              | Get current camera attitude, printed to console.                                                                                                          |
| `turn_to(yaw, pitch)`          | `yaw`: Horizontal rotation angle; `pitch`: Vertical rotation angle | Rotate camera to a certain angle, `yaw`: -135.0 to 135.0; `pitch`: -90.0 to 25.0.                                                                         |
| `single_turn_to(angle, direction)` | `angle`: Rotation angle; `direction`: Direction | Control camera single-axis rotation, `angle` determines angle, `direction` determines direction.                                                                                 |
| `get_config_info()`            | None                              | Get gimbal configuration information, printed to console.                                                                                                          |
| `get_encode_info()`            | None                              | Get camera encoding information, printed to console.                                                                                                          |
| `format_SDcard()`              | None                              | Format SD card.                                                                                                                              |
| `device_restart(camera_restart, gimbal_restart)` | `camera_restart`: 0 or 1; `gimbal_restart`: 0 or 1 | Control camera and gimbal restart, by setting parameters 0 or 1 to determine whether to restart.                                                                                     |
| `close()`                      | None                              | End control, called at the end of the program.                                                                                                                    |


## Author

- Institution: Shanghai Jiao Tong University
- Email: [zhangpengcheng@sjtu.edu.cn](mailto:zhangpengcheng@sjtu.edu.cn)
- GitHub: [https://github.com/Percylevent](https://github.com/Percylevent)



## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

