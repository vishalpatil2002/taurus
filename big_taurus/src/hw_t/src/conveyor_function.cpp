#include "conveyor_control.h"
#include <iostream>
#include <unistd.h>
#include <errno.h>

// ---------------- Helpers ----------------
int32_t ConveyorControl::two_cmp(uint32_t val, int bits)
{
    if (val >= (1u << (bits - 1)))
        return (int32_t)(val - (1u << bits));
    return (int32_t)val;
}

// ---------------- Constructor ----------------
ConveyorControl::ConveyorControl()
{
    connected_ = false;
    conveyor_status_ = 0;

    mod_ = modbus_new_rtu("/dev/CONVEYOR", 115200, 'N', 8, 1);
    if (!mod_ || modbus_connect(mod_) == -1)
    {
        std::cerr << "Failed Modbus RTU connection for conveyor\n";
        mod_ = nullptr;
        return;
    }

    connected_ = true;
    std::cout << "Conveyor connected\n";
}

// ---------------- Destructor ----------------
ConveyorControl::~ConveyorControl()
{
    end();
}

bool ConveyorControl::isConnected() const
{
    return connected_;
}

// ---------------- Low-level Modbus ----------------
void ConveyorControl::writeRegister(int address, int value, int slave)
{
    modbus_set_slave(mod_, slave);
    if (modbus_write_register(mod_, address, value) == -1)
        conveyor_status_ = 0;
    else
        conveyor_status_ = 1;
}

int32_t ConveyorControl::readRegister(int address, int slave, bool signed_mode)
{
    modbus_set_slave(mod_, slave);
    uint16_t reg[1];

    if (modbus_read_registers(mod_, address, 1, reg) == -1)
    {
        conveyor_status_ = 0;
        return 0;
    }

    conveyor_status_ = 1;
    return signed_mode ? two_cmp(reg[0], 16) : reg[0];
}

std::vector<int> ConveyorControl::getBits(uint32_t val, int bits)
{
    std::vector<int> bits_set;
    for (int i = 0; i < bits; i++)
        if (val & (1u << i)) bits_set.push_back(i);
    return bits_set;
}

std::vector<int> ConveyorControl::readAlarm(int slave)
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


int32_t ConveyorControl::longRead(int address, int slave, bool unsigned_mode, int32_t prev)
{
    modbus_set_slave(mod_, slave);
    uint16_t regs[2];

    if (modbus_read_registers(mod_, address, 2, regs) == -1)
    {
        conveyor_status_ = 0;
        return prev;
    }

    conveyor_status_ = 1;
    uint32_t val = ((uint32_t)regs[0] << 16) | regs[1];
    return unsigned_mode ? (int32_t)val : two_cmp(val, 32);
}

// ---------------- Conveyor Functions -----------------

// Set conveyor speed
void ConveyorControl::setConveyorSpeed(int slave)
{
    writeRegister(48, FIXED_SPEED, slave);   // speed register
    std::cout << "Conveyor speed set to " << FIXED_SPEED << std::endl;
}

// Conveyor FORWARD
void ConveyorControl::conveyorForward(int slave)
{
    writeRegister(48, FIXED_SPEED, slave);
    writeRegister(124, 159, slave); // jog prep
    writeRegister(124, 150, slave); // forward direction
    std::cout << "Conveyor FORWARD with speed " << FIXED_SPEED << "\n";
}

// Conveyor BACKWARD
void ConveyorControl::conveyorBackward(int slave)
{
    writeRegister(48, -FIXED_SPEED, slave);
    writeRegister(124, 159, slave); // jog prep
    writeRegister(124, 150, slave); // reverse direction
    std::cout << "Conveyor BACKWARD with speed " << FIXED_SPEED << "\n";
}

// STOP (critical)
void ConveyorControl::conveyorStop(int slave)
{
    writeRegister(124, 226, slave); // stop
    writeRegister(124, 158, slave); // disable
    std::cout << "Conveyor STOPPED\n";
}

// Encoder position
int32_t ConveyorControl::getConveyorPosition(int slave, int32_t prev)
{
    return longRead(10, slave, false, prev);
}

void ConveyorControl::resetAlarm(int slave)
{
    writeRegister(124, 186, slave);
    std::cout << "Conveyor alarms reset" << std::endl;
}

// ---------------- Cleanup ----------------
void ConveyorControl::end()
{
    if (!mod_) return;

    modbus_close(mod_);
    modbus_free(mod_);
    mod_ = nullptr;
    connected_ = false;

    std::cout << "Conveyor connection closed\n";
}