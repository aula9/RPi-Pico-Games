from machine import Pin, PWM, ADC , SPI
import utime
import max7219
import math
# define LED matrix pins
spi = SPI(0,sck=Pin(6),mosi=Pin(7))
CS_PIN = machine.Pin(5, machine.Pin.OUT)
xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
button = Pin(22,Pin.IN, Pin.PULL_UP)
# initialize LED matrix
led_matrix = max7219.Matrix8x8(spi, CS_PIN, 1)
led_matrix.brightness(10)
player1_score = 0
player2_score = 0
ball_x = 3
ball_y = 3
ball_vx = 1
ball_vy = 1
paddle1_y = 2
paddle2_y = 2
def update_game():
    global ball_x, ball_y, ball_vx, ball_vy, player1_score, player2_score, paddle1_y, paddle2_y
    
    
    ball_x += ball_vx
    ball_y += ball_vy
    
    
    if ball_y == 0 or ball_y == 7:
        ball_vy = -ball_vy
        
    
    if ball_x == 0 and paddle1_y <= ball_y <= paddle1_y + 2:
        ball_vx = -ball_vx
        
     
    if ball_x == 7 and paddle2_y <= ball_y <= paddle2_y + 2:
        ball_vx = -ball_vx
        
    
    if ball_x == -1:
        player2_score += 1
        ball_x = 3
        ball_y = 3
        

    if ball_x == 8:
        player1_score += 1
        ball_x = 3
        ball_y = 3
        
    
    if button.value() == 0:
        led_matrix.pixel(ball_x, ball_y, 0)


def draw_game():
    global ball_x, ball_y, player1_score, player2_score, paddle1_y, paddle2_y
    
    
    led_matrix.fill(0)
    
    
    led_matrix.pixel(ball_x, ball_y, 1)
    
    
    for i in range(paddle1_y, paddle1_y + 3):
        led_matrix.pixel(0, i, 1)
        
    
    for i in range(paddle2_y, paddle2_y + 3):
        led_matrix.pixel(7, i, 1)
        
    led_matrix.show()

while True:
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    paddle1_y = xValue //255
    paddle2_y = yValue //255
    update_game()
    draw_game()

    buttonValue = button.value()
    xStatus = "middle"
    yStatus = "middle"
    buttonStatus = "not pressed"
    if xValue <= 900:
        xStatus = "left"
    elif xValue >= 60000:
        xStatus = "right"
    if yValue <= 600:
        yStatus = "up"
    elif yValue >= 60000:
        yStatus = "down"
    if buttonValue == 0:
        
        print(player1_score)
        print(player2_score)
        if(player1_score > player2_score):
            led_matrix.fill(0)
            led_matrix.text('A', 1, 0)
            led_matrix.show()
        elif(player1_score < player2_score):
            led_matrix.fill(0)
            led_matrix.text('B', 1, 0)
            led_matrix.show()
        elif(player1_score == player2_score):
            led_matrix.fill(0)
            led_matrix.text('=', 1, 0)
            led_matrix.show()
        utime.sleep(1)
        
    print("X: " + xStatus + ", Y: " + yStatus + " -- button " + buttonStatus)
    utime.sleep(0.1)
