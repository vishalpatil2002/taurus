#pragma once
#include <modbus/modbus.h>
#include <vector>
#include <utility>
#include <cstdint>
#include <iostream>

class Moons {
public:
    Moons();
    ~Moons();
    bool isConnected() const;

    // ==== Core interface ====
    void resetAlarm();
    void startJog();
    void stopJog();
    void disableMotor();  // (optional, can be empty if unused)
    void setSpeed(int motor_add, int speed1, int speed2);
    std::pair<int,int> getSpeed();
    std::pair<int,int> getEncoder(int prev1, int prev2);
    void setEncoder(std::pair<int,int> enc);
    std::vector<int> readAlarm(int slave);
    std::pair<int,int> getCurrent();

    // ==== Low-level Modbus ====
    int32_t readRegister(int address, int slave, bool signed_mode = false);
    int32_t longRead(int address, int slave, bool unsigned_mode = true, int32_t prev = 0);
    void longWrite(int address, int32_t value, int slave);
    void end();  // cleanup
    bool brakeStatus(int slave);
    
    void setM0Alive();
    int getPLCBit(int bit);

private:
    modbus_t* mod_;
    modbus_t* tcp_mod_ = nullptr;

    int motor_status_;
    bool connected_;

    // Helper functions
    int32_t two_cmp(uint32_t val, int bits);
    std::vector<int> getBits(uint32_t val, int bits);
    void writeRegister(int address, int value, int slave);
};
