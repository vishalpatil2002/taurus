; Auto-generated. Do not edit!


(cl:in-package hw_t-msg)


;//! \htmlinclude machineControlFeedback.msg.html

(cl:defclass <machineControlFeedback> (roslisp-msg-protocol:ros-message)
  ((move_base_state
    :reader move_base_state
    :initarg :move_base_state
    :type cl:string
    :initform "")
   (control_status
    :reader control_status
    :initarg :control_status
    :type cl:string
    :initform "")
   (reached
    :reader reached
    :initarg :reached
    :type cl:string
    :initform ""))
)

(cl:defclass machineControlFeedback (<machineControlFeedback>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <machineControlFeedback>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'machineControlFeedback)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hw_t-msg:<machineControlFeedback> is deprecated: use hw_t-msg:machineControlFeedback instead.")))

(cl:ensure-generic-function 'move_base_state-val :lambda-list '(m))
(cl:defmethod move_base_state-val ((m <machineControlFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:move_base_state-val is deprecated.  Use hw_t-msg:move_base_state instead.")
  (move_base_state m))

(cl:ensure-generic-function 'control_status-val :lambda-list '(m))
(cl:defmethod control_status-val ((m <machineControlFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:control_status-val is deprecated.  Use hw_t-msg:control_status instead.")
  (control_status m))

(cl:ensure-generic-function 'reached-val :lambda-list '(m))
(cl:defmethod reached-val ((m <machineControlFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:reached-val is deprecated.  Use hw_t-msg:reached instead.")
  (reached m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <machineControlFeedback>) ostream)
  "Serializes a message object of type '<machineControlFeedback>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'move_base_state))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'move_base_state))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'control_status))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'control_status))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'reached))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'reached))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <machineControlFeedback>) istream)
  "Deserializes a message object of type '<machineControlFeedback>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'move_base_state) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'move_base_state) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'control_status) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'control_status) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'reached) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'reached) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<machineControlFeedback>)))
  "Returns string type for a message object of type '<machineControlFeedback>"
  "hw_t/machineControlFeedback")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'machineControlFeedback)))
  "Returns string type for a message object of type 'machineControlFeedback"
  "hw_t/machineControlFeedback")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<machineControlFeedback>)))
  "Returns md5sum for a message object of type '<machineControlFeedback>"
  "64bf29fd6eb02a8fcdd0397bea2b1cef")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'machineControlFeedback)))
  "Returns md5sum for a message object of type 'machineControlFeedback"
  "64bf29fd6eb02a8fcdd0397bea2b1cef")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<machineControlFeedback>)))
  "Returns full string definition for message of type '<machineControlFeedback>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Feedback~%string move_base_state~%string control_status~%string reached~%~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'machineControlFeedback)))
  "Returns full string definition for message of type 'machineControlFeedback"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Feedback~%string move_base_state~%string control_status~%string reached~%~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <machineControlFeedback>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'move_base_state))
     4 (cl:length (cl:slot-value msg 'control_status))
     4 (cl:length (cl:slot-value msg 'reached))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <machineControlFeedback>))
  "Converts a ROS message object to a list"
  (cl:list 'machineControlFeedback
    (cl:cons ':move_base_state (move_base_state msg))
    (cl:cons ':control_status (control_status msg))
    (cl:cons ':reached (reached msg))
))
