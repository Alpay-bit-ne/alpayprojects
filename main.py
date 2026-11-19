from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from deep_translator import GoogleTranslator, MyMemoryTranslator

app = FastAPI()

LANG_MAP = {
    "Almanca": "de",
    "Türkçe": "tr",
    "German": "de",
    "Turkish": "tr",
}

@app.post("/translate")
async def translate(request: Request):
    try:
        data = await request.json()
        text = (data.get("text") or "").strip()
        source = LANG_MAP.get(data.get("source", ""), "de")
        target = LANG_MAP.get(data.get("target", ""), "tr")

        if not text:
            return JSONResponse({"result": ""})

        try:
            translated = MyMemoryTranslator(source=source, target=target).translate(text)
            if translated and "MYMEMORY WARNING" not in translated.upper():
                return {"result": translated}
        except Exception:
            pass

        translated = GoogleTranslator(source=source, target=target).translate(text)
        return {"result": translated or "Çeviri alınamadı."}

    except Exception as e:
        return JSONResponse({"result": f"Hata: {str(e)}"})

app.mount("/", StaticFiles(directory="static", html=True), name="static")
    except Exception as e:
        return JSONResponse({"result": f"Hata: {str(e)}"})

app.mount("/", StaticFiles(directory="static", html=True), name="static")
