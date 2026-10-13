// Auto-generated. Do not edit!

// (in-package hw_t.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class bms {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.cumulative_voltage = null;
      this.soc = null;
      this.health = null;
    }
    else {
      if (initObj.hasOwnProperty('cumulative_voltage')) {
        this.cumulative_voltage = initObj.cumulative_voltage
      }
      else {
        this.cumulative_voltage = 0;
      }
      if (initObj.hasOwnProperty('soc')) {
        this.soc = initObj.soc
      }
      else {
        this.soc = 0;
      }
      if (initObj.hasOwnProperty('health')) {
        this.health = initObj.health
      }
      else {
        this.health = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type bms
    // Serialize message field [cumulative_voltage]
    bufferOffset = _serializer.int32(obj.cumulative_voltage, buffer, bufferOffset);
    // Serialize message field [soc]
    bufferOffset = _serializer.int32(obj.soc, buffer, bufferOffset);
    // Serialize message field [health]
    bufferOffset = _serializer.string(obj.health, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type bms
    let len;
    let data = new bms(null);
    // Deserialize message field [cumulative_voltage]
    data.cumulative_voltage = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [soc]
    data.soc = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [health]
    data.health = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.health);
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'hw_t/bms';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0c354b6465cf619113f97c8e49600de9';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 cumulative_voltage
    int32 soc
    string health
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new bms(null);
    if (msg.cumulative_voltage !== undefined) {
      resolved.cumulative_voltage = msg.cumulative_voltage;
    }
    else {
      resolved.cumulative_voltage = 0
    }

    if (msg.soc !== undefined) {
      resolved.soc = msg.soc;
    }
    else {
      resolved.soc = 0
    }

    if (msg.health !== undefined) {
      resolved.health = msg.health;
    }
    else {
      resolved.health = ''
    }

    return resolved;
    }
};

module.exports = bms;
