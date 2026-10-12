#include "lift_control.h"
#include <iostream>
#include<unistd.h>
#include <errno.h>

// ---------------- Helpers ----------------
int32_t Moons::two_cmp(uint32_t val, int bits)
{
    if (val >= (1u << (bits - 1)))
        return (int32_t)(val - (1u << bits));
    return (int32_t)val;
}

// ---------------- Constructor ----------------
Moons::Moons()
{
    connected_ = false;
    motor_status_ = 0;

    mod_ = modbus_new_rtu("/dev/LIFT", 115200, 'N', 8, 1);
    if (!mod_ || modbus_connect(mod_) == -1)
    {
        std::cerr << "Failed Modbus RTU connection\n";
        mod_ = nullptr;
        return;
    }

    connected_ = true;
    std::cout << "Moons lift connected\n";
}

// ---------------- Destructor ----------------
Moons::~Moons()
{
    end();
}

bool Moons::isConnected() const
{
    return connected_;
}

// ---------------- Low-level Modbus ----------------
void Moons::writeRegister(int address, int value, int slave)
{
    modbus_set_slave(mod_, slave);
    if (modbus_write_register(mod_, address, value) == -1)
        motor_status_ = 0;
    else
        motor_status_ = 1;
}

int32_t Moons::readRegister(int address, int slave, bool signed_mode)
{
    modbus_set_slave(mod_, slave);
    uint16_t reg[1];

    if (modbus_read_registers(mod_, address, 1, reg) == -1)
    {
        motor_status_ = 0;
        return 0;
    }

    motor_status_ = 1;
    return signed_mode ? two_cmp(reg[0], 16) : reg[0];
}

std::vector<int> Moons::getBits(uint32_t val, int bits)
{
    std::vector<int> bits_set;
    for (int i = 0; i < bits; i++)
        if (val & (1u << i)) bits_set.push_back(i);
    return bits_set;
}

std::vector<int> Moons::readAlarm(int slave)
{
    int32_t val = longRead(0, slave, false, 0);
    std::vector<int> alarms = getBits(val, 32);

    std::vector<std::string> alarm_messages = {
        "position error overrun", "reverse prohibition limit", "positive prohibition limit",
        "over temperature", "internal error", "supply voltage out of range", "reserved",
        "drive overcurrent", "reserved", "motor encoder not connected", "communication exception",
        "reserved", "vent failure", "motor overload protection", "reserved", "unusual start alarm",
        "input phase loss", "STO", "reserved", "motor speed exceeds limit", "drive undervoltage",
        "emergency stop", "second encoder not connected", "full closed loop deviation overrun",
        "absolute encoder battery undervoltage", "accurate position lost", "absolute position overflow",
        "communication interrupt", "absolute encoder multi-turn error", "abnormal motor action protection",
        "EtherCAT communication error", "Back to origin parameter configuration error"
    };

    for (int i : alarms)
    {
        if (i < (int)alarm_messages.size())
            std::cout << "Alarm (slave " << slave << "): "
                      << alarm_messages[i] << std::endl;
    }

    return alarms;
}

void Moons::longWrite(int address, int32_t value, int slave)
{
    modbus_set_slave(mod_, slave);
    uint16_t regs[2] =
    {
        (uint16_t)(value >> 16),
        (uint16_t)(value & 0xFFFF)
    };

    if (modbus_write_registers(mod_, address, 2, regs) == -1)
        motor_status_ = 0;
    else
        motor_status_ = 1;
}

int32_t Moons::longRead(int address, int slave, bool unsigned_mode, int32_t prev)
{
    modbus_set_slave(mod_, slave);
    uint16_t regs[2];

    if (modbus_read_registers(mod_, address, 2, regs) == -1)
    {
        motor_status_ = 0;
        return prev;
    }

    motor_status_ = 1;
    uint32_t val = ((uint32_t)regs[0] << 16) | regs[1];
    return unsigned_mode ? (int32_t)val : two_cmp(val, 32);
}
double Moons::getencoder(int slave){
      std::cout << "encoder " << slave << "): "
                      << longRead(4,slave,0,0) << std::endl;
      return 200000;
      
}

// ---------------- Lift Functions -----------------2147483642

// ONLY slow speed for lift
void Moons::setLiftSpeed(int slave, int32_t speed)
{
    longWrite(342, speed, slave);   // speed register
    std::cout << "Lift speed set to " << speed << std::endl;
}

// Lift UP (slow)
void Moons::liftUp(int slave)
{
    longWrite(342, 15000, slave);
    writeRegister(124, 159, slave); // jog prep
    writeRegister(124, 150, slave); // forward
    std::cout << "Lift UP\n";
}

// Lift DOWN (slow)
void Moons::liftDown(int slave)
{
    longWrite(342, -15000, slave);
    writeRegister(124, 159, slave); // jog prep
    writeRegister(124, 150, slave); // reverse
    std::cout << "Lift DOWN\n";
}

// STOP (critical)
void Moons::stopLift(int slave)
{
    writeRegister(124, 226, slave); // stop
    writeRegister(124, 158, slave); // disable
    std::cout << "Lift STOPPED\n";
}

// Encoder position
int32_t Moons::getLiftPosition(int slave, int32_t prev)
{
    return longRead(10, slave, false, prev);
}

void Moons::zeroEncoder(int slave, int32_t value)
{
    if (!connected_ || !mod_) return;

    longWrite(125, value, slave);

    longRead(125, slave, false, value);

    writeRegister(124, 0x98, slave);

    std::cout << "Encoder zero set (slave " << slave << ")\n";
}

void Moons::setPosition(int slave, int32_t position, int32_t speed)
{
    if (!connected_ || !mod_) return;

    longWrite(30, position, slave);//position
    longWrite(342, speed, slave);// speed
    // writeRegister(29, speed, slave);
    writeRegister(124, 0x67, slave);

    writeRegister(124, 159, slave); // jog prep
    writeRegister(124, 150, slave);

    std::cout << "Move command sent | Pos: "
              << position << " Speed: " << speed
              << " Slave: " << slave << std::endl;
}

void Moons::resetAlarm(int slave)
{
    writeRegister(124, 186, slave);
    std::cout << "Alarms reset" << std::endl;
}

// ---------------- Cleanup ----------------
void Moons::end()
{
    if (!mod_) return;

    modbus_close(mod_);
    modbus_free(mod_);
    mod_ = nullptr;
    connected_ = false;

    std::cout << "Moons lift connection closed\n";
}
