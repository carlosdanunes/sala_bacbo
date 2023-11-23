# Configurações iniciais
token = '6963692330:AAE605_UX1fLt18Qa8NMC_l69f09IGLbTMg' # Insira o Token do seu Bot
chat_id = -1002077929192 # Insira o CHAT ID do grupo

# Importações
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
from time import sleep

# Funções
def verifica_inatividade():
    # Verifica se está inativo
    if len(driver.find_elements(By.CSS_SELECTOR, 'div[data-role="inactivity-message-clickable"]')) > 0:
        driver.find_element(By.CSS_SELECTOR, 'div[data-role="inactivity-message-clickable"]').click()

def verifica_sessao():
    # Verifica se a sessão expirou 
    if len(driver.find_elements(By.CSS_SELECTOR, 'button[data-role="button-ok"]')) > 0:
        driver.get(url)
        iframe = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'iframe')))
        driver.switch_to.frame(iframe)
        sleep(1)
        iframe = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'iframe')))
        driver.switch_to.frame(iframe)
        sleep(2)

def enviar_mensagem(mensagem):
    try:
        data = {"chat_id": chat_id, "text": mensagem}
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data)
    except Exception as e:
        print("Erro ao enviar mensagem para o Telegram: ", e)

url = "https://launchdigi.net/GamesLaunch/Launch?deviceType=1&gameId=14529&lang=pt&mainDomain=strike777.bet&operatorId=88AAAC1D&playMode=real&token=strike777_CvWF0YRBpQIIatLP"
path_cache = os.getcwd() + "\cache"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-notifications')
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-popup-block')
chrome_options.add_argument("no-default-browser-check")
if os.path.exists(path_cache) == False:
    os.makedirs(path_cache)
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--user-data-dir=" + path_cache)

# Abre uma nova instância do navegador
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(chrome_options, servico)
action = ActionChains(driver)
driver.get(url)

# Move para os IFRAMES
iframe = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'iframe')))
driver.switch_to.frame(iframe)
sleep(1)
iframe = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'iframe')))
driver.switch_to.frame(iframe)
sleep(5)

#---------------------------------------------------------------------------------
ultimos_3 = []
verficar = ""
regra = False
dobrou = False
loss = False
loss_index = 4

while True:
    verifica_inatividade()
    verifica_sessao()
    todos_resultados = driver.find_element(By.CSS_SELECTOR, 'svg[data-role="Bead-road"]').find_element(By.CSS_SELECTOR, 'svg').find_elements(By.CSS_SELECTOR, 'svg[data-type="roadItem"]')
    qtde_total = len(todos_resultados)

    # Espera próxima rodada
    while qtde_total == len(driver.find_element(By.CSS_SELECTOR, 'svg[data-role="Bead-road"]').find_element(By.CSS_SELECTOR, 'svg').find_elements(By.CSS_SELECTOR, 'svg[data-type="roadItem"]')):
        verifica_inatividade()
        verifica_sessao()
        pass

    # Coleta o último resultado
    todos_resultados = driver.find_element(By.CSS_SELECTOR, 'svg[data-role="Bead-road"]').find_element(By.CSS_SELECTOR, 'svg').find_elements(By.CSS_SELECTOR, 'svg[data-type="roadItem"]')
    ultimo_resultado = todos_resultados[-1]
    qtde_total = len(todos_resultados)

    # Define o resultado
    if ultimo_resultado.text == 'P':
        resultado = 'Azul'
    elif ultimo_resultado.text == 'B':
        resultado = 'Vermelho'
    elif ultimo_resultado.text == 'T':
        resultado = 'Tie'
    print("Resultado: ", resultado)

    if loss:
        # Se for LOSS, fica 3 rodadas sem mandar sinal
        loss_index -= 1
        if not loss_index == 0:
            continue
        else: 
            ultimos_3 = []
            verficar = ""
            regra = False
            dobrou = False
            loss = False
            loss_index = 3

    if regra:
        if resultado == verficar:
            enviar_mensagem("""
✅✅✅ GREEN ✅✅✅
""")
            dobrou = False
            verficar = ""
        else:
            if dobrou:
                # Após 2 gales e não der, é loss
                enviar_mensagem("""
❌ LOSS ❌
3 rodadas sem operar..
""")
                verficar = ""
                dobrou = False
                loss = True
                continue
            else:
                if verficar == "Vermelho":
                    emoji = "🔴"
                elif verficar == "Azul":
                    emoji = "🔵"
                enviar_mensagem(f"""
🔄️ Fazer 2 GALES, Dobrar no {emoji}
""")
                dobrou = True
                continue

    # Pega últimos 3 resutados
    ultimos_3.insert(0, resultado)
    ultimos_3 = ultimos_3[:3]
    print(ultimos_3)

    # RULES
    # Após 3 vermelhos o sinal manda entrar no azul
    if ultimos_3 == ['Vermelho', 'Vermelho', 'Vermelho']:
        verficar = "Azul"
        regra = True

    # Após 3 azuis o sinal manda entrar no vermelho
    elif ultimos_3 == ['Azul', 'Azul', 'Azul']:
        verficar = "Vermelho"
        regra = True

    # Tie, vermelho, tie, entra no azul
    elif ultimos_3 == ['Tie', 'Vermelho', 'Tie']:
        verficar = "Azul"
        regra = True
    
    # Tie, azul, tie, entra no vermelho
    elif  ultimos_3 == ['Tie', 'Azul', 'Tie']:
        verficar = "Vermelho"
        regra = True

    # Vermelho e 2 ties entra no azul
    elif  ultimos_3 == ['Vermelho', 'Tie', 'Tie']:
        verficar = "Azul"
        regra = True

    # Azul e 2 ties with entra no vermelho
    elif ultimos_3 == ['Azul', 'Tie', 'Tie']:
        verficar = "Vermelho"
        regra = True

    # Vermelho, tie e vermelho entra no azul
    elif ultimos_3 == ['Vermelho', 'Tie', 'Vermelho']:
        verficar = "Azul"
        regra = True

    # Azul, tie e azul entra no vermelho
    elif ultimos_3 == ['Azul', 'Tie', 'Azul']:
        verficar = "Vermelho"
        regra = True
    else:
        regra = False

    if verficar == 'Azul':
        mensagem = """
🚀 ENTRADA CONFIRMADA 🚀

Apostar no 🔵
""" 
    elif verficar == 'Vermelho':
        mensagem = """
🚀 ENTRADA CONFIRMADA 🚀

Apostar no 🔴
"""
    if verficar:
        print(mensagem)
        enviar_mensagem(mensagem)