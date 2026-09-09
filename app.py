import customtkinter as ctk
import requests
import subprocess
import threading
import json
ollama = subprocess.Popen([
    r"C:\Users\ordin\AppData\Local\Programs\Ollama\ollama.exe","serve"
    ])

print("Ollama server is active")
app = ctk.CTk()
app.geometry("1280x720")
app.title("simple visual interface for ollama")

def send_to_ia():
    text = text_zone.get()
    reponse_ia.delete("1.0", "end")
    # Faire la requête dans un autre thread
    threading.Thread(
        target=requete_ia,
        args=(text,),
        daemon=True
    ).start()


def requete_ia(text):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:1b",
            "prompt": text,
            "stream": True
        },
        stream=True
    )

    for ligne in response.iter_lines():
        if ligne:
            data = ligne.decode("utf-8")
            morceau = json.loads(data)["response"]

            app.after(
                0,
                lambda m=morceau: print_response(m)
            )
def print_response(morceau):
    reponse_ia.insert("end", morceau)
    reponse_ia.see("end")

cadre = ctk.CTkFrame(app)
cadre.place(x=400, y=700)

text_zone = ctk.CTkEntry(
    cadre,
    placeholder_text="Write something...",
    width=400,
    height=50
)
text_zone.pack(side="left", padx=10)
bouton = ctk.CTkButton(cadre, text="send", command=send_to_ia)
bouton.pack(side="left", padx=10)
reponse_ia = ctk.CTkTextbox(
    app,
    width=700,
    height=400
)

reponse_ia.place(relx=0.5, rely=0.3, anchor="center")
def stop_server():
    print("Ollama is stopping...")

    resultat = subprocess.run(["powershell","-Command","(Get-NetTCPConnection -LocalPort 11434 -ErrorAction SilentlyContinue).OwningProcess"],
            capture_output=True,
            text=True
        )

    pid = resultat.stdout.strip()
    subprocess.run([
                "taskkill",
                "/PID", pid,
                "/T",
                "/F"
    ])
    app.destroy()
app.bind("<Return>", lambda event: send_to_ia())

app.protocol("WM_DELETE_WINDOW", stop_server)

app.mainloop()