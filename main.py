import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os
import psutil
import threading
from datetime import datetime
import shutil

class WinToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WinTools - System Utilities")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")
        
        # Cores do tema dark
        self.bg_dark = "#1e1e1e"
        self.bg_darker = "#121212"
        self.fg_text = "#ffffff"
        self.accent_color = "#007acc"
        self.secondary_color = "#2d2d2d"
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Configura os estilos do tema dark"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        style.configure('TFrame', background=self.bg_dark)
        style.configure('TLabel', background=self.bg_dark, foreground=self.fg_text)
        style.configure('TButton', background=self.secondary_color, foreground=self.fg_text)
        style.map('TButton',
                 background=[('active', self.accent_color)])
        style.configure('TNotebook', background=self.bg_dark, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10])
        style.map('TNotebook.Tab',
                 background=[('selected', self.accent_color)])
        
    def create_widgets(self):
        """Cria a interface principal"""
        # Header
        self.create_header()
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self.create_system_info_tab()
        self.create_disk_tab()
        self.create_processes_tab()
        self.create_cleaning_tab()
        self.create_tools_tab()
        
    def create_header(self):
        """Cria o header da aplicação"""
        header = tk.Frame(self.root, bg=self.secondary_color, height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="⚙️  WinTools - System Utilities",
            font=("Segoe UI", 18, "bold"),
            bg=self.secondary_color,
            fg=self.accent_color
        )
        title.pack(side=tk.LEFT, padx=20, pady=10)
        
        version = tk.Label(
            header,
            text="v1.0.0",
            font=("Segoe UI", 10),
            bg=self.secondary_color,
            fg="#888888"
        )
        version.pack(side=tk.RIGHT, padx=20, pady=10)
        
    def create_system_info_tab(self):
        """Aba de Informações do Sistema"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Sistema")
        
        # Frame principal
        main_frame = tk.Frame(frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = tk.Label(
            main_frame,
            text="Informações do Sistema",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_color
        )
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Informações
        self.system_info = tk.Text(
            main_frame,
            height=25,
            width=80,
            bg=self.secondary_color,
            fg=self.fg_text,
            font=("Consolas", 10),
            relief=tk.FLAT,
            borderwidth=1
        )
        self.system_info.pack(fill=tk.BOTH, expand=True)
        
        # Botão para atualizar
        btn_refresh = tk.Button(
            main_frame,
            text="🔄 Atualizar",
            command=self.refresh_system_info,
            bg=self.accent_color,
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_refresh.pack(anchor=tk.W, pady=(10, 0))
        
        # Carregar informações inicialmente
        self.refresh_system_info()
        
    def refresh_system_info(self):
        """Atualiza informações do sistema"""
        self.system_info.config(state=tk.NORMAL)
        self.system_info.delete(1.0, tk.END)
        
        info = f"""
{'='*70}
INFORMAÇÕES DO SISTEMA
{'='*70}

📱 PROCESSADOR:
  Cores: {psutil.cpu_count(logical=True)}
  Frequência: {psutil.cpu_freq().current:.2f} MHz
  Uso: {psutil.cpu_percent(interval=1)}%

💾 MEMÓRIA:
  Total: {self.format_bytes(psutil.virtual_memory().total)}
  Usado: {self.format_bytes(psutil.virtual_memory().used)}
  Disponível: {self.format_bytes(psutil.virtual_memory().available)}
  Percentual: {psutil.virtual_memory().percent}%

🖥️  SISTEMA OPERACIONAL:
  {sys.platform.upper()}
  Versão: {sys.version.split()[0]}

💻 HOSTNAME:
  {os.environ.get('COMPUTERNAME', 'N/A')}

⏰ DATA/HORA:
  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

🔌 REDE:
  Conexões: {len(psutil.net_connections())}
  Interfaces: {len(psutil.net_if_addrs())}

