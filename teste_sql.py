
import threading
import pytds
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# --- PREENCHA COM OS DADOS DO SEU SQL SERVER ---
DB_HOST = "127.0.0.1"      # IP do PC na rede Wi-Fi
DB_PORT = 3000                # Porta do SQL Server
DB_NAME = "CAPESTACIONAMENTO"    # Nome do banco de dados
DB_USER = "suv"       # Usuário do SQL Server
DB_PASS = "201801"         # Senha do SQL Server
TABELA_TESTE = "TblQualificador1"    # Nome de uma tabela existente


class TesteConexaoSQL(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=25, spacing=20)

        self.lbl_resultado = Label(
            text="Pronto para testar.\nToque no botão abaixo para conectar.",
            halign="center",
            valign="middle",
            font_size="16sp",
        )
        self.lbl_resultado.bind(size=self.lbl_resultado.setter("text_size"))

        self.btn_conectar = Button(
            text="Testar Conexão e Ler 5 Registros",
            size_hint=(1, 0.2),
            background_color=(0.1, 0.5, 0.8, 1),
        )
        self.btn_conectar.bind(on_press=self.iniciar_teste)

        layout.add_widget(self.lbl_resultado)
        layout.add_widget(self.btn_conectar)
        return layout

    def iniciar_teste(self, instance):
        self.btn_conectar.disabled = True
        self.lbl_resultado.text = f"Conectando em {DB_HOST}:{DB_PORT}..."
        threading.Thread(target=self.executar_consulta, daemon=True).start()

    def executar_consulta(self):
        try:
            with pytds.connect(
                dsn=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                timeout=8,
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT TOP 5 * FROM {TABELA_TESTE}")
                    colunas = [col[0] for col in cursor.description]
                    linhas = cursor.fetchall()

                    texto = f"Conectado com sucesso!\nColunas: {', '.join(colunas[:4])}\n\n"
                    for i, linha in enumerate(linhas, 1):
                        texto += f"Reg {i}: {linha[:3]}\n"

        except Exception as e:
            texto = f"Erro ao conectar:\n{str(e)}"

        Clock.schedule_once(lambda dt: self.atualizar_interface(texto))

    def atualizar_interface(self, texto):
        self.lbl_resultado.text = texto
        self.btn_conectar.disabled = False


if __name__ == "__main__":
    TesteConexaoSQL().run()
