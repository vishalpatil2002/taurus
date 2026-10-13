; Auto-generated. Do not edit!


(cl:in-package hw_t-msg)


;//! \htmlinclude bms.msg.html

(cl:defclass <bms> (roslisp-msg-protocol:ros-message)
  ((cumulative_voltage
    :reader cumulative_voltage
    :initarg :cumulative_voltage
    :type cl:integer
    :initform 0)
   (soc
    :reader soc
    :initarg :soc
    :type cl:integer
    :initform 0)
   (health
    :reader health
    :initarg :health
    :type cl:string
    :initform ""))
)

(cl:defclass bms (<bms>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <bms>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'bms)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hw_t-msg:<bms> is deprecated: use hw_t-msg:bms instead.")))

(cl:ensure-generic-function 'cumulative_voltage-val :lambda-list '(m))
(cl:defmethod cumulative_voltage-val ((m <bms>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:cumulative_voltage-val is deprecated.  Use hw_t-msg:cumulative_voltage instead.")
  (cumulative_voltage m))

(cl:ensure-generic-function 'soc-val :lambda-list '(m))
(cl:defmethod soc-val ((m <bms>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:soc-val is deprecated.  Use hw_t-msg:soc instead.")
  (soc m))

(cl:ensure-generic-function 'health-val :lambda-list '(m))
(cl:defmethod health-val ((m <bms>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:health-val is deprecated.  Use hw_t-msg:health instead.")
  (health m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <bms>) ostream)
  "Serializes a message object of type '<bms>"
  (cl:let* ((signed (cl:slot-value msg 'cumulative_voltage)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'soc)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'health))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'health))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <bms>) istream)
  "Deserializes a message object of type '<bms>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'cumulative_voltage) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'soc) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'health) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'health) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<bms>)))
  "Returns string type for a message object of type '<bms>"
  "hw_t/bms")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'bms)))
  "Returns string type for a message object of type 'bms"
  "hw_t/bms")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<bms>)))
  "Returns md5sum for a message object of type '<bms>"
  "0c354b6465cf619113f97c8e49600de9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'bms)))
  "Returns md5sum for a message object of type 'bms"
  "0c354b6465cf619113f97c8e49600de9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<bms>)))
  "Returns full string definition for message of type '<bms>"
  (cl:format cl:nil "int32 cumulative_voltage~%int32 soc~%string health~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'bms)))
  "Returns full string definition for message of type 'bms"
  (cl:format cl:nil "int32 cumulative_voltage~%int32 soc~%string health~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <bms>))
  (cl:+ 0
     4
     4
     4 (cl:length (cl:slot-value msg 'health))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <bms>))
  "Converts a ROS message object to a list"
  (cl:list 'bms
    (cl:cons ':cumulative_voltage (cumulative_voltage msg))
    (cl:cons ':soc (soc msg))
    (cl:cons ':health (health msg))
))
