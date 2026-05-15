from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx

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
        text   = data.get("text", "")
        source = LANG_MAP.get(data.get("source", ""), "de")
        target = LANG_MAP.get(data.get("target", ""), "tr")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://api.mymemory.translated.net/get",
                params={
                    "q": text,
                    "langpair": f"{source}|{target}"
                }
            )

        if response.status_code == 200:
            translated = response.json().get("responseData", {}).get("translatedText", "Çeviri alınamadı.")
            return {"result": translated}
        else:
            return JSONResponse({"result": f"Hata: {response.status_code}"})

    except Exception as e:
        return JSONResponse({"result": f"Hata: {str(e)}"})


app.mount("/", StaticFiles(directory="static", html=True), name="static")
