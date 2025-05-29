# 🤖 Robô Controlado via Node-RED com Interface Pygame

Este projeto simula um **robô virtual** que se movimenta dentro de um labirinto utilizando **Python** e **Pygame**, controlado por comandos recebidos de um servidor **Node-RED**.

---

## 🛠 Tecnologias Utilizadas

- **Python 3**
- **Pygame**
- **Threading**
- **Requests**
- **Node-RED**

---

## 🎮 Funcionalidades

- Interface gráfica com labirinto 2D.
- Robô controlado remotamente com comandos:
  - `cima`, `baixo`, `esquerda`, `direita`
- Comunicação com servidor Node-RED via HTTP (GET e POST).
- Retorno automático da posição atual e status do movimento.

---

## 📁 Estrutura do Projeto

📦 robo-node-red
┣ 📄 robo_node_red.py
┣ 📄 README.md
┗ 📄 .gitignore


---

## ▶️ Como Executar

### 1. Instale as dependências

```bash
pip install pygame requests

python robo_node_red.py
````

3. Configure seu servidor Node-RED com os endpoints:
GET /controle_robo: envia comandos (cima, baixo, etc.)

POST /retorno_robo: recebe a posição e status da movimentação

🧠 Lógica do Código
✅ Movimento

```bash
def mover_para(x, y):
    global pos_x, pos_y
    if 0 <= x < COLUNAS and 0 <= y < LINHAS:
        if labirinto[y][x] == 0:
            pos_x, pos_y = x, y
            return "aceito"
    return "rejeitado"
```
🌐 Comunicação com Node-RED

```bash
r = requests.get("http://localhost:1880/controle_robo")
requests.post("http://localhost:1880/retorno_robo", json={"x": pos_x, "y": pos_y, "status": status})
```
🎨 Renderização com Pygame

```bash
pygame.draw.rect(tela, cor, (x * LARGURA_CELULA, y * ALTURA_CELULA, LARGURA_CELULA, ALTURA_CELULA))
pygame.draw.circle(tela, VERDE, (centro_x, centro_y), 15)
```

💡 Possíveis Melhorias Futuras
Histórico do caminho percorrido.

Modo automático (IA simples).

Interface com botões no Node-RED.

Sons ou efeitos visuais.



