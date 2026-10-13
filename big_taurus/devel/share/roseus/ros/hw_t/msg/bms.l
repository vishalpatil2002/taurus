;; Auto-generated. Do not edit!


(when (boundp 'hw_t::bms)
  (if (not (find-package "HW_T"))
    (make-package "HW_T"))
  (shadow 'bms (find-package "HW_T")))
(unless (find-package "HW_T::BMS")
  (make-package "HW_T::BMS"))

(in-package "ROS")
;;//! \htmlinclude bms.msg.html


(defclass hw_t::bms
  :super ros::object
  :slots (_cumulative_voltage _soc _health ))

(defmethod hw_t::bms
  (:init
   (&key
    ((:cumulative_voltage __cumulative_voltage) 0)
    ((:soc __soc) 0)
    ((:health __health) "")
    )
   (send-super :init)
   (setq _cumulative_voltage (round __cumulative_voltage))
   (setq _soc (round __soc))
   (setq _health (string __health))
   self)
  (:cumulative_voltage
   (&optional __cumulative_voltage)
   (if __cumulative_voltage (setq _cumulative_voltage __cumulative_voltage)) _cumulative_voltage)
  (:soc
   (&optional __soc)
   (if __soc (setq _soc __soc)) _soc)
  (:health
   (&optional __health)
   (if __health (setq _health __health)) _health)
  (:serialization-length
   ()
   (+
    ;; int32 _cumulative_voltage
    4
    ;; int32 _soc
    4
    ;; string _health
    4 (length _health)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _cumulative_voltage
       (write-long _cumulative_voltage s)
     ;; int32 _soc
       (write-long _soc s)
     ;; string _health
       (write-long (length _health) s) (princ _health s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _cumulative_voltage
     (setq _cumulative_voltage (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _soc
     (setq _soc (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _health
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _health (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get hw_t::bms :md5sum-) "0c354b6465cf619113f97c8e49600de9")
(setf (get hw_t::bms :datatype-) "hw_t/bms")
(setf (get hw_t::bms :definition-)
      "int32 cumulative_voltage
int32 soc
string health

")



(provide :hw_t/bms "0c354b6465cf619113f97c8e49600de9")


