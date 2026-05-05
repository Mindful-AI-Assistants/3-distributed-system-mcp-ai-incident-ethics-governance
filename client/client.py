#!/usr/bin/env python3
"""
MCP Smart Incident Analyzer - Cliente
Cliente MCP que envia incidentes para análise via JSON-RPC 2.0
"""

import json
import asyncio
import logging
from typing import Dict, Any, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MCP-Client')


class MCPClient:
    """Cliente MCP que se conecta ao servidor"""
    
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.connected = False
        self.request_id_counter = 0
    
    async def connect(self):
        """Conecta ao servidor MCP"""
        try:
            self.reader, self.writer = await asyncio.open_connection(
                self.host, 
                self.port
            )
            self.connected = True
            logger.info(f"Conectado ao servidor {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Erro ao conectar ao servidor: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do servidor"""
        if self.writer:
            self.writer.close()
            self.connected = False
            logger.info("Desconectado do servidor")
    
    def generate_request_id(self) -> str:
        """Gera um ID único para a requisição"""
        self.request_id_counter += 1
        return f"req-{self.request_id_counter:03d}"
    
    async def send_request(self, method: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Envia uma requisição JSON-RPC 2.0 para o servidor"""
        
        if not self.connected:
            logger.error("Cliente não está conectado ao servidor")
            return None
        
        # Monta a requisição JSON-RPC 2.0
        request = {
            'jsonrpc': '2.0',
            'id': self.generate_request_id(),
            'method': method,
            'params': params
        }
        
        try:
            # Envia a requisição
            request_data = json.dumps(request) + '\n'
            self.writer.write(request_data.encode())
            await self.writer.drain()
            
            logger.info(f"Requisição enviada: {method} (ID: {request['id']})")
            
            # Aguarda a resposta
            response_data = await self.reader.readline()
            
            if not response_data:
                logger.error("Servidor encerrou a conexão")
                return None
            
            # Decodifica a resposta
            response = json.loads(response_data.decode())
            logger.info(f"Resposta recebida (ID: {response.get('id')})")
            
            return response
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar resposta: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao enviar requisição: {e}")
            return None
    
    async def ping(self) -> bool:
        """Testa a conectividade com o servidor"""
        response = await self.send_request('ping', {})
        
        if response and 'result' in response:
            status = response['result'].get('status')
            if status == 'pong':
                logger.info("✓ Ping bem-sucedido")
                return True
        
        logger.error("✗ Ping falhou")
        return False
    
    async def analyze_incident(self, 
                               incident_text: str,
                               severity: str = 'medium',
                               source: str = 'client',
                               context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Envia um incidente para análise"""
        
        params = {
            'incident_text': incident_text,
            'severity': severity,
            'source': source,
            'context': context or {}
        }
        
        response = await self.send_request('analyze_incident', params)
        
        if response and 'result' in response:
            return response['result']
        elif response and 'error' in response:
            logger.error(f"Erro do servidor: {response['error']}")
            return None
        
        return None
    
    async def get_stats(self) -> Optional[Dict[str, Any]]:
        """Obtém estatísticas do servidor"""
        response = await self.send_request('get_stats', {})
        
        if response and 'result' in response:
            return response['result']
        
        return None
    
    def print_result(self, result: Dict[str, Any]):
        """Exibe o resultado de forma formatada"""
        print("\n" + "=" * 60)
        print("RESULTADO DA ANÁLISE")
        print("=" * 60)
        print(f"ID do Incidente: {result.get('incident_id', 'N/A')}")
        print(f"Classificação: {result.get('classification', 'N/A')}")
        print(f"Prioridade: {result.get('priority', 'N/A')}")
        print(f"Status: {result.get('status', 'N/A')}")
        print(f"Analisado em: {result.get('analyzed_at', 'N/A')}")
        print(f"Fonte: {result.get('source', 'N/A')}")
        print()
        print("Recomendação:")
        print(f"  {result.get('recommendation', 'N/A')}")
        print()
        context_summary = result.get('context_summary', {})
        print(f"Ambiente: {context_summary.get('environment', 'N/A')}")
        print(f"Região: {context_summary.get('region', 'N/A')}")
        print("=" * 60)


async def run_examples(client: MCPClient):
    """Executa exemplos de uso"""
    
    print("\n" + "=" * 60)
    print("EXEMPLOS DE USO")
    print("=" * 60)
    
    # Exemplo 1: Incidente de segurança crítico
    print("\n[1] Analisando incidente de segurança crítico...")
    result1 = await client.analyze_incident(
        incident_text="Múltiplas tentativas de acesso suspeito detectadas no sistema.",
        severity="high",
        source="auth-service",
        context={
            "environment": "production",
            "region": "sa-east-1"
        }
    )
    
    if result1:
        client.print_result(result1)
    
    await asyncio.sleep(1)
    
    # Exemplo 2: Incidente de performance
    print("\n[2] Analisando incidente de performance...")
    result2 = await client.analyze_incident(
        incident_text="Sistema apresentando latência elevada e timeout nas requisições.",
        severity="medium",
        source="api-gateway",
        context={
            "environment": "production",
            "region": "us-east-1"
        }
    )
    
    if result2:
        client.print_result(result2)
    
    await asyncio.sleep(1)
    
    # Exemplo 3: Erro de aplicação
    print("\n[3] Analisando erro de aplicação...")
    result3 = await client.analyze_incident(
        incident_text="Exception crítica detectada: NullPointerException no módulo de pagamento.",
        severity="critical",
        source="payment-service",
        context={
            "environment": "production",
            "region": "eu-west-1"
        }
    )
    
    if result3:
        client.print_result(result3)
    
    await asyncio.sleep(1)
    
    # Obter estatísticas
    print("\n[4] Obtendo estatísticas do servidor...")
    stats = await client.get_stats()
    
    if stats:
        print("\n" + "=" * 60)
        print("ESTATÍSTICAS DO SERVIDOR")
        print("=" * 60)
        print(f"Total de incidentes processados: {stats.get('total_incidents', 0)}")
        print(f"Status do servidor: {stats.get('server_status', 'unknown')}")
        print("=" * 60)


async def interactive_mode(client: MCPClient):
    """Modo interativo para enviar incidentes"""
    
    print("\n" + "=" * 60)
    print("MODO INTERATIVO")
    print("=" * 60)
    print("Digite 'sair' para encerrar")
    print()
    
    while True:
        try:
            # Solicita entrada do usuário
            print("\nDescreva o incidente:")
            incident_text = input("> ")
            
            if incident_text.lower() in ['sair', 'exit', 'quit']:
                break
            
            if not incident_text.strip():
                continue
            
            print("\nSeveridade (low/medium/high/critical) [medium]:")
            severity = input("> ").strip() or 'medium'
            
            print("\nFonte do incidente [user-input]:")
            source = input("> ").strip() or 'user-input'
            
            # Analisa o incidente
            result = await client.analyze_incident(
                incident_text=incident_text,
                severity=severity,
                source=source,
                context={
                    "environment": "interactive",
                    "region": "local"
                }
            )
            
            if result:
                client.print_result(result)
            else:
                print("\n✗ Falha ao analisar o incidente")
        
        except KeyboardInterrupt:
            print("\n\nEncerrando modo interativo...")
            break
        except Exception as e:
            logger.error(f"Erro no modo interativo: {e}")


async def main():
    """Função principal"""
    print("=" * 60)
    print("MCP Smart Incident Analyzer - Cliente")
    print("=" * 60)
    print()
    
    # Cria o cliente
    client = MCPClient(host='localhost', port=8000)
    
    # Conecta ao servidor
    print("Conectando ao servidor MCP...")
    if not await client.connect():
        print("✗ Falha ao conectar ao servidor")
        print("  Certifique-se de que o servidor está rodando")
        return
    
    print("✓ Conectado com sucesso")
    
    # Testa conectividade
    print("\nTestando conectividade...")
    if not await client.ping():
        print("✗ Falha no teste de conectividade")
        return
    
    print("✓ Servidor respondendo corretamente")
    
    try:
        # Menu principal
        while True:
            print("\n" + "=" * 60)
            print("MENU PRINCIPAL")
            print("=" * 60)
            print("1. Executar exemplos de uso")
            print("2. Modo interativo")
            print("3. Obter estatísticas")
            print("4. Teste de ping")
            print("5. Sair")
            print()
            
            choice = input("Escolha uma opção: ").strip()
            
            if choice == '1':
                await run_examples(client)
            elif choice == '2':
                await interactive_mode(client)
            elif choice == '3':
                stats = await client.get_stats()
                if stats:
                    print("\n" + "=" * 60)
                    print("ESTATÍSTICAS DO SERVIDOR")
                    print("=" * 60)
                    print(f"Total de incidentes: {stats.get('total_incidents', 0)}")
                    print(f"Status: {stats.get('server_status', 'unknown')}")
                    print("=" * 60)
            elif choice == '4':
                await client.ping()
            elif choice == '5':
                break
            else:
                print("Opção inválida")
    
    except KeyboardInterrupt:
        print("\n\nEncerrando cliente...")
    finally:
        client.disconnect()
        print("\nCliente encerrado")


if __name__ == '__main__':
    asyncio.run(main())
