import machine
import utime
import constants

class Buzzer():
    def __init__(self, pin):
        # Define the PWM output pin
        buzzer_pin = machine.Pin(pin)
        self.buzzer_pwm = machine.PWM(buzzer_pin)
        
    # Function to play a single beep
    def play_beep(self, alarm_frequency, beep_duration_ms):
        self.buzzer_pwm.freq(alarm_frequency)
        self.buzzer_pwm.duty_u16(65535)  # 100% duty cycle (volume)
        utime.sleep_ms(beep_duration_ms)
        self.buzzer_pwm.duty_u16(0)

    def alert(self, type):
        # Define the note frequency for the alarm beep (e.g., a high-pitched tone)
        alarm_frequency = 100
        # Define the duration for each beep in milliseconds
        beep_duration_ms = 200 
        # Define the duration of the pause between beeps in milliseconds
        pause_duration_ms = 100
        # define the number of beeps
        beep_count = 1
        if(type == constants.ALARM_SUCCESS):
            alarm_frequency = 100
            beep_duration_ms = 200 
            pause_duration_ms = 100
            beep_count = 3
        elif(type == constants.ALARM_ERROR):
            alarm_frequency = 100
            beep_duration_ms = 500 
            pause_duration_ms = 100
            beep_count = 1

        # Play the alarm sound with three beeps
        for _ in range(beep_count):
            self.play_beep(alarm_frequency, beep_duration_ms)
            utime.sleep_ms(pause_duration_ms)

        # Cleanup the PWM
        self.buzzer_pwm.deinit()
        
alarm = Buzzer(0)
alarm.alert(constants.ALARM_SUCCESS)