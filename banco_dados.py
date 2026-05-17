"""
BANCO DE DADOS - Armazena padrões e histórico de aprendizado
Persiste dados para análise contínua
"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os


class BancoDadosAviator:
    """Banco de dados para armazenar padrões e histórico"""
    
    def __init__(self, caminho_db: str = "aviator_ia.db"):
        self.caminho_db = caminho_db
        self.conexao = None
        self._inicializar_db()
    
    def _inicializar_db(self):
        """Inicializar banco de dados"""
        
        self.conexao = sqlite3.connect(self.caminho_db)
        self.conexao.row_factory = sqlite3.Row
        cursor = self.conexao.cursor()
        
        # Tabela de velas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS velas (
                id TEXT PRIMARY KEY,
                multiplicador REAL,
                timestamp TEXT,
                data TEXT,
                cor TEXT,
                capturado_em TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de padrões
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS padroes (
                id TEXT PRIMARY KEY,
                sequencia_cores TEXT,
                proxima_cor_prevista TEXT,
                confianca REAL,
                acertos INTEGER,
                erros INTEGER,
                peso REAL,
                ultima_atualizacao TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de feedback
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                tipo TEXT,
                multiplicador REAL,
                cor_prevista TEXT,
                cor_real TEXT,
                foi_correto BOOLEAN,
                timestamp TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de estatísticas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estatisticas (
                id TEXT PRIMARY KEY,
                total_velas INTEGER,
                total_padroes INTEGER,
                total_acertos INTEGER,
                total_erros INTEGER,
                precisao REAL,
                progresso_aprendizado REAL,
                data TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conexao.commit()
    
    def adicionar_vela(self, vela: Dict) -> bool:
        """Adicionar vela ao banco de dados"""
        
        try:
            cursor = self.conexao.cursor()
            
            # Determinar cor
            mult = vela['multiplicador']
            if 1.0 <= mult <= 1.99:
                cor = 'azul'
            elif 2.0 <= mult <= 9.99:
                cor = 'roxa'
            elif mult >= 10.0:
                cor = 'rosa'
            else:
                cor = 'desconhecida'
            
            cursor.execute('''
                INSERT INTO velas (id, multiplicador, timestamp, data, cor, capturado_em)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                vela.get('id', f"vela_{datetime.now().timestamp()}"),
                mult,
                vela.get('timestamp', datetime.now().strftime("%H:%M:%S")),
                vela.get('data', datetime.now().strftime("%Y-%m-%d")),
                cor,
                vela.get('capturado_em', datetime.now().isoformat())
            ))
            
            self.conexao.commit()
            return True
        
        except Exception as e:
            print(f"Erro ao adicionar vela: {e}")
            return False
    
    def obter_ultimas_velas(self, quantidade: int = 50) -> List[Dict]:
        """Obter últimas N velas"""
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute('''
                SELECT * FROM velas
                ORDER BY criado_em DESC
                LIMIT ?
            ''', (quantidade,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        
        except Exception as e:
            print(f"Erro ao obter velas: {e}")
            return []
    
    def obter_velas_por_cor(self, cor: str) -> List[Dict]:
        """Obter velas por cor"""
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute('''
                SELECT * FROM velas
                WHERE cor = ?
                ORDER BY criado_em DESC
            ''', (cor,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        
        except Exception as e:
            print(f"Erro ao obter velas por cor: {e}")
            return []
    
    def obter_velas_por_hora(self, hora: str) -> List[Dict]:
        """Obter velas capturadas em uma hora específica"""
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute('''
                SELECT * FROM velas
                WHERE timestamp LIKE ?
                ORDER BY criado_em DESC
            ''', (f"{hora}:%",))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        
        except Exception as e:
            print(f"Erro ao obter velas por hora: {e}")
            return []
    
    def adicionar_padrao(self, padrao: Dict) -> bool:
        """Adicionar padrão ao banco de dados"""
        
        try:
            cursor = self.conexao.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO padroes 
                (id, sequencia_cores, proxima_cor_prevista, confianca, acertos, erros, peso, ultima_atualizacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                padrao['id'],
                json.dumps(padrao.get('cores_sequencia', [])),
                padrao.get('proxima_cor_prevista', 'desconhecida'),
                padrao.get('confianca', 0),
                padrao.get('acertos', 0),
                padrao.get('erros', 0),
                padrao.get('peso', 0.5),
                datetime.now().isoformat()
            ))
            
            self.conexao.commit()
            return True
        
        except Exception as e:
            print(f"Erro ao adicionar padrão: {e}")
            return False
    
    def obter_padroes(self, limite: int = 100) -> List[Dict]:
        """Obter padrões mais confiáveis"""
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute('''
                SELECT * FROM padroes
                ORDER BY confianca DESC, peso DESC
                LIMIT ?
            ''', (limite,))
            
            rows = cursor.fetchall()
            padroes = []
            
            for row in rows:
                padrao = dict(row)
                padrao['cores_sequencia'] = json.loads(padrao['sequencia_cores'])
                padroes.append(padrao)
            
            return padroes
        
        except Exception as e:
            print(f"Erro ao obter padrões: {e}")
            return []
    
    def adicionar_feedback(self, feedback: Dict) -> bool:
        """Adicionar feedback ao banco de dados"""
        
        try:
            cursor = self.conexao.cursor()
            
            cursor.execute('''
                INSERT INTO feedback 
                (id, tipo, multiplicador, cor_prevista, cor_real, foi_correto, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                feedback.get('id', f"feedback_{datetime.now().timestamp()}"),
                feedback.get('tipo', 'manual'),
                feedback.get('multiplicador', 0),
                feedback.get('cor_prevista', 'desconhecida'),
                feedback.get('cor_real', 'desconhecida'),
                feedback.get('foi_correto', False),
                datetime.now().isoformat()
            ))
            
            self.conexao.commit()
            return True
        
        except Exception as e:
            print(f"Erro ao adicionar feedback: {e}")
            return False
    
    def obter_feedback_recente(self, quantidade: int = 100) -> List[Dict]:
        """Obter feedback recente"""
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute('''
                SELECT * FROM feedback
                ORDER BY criado_em DESC
                LIMIT ?
            ''', (quantidade,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        
        except Exception as e:
            print(f"Erro ao obter feedback: {e}")
            return []
    
    def salvar_estatisticas(self, stats: Dict) -> bool:
        """Salvar estatísticas"""
        
        try:
            cursor = self.conexao.cursor()
            
            cursor.execute('''
                INSERT INTO estatisticas 
                (id, total_velas, total_padroes, total_acertos, total_erros, precisao, progresso_aprendizado, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                f"stats_{datetime.now().timestamp()}",
                stats.get('total_velas_processadas', 0),
                stats.get('total_padroes_aprendidos', 0),
                stats.get('total_acertos', 0),
                stats.get('total_erros', 0),
                stats.get('precisao', 0),
                stats.get('progresso_aprendizado', 0),
                datetime.now().strftime("%Y-%m-%d")
            ))
            
            self.conexao.commit()
            return True
        
        except Exception as e:
            print(f"Erro ao salvar estatísticas: {e}")
            return False
    
    def obter_estatisticas_gerais(self) -> Dict:
        """Obter estatísticas gerais"""
        
        try:
            cursor = self.conexao.cursor()
            
            # Total de velas
            cursor.execute('SELECT COUNT(*) as total FROM velas')
            total_velas = cursor.fetchone()['total']
            
            # Total de padrões
            cursor.execute('SELECT COUNT(*) as total FROM padroes')
            total_padroes = cursor.fetchone()['total']
            
            # Total de feedback correto
            cursor.execute('SELECT COUNT(*) as total FROM feedback WHERE foi_correto = 1')
            total_acertos = cursor.fetchone()['total']
            
            # Total de feedback incorreto
            cursor.execute('SELECT COUNT(*) as total FROM feedback WHERE foi_correto = 0')
            total_erros = cursor.fetchone()['total']
            
            # Velas por cor
            cursor.execute('SELECT cor, COUNT(*) as total FROM velas GROUP BY cor')
            velas_por_cor = {row['cor']: row['total'] for row in cursor.fetchall()}
            
            # Precisão
            total_feedback = total_acertos + total_erros
            precisao = (total_acertos / total_feedback * 100) if total_feedback > 0 else 0
            
            # Progresso de aprendizado
            progresso = min(100, (total_padroes / 1000) * 100)
            
            return {
                'total_velas': total_velas,
                'total_padroes': total_padroes,
                'total_acertos': total_acertos,
                'total_erros': total_erros,
                'precisao': round(precisao, 2),
                'progresso_aprendizado': round(progresso, 2),
                'velas_por_cor': velas_por_cor
            }
        
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def limpar_banco(self):
        """Limpar banco de dados"""
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM velas')
            cursor.execute('DELETE FROM padroes')
            cursor.execute('DELETE FROM feedback')
            cursor.execute('DELETE FROM estatisticas')
            self.conexao.commit()
            return True
        
        except Exception as e:
            print(f"Erro ao limpar banco: {e}")
            return False
    
    def fechar(self):
        """Fechar conexão com banco de dados"""
        if self.conexao:
            self.conexao.close()
    
    def __del__(self):
        """Destrutor"""
        self.fechar()


# Singleton
_banco_instance = None

def obter_banco(caminho_db: str = "aviator_ia.db") -> BancoDadosAviator:
    """Obter instância singleton do banco de dados"""
    global _banco_instance
    if _banco_instance is None:
        _banco_instance = BancoDadosAviator(caminho_db)
    return _banco_instance

def resetar_banco():
    """Resetar banco de dados"""
    global _banco_instance
    if _banco_instance:
        _banco_instance.fechar()
    _banco_instance = None
