#!/usr/bin/env python3
"""
MCP Smart Incident Analyzer - Servidor
Servidor MCP que processa e analisa incidentes usando JSON-RPC 2.0
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MCP-Server')


class IncidentAnalyzer:
    """Classe responsável pela análise de incidentes"""
    
    def __init__(self):
        self.incident_count = 0
        self.categories = {
            'security': ['acesso', 'suspeito', 'invasão', 'malware', 'phishing'],
            'performance': ['lento', 'timeout', 'latência', 'indisponível'],
            'error': ['erro', 'falha', 'exception', 'crash'],
            'warning': ['aviso', 'alerta', 'atenção']
        }
    
    def classify_incident(self, incident_text: str) -> str:
        """Classifica o incidente baseado no texto"""
        incident_lower = incident_text.lower()
        
        for category, keywords in self.categories.items():
            if any(keyword in incident_lower for keyword in keywords):
                return f"{category}_incident"
        
        return "general_incident"
    
    def determine_priority(self, severity: str) -> str:
        """Determina a prioridade baseada na severidade"""
        severity_map = {
            'critical': 'critical',
            'high': 'high',
            'medium': 'medium',
            'low': 'low'
        }
        return severity_map.get(severity.lower(), 'medium')
    
    def generate_recommendation(self, classification: str, severity: str) -> str:
        """Gera recomendação baseada na classificação e severidade"""
        recommendations = {
            'security_incident': {
                'critical': 'Isolamento imediato do sistema e acionamento da equipe de segurança.',
                'high': 'Iniciar investigação e isolar origem do evento.',
                'medium': 'Monitorar atividade e revisar logs de acesso.',
                'low': 'Registrar ocorrência para análise posterior.'
            },
            'performance_incident': {
                'critical': 'Escalar recursos e iniciar análise de bottlenecks.',
                'high': 'Verificar métricas de sistema e aplicação.',
                'medium': 'Monitorar tendências de performance.',
                'low': 'Documentar para revisão futura.'
            },
            'error_incident': {
                'critical': 'Rollback imediato e análise de stack trace.',
                'high': 'Investigar logs de erro e corrigir bug.',
                'medium': 'Analisar frequência e impacto do erro.',
                'low': 'Adicionar à fila de correções.'
            }
        }
        
        category_recs = recommendations.get(classification, {})
        return category_recs.get(severity, 'Analisar contexto e tomar ação apropriada.')
    
    def analyze(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa e analisa um incidente"""
        self.incident_count += 1
        
        incident_text = incident_data.get('incident_text', '')
        severity = incident_data.get('severity', 'medium')
        source = incident_data.get('source', 'unknown')
        context = incident_data.get('context', {})
        
        # Análise
        classification = self.classify_incident(incident_text)
        priority = self.determine_priority(severity)
        recommendation = self.generate_recommendation(classification, severity)
        
        # Resultado da análise
        result = {
            'classification': classification,
            'priority': priority,
            'recommendation': recommendation,
            'status': 'processed',
            'analyzed_at': datetime.now().isoformat(),
            'incident_id': f"INC-{self.incident_count:04d}",
            'source': source,
            'context_summary': {
                'environment': context.get('environment', 'unknown'),
                'region': context.get('region', 'unknown')
            }
        }
        
        logger.info(f"Incidente processado: {result['incident_id']} - {classification}")
        return result


class MCPServer:
    """Servidor MCP que implementa JSON-RPC 2.0"""
    
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port
        self.analyzer = IncidentAnalyzer()
        self.running = False
    
    def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma requisição JSON-RPC 2.0"""
        
        # Validação básica da estrutura JSON-RPC
        if 'jsonrpc' not in request_data or request_data['jsonrpc'] != '2.0':
            return self.error_response(
                -32600, 
                "Invalid Request", 
                request_data.get('id')
            )
        
        if 'method' not in request_data:
            return self.error_response(
                -32600, 
                "Missing method field", 
                request_data.get('id')
            )
        
        method = request_data['method']
        params = request_data.get('params', {})
        request_id = request_data.get('id')
        
        # Roteamento de métodos
        if method == 'analyze_incident':
            try:
                result = self.analyzer.analyze(params)
                return self.success_response(result, request_id)
            except Exception as e:
                logger.error(f"Erro ao processar incidente: {str(e)}")
                return self.error_response(
                    -32603, 
                    f"Internal error: {str(e)}", 
                    request_id
                )
        
        elif method == 'ping':
            return self.success_response({'status': 'pong'}, request_id)
        
        elif method == 'get_stats':
            stats = {
                'total_incidents': self.analyzer.incident_count,
                'server_status': 'running',
                'uptime': 'active'
            }
            return self.success_response(stats, request_id)
        
        else:
            return self.error_response(
                -32601, 
                f"Method not found: {method}", 
                request_id
            )
    
    def success_response(self, result: Any, request_id: Optional[str]) -> Dict[str, Any]:
        """Cria uma resposta de sucesso JSON-RPC 2.0"""
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': result
        }
    
    def error_response(self, code: int, message: str, request_id: Optional[str]) -> Dict[str, Any]:
        """Cria uma resposta de erro JSON-RPC 2.0"""
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': code,
                'message': message
            }
        }
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Gerencia a conexão com um cliente"""
        addr = writer.get_extra_info('peername')
        logger.info(f"Cliente conectado: {addr}")
        
        try:
            while True:
                # Lê a requisição
                data = await reader.readline()
                
                if not data:
                    break
                
                # Decodifica e processa
                try:
                    request = json.loads(data.decode())
                    logger.info(f"Requisição recebida: {request.get('method', 'unknown')}")
                    
                    # Processa a requisição
                    response = self.handle_request(request)
                    
                    # Envia a resposta
                    response_data = json.dumps(response) + '\n'
                    writer.write(response_data.encode())
                    await writer.drain()
                    
                    logger.info(f"Resposta enviada para {addr}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Erro ao decodificar JSON: {e}")
                    error_resp = self.error_response(-32700, "Parse error", None)
                    writer.write((json.dumps(error_resp) + '\n').encode())
                    await writer.drain()
                
        except Exception as e:
            logger.error(f"Erro na conexão com {addr}: {e}")
        finally:
            logger.info(f"Cliente desconectado: {addr}")
            writer.close()
            await writer.wait_closed()
    
    async def start(self):
        """Inicia o servidor"""
        server = await asyncio.start_server(
            self.handle_client, 
            self.host, 
            self.port
        )
        
        addr = server.sockets[0].getsockname()
        logger.info(f"Servidor MCP iniciado em {addr[0]}:{addr[1]}")
        logger.info("Aguardando conexões...")
        
        self.running = True
        
        async with server:
            await server.serve_forever()


async def main():
    """Função principal"""
    print("=" * 60)
    print("MCP Smart Incident Analyzer - Servidor")
    print("=" * 60)
    print()
    
    server = MCPServer(host='localhost', port=8000)
    
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("\nServidor encerrado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")


if __name__ == '__main__':
    asyncio.run(main())
