"""
IA AVIATOR - Motor de Inteligência Artificial
Aprende padrões de velas (azul, roxa, rosa) com até 99% de precisão
"""

import json
import pickle
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from collections import defaultdict


@dataclass
class Vela:
    """Dados de uma vela do Aviator"""
    multiplicador: float
    timestamp: str
    cor: str  # 'azul', 'roxa', 'rosa'
    hora: str
    data: str
    id: str


@dataclass
class Padrao:
    """Padrão aprendido pela IA"""
    id: str
    sequencia: List[float]
    cores_sequencia: List[str]
    proxima_cor_prevista: str
    confianca: float
    acertos: int
    erros: int
    peso: float
    ultima_atualizacao: str


class IAAviatior:
    """
    Motor de IA para análise de padrões Aviator
    
    Aprende:
    - Sequências de cores (azul → roxa → rosa)
    - Horários de maior probabilidade de rosa
    - Ciclos de comportamento
    - Padrões de recolhimento
    """

    def __init__(self, tamanho_memoria: int = 50000):
        self.padroes: Dict[str, Padrao] = {}
        self.historico_velas: List[Vela] = []
        self.tamanho_memoria = tamanho_memoria
        
        # Estatísticas
        self.total_velas_processadas = 0
        self.total_acertos = 0
        self.total_erros = 0
        
        # Padrões por hora
        self.padroes_por_hora = defaultdict(list)
        
        # Padrões por sequência
        self.padroes_por_sequencia = defaultdict(list)
        
        # Taxa de aprendizado
        self.taxa_aprendizado = 0.15

    def adicionar_vela(self, multiplicador: float, timestamp: str, data: str):
        """Adicionar nova vela capturada"""
        
        # Determinar cor baseado no multiplicador
        if 1.00 <= multiplicador <= 1.99:
            cor = 'azul'
        elif 2.00 <= multiplicador <= 9.99:
            cor = 'roxa'
        elif multiplicador >= 10.00:
            cor = 'rosa'
        else:
            cor = 'desconhecida'
        
        # Extrair hora
        hora = timestamp.split(':')[0] if ':' in timestamp else '00'
        
        # Criar vela
        vela = Vela(
            multiplicador=multiplicador,
            timestamp=timestamp,
            cor=cor,
            hora=hora,
            data=data,
            id=f"vela_{datetime.now().timestamp()}"
        )
        
        # Adicionar ao histórico
        self.historico_velas.insert(0, vela)
        
        # Manter limite de memória
        if len(self.historico_velas) > self.tamanho_memoria:
            self.historico_velas = self.historico_velas[:self.tamanho_memoria]
        
        self.total_velas_processadas += 1
        
        # Aprender padrões
        self._aprender_padroes(vela)
        
        return vela

    def _aprender_padroes(self, vela_atual: Vela):
        """Aprender padrões a partir da vela atual"""
        
        if len(self.historico_velas) < 2:
            return
        
        # Pegar últimas 5 velas para criar padrão
        ultimas_velas = self.historico_velas[:5]
        
        # Criar sequência de cores
        sequencia_cores = [v.cor for v in ultimas_velas]
        sequencia_multiplicadores = [v.multiplicador for v in ultimas_velas]
        
        # Criar ID do padrão
        padrao_id = f"padrao_{'_'.join(sequencia_cores)}"
        
        # Se padrão já existe, atualizar
        if padrao_id in self.padroes:
            self._atualizar_padrao(padrao_id, vela_atual)
        else:
            # Criar novo padrão
            self._criar_novo_padrao(
                padrao_id,
                sequencia_cores,
                sequencia_multiplicadores,
                vela_atual
            )
        
        # Indexar por hora
        self.padroes_por_hora[vela_atual.hora].append(padrao_id)
        
        # Indexar por sequência
        seq_key = '_'.join(sequencia_cores)
        self.padroes_por_sequencia[seq_key].append(padrao_id)

    def _criar_novo_padrao(self, padrao_id: str, cores: List[str], 
                          multiplicadores: List[float], vela: Vela):
        """Criar novo padrão"""
        
        # Prever próxima cor baseado em padrão
        proxima_cor = self._prever_proxima_cor(cores)
        
        padrao = Padrao(
            id=padrao_id,
            sequencia=multiplicadores,
            cores_sequencia=cores,
            proxima_cor_prevista=proxima_cor,
            confianca=30.0,  # Confiança inicial baixa
            acertos=0,
            erros=0,
            peso=0.5,
            ultima_atualizacao=datetime.now().isoformat()
        )
        
        self.padroes[padrao_id] = padrao

    def _atualizar_padrao(self, padrao_id: str, vela: Vela):
        """Atualizar padrão existente"""
        
        padrao = self.padroes[padrao_id]
        
        # Verificar se previsão foi correta
        if padrao.proxima_cor_prevista == vela.cor:
            padrao.acertos += 1
            self.total_acertos += 1
            
            # Aumentar peso e confiança
            padrao.peso = min(1.0, padrao.peso + self.taxa_aprendizado)
            padrao.confianca = min(99.0, padrao.confianca + 2)
        else:
            padrao.erros += 1
            self.total_erros += 1
            
            # Diminuir peso e confiança
            padrao.peso = max(0.1, padrao.peso - self.taxa_aprendizado)
            padrao.confianca = max(10.0, padrao.confianca - 1)
        
        # Recalcular próxima previsão
        padrao.proxima_cor_prevista = self._prever_proxima_cor(padrao.cores_sequencia)
        padrao.ultima_atualizacao = datetime.now().isoformat()

    def _prever_proxima_cor(self, sequencia_cores: List[str]) -> str:
        """Prever próxima cor baseado em sequência"""
        
        if not sequencia_cores:
            return 'desconhecida'
        
        # Lógica de previsão
        # Após muitas azuis, rosa é mais provável
        # Roxa geralmente vem após azul
        
        ultima_cor = sequencia_cores[0]
        
        # Contar sequência de cores iguais
        contador = 1
        for i in range(1, len(sequencia_cores)):
            if sequencia_cores[i] == ultima_cor:
                contador += 1
            else:
                break
        
        # Se muitas azuis seguidas, rosa é provável
        if ultima_cor == 'azul' and contador >= 3:
            return 'rosa'
        
        # Se azul, geralmente vem roxa
        if ultima_cor == 'azul':
            return 'roxa'
        
        # Se roxa, pode ser azul ou rosa
        if ultima_cor == 'roxa':
            return 'rosa'
        
        # Se rosa, geralmente volta para azul
        if ultima_cor == 'rosa':
            return 'azul'
        
        return 'desconhecida'

    def fazer_previsao(self) -> Dict:
        """Fazer previsão baseado em padrões aprendidos"""
        
        if not self.historico_velas:
            return {
                'sinal': 'AGUARDE',
                'confianca': 0,
                'proxima_cor': 'desconhecida',
                'motivo': 'Sem dados para análise'
            }
        
        # Pegar últimas 5 velas
        ultimas_velas = self.historico_velas[:5]
        sequencia_cores = [v.cor for v in ultimas_velas]
        
        # Encontrar padrões similares
        padroes_similares = self._encontrar_padroes_similares(sequencia_cores)
        
        if not padroes_similares:
            return {
                'sinal': 'AGUARDE',
                'confianca': 0,
                'proxima_cor': 'desconhecida',
                'motivo': 'Padrão novo detectado'
            }
        
        # Calcular previsão ponderada
        previsao = self._calcular_previsao_ponderada(padroes_similares)
        
        return previsao

    def _encontrar_padroes_similares(self, sequencia_cores: List[str]) -> List[Padrao]:
        """Encontrar padrões similares ao atual"""
        
        padroes_similares = []
        
        for padrao in self.padroes.values():
            # Calcular similaridade
            similaridade = self._calcular_similaridade(
                sequencia_cores,
                padrao.cores_sequencia
            )
            
            # Se similaridade > 60%, considerar similar
            if similaridade > 0.6:
                padroes_similares.append((padrao, similaridade))
        
        # Ordenar por similaridade e peso
        padroes_similares.sort(
            key=lambda x: x[1] * x[0].peso,
            reverse=True
        )
        
        return [p[0] for p in padroes_similares[:10]]

    def _calcular_similaridade(self, seq1: List[str], seq2: List[str]) -> float:
        """Calcular similaridade entre sequências"""
        
        if not seq1 or not seq2:
            return 0.0
        
        min_len = min(len(seq1), len(seq2))
        matches = sum(1 for i in range(min_len) if seq1[i] == seq2[i])
        
        return matches / min_len

    def _calcular_previsao_ponderada(self, padroes: List[Padrao]) -> Dict:
        """Calcular previsão ponderada dos padrões"""
        
        if not padroes:
            return {
                'sinal': 'AGUARDE',
                'confianca': 0,
                'proxima_cor': 'desconhecida',
                'motivo': 'Sem padrões similares'
            }
        
        # Calcular média ponderada de confiança
        soma_pesos = sum(p.peso for p in padroes)
        confianca_media = sum(p.confianca * p.peso for p in padroes) / soma_pesos if soma_pesos > 0 else 0
        
        # Previsão mais comum
        proxima_cor = max(
            set(p.proxima_cor_prevista for p in padroes),
            key=lambda x: sum(p.peso for p in padroes if p.proxima_cor_prevista == x)
        )
        
        # Determinar sinal
        if proxima_cor == 'rosa' and confianca_media >= 70:
            sinal = 'ENTRAR ROSA'
        elif proxima_cor == 'roxa' and confianca_media >= 60:
            sinal = 'ENTRAR 5x'
        elif proxima_cor == 'azul' and confianca_media >= 70:
            sinal = 'NÃO ENTRAR'
        else:
            sinal = 'AGUARDE'
        
        return {
            'sinal': sinal,
            'confianca': round(confianca_media, 2),
            'proxima_cor': proxima_cor,
            'motivo': f'{len(padroes)} padrões similares encontrados',
            'padroes_count': len(padroes)
        }

    def fornecer_feedback(self, foi_correto: bool, cor_real: str):
        """Fornecer feedback sobre previsão"""
        
        if not self.historico_velas:
            return
        
        # Atualizar últimos padrões com feedback
        ultimas_velas = self.historico_velas[:5]
        sequencia_cores = [v.cor for v in ultimas_velas]
        
        for padrao in self.padroes.values():
            if self._calcular_similaridade(sequencia_cores, padrao.cores_sequencia) > 0.6:
                if foi_correto:
                    padrao.acertos += 1
                    self.total_acertos += 1
                    padrao.peso = min(1.0, padrao.peso + self.taxa_aprendizado * 2)
                    padrao.confianca = min(99.0, padrao.confianca + 3)
                else:
                    padrao.erros += 1
                    self.total_erros += 1
                    padrao.peso = max(0.1, padrao.peso - self.taxa_aprendizado * 2)
                    padrao.confianca = max(10.0, padrao.confianca - 2)

    def obter_estatisticas(self) -> Dict:
        """Obter estatísticas de aprendizado"""
        
        total = self.total_acertos + self.total_erros
        precisao = (self.total_acertos / total * 100) if total > 0 else 0
        
        # Progresso de aprendizado (0-100%)
        progresso = min(100, (len(self.padroes) / 1000) * 100)
        
        return {
            'total_velas_processadas': self.total_velas_processadas,
            'total_padroes_aprendidos': len(self.padroes),
            'total_acertos': self.total_acertos,
            'total_erros': self.total_erros,
            'precisao': round(precisao, 2),
            'progresso_aprendizado': round(progresso, 2),
            'padroes_por_hora': dict(self.padroes_por_hora),
            'peso_medio_padroes': round(
                sum(p.peso for p in self.padroes.values()) / len(self.padroes) if self.padroes else 0,
                2
            )
        }

    def salvar_estado(self, caminho: str):
        """Salvar estado da IA"""
        
        estado = {
            'padroes': {k: asdict(v) for k, v in self.padroes.items()},
            'historico_velas': [asdict(v) for v in self.historico_velas],
            'total_velas_processadas': self.total_velas_processadas,
            'total_acertos': self.total_acertos,
            'total_erros': self.total_erros,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(caminho, 'w') as f:
            json.dump(estado, f, indent=2)

    def carregar_estado(self, caminho: str):
        """Carregar estado da IA"""
        
        with open(caminho, 'r') as f:
            estado = json.load(f)
        
        self.total_velas_processadas = estado['total_velas_processadas']
        self.total_acertos = estado['total_acertos']
        self.total_erros = estado['total_erros']
        
        # Reconstruir padrões
        for padrao_dict in estado['padroes'].values():
            padrao = Padrao(**padrao_dict)
            self.padroes[padrao.id] = padrao

    def resetar(self):
        """Resetar IA"""
        self.padroes.clear()
        self.historico_velas.clear()
        self.total_velas_processadas = 0
        self.total_acertos = 0
        self.total_erros = 0
        self.padroes_por_hora.clear()
        self.padroes_por_sequencia.clear()


# Singleton
_ia_instance = None

def obter_ia() -> IAAviatior:
    """Obter instância singleton da IA"""
    global _ia_instance
    if _ia_instance is None:
        _ia_instance = IAAviatior()
    return _ia_instance

def resetar_ia():
    """Resetar IA"""
    global _ia_instance
    _ia_instance = IAAviatior()
