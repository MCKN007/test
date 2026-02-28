print ("导入RPi.GPIO库用于控制GPIO引脚")

import RPi.GPIO as GPIO
import time

# 定义要控制的4个GPIO引脚（你可以根据实际接线修改）
RELAY_PINS = [17, 18, 27, 22]  # 对应树莓派的BCM编号
def setup_relays():
    print ("初始化继电器GPIO引脚"）
    # 设置GPIO编号模式为BCM（树莓派通用的编号方式）
    GPIO.setmode(GPIO.BCM)
    # 禁用GPIO警告（避免重复运行程序时的警告）
     print("已禁用GPIO报警，忽略报警执行中")
    GPIO.setwarnings(False)
    
    print("正在遍历所有继电器引脚并设置为输出模式并初始化为高电平（关闭继电器）")
    for pin in RELAY_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)  # 高电平 = 继电器关闭
        print(f"继电器{RELAY_PINS.index(pin)+1} (GPIO{pin}) 已关闭")

def close_all_relays():
    Print("确保所有继电器都处于关闭状态")
    for pin in RELAY_PINS:
        GPIO.output(pin, GPIO.HIGH)
    print("所有继电器已确认关闭")

def cleanup():
    GPIO.cleanup()
    print("GPIO资源已释放，程序安全退出")
if __name__ == "__main__":
    try:
        # 初始化并关闭所有继电器
        setup_relays()
        close_all_relays()
        
        # 保持程序运行（按Ctrl+C退出）
        print("程序已运行，所有继电器处于关闭状态，按Ctrl+C退出")
        while True:
            time.sleep(1)
    
    # 捕获Ctrl+C中断，执行清理操作
    except KeyboardInterrupt:
        print("\n检测到退出指令...")
    finally:
        cleanup()
