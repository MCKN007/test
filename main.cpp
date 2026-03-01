#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>  // 用于sleep函数（秒级延时）
#include <stdexcept> // 用于异常处理

// GPIO sysfs 基础路径
const std::string GPIO_BASE_PATH = "/sys/class/gpio/";

// GPIO操作类
class GPIO {
private:
    int pin;
    std::string pinPath;

    // 向指定文件写入内容（核心操作）
    bool writeFile(const std::string& filePath, const std::string& content) {
        std::ofstream file(filePath);
        if (!file.is_open()) {
            std::cerr << "错误：无法打开文件 " << filePath << std::endl;
            return false;
        }
        file << content;
        file.close();
        return true;
    }

public:
    // 构造函数：初始化引脚号和路径
    GPIO(int pinNum) : pin(pinNum) {
        pinPath = GPIO_BASE_PATH + "gpio" + std::to_string(pin);
    }

    // 导出GPIO引脚（必须先导出才能操作）
    bool exportPin() {
        return writeFile(GPIO_BASE_PATH + "export", std::to_string(pin));
    }

    // 取消导出GPIO（释放资源）
    bool unexportPin() {
        return writeFile(GPIO_BASE_PATH + "unexport", std::to_string(pin));
    }

    // 设置GPIO方向（in/out）
    bool setDirection(const std::string& dir) {
        if (dir != "in" && dir != "out") {
            std::cerr << "错误：方向只能是 in 或 out" << std::endl;
            return false;
        }
        return writeFile(pinPath + "/direction", dir);
    }

    // 设置GPIO输出电平（0=低，1=高）
    bool setValue(int val) {
        if (val != 0 && val != 1) {
            std::cerr << "错误：电平只能是 0 或 1" << std::endl;
            return false;
        }
        return writeFile(pinPath + "/value", std::to_string(val));
    }

    // 析构函数：自动取消导出，防止资源残留
    ~GPIO() {
        unexportPin();
    }
};

// 主函数：控制GPIO18 高电平10秒 → 低电平
int main() {
    // 初始化GPIO18（BCM编号）
    GPIO gpio18(18);

    try {
        // 1. 导出引脚（必须步骤）
        if (!gpio18.exportPin()) {
            throw std::runtime_error("导出GPIO18失败");
        }
        // 短暂延时，确保系统完成引脚导出
        sleep(1);

        // 2. 设置引脚为输出模式
        if (!gpio18.setDirection("out")) {
            throw std::runtime_error("设置GPIO18为输出模式失败");
        }

        // 3. 设置高电平，并提示
        std::cout << "GPIO18 输出高电平，保持10秒..." << std::endl;
        if (!gpio18.setValue(1)) {
            throw std::runtime_error("设置GPIO18高电平失败");
        }

        // 4. 保持高电平10秒
        sleep(10);

        // 5. 设置低电平，并提示
        std::cout << "10秒已到，GPIO18 切换为低电平" << std::endl;
        if (!gpio18.setValue(0)) {
            throw std::runtime_error("设置GPIO18低电平失败");
        }

        // 6. 程序结束前短暂延时，确保低电平生效
        sleep(1);
    }
    catch (const std::exception& e) {
        // 异常处理：打印错误并清理引脚
        std::cerr << "程序异常：" << e.what() << std::endl;
        gpio18.unexportPin();
        return 1;
    }

    // 正常结束，析构函数会自动取消导出引脚
    std::cout << "程序执行完成" << std::endl;
    return 0;
}