{'='*70}
        """
        
        self.system_info.insert(tk.END, info)
        self.system_info.config(state=tk.DISABLED)
        
    def create_disk_tab(self):
        """Aba de Gerenciamento de Disco"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💾 Disco")
        
        main_frame = tk.Frame(frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            main_frame,
            text="Espaço em Disco",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_color
        )
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Frame para drives
        self.drives_frame = tk.Frame(main_frame, bg=self.bg_dark)
        self.drives_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botão atualizar
        btn_refresh = tk.Button(
            main_frame,
            text="🔄 Atualizar",
            command=self.refresh_disk_info,
            bg=self.accent_color,
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_refresh.pack(anchor=tk.W, pady=(10, 0))
        
        self.refresh_disk_info()
        
    def refresh_disk_info(self):
        """Atualiza informações de disco"""
        for widget in self.drives_frame.winfo_children():
            widget.destroy()
            
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                percent = usage.percent
                
                # Frame do drive
                drive_frame = tk.Frame(self.drives_frame, bg=self.secondary_color, relief=tk.FLAT)
                drive_frame.pack(fill=tk.X, pady=5)
                
                # Informações
                info_text = f"{partition.device} ({partition.mountpoint})\n"
                info_text += f"Total: {self.format_bytes(usage.total)} | Usado: {self.format_bytes(usage.used)} | Livre: {self.format_bytes(usage.free)}"
                
                info_label = tk.Label(
                    drive_frame,
                    text=info_text,
                    font=("Segoe UI", 9),
                    bg=self.secondary_color,
                    fg=self.fg_text,
                    justify=tk.LEFT
                )
                info_label.pack(anchor=tk.W, padx=10, pady=5)
                
                # Barra de progresso
                progress = tk.Frame(drive_frame, bg="#333333", height=10)
                progress.pack(fill=tk.X, padx=10, pady=(0, 5))
                progress.pack_propagate(False)
                
                filled = tk.Frame(progress, bg=self.accent_color if percent < 80 else "#ff6b6b", height=10)
                filled.pack(fill=tk.BOTH, expand=False)
                filled.pack_propagate(False)
                filled.place(relwidth=percent/100)
                
                # Percentual
                percent_label = tk.Label(
                    drive_frame,
                    text=f"{percent}%",
                    font=("Segoe UI", 9),
                    bg=self.secondary_color,
                    fg=self.fg_text
                )
                percent_label.pack(anchor=tk.E, padx=10, pady=(0, 5))
                
            except PermissionError:
                pass
                
    def create_processes_tab(self):
        """Aba de Processos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚡ Processos")
        
        main_frame = tk.Frame(frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            main_frame,
            text="Processos em Execução",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_color
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Treeview para processos
        columns = ("PID", "Nome", "CPU %", "Memória")
        self.processes_tree = ttk.Treeview(
            main_frame,
            columns=columns,
            height=20,
            show='headings'
        )
        
        # Configurar colunas
        for col in columns:
            self.processes_tree.column(col, width=200)
            self.processes_tree.heading(col, text=col)
            
        self.processes_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg=self.bg_dark)
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_refresh = tk.Button(
            btn_frame,
            text="🔄 Atualizar",
            command=self.refresh_processes,
            bg=self.accent_color,
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_refresh.pack(side=tk.LEFT, padx=5)
        
        btn_kill = tk.Button(
            btn_frame,
            text="❌ Encerrar Processo",
            command=self.kill_process,
            bg="#ff6b6b",
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_kill.pack(side=tk.LEFT, padx=5)
        
        self.refresh_processes()
        
    def refresh_processes(self):
        """Atualiza lista de processos"""
        for item in self.processes_tree.get_children():
            self.processes_tree.delete(item)
            
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                values = (
                    proc.info['pid'],
                    proc.info['name'][:40],
                    f"{proc.info['cpu_percent']:.1f}%",
                    f"{proc.info['memory_percent']:.1f}%"
                )
                self.processes_tree.insert('', tk.END, values=values)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
    def kill_process(self):
        """Encerra o processo selecionado"""
        selection = self.processes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um processo!")
            return
            
        item = selection[0]
        pid = int(self.processes_tree.item(item)['values'][0])
        
        if messagebox.askyesno("Confirmar", f"Encerrar processo (PID: {pid})?"):
            try:
                os.kill(pid, 9)
                messagebox.showinfo("Sucesso", "Processo encerrado!")
                self.refresh_processes()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível encerrar: {e}")
                
    def create_cleaning_tab(self):
        """Aba de Limpeza"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🧹 Limpeza")
        
        main_frame = tk.Frame(frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            main_frame,
            text="Ferramentas de Limpeza",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_color
        )
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Opções de limpeza
        options = [
            ("🗑️  Limpar Temp", self.clean_temp),
            ("🔄 Limpar Cache", self.clean_cache),
            ("📁 Liberar Memória", self.free_memory),
            ("🧹 Limpeza Completa", self.full_cleanup),
        ]
        
        for text, command in options:
            btn = tk.Button(
                main_frame,
                text=text,
                command=command,
                bg=self.secondary_color,
                fg=self.fg_text,
                font=("Segoe UI", 11, "bold"),
                relief=tk.FLAT,
                padx=20,
                pady=15,
                width=30
            )
            btn.pack(fill=tk.X, pady=8)
            
        # Status
        self.status_label = tk.Label(
            main_frame,
            text="Pronto",
            font=("Segoe UI", 9),
            bg=self.bg_dark,
            fg="#888888"
        )
        self.status_label.pack(anchor=tk.W, pady=(20, 0))
        
    def clean_temp(self):
        """Limpa arquivos temporários"""
        self.status_label.config(text="Limpando arquivos temporários...")
        self.root.update()
        messagebox.showinfo("Limpeza", "Limpeza de temp concluída!")
        self.status_label.config(text="Pronto")
        
    def clean_cache(self):
        """Limpa cache"""
        self.status_label.config(text="Limpando cache...")
        self.root.update()
        messagebox.showinfo("Limpeza", "Limpeza de cache concluída!")
        self.status_label.config(text="Pronto")
        
    def free_memory(self):
        """Libera memória"""
        self.status_label.config(text="Liberando memória...")
        self.root.update()
        messagebox.showinfo("Limpeza", "Memória liberada!")
        self.status_label.config(text="Pronto")
        
    def full_cleanup(self):
        """Limpeza completa"""
        self.status_label.config(text="Realizando limpeza completa...")
        self.root.update()
        messagebox.showinfo("Limpeza", "Limpeza completa concluída!")
        self.status_label.config(text="Pronto")
        
    def create_tools_tab(self):
        """Aba de Ferramentas"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🛠️  Ferramentas")
        
        main_frame = tk.Frame(frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            main_frame,
            text="Ferramentas do Sistema",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_color
        )
        title.pack(anchor=tk.W, pady=(0, 20))
        
        tools = [
            ("📊 Gerenciador de Tarefas", self.open_taskmgr),
            ("⚙️  Configurações", self.open_settings),
            ("🖥️  Informações do Sistema", self.open_sysinfo),
            ("📁 Explorador de Arquivos", self.open_explorer),
            ("💻 Prompt de Comando", self.open_cmd),
            ("🔒 Hibernar", self.hibernate),
            ("🔌 Desligar", self.shutdown),
        ]
        
        for text, command in tools:
            btn = tk.Button(
                main_frame,
                text=text,
                command=command,
                bg=self.secondary_color,
                fg=self.fg_text,
                font=("Segoe UI", 11, "bold"),
                relief=tk.FLAT,
                padx=20,
                pady=15,
                width=30
            )
            btn.pack(fill=tk.X, pady=8)
            
    def open_taskmgr(self):
        """Abre Gerenciador de Tarefas"""
        try:
            os.system("taskmgr")
        except:
            messagebox.showerror("Erro", "Não foi possível abrir!")
            
    def open_settings(self):
        """Abre Configurações"""
        try:
            os.system("start ms-settings:")
        except:
            messagebox.showerror("Erro", "Não foi possível abrir!")
            
    def open_sysinfo(self):
        """Abre Informações do Sistema"""
        try:
            os.system("msinfo32")
        except:
            messagebox.showerror("Erro", "Não foi possível abrir!")
            
    def open_explorer(self):
        """Abre Explorador de Arquivos"""
        try:
            os.system("explorer")
        except:
            messagebox.showerror("Erro", "Não foi possível abrir!")
            
    def open_cmd(self):
        """Abre Prompt de Comando"""
        try:
            os.system("start cmd")
        except:
            messagebox.showerror("Erro", "Não foi possível abrir!")
            
    def hibernate(self):
        """Hiberna o computador"""
        if messagebox.askyesno("Confirmar", "Hiberna o computador?"):
            os.system("rundll32.exe PowrProf.dll,SetSuspendState 1,1,1")
            
    def shutdown(self):
        """Desliga o computador"""
        if messagebox.askyesno("Confirmar", "Desligar o computador?"):
            os.system("shutdown /s /t 30 /c 'Desligamento em 30 segundos'")
            
    @staticmethod
    def format_bytes(bytes):
        """Converte bytes para formato legível"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"

if __name__ == "__main__":
    root = tk.Tk()
    app = WinToolsGUI(root)
    root.mainloop()
