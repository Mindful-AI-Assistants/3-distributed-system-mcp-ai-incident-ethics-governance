#!/usr/bin/env python3
"""
MCP Smart Incident Analyzer - Testes de Conectividade
Testes automatizados para validar a comunicação cliente-servidor
"""

import asyncio
import json
import pytest
from typing import Dict, Any


class TestConnectivity:
    """Testes de conectividade do sistema MCP"""
    
    @pytest.fixture
    async def client_connection(self):
        """Fixture para criar conexão com o servidor"""
        try:
            reader, writer = await asyncio.open_connection('localhost', 8000)
            yield reader, writer
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            pytest.skip(f"Servidor não disponível: {e}")
    
    async def send_request(self, writer, reader, method: str, params: Dict[str, Any], request_id: str):
        """Helper para enviar requisição e receber resposta"""
        request = {
            'jsonrpc': '2.0',
            'id': request_id,
            'method': method,
            'params': params
        }
        
        # Envia requisição
        request_data = json.dumps(request) + '\n'
        writer.write(request_data.encode())
        await writer.drain()
        
        # Recebe resposta
        response_data = await reader.readline()
        return json.loads(response_data.decode())
    
    @pytest.mark.asyncio
    async def test_server_connection(self):
        """Teste 1: Verificar se o servidor aceita conexões"""
        try:
            reader, writer = await asyncio.open_connection('localhost', 8000)
            assert reader is not None
            assert writer is not None
            writer.close()
            await writer.wait_closed()
            print("✓ Teste 1 PASSOU: Servidor aceitou a conexão")
        except Exception as e:
            pytest.fail(f"✗ Teste 1 FALHOU: Não foi possível conectar ao servidor: {e}")
    
    @pytest.mark.asyncio
    async def test_ping_method(self, client_connection):
        """Teste 2: Verificar método ping"""
        reader, writer = client_connection
        
        response = await self.send_request(
            writer, reader,
            method='ping',
            params={},
            request_id='test-001'
        )
        
        # Validações
        assert response.get('jsonrpc') == '2.0', "Versão JSON-RPC inválida"
        assert response.get('id') == 'test-001', "ID da requisição não corresponde"
        assert 'result' in response, "Resposta não contém 'result'"
        assert response['result'].get('status') == 'pong', "Status do ping incorreto"
        
        print("✓ Teste 2 PASSOU: Método ping funciona corretamente")
    
    @pytest.mark.asyncio
    async def test_analyze_incident_method(self, client_connection):
        """Teste 3: Verificar método analyze_incident"""
        reader, writer = client_connection
        
        params = {
            'incident_text': 'Teste de incidente para validação',
            'severity': 'low',
            'source': 'test-suite',
            'context': {
                'environment': 'test',
                'region': 'local'
            }
        }
        
        response = await self.send_request(
            writer, reader,
            method='analyze_incident',
            params=params,
            request_id='test-002'
        )
        
        # Validações
        assert response.get('jsonrpc') == '2.0', "Versão JSON-RPC inválida"
        assert response.get('id') == 'test-002', "ID da requisição não corresponde"
        assert 'result' in response, "Resposta não contém 'result'"
        
        result = response['result']
        assert 'classification' in result, "Resultado não contém classificação"
        assert 'priority' in result, "Resultado não contém prioridade"
        assert 'recommendation' in result, "Resultado não contém recomendação"
        assert 'status' in result, "Resultado não contém status"
        assert result['status'] == 'processed', "Status do processamento incorreto"
        
        print("✓ Teste 3 PASSOU: Método analyze_incident funciona corretamente")
    
    @pytest.mark.asyncio
    async def test_get_stats_method(self, client_connection):
        """Teste 4: Verificar método get_stats"""
        reader, writer = client_connection
        
        response = await self.send_request(
            writer, reader,
            method='get_stats',
            params={},
            request_id='test-003'
        )
        
        # Validações
        assert response.get('jsonrpc') == '2.0', "Versão JSON-RPC inválida"
        assert 'result' in response, "Resposta não contém 'result'"
        
        result = response['result']
        assert 'total_incidents' in result, "Estatísticas não contêm total de incidentes"
        assert 'server_status' in result, "Estatísticas não contêm status do servidor"
        
        print("✓ Teste 4 PASSOU: Método get_stats funciona corretamente")
    
    @pytest.mark.asyncio
    async def test_invalid_method(self, client_connection):
        """Teste 5: Verificar tratamento de método inválido"""
        reader, writer = client_connection
        
        response = await self.send_request(
            writer, reader,
            method='invalid_method',
            params={},
            request_id='test-004'
        )
        
        # Validações
        assert response.get('jsonrpc') == '2.0', "Versão JSON-RPC inválida"
        assert 'error' in response, "Resposta não contém 'error'"
        assert response['error']['code'] == -32601, "Código de erro incorreto"
        
        print("✓ Teste 5 PASSOU: Método inválido tratado corretamente")
    
    @pytest.mark.asyncio
    async def test_multiple_requests(self, client_connection):
        """Teste 6: Verificar processamento de múltiplas requisições"""
        reader, writer = client_connection
        
        # Envia 3 requisições seguidas
        for i in range(3):
            response = await self.send_request(
                writer, reader,
                method='ping',
                params={},
                request_id=f'test-multi-{i}'
            )
            
            assert response.get('id') == f'test-multi-{i}', f"ID incorreto na requisição {i}"
            assert 'result' in response, f"Resultado ausente na requisição {i}"
        
        print("✓ Teste 6 PASSOU: Múltiplas requisições processadas corretamente")


async def run_manual_tests():
    """Executa testes manuais sem pytest"""
    print("=" * 60)
    print("TESTES DE CONECTIVIDADE - Execução Manual")
    print("=" * 60)
    print()
    
    test = TestConnectivity()
    
    try:
        # Teste 1: Conexão
        print("[1/6] Testando conexão com o servidor...")
        await test.test_server_connection()
        
        # Prepara conexão para os próximos testes
        reader, writer = await asyncio.open_connection('localhost', 8000)
        
        # Teste 2: Ping
        print("\n[2/6] Testando método ping...")
        await test.test_ping_method((reader, writer))
        
        # Teste 3: Analyze Incident
        print("\n[3/6] Testando método analyze_incident...")
        await test.test_analyze_incident_method((reader, writer))
        
        # Teste 4: Get Stats
        print("\n[4/6] Testando método get_stats...")
        await test.test_get_stats_method((reader, writer))
        
        # Teste 5: Método Inválido
        print("\n[5/6] Testando método inválido...")
        await test.test_invalid_method((reader, writer))
        
        # Teste 6: Múltiplas Requisições
        print("\n[6/6] Testando múltiplas requisições...")
        await test.test_multiple_requests((reader, writer))
        
        writer.close()
        await writer.wait_closed()
        
        print("\n" + "=" * 60)
        print("TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        print("\nCertifique-se de que o servidor está rodando:")
        print("  python server/server.py")


if __name__ == '__main__':
    print("Iniciando testes de conectividade...")
    print("(Certifique-se de que o servidor está rodando)")
    print()
    
    asyncio.run(run_manual_tests())
