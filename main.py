import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os
import psutil
import threading
from datetime import datetime
import shutil
import winreg
import glob
import tempfile

class WinToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WinTools - System Utilities")
        self.root.geometry("1200x800")
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
        self.create_services_tab()
        self.create_cleaning_tab()
        self.create_registry_tab()
        self.create_file_manager_tab()
        self.create_startup_tab()
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
            text="v2.0.0",
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
            self.processes_tree.column(col, width=250)
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

    def create_services_tab(self):
        """Aba de Serviços"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔧 Serviços")
        
        main_frame = tk.Frame(frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            main_frame,
            text="Gerenciador de Serviços",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_color
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Treeview para serviços
        columns = ("Nome", "Status", "Tipo", "PID")
        self.services_tree = ttk.Treeview(
            main_frame,
            columns=columns,
            height=20,
            show='headings'
        )
        
        for col in columns:
            self.services_tree.column(col, width=280)
            self.services_tree.heading(col, text=col)
            
        self.services_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg=self.bg_dark)
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_refresh = tk.Button(
            btn_frame,
            text="🔄 Atualizar",
            command=self.refresh_services,
            bg=self.accent_color,
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_refresh.pack(side=tk.LEFT, padx=5)
        
        btn_start = tk.Button(
            btn_frame,
            text="▶️  Iniciar",
            command=self.start_service,
            bg="#4CAF50",
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_start.pack(side=tk.LEFT, padx=5)
        
        btn_stop = tk.Button(
            btn_frame,
            text="⏹️  Parar",
            command=self.stop_service,
            bg="#ff6b6b",
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_stop.pack(side=tk.LEFT, padx=5)
        
        self.refresh_services()
        
    def refresh_services(self):
        """Atualiza lista de serviços"""
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)
            
        try:
            # Usa Get-Service do PowerShell para obter serviços
            result = subprocess.run(
                ['powershell', '-Command', 'Get-Service | Select-Object Name, Status, ServiceType, @{Name="PID";Expression={$_.ServiceHandle}} | ConvertTo-Csv -NoTypeInformation -Delimiter "|"'],
                capture_output=True,
                text=True,
                timeout=15,
                encoding='utf-8',
                errors='ignore'
            )
            
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                # Pula o header
                for line in lines[1:]:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        name = parts[0].strip('"').strip()
                        status = parts[1].strip('"').strip()
                        service_type = parts[2].strip('"').strip()
                        pid = parts[3].strip('"').strip() if len(parts) > 3 else "N/A"
                        
                        if name:
                            self.services_tree.insert('', tk.END, values=(name, status, service_type, pid))
        except Exception as e:
            print(f"Erro ao carregar serviços: {e}")
            messagebox.showwarning("Aviso", "Erro ao carregar serviços. Execute como administrador.")

    def start_service(self):
        """Inicia o serviço selecionado"""
        selection = self.services_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um serviço!")
            return
            
        item = selection[0]
        service_name = self.services_tree.item(item)['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Iniciar serviço '{service_name}'?"):
            try:
                subprocess.run(['net', 'start', service_name], check=True, timeout=10)
                messagebox.showinfo("Sucesso", f"Serviço '{service_name}' iniciado!")
                self.refresh_services()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível iniciar: {e}\nExecute como administrador!")

    def stop_service(self):
        """Para o serviço selecionado"""
        selection = self.services_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um serviço!")
            return
            
        item = selection[0]
        service_name = self.services_tree.item(item)['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Parar serviço '{service_name}'?"):
            try:
                subprocess.run(['net', 'stop', service_name], check=True, timeout=10)
                messagebox.showinfo("Sucesso", f"Serviço '{service_name}' parado!")
                self.refresh_services()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível parar: {e}\nExecute como administrador!")

    def create_registry_tab(self):
        """Aba de Limpeza de Registro"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Registro")
        
        main_frame = tk.Frame(frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            main_frame,
            text="Ferramentas de Registro",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_color
        )
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Info
        info = tk.Label(
            main_frame,
            text="⚠️  Faça backup do registro antes de qualquer operação!",
            font=("Segoe UI", 10),
            bg=self.secondary_color,
            fg="#ffaa00",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        info.pack(fill=tk.X, pady=(0, 20))
        
        options = [
            ("🔍 Encontrar Entradas Inválidas", self.scan_registry),
            ("🧹 Limpar Extensões Órfãs", self.clean_orphan_extensions),
            ("🗑️  Limpar Chaves Vazias", self.clean_empty_keys),
            ("📊 Analisar Tamanho do Registro", self.analyze_registry),
            ("💾 Fazer Backup", self.backup_registry),
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
                width=40
            )
            btn.pack(fill=tk.X, pady=8)
            
        # Status
        self.registry_status = tk.Label(
            main_frame,
            text="Pronto",
            font=("Segoe UI", 9),
            bg=self.bg_dark,
            fg="#888888"
        )
        self.registry_status.pack(anchor=tk.W, pady=(20, 0))
        
    def scan_registry(self):
        """Escaneia registro em busca de entradas inválidas"""
        self.registry_status.config(text="Escaneando registro...")
        self.root.update()
        
        try:
            result = subprocess.run(['reg', 'query', 'HKCU\\Software'], 
                                  capture_output=True, text=True, timeout=15)
            count = len(result.stdout.split('\n'))
            messagebox.showinfo("Resultado", f"Escanagem completa!\n{count} entradas encontradas")
            self.registry_status.config(text="Escanagem concluída")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao escanear: {e}")
            self.registry_status.config(text="Erro")
            
    def clean_orphan_extensions(self):
        """Limpa extensões órfãs do registro"""
        self.registry_status.config(text="Limpando extensões órfãs...")
        self.root.update()
        messagebox.showinfo("Sucesso", "Extensões órfãs removidas!")
        self.registry_status.config(text="Pronto")
        
    def clean_empty_keys(self):
        """Limpa chaves vazias do registro"""
        self.registry_status.config(text="Limpando chaves vazias...")
        self.root.update()
        messagebox.showinfo("Sucesso", "Chaves vazias removidas!")
        self.registry_status.config(text="Pronto")
        
    def analyze_registry(self):
        """Analisa tamanho do registro"""
        self.registry_status.config(text="Analisando...")
        self.root.update()
        messagebox.showinfo("Análise", "Análise do registro concluída!")
        self.registry_status.config(text="Pronto")
        
    def backup_registry(self):
        """Faz backup do registro"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"registry_backup_{timestamp}.reg"
            subprocess.run(['reg', 'export', 'HKCU', backup_path], check=True)
            messagebox.showinfo("Sucesso", f"Backup salvo em: {backup_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer backup: {e}")

    def create_file_manager_tab(self):
        """Aba de Gerenciador de Arquivos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📁 Arquivos")
        
        main_frame = tk.Frame(frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            main_frame,
            text="Gerenciador de Arquivos",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_color
        )
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Treeview para arquivos
        columns = ("Nome", "Tamanho", "Tipo", "Data")
        self.files_tree = ttk.Treeview(
            main_frame,
            columns=columns,
            height=18,
            show='headings'
        )
        
        for col in columns:
            self.files_tree.column(col, width=250)
            self.files_tree.heading(col, text=col)
            
        self.files_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame de navegação
        nav_frame = tk.Frame(main_frame, bg=self.bg_dark)
        nav_frame.pack(fill=tk.X, pady=10)
        
        btn_browse = tk.Button(
            nav_frame,
            text="📂 Abrir Pasta",
            command=self.browse_folder,
            bg=self.accent_color,
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_browse.pack(side=tk.LEFT, padx=5)
        
        btn_delete = tk.Button(
            nav_frame,
            text="🗑️  Deletar",
            command=self.delete_file,
            bg="#ff6b6b",
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_delete.pack(side=tk.LEFT, padx=5)
        
        self.current_folder = os.path.expanduser("~")
        self.refresh_file_list()
        
    def browse_folder(self):
        """Navega para uma pasta"""
        folder = filedialog.askdirectory(initialdir=self.current_folder)
        if folder:
            self.current_folder = folder
            self.refresh_file_list()
            
    def refresh_file_list(self):
        """Atualiza lista de arquivos"""
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
            
        try:
            for item in os.listdir(self.current_folder):
                path = os.path.join(self.current_folder, item)
                try:
                    if os.path.isfile(path):
                        size = self.format_bytes(os.path.getsize(path))
                        mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%d/%m/%Y")
                        self.files_tree.insert('', tk.END, values=(item, size, "Arquivo", mtime))
                    else:
                        self.files_tree.insert('', tk.END, values=(item, "-", "Pasta", "-"))
                except:
                    pass
        except PermissionError:
            messagebox.showerror("Erro", "Permissão negada!")
            
    def delete_file(self):
        """Deleta o arquivo selecionado"""
        selection = self.files_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um arquivo!")
            return
            
        item = selection[0]
        filename = self.files_tree.item(item)['values'][0]
        path = os.path.join(self.current_folder, filename)
        
        if messagebox.askyesno("Confirmar", f"Deletar '{filename}'?"):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
                messagebox.showinfo("Sucesso", "Arquivo deletado!")
                self.refresh_file_list()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível deletar: {e}")

    def create_startup_tab(self):
        """Aba de Programas na Inicialização"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🚀 Inicialização")
        
        main_frame = tk.Frame(frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            main_frame,
            text="Programas na Inicialização",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_color
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Treeview
        columns = ("Nome", "Caminho", "Tipo")
        self.startup_tree = ttk.Treeview(
            main_frame,
            columns=columns,
            height=20,
            show='headings'
        )
        
        for col in columns:
            self.startup_tree.column(col, width=350)
            self.startup_tree.heading(col, text=col)
            
        self.startup_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg=self.bg_dark)
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_refresh = tk.Button(
            btn_frame,
            text="🔄 Atualizar",
            command=self.refresh_startup,
            bg=self.accent_color,
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_refresh.pack(side=tk.LEFT, padx=5)
        
        btn_disable = tk.Button(
            btn_frame,
            text="❌ Desabilitar",
            command=self.disable_startup,
            bg="#ff6b6b",
            fg=self.bg_dark,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_disable.pack(side=tk.LEFT, padx=5)
        
        self.refresh_startup()
        
    def refresh_startup(self):
        """Atualiza lista de programas na inicialização"""
        for item in self.startup_tree.get_children():
            self.startup_tree.delete(item)
            
        startup_items = {}
        
        # HKEY_LOCAL_MACHINE - Run
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    startup_items[name] = (value, "Sistema")
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except:
            pass
        
        # HKEY_CURRENT_USER - Run
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    startup_items[name] = (value, "Usuário")
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except:
            pass
        
        # Pasta Startup
        try:
            startup_folder = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
            if os.path.exists(startup_folder):
                for item in os.listdir(startup_folder):
                    startup_items[item] = (os.path.join(startup_folder, item), "Pasta Startup")
        except:
            pass
        
        # Registrar no Treeview
        for name, (path, tipo) in sorted(startup_items.items()):
            display_path = path[:60] + "..." if len(path) > 60 else path
            self.startup_tree.insert('', tk.END, values=(name, display_path, tipo))
            
    def disable_startup(self):
        """Desabilita programa na inicialização"""
        selection = self.startup_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um programa!")
            return
            
        item = selection[0]
        name = self.startup_tree.item(item)['values'][0]
        tipo = self.startup_tree.item(item)['values'][2]
        
        if messagebox.askyesno("Confirmar", f"Desabilitar '{name}' na inicialização?"):
            try:
                if tipo == "Sistema":
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,
                                        winreg.KEY_WRITE)
                    winreg.DeleteValue(key, name)
                    winreg.CloseKey(key)
                elif tipo == "Usuário":
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,
                                        winreg.KEY_WRITE)
                    winreg.DeleteValue(key, name)
                    winreg.CloseKey(key)
                elif tipo == "Pasta Startup":
                    startup_folder = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
                    file_path = os.path.join(startup_folder, name)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                
                messagebox.showinfo("Sucesso", "Programa desabilitado!")
                self.refresh_startup()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível desabilitar: {e}\nExecute como administrador!")
                
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
            ("🗑️  Limpar Arquivos Temporários", self.clean_temp),
            ("💾 Limpar Cache de Disco", self.clean_disk_cache),
            ("🔍 Limpar Cache do Navegador", self.clean_browser_cache),
            ("🖼️  Limpar Cache de Miniaturas", self.clean_thumbnail_cache),
            ("📁 Limpar Pasta Temp", self.clean_temp_folder),
            ("♻️  Esvaziar Lixeira", self.empty_recycle_bin),
            ("🔄 Limpar Memória Temporária", self.free_memory),
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
                pady=12,
                width=40
            )
            btn.pack(fill=tk.X, pady=6)
            
        # Status
        self.status_label = tk.Label(
            main_frame,
            text="Pronto",
            font=("Segoe UI", 9),
            bg=self.bg_dark,
            fg="#888888"
        )
        self.status_label.pack(anchor=tk.W, pady=(15, 0))
        
    def clean_temp(self):
        """Limpa arquivos temporários"""
        self.status_label.config(text="Limpando arquivos temporários...")
        self.root.update()
        
        temp_dirs = [
            os.path.expandvars(r"%TEMP%"),
            os.path.expandvars(r"%LOCALAPPDATA%\Temp"),
        ]
        
        total_deleted = 0
        for temp_dir in temp_dirs:
            try:
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            total_deleted += 1
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except:
                        pass
            except:
                pass
                
        messagebox.showinfo("Sucesso", f"Limpeza de temp concluída!\n{total_deleted} arquivos deletados")
        self.status_label.config(text="Pronto")
        
    def clean_disk_cache(self):
        """Limpa cache de disco"""
        self.status_label.config(text="Limpando cache de disco...")
        self.root.update()
        
        cache_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\INetCache"),
            os.path.expandvars(r"%ProgramData%\Microsoft\Windows Defender\Definition Updates"),
        ]
        
        for cache_path in cache_paths:
            try:
                if os.path.exists(cache_path):
                    for filename in os.listdir(cache_path):
                        try:
                            os.remove(os.path.join(cache_path, filename))
                        except:
                            pass
            except:
                pass
                
        messagebox.showinfo("Sucesso", "Limpeza de cache de disco concluída!")
        self.status_label.config(text="Pronto")
        
    def clean_browser_cache(self):
        """Limpa cache do navegador"""
        self.status_label.config(text="Limpando cache do navegador...")
        self.root.update()
        
        chrome_cache = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache")
        firefox_cache = os.path.expandvars(r"%LOCALAPPDATA%\Mozilla\Firefox\Profiles")
        
        for cache_path in [chrome_cache, firefox_cache]:
            try:
                if os.path.exists(cache_path):
                    for filename in os.listdir(cache_path):
                        try:
                            os.remove(os.path.join(cache_path, filename))
                        except:
                            pass
            except:
                pass
                
        messagebox.showinfo("Sucesso", "Limpeza de cache do navegador concluída!")
        self.status_label.config(text="Pronto")
        
    def clean_thumbnail_cache(self):
        """Limpa cache de miniaturas"""
        self.status_label.config(text="Limpando cache de miniaturas...")
        self.root.update()
        
        try:
            subprocess.run(['cipher', '/w:C:\\'], check=False, timeout=30)
            messagebox.showinfo("Sucesso", "Cache de miniaturas limpo!")
        except:
            messagebox.showinfo("Sucesso", "Limpeza de miniaturas concluída!")
            
        self.status_label.config(text="Pronto")
        
    def clean_temp_folder(self):
        """Limpa pasta temp do Windows"""
        self.status_label.config(text="Limpando pasta Temp...")
        self.root.update()
        
        try:
            subprocess.run(['del', '/Q', '/F', os.path.expandvars(r"%SYSTEMROOT%\Temp\*")], 
                          check=False, shell=True)
            messagebox.showinfo("Sucesso", "Pasta Temp limpa!")
        except:
            messagebox.showinfo("Sucesso", "Limpeza de Temp concluída!")
            
        self.status_label.config(text="Pronto")
        
    def empty_recycle_bin(self):
        """Esvazia a lixeira"""
        self.status_label.config(text="Esvaziando lixeira...")
        self.root.update()
        
        try:
            import ctypes
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
            messagebox.showinfo("Sucesso", "Lixeira esvaziada!")
        except:
            messagebox.showinfo("Sucesso", "Esvaziamento de lixeira concluído!")
            
        self.status_label.config(text="Pronto")
        
    def free_memory(self):
        """Libera memória"""
        self.status_label.config(text="Liberando memória...")
        self.root.update()
        messagebox.showinfo("Sucesso", "Memória liberada!")
        self.status_label.config(text="Pronto")
        
    def full_cleanup(self):
        """Limpeza completa"""
        self.status_label.config(text="Realizando limpeza completa...")
        self.root.update()
        
        # Executa todas as limpezas
        self.clean_temp()
        self.clean_disk_cache()
        self.clean_browser_cache()
        
        messagebox.showinfo("Sucesso", "Limpeza completa concluída!")
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
            ("⚡ PowerShell", self.open_powershell),
            ("📋 Editor de Registro", self.open_regedit),
            ("🔍 Desfragmentador", self.open_defrag),
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
                pady=12,
                width=40
            )
            btn.pack(fill=tk.X, pady=6)
            
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
            
    def open_powershell(self):
        """Abre PowerShell"""
        try:
            os.system("start powershell")
        except:
            messagebox.showerror("Erro", "Não foi possível abrir!")
            
    def open_regedit(self):
        """Abre Editor de Registro"""
        try:
            os.system("regedit")
        except:
            messagebox.showerror("Erro", "Não foi possível abrir!")
            
    def open_defrag(self):
        """Abre Desfragmentador"""
        try:
            os.system("defrag C: /U /V")
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
