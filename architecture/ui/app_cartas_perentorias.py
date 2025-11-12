import customtkinter as ctk
from tkinter import StringVar, messagebox
from core.logic import obtener_datos_proyecto

# Configuración del tema general
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CartaPerentoriaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Cartas Perentorias Innova Chile")
        self.geometry("620x720")
        self.resizable(False, False)

        # ─────────────────────────────────────────────
        # Título principal
        # ─────────────────────────────────────────────
        title = ctk.CTkLabel(self, text="Gestión de Cartas Perentorias Innova Chile",
                            font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        title.pack(pady=(20, 10))

        # ─────────────────────────────────────────────
        # Sección de búsqueda
        # ─────────────────────────────────────────────
        search_frame = ctk.CTkFrame(self, corner_radius=10)
        search_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(search_frame, text="Buscar proyecto por código:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.codigo_entry = ctk.CTkEntry(search_frame, width=180)
        self.codigo_entry.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(search_frame, text="Buscar", command=self.buscar_proyecto).grid(row=0, column=2, padx=10, pady=10)

        # ─────────────────────────────────────────────
        # Información del proyecto
        # ─────────────────────────────────────────────
        info_frame = ctk.CTkFrame(self, corner_radius=10)
        info_frame.pack(pady=10, padx=20, fill="x")

        self.nombre_proyecto_var = StringVar()
        self.beneficiario_var = StringVar()
        self.responsable_var = StringVar()

        ctk.CTkLabel(info_frame, text="Nombre del Proyecto:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
        ctk.CTkEntry(info_frame, textvariable=self.nombre_proyecto_var, width=350).grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(info_frame, text="Beneficiario:").grid(row=1, column=0, padx=10, pady=8, sticky="e")
        ctk.CTkEntry(info_frame, textvariable=self.beneficiario_var, width=350).grid(row=1, column=1, padx=10, pady=8)

        ctk.CTkLabel(info_frame, text="Responsable:").grid(row=2, column=0, padx=10, pady=8, sticky="e")
        ctk.CTkEntry(info_frame, textvariable=self.responsable_var, width=350).grid(row=2, column=1, padx=10, pady=8)

        # ─────────────────────────────────────────────
        # Acción y selección de informe
        # ─────────────────────────────────────────────
        action_frame = ctk.CTkFrame(self, corner_radius=10)
        action_frame.pack(pady=(15, 10), padx=20, fill="x")

        ctk.CTkLabel(action_frame, text="Acción:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
        self.accion_combo = ctk.CTkComboBox(action_frame,
                                            values=["Generar carta perentoria", "Generar carta de incumplimiento"],
                                            width=250)
        self.accion_combo.grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(action_frame, text="Informe asociado:").grid(row=1, column=0, padx=10, pady=8, sticky="e")
        self.informe_combo = ctk.CTkComboBox(action_frame,
                                            values=["Informe de avance", "Informe técnico", "Informe final"],
                                            width=250)
        self.informe_combo.grid(row=1, column=1, padx=10, pady=8)

        # ─────────────────────────────────────────────
        # Botón generar
        # ─────────────────────────────────────────────
        generate_btn = ctk.CTkButton(self, text="GENERAR DOCUMENTO", width=560, height=40,
                                    fg_color="#221E7C", hover_color="#3F3F3F",
                                    command=self.generar_documento)
        generate_btn.pack(pady=(20, 10))

        # ─────────────────────────────────────────────
        # Footer
        # ─────────────────────────────────────────────
        footer = ctk.CTkLabel(self, text="\nCORFO\nInnova Chile - Corfo",
                            font=ctk.CTkFont(size=12, slant="italic"), text_color="#72C7D5")
        footer.pack(pady=(20, 10))

    # ─────────────────────────────────────────────
    # Lógica simulada
    # ─────────────────────────────────────────────
    def buscar_proyecto(self):
        codigo = self.codigo_entry.get().strip()
        if not codigo:
            messagebox.showwarning("Atención", "Ingrese un código de proyecto.")
            return

        # Aquí llamas a tu lógica real (SOAP o JSON)
        # Ejemplo de integración:
        from core.logic import obtener_datos_proyecto  # <-- debes tener esta función en tu capa lógica

        try:
            project_info = obtener_datos_proyecto(codigo)

            # Rellenar campos de texto
            self.nombre_proyecto_var.set(project_info.get("nombreProyecto", ""))
            self.beneficiario_var.set(project_info.get("beneficiario", ""))
            self.responsable_var.set(project_info.get("representanteLegal", ""))

            # Limpiar y actualizar informes disponibles
            informes_disponibles = project_info.get("informesDisponibles", [])
            if informes_disponibles:
                self.informe_combo.configure(values=informes_disponibles)
                self.informe_combo.set(informes_disponibles[0])
            else:
                self.informe_combo.configure(values=["No hay informes disponibles"])
                self.informe_combo.set("No hay informes disponibles")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener información del proyecto.\n\n{e}")


    def generar_documento(self):
        accion = self.accion_combo.get().strip()
        informe = self.informe_combo.get().strip().upper()
        codigo = self.codigo_entry.get().strip()

        if not codigo or not accion or not informe:
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el código, seleccionar acción e informe asociado."
            )
            return

        try:
            # 🔹 Importaciones necesarias
            from architecture.document_processing.document_processor import DocumentProcessor
            from architecture.data_access.integration_data_manager import IntegrationDataManager

            # 🔹 Obtener la data completa desde IntegrationDataManager (SOAP + Excel)
            integration = IntegrationDataManager()
            data = integration.get_integrated_data(codigo)

            # 🔹 Crear instancia del procesador de documentos
            processor = DocumentProcessor()

            # ─────────────────────────────────────────────
            # ✅ Detección de tipo de carta (comparación exacta)
            # ─────────────────────────────────────────────
            accion_normalizada = accion.lower().strip()
            if "incumplimiento" in accion_normalizada:
                tipo_carta = "incumplimiento"
            elif "perentoria" in accion_normalizada:
                tipo_carta = "perentoria"
            else:
                tipo_carta = "perentoria"  # fallback por defecto
            # ─────────────────────────────────────────────

            # 🔍 Debug opcional
            print(f"📄 Código proyecto: {codigo}")
            print(f"🧾 Tipo carta: {tipo_carta}")
            print(f"📨 Informe seleccionado: {informe}")
            print(f"📋 Informes disponibles en data: {[r.get('reportType') for r in data.get('reports', [])]}")

            # 🔹 Llamar al generador
            try:
                output_path = processor.generate_letter(
                    data=data,
                    report_type=informe,
                    letter_type=tipo_carta
                )
            except ValueError as err:
                # 🔸 Fallback automático si no encuentra el informe
                reports = data.get("reports", [])
                if reports:
                    default_report = reports[0].get("reportType", "").strip()
                    messagebox.showwarning(
                        "Aviso",
                        f"No se encontró el informe '{informe}'. "
                        f"Se generará la carta utilizando '{default_report}'."
                    )
                    output_path = processor.generate_letter(
                        data=data,
                        report_type=default_report,
                        letter_type=tipo_carta
                    )
                else:
                    raise err

            # 🔹 Confirmación
            messagebox.showinfo(
                "Éxito",
                f"Carta generada exitosamente:\n{output_path}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un problema al generar la carta.\n\n{e}"
            )
# ─────────────────────────────────────────────
# Lanzamiento de la app
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = CartaPerentoriaApp()
    app.mainloop()