"""
TTS 语音朗读工具
用浏览器内置 Web Speech API（零依赖、免费）
用法：
  from ui.tts import speak, stop_speaking
  speak("这是朗读的文本")
  speak("你好，世界", rate=0.9, pitch=1.0, lang="zh-CN")
  stop_speaking()
"""

from nicegui import ui

def speak(text: str, rate: float = 1.0, pitch: float = 1.0, lang: str = "zh-CN", volume: float = 1.0) -> None:
    escaped = text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    js = f"""
    (function() {{
      if (!('speechSynthesis' in window)) {{ return; }}
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance("{escaped}");
      u.rate = {rate};
      u.pitch = {pitch};
      u.lang = "{lang}";
      u.volume = {volume};
      window.speechSynthesis.speak(u);
    }})();
    """
    ui.run_javascript(js)

def stop_speaking() -> None:
    ui.run_javascript(
        "(function(){ if('speechSynthesis' in window){ window.speechSynthesis.cancel(); } })();"
    )
