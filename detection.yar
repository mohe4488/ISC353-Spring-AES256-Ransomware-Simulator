import "math"

rule Detect_Ransomware_Behavior {
    meta:
        description = "High entropy detection"
    
    condition:
      
        filesize > 100 and math.entropy(0, filesize) >= 5.0
}
