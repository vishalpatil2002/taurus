; Auto-generated. Do not edit!


(cl:in-package hw_t-msg)


;//! \htmlinclude machineControlResult.msg.html

(cl:defclass <machineControlResult> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (distance_reached
    :reader distance_reached
    :initarg :distance_reached
    :type cl:string
    :initform "")
   (dock_done
    :reader dock_done
    :initarg :dock_done
    :type cl:boolean
    :initform cl:nil)
   (rotate_done
    :reader rotate_done
    :initarg :rotate_done
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass machineControlResult (<machineControlResult>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <machineControlResult>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'machineControlResult)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hw_t-msg:<machineControlResult> is deprecated: use hw_t-msg:machineControlResult instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <machineControlResult>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:success-val is deprecated.  Use hw_t-msg:success instead.")
  (success m))

(cl:ensure-generic-function 'distance_reached-val :lambda-list '(m))
(cl:defmethod distance_reached-val ((m <machineControlResult>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:distance_reached-val is deprecated.  Use hw_t-msg:distance_reached instead.")
  (distance_reached m))

(cl:ensure-generic-function 'dock_done-val :lambda-list '(m))
(cl:defmethod dock_done-val ((m <machineControlResult>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:dock_done-val is deprecated.  Use hw_t-msg:dock_done instead.")
  (dock_done m))

(cl:ensure-generic-function 'rotate_done-val :lambda-list '(m))
(cl:defmethod rotate_done-val ((m <machineControlResult>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hw_t-msg:rotate_done-val is deprecated.  Use hw_t-msg:rotate_done instead.")
  (rotate_done m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <machineControlResult>) ostream)
  "Serializes a message object of type '<machineControlResult>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'distance_reached))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'distance_reached))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'dock_done) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'rotate_done) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <machineControlResult>) istream)
  "Deserializes a message object of type '<machineControlResult>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'distance_reached) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'distance_reached) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:slot-value msg 'dock_done) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'rotate_done) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<machineControlResult>)))
  "Returns string type for a message object of type '<machineControlResult>"
  "hw_t/machineControlResult")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'machineControlResult)))
  "Returns string type for a message object of type 'machineControlResult"
  "hw_t/machineControlResult")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<machineControlResult>)))
  "Returns md5sum for a message object of type '<machineControlResult>"
  "482d35fe79b44b8f02c11d9391c4600a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'machineControlResult)))
  "Returns md5sum for a message object of type 'machineControlResult"
  "482d35fe79b44b8f02c11d9391c4600a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<machineControlResult>)))
  "Returns full string definition for message of type '<machineControlResult>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Result~%bool success~%string distance_reached~%bool dock_done~%bool rotate_done~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'machineControlResult)))
  "Returns full string definition for message of type 'machineControlResult"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Result~%bool success~%string distance_reached~%bool dock_done~%bool rotate_done~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <machineControlResult>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'distance_reached))
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <machineControlResult>))
  "Converts a ROS message object to a list"
  (cl:list 'machineControlResult
    (cl:cons ':success (success msg))
    (cl:cons ':distance_reached (distance_reached msg))
    (cl:cons ':dock_done (dock_done msg))
    (cl:cons ':rotate_done (rotate_done msg))
))
