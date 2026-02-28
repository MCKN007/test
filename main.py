print ("导入RPi.GPIO库用于控制GPIO引脚")
# 导入RPi.GPIO库用于控制GPIO引脚
import RPi.GPIO as GPIO
import time

# 定义所有可用的继电器控制引脚（根据实际接线修改！）
AVAILABLE_PINS = [17, 18, 27, 22]  # 树莓派BCM编号
# 继电器触发逻辑（大多数3.3V继电器为低电平触发，如需高电平触发则反转）
RELAY_ON = GPIO.LOW    # 开启继电器的电平
RELAY_OFF = GPIO.HIGH  # 关闭继电器的电平

def setup_relays():
    """初始化继电器GPIO引脚，默认全部关闭"""
    # 设置GPIO编号模式为BCM（树莓派官方推荐）
    GPIO.setmode(GPIO.BCM)
    # 禁用GPIO重复初始化警告
    GPIO.setwarnings(False)
    
    # 初始化所有可用引脚为输出模式，并默认关闭继电器
    for pin in AVAILABLE_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, RELAY_OFF)
    print(f"✅ 继电器初始化完成")
    print(f"🔧 可用控制引脚：{AVAILABLE_PINS}")
    print(f"📌 指令说明：start=开启继电器 | stop=关闭继电器 | q=退出程序\n")

def parse_pin_input(input_str):
    """解析用户输入的引脚号，返回有效整数列表"""
    # 去除空格并按逗号分割
    pin_str_list = [p.strip() for p in input_str.split(',') if p.strip()]
    valid_pins = []
    
    for pin_str in pin_str_list:
        try:
            pin = int(pin_str)
            if pin in AVAILABLE_PINS:
                valid_pins.append(pin)
            else:
                print(f"⚠️  警告：引脚{pin}不在可用列表中，已跳过")
        except ValueError:
            print(f"⚠️  警告：'{pin_str}' 不是有效数字引脚号，已跳过")
    
    return valid_pins

def control_relays(operation, target_pins):
    """执行继电器控制操作"""
    if not target_pins:
        print("❌ 无有效引脚可执行操作")
        return
    
    # 确定要输出的电平
    target_level = RELAY_ON if operation == "start" else RELAY_OFF
    operation_text = "开启" if operation == "start" else "关闭"
    
    # 执行控制
    for pin in target_pins:
        GPIO.output(pin, target_level)
        print(f"✅ 继电器引脚{pin}已{operation_text}")

def cleanup():
    """程序退出时清理GPIO资源，避免引脚状态异常"""
    GPIO.cleanup()
    print("\n🔌 GPIO资源已释放，程序安全退出")

if __name__ == "__main__":
    try:
        # 初始化继电器
        setup_relays()
        
        while True:
            # 第一步：获取操作指令
            op_input = input("请输入操作指令（start=开启 | stop=关闭 | q=退出）：").strip().lower()
            
            # 退出逻辑
            if op_input == 'q':
                break
            
            # 校验操作指令合法性
            if op_input not in ['start', 'stop']:
                print("❌ 无效指令！仅支持 start/stop/q")
                continue
            
            # 第二步：获取要控制的引脚号
            pin_input = input(f"请输入要{('开启' if op_input == 'start' else '关闭')}的继电器引脚号（多个用逗号分隔）：").strip()
            target_pins = parse_pin_input(pin_input)
            
            # 执行控制操作
            control_relays(op_input, target_pins)
    
    # 捕获Ctrl+C强制退出
    except KeyboardInterrupt:
        print("\n\n⚠️  检测到强制退出指令...")
    finally:
        # 无论正常退出还是强制退出，都清理GPIO
        cleanup()
