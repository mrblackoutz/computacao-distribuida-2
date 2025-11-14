"""
Script para testar condição de corrida
Dispara múltiplas requisições simultâneas para o mesmo horário
ENTREGA 2: Demonstra o PROBLEMA (múltiplos agendamentos são criados)
"""

import requests
import threading
from datetime import datetime, timedelta
import json
import time

BASE_URL = 'http://localhost:5000/api/v1'

def criar_cientista_teste():
    """Cria um cientista para teste"""
    timestamp = datetime.now().timestamp()
    data = {
        'nome': 'Alan Turing',
        'email': f'alan.turing.teste.{timestamp}@test.com',
        'instituicao': 'University of Manchester',
        'pais': 'Reino Unido',
        'especialidade': 'Computação Quântica'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/cientistas', json=data, timeout=10)
        if response.status_code == 201:
            return response.json()['id']
        else:
            print(f"Erro ao criar cientista: {response.text}")
            return None
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return None

def tentar_agendamento(cientista_id, horario_inicio, horario_fim, thread_id):
    """Tenta criar um agendamento"""
    data = {
        'cientista_id': cientista_id,
        'horario_inicio_utc': horario_inicio,
        'horario_fim_utc': horario_fim,
        'objeto_celeste': f'Teste Concorrência Thread {thread_id}',
        'observacoes': f'Requisição da thread {thread_id}'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/agendamentos', json=data, timeout=10)
        erro = response.json().get('error', 'Sucesso') if response.status_code != 201 else 'Sucesso'
        print(f"[Thread {thread_id:02d}] Status: {response.status_code} - {erro}")
        return response.status_code, response.json()
    except Exception as e:
        print(f"[Thread {thread_id:02d}] Erro: {str(e)}")
        return None, None

def teste_concorrencia(num_threads=10):
    """Executa teste de concorrência"""
    print("="*80)
    print("TESTE DE CONDIÇÃO DE CORRIDA - ENTREGA 2 (SEM LOCK)")
    print("="*80)
    print(f"\nConfigurando teste com {num_threads} threads simultâneas...\n")
    
    # Criar cientista
    print("1. Criando cientista de teste...")
    cientista_id = criar_cientista_teste()
    if not cientista_id:
        print("Falha ao criar cientista. Abortando teste.")
        return
    print(f"   Cientista criado: ID {cientista_id}\n")
    
    # Definir horário no futuro (25 horas a partir de agora)
    agora = datetime.now(datetime.timezone.utc)
    inicio = agora + timedelta(hours=25)
    # Arredondar para múltiplo de 5 minutos
    inicio = inicio.replace(minute=(inicio.minute // 5) * 5, second=0, microsecond=0)
    fim = inicio + timedelta(minutes=30)
    
    horario_inicio_str = inicio.isoformat() + 'Z'
    horario_fim_str = fim.isoformat() + 'Z'
    
    print(f"2. Horário alvo: {horario_inicio_str} - {horario_fim_str}\n")
    print(f"3. Disparando {num_threads} requisições simultâneas...\n")
    
    # Criar threads
    threads = []
    resultados = []
    
    for i in range(num_threads):
        def wrapper(tid=i):
            status, response = tentar_agendamento(
                cientista_id, 
                horario_inicio_str, 
                horario_fim_str, 
                tid
            )
            resultados.append((tid, status, response))
        
        thread = threading.Thread(target=wrapper)
        threads.append(thread)
    
    # Disparar todas ao mesmo tempo
    for thread in threads:
        thread.start()
    
    # Aguardar conclusão
    for thread in threads:
        thread.join()
    
    print("\n" + "="*80)
    print("RESULTADOS")
    print("="*80 + "\n")
    
    # Analisar resultados
    sucessos = [r for r in resultados if r[1] == 201]
    conflitos = [r for r in resultados if r[1] == 409]
    erros = [r for r in resultados if r[1] not in [201, 409]]
    
    print(f"✓ Sucessos (201):  {len(sucessos)}")
    print(f"✗ Conflitos (409): {len(conflitos)}")
    print(f"⚠ Outros erros:    {len(erros)}")
    
    if len(sucessos) > 1:
        print(f"\n🚨 CONDIÇÃO DE CORRIDA DETECTADA! {len(sucessos)} agendamentos criados para o mesmo horário!")
        print("\nIDs dos agendamentos duplicados:")
        for tid, status, response in sucessos:
            if response and 'id' in response:
                print(f"   - Thread {tid:02d}: Agendamento ID {response['id']}")
    elif len(sucessos) == 1:
        print("\n✓ Apenas 1 agendamento criado (comportamento esperado COM lock)")
    else:
        print("\n⚠ Nenhum agendamento criado (investigar)")
    
    print("\n" + "="*80)
    print("VERIFICAÇÃO NO BANCO DE DADOS")
    print("="*80 + "\n")
    
    # Consultar agendamentos criados
    time.sleep(0.5)  # Aguardar para garantir consistência
    response = requests.get(
        f'{BASE_URL}/agendamentos',
        params={
            'cientista_id': cientista_id,
            'status': 'AGENDADO'
        }
    )
    
    if response.status_code == 200:
        agendamentos = response.json()['agendamentos']
        print(f"Agendamentos encontrados no banco: {len(agendamentos)}")
        
        # Agrupar por horário
        horarios = {}
        for ag in agendamentos:
            key = (ag['horario_inicio_utc'], ag['horario_fim_utc'])
            if key not in horarios:
                horarios[key] = []
            horarios[key].append(ag['id'])
        
        print("\nAgendamentos por horário:")
        for (inicio, fim), ids in horarios.items():
            print(f"   {inicio} - {fim}: {len(ids)} agendamento(s) - IDs: {ids}")
            if len(ids) > 1:
                print(f"      🚨 CONFLITO DETECTADO!")
    
    print("\n" + "="*80)
    print("ANÁLISE DOS LOGS")
    print("="*80)
    print("\nPara analisar os logs:")
    print("   1. Examine 'servico-agendamento/logs/app.log' para ver os logs entrelaçados")
    print("   2. Examine 'servico-agendamento/logs/audit.log' para ver os eventos de auditoria")
    print("   3. Procure por múltiplos eventos 'AGENDAMENTO_CRIADO' para o mesmo horário")
    print("\nComandos úteis (Linux/Mac):")
    print("   cat servico-agendamento/logs/app.log | grep 'Iniciando verificação de conflito'")
    print("   cat servico-agendamento/logs/audit.log | grep 'AGENDAMENTO_CRIADO'")
    print("\nComandos úteis (Windows/PowerShell):")
    print("   Select-String -Path servico-agendamento\\logs\\app.log -Pattern 'Iniciando verificação'")
    print("   Select-String -Path servico-agendamento\\logs\\audit.log -Pattern 'AGENDAMENTO_CRIADO'")
    print("="*80 + "\n")

if __name__ == '__main__':
    import sys
    
    num_threads = 10
    if len(sys.argv) > 1:
        try:
            num_threads = int(sys.argv[1])
        except ValueError:
            print("Uso: python test_concorrencia.py [num_threads]")
            sys.exit(1)
    
    teste_concorrencia(num_threads)
