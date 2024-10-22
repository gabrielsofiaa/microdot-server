# Aplicacion del servidor
from boot import do_connect
from microdot import Microdot, send_file
from machine import Pin
import neopixel

# Definir pines para los LEDs individuales
led_pin_rojo = Pin(32, Pin.OUT, value=0)
led_pin_verde = Pin(33, Pin.OUT, value=0)
led_pin_azul = Pin(25, Pin.OUT, value=0)

# Definir el pin para los LEDs RGB (NeoPixel) y asignar los colores iniciales
led_rgb_strip = neopixel.NeoPixel(Pin(27), 4)
for i in range(4):
    led_rgb_strip[i] = (0, 0, 0)

led_rgb_strip.write()

# Conexión Wi-Fi
do_connect()
app = Microdot()

# Ruta principal que sirve el archivo HTML
@app.route('/')
async def index(request):
    return send_file('index.html')

# Ruta para servir archivos estáticos (como CSS, JS, etc.)
@app.route('/<dir>/<file>')
async def static(request, dir, file):
    return send_file("/{}/{}".format(dir, file))

# Ruta para alternar el estado de los LEDs individuales
@app.route('/led/toggle/<led>')
async def led_toggle(request, led):
    global led_pin_rojo, led_pin_verde, led_pin_azul
    
    if led == 'LED1':
        led_pin_rojo.value(not led_pin_rojo.value())
    elif led == 'LED2':
        led_pin_verde.value(not led_pin_verde.value())
    elif led == 'LED3':
        led_pin_azul.value(not led_pin_azul.value())
        
    return {"status": "OK"}

# Ruta para cambiar el valor del componente rojo del LED RGB
@app.route('/rgbled/change/red/<int:red_value>')
async def rgb_led_red(request, red_value):
    global led_rgb_strip
    green_value = led_rgb_strip[0][1]
    blue_value = led_rgb_strip[0][2]
    
    for pixel in range(4):
        led_rgb_strip[pixel] = (red_value, green_value, blue_value)
        
    led_rgb_strip.write()

# Ruta para cambiar el valor del componente azul del LED RGB
@app.route('/rgbled/change/blue/<int:blue_value>')
async def rgb_led_blue(request, blue_value):
    global led_rgb_strip
    
    red_value = led_rgb_strip[0][0]
    green_value = led_rgb_strip[0][1]
    
    for pixel in range(4):
        led_rgb_strip[pixel] = (red_value, green_value, blue_value)
        
    led_rgb_strip.write()

# Ruta para cambiar el valor del componente verde del LED RGB
@app.route('/rgbled/change/green/<int:green_value>')
async def rgb_led_green(request, green_value):
    global led_rgb_strip
    
    red_value = led_rgb_strip[0][0]
    blue_value = led_rgb_strip[0][2]
    
    for pixel in range(4):
        led_rgb_strip[pixel] = (red_value, green_value, blue_value)
        
    led_rgb_strip.write()

# Iniciar la aplicación web en el puerto 80
app.run(port=80)