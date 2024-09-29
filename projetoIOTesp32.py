import dht
import machine
import time
import urequests
import network

# Inicializa o sensor DHT11 no pino 4
d = dht.DHT11(machine.Pin(4))

# Inicializa o relé no pino 2
relay = machine.Pin(2, machine.Pin.OUT)

# Chave API do ThingSpeak
THINGSPEAK_API_KEY = "sua chave API"
THINGSPEAK_URL = "sua url https......"

# Limites para ligar o relé
TEMP_THRESHOLD = 31  # Exemplo: Ligar o relé se a temperatura for maior que 31°C
HUM_THRESHOLD = 70   # Exemplo: Ligar o relé se a umidade for maior que 70%

# Função para conectar ao Wi-Fi
def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect("sua senha de wifi", "sua senha de wifi")

    while not station.isconnected():
        print("Conectando ao Wi-Fi...")
        time.sleep(1)

    print("Conectado ao Wi-Fi. IP:", station.ifconfig())

# Substitua "SEU_SSID" e "SUA_SENHA" pelas credenciais da sua rede
connect_wifi("FIBRA-D284", "0Z42006515")

# Função para enviar dados ao ThingSpeak
def send_to_thingspeak(temp, hum):
    try:
        # Cria a URL com os dados corretos
        url = "{}?api_key={}&field1={}&field2={}".format(THINGSPEAK_URL, THINGSPEAK_API_KEY, temp, hum)
        
        # Faz a requisição HTTP GET para ThingSpeak
        response = urequests.get(url)
        
        # Exibe a resposta no console
        print("Dados enviados para ThingSpeak: Temp={}C Umidade={}%. Resposta: {}".format(temp, hum, response.text))
        
        # Fecha a conexão
        response.close()
    except OSError as e:
        print("Erro ao enviar dados para ThingSpeak: ", e)

while True:
    # Mede temperatura e umidade
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    
    # Exibe as leituras
    print("Temp={}C Umid={}%" .format(temp, hum))
    
    # Envia dados para ThingSpeak
    send_to_thingspeak(temp, hum)
    
    # Lógica para ligar o relé se uma das condições for verdadeira
    if temp > TEMP_THRESHOLD or hum > HUM_THRESHOLD:
        relay.on()  # Liga o relé
        print("Relé ligado! Temperatura ou umidade acima do limite.")
    else:
        relay.off()  # Desliga o relé
        print("Relé desligado.")
    
    # Espera 20 segundos antes da próxima leitura
    time.sleep(20)

