"""
CAPTURADOR DE DADOS - Extrai dados do Aviator em tempo real
Monitora multiplicadores e cria padrões de velas
"""

import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import streamlit as st


class CapturadorDados:
    """Captura dados do Aviator via iframe"""
    
    def __init__(self):
        self.velas_capturadas: List[Dict] = []
        self.ultima_rodada_processada = None
        self.contador_rodadas = 0
        self.dados_brutos = []
    
    def extrair_multiplicador_do_texto(self, texto: str) -> Optional[float]:
        """Extrair multiplicador de um texto"""
        
        # Padrões possíveis: 1.50x, 2.45x, 10.00x, 56.21x
        padrao = r'(\d+\.?\d*)[xX]'
        match = re.search(padrao, texto)
        
        if match:
            try:
                valor = float(match.group(1))
                # Validar se é um multiplicador válido
                if 1.0 <= valor <= 5000.0:
                    return valor
            except ValueError:
                pass
        
        return None
    
    def extrair_timestamp(self, texto: str) -> Optional[str]:
        """Extrair timestamp de um texto"""
        
        # Padrão: HH:MM:SS
        padrao = r'(\d{2}):(\d{2}):(\d{2})'
        match = re.search(padrao, texto)
        
        if match:
            return match.group(0)
        
        return None
    
    def processar_dados_brutos(self, dados_brutos: str) -> Optional[Dict]:
        """
        Processar dados brutos capturados do iframe
        
        Espera formato como:
        "2.45x 14:32:15"
        ou
        "Rodada #1234 - Resultado: 5.67x - Hora: 14:32:15"
        """
        
        if not dados_brutos or not isinstance(dados_brutos, str):
            return None
        
        # Limpar dados
        dados_limpos = dados_brutos.strip()
        
        # Extrair multiplicador
        multiplicador = self.extrair_multiplicador_do_texto(dados_limpos)
        
        if multiplicador is None:
            return None
        
        # Extrair timestamp
        timestamp = self.extrair_timestamp(dados_limpos)
        
        if timestamp is None:
            # Usar hora atual se não encontrar
            timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Extrair data
        data = datetime.now().strftime("%Y-%m-%d")
        
        # Criar vela
        vela = {
            'multiplicador': multiplicador,
            'timestamp': timestamp,
            'data': data,
            'capturado_em': datetime.now().isoformat(),
            'id': f"vela_{datetime.now().timestamp()}"
        }
        
        return vela
    
    def adicionar_vela_manual(self, multiplicador: float, timestamp: str = None) -> Dict:
        """Adicionar vela manualmente (para testes)"""
        
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M:%S")
        
        data = datetime.now().strftime("%Y-%m-%d")
        
        vela = {
            'multiplicador': multiplicador,
            'timestamp': timestamp,
            'data': data,
            'capturado_em': datetime.now().isoformat(),
            'id': f"vela_{datetime.now().timestamp()}"
        }
        
        self.velas_capturadas.append(vela)
        self.contador_rodadas += 1
        
        return vela
    
    def obter_ultimas_velas(self, quantidade: int = 50) -> List[Dict]:
        """Obter últimas N velas capturadas"""
        return self.velas_capturadas[:quantidade]
    
    def obter_velas_por_hora(self, hora: str) -> List[Dict]:
        """Obter velas capturadas em uma hora específica"""
        return [v for v in self.velas_capturadas if v['timestamp'].startswith(hora)]
    
    def obter_velas_por_cor(self, cor: str) -> List[Dict]:
        """Obter velas por cor"""
        
        velas_por_cor = []
        
        for vela in self.velas_capturadas:
            mult = vela['multiplicador']
            
            if cor == 'azul' and 1.0 <= mult <= 1.99:
                velas_por_cor.append(vela)
            elif cor == 'roxa' and 2.0 <= mult <= 9.99:
                velas_por_cor.append(vela)
            elif cor == 'rosa' and mult >= 10.0:
                velas_por_cor.append(vela)
        
        return velas_por_cor
    
    def obter_estatisticas(self) -> Dict:
        """Obter estatísticas de captura"""
        
        if not self.velas_capturadas:
            return {
                'total_velas': 0,
                'velas_azuis': 0,
                'velas_roxas': 0,
                'velas_rosas': 0,
                'multiplicador_medio': 0,
                'multiplicador_maximo': 0,
                'multiplicador_minimo': 0,
                'taxa_rosas': 0
            }
        
        azuis = self.obter_velas_por_cor('azul')
        roxas = self.obter_velas_por_cor('roxa')
        rosas = self.obter_velas_por_cor('rosa')
        
        multiplicadores = [v['multiplicador'] for v in self.velas_capturadas]
        
        return {
            'total_velas': len(self.velas_capturadas),
            'velas_azuis': len(azuis),
            'velas_roxas': len(roxas),
            'velas_rosas': len(rosas),
            'multiplicador_medio': round(sum(multiplicadores) / len(multiplicadores), 2),
            'multiplicador_maximo': max(multiplicadores),
            'multiplicador_minimo': min(multiplicadores),
            'taxa_rosas': round((len(rosas) / len(self.velas_capturadas)) * 100, 2) if self.velas_capturadas else 0
        }
    
    def limpar_historico(self):
        """Limpar histórico de velas"""
        self.velas_capturadas.clear()
        self.contador_rodadas = 0
    
    def exportar_dados(self) -> str:
        """Exportar dados em formato CSV"""
        
        if not self.velas_capturadas:
            return ""
        
        # Cabeçalho
        csv = "multiplicador,timestamp,data,capturado_em,cor\n"
        
        # Dados
        for vela in self.velas_capturadas:
            mult = vela['multiplicador']
            
            if 1.0 <= mult <= 1.99:
                cor = 'azul'
            elif 2.0 <= mult <= 9.99:
                cor = 'roxa'
            elif mult >= 10.0:
                cor = 'rosa'
            else:
                cor = 'desconhecida'
            
            csv += f"{mult},{vela['timestamp']},{vela['data']},{vela['capturado_em']},{cor}\n"
        
        return csv


class MonitorAviator:
    """Monitora Aviator em tempo real"""
    
    def __init__(self, capturador: CapturadorDados):
        self.capturador = capturador
        self.monitorando = False
        self.intervalo_verificacao = 1  # segundos
    
    def iniciar_monitoramento(self):
        """Iniciar monitoramento"""
        self.monitorando = True
        st.session_state.monitorando = True
    
    def parar_monitoramento(self):
        """Parar monitoramento"""
        self.monitorando = False
        st.session_state.monitorando = False
    
    def processar_captura(self, dados: str) -> Optional[Dict]:
        """Processar dados capturados"""
        
        vela = self.capturador.processar_dados_brutos(dados)
        
        if vela:
            self.capturador.velas_capturadas.append(vela)
            self.capturador.contador_rodadas += 1
        
        return vela


# Singleton
_capturador_instance = None
_monitor_instance = None

def obter_capturador() -> CapturadorDados:
    """Obter instância singleton do capturador"""
    global _capturador_instance
    if _capturador_instance is None:
        _capturador_instance = CapturadorDados()
    return _capturador_instance

def obter_monitor() -> MonitorAviator:
    """Obter instância singleton do monitor"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = MonitorAviator(obter_capturador())
    return _monitor_instance

def resetar_capturador():
    """Resetar capturador"""
    global _capturador_instance
    _capturador_instance = CapturadorDados()
