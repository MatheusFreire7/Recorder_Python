# Gravador de Tela e Áudio  🌟

Este é um projeto Python que permite gravar a tela e o áudio do seu computador. Ele fornece uma interface gráfica simples para iniciar e interromper a gravação, e combina o vídeo e o áudio gravados em um único arquivo de vídeo.

## Pré-requisitos 🛠️

Antes de usar este aplicativo, você deve ter instalado as seguintes dependências:

- Python 3.x
- tkinter
- Pillow (PIL)
- OpenCV (cv2)
- PyAudio
- moviepy
- keyboard
- pyautogui

Você pode instalar essas dependências usando o gerenciador de pacotes Python, pip. Por exemplo:

```bash
pip install tkinter Pillow opencv-python pyaudio moviepy keyboard pyautogui
```

## Como Usar 🚀
1. **Clone o repositório**:
``` base
   git clone https://github.com/MatheusFreire7/Recorder_Python.git
   cd Recorder_Python
```

2. **Execute o aplicativo Python**:
 ``` base
  python Recorder.py
```

- A interface gráfica será exibida, permitindo que você inicie a gravação.

- Pressione o botão "Iniciar" para iniciar a gravação. A gravação de tela e áudio começará.

- Para interromper a gravação, pressione a tecla "ESC" ou clique no botão "Parar". Os arquivos de vídeo e áudio gravados serão salvos no diretório do projeto.

- O vídeo gravado incluirá tanto o vídeo da tela quanto o áudio capturado.

- O vídeo final com áudio incorporado é salvo como "video_com_audio.mp4".

## Licença 📝
Este projeto está licenciado sob a [Licença MIT](LICENSE).
