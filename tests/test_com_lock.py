"""
Script para testar o sistema COM lock (Entrega 3)
Deve demonstrar que apenas 1 agendamento é criado
"""

import requests
import threading
from datetime import datetime, timedelta, timezone
import json
import time

BASE_URL = 'http://localhost:5000/api/v1'
COORDENADOR_URL = 'http://localhost:3000'

def verificar_servicos():
    """Verifica se ambos os serviços estão rodando"""
    print("Verificando serviços...")
    
    try:
        resp1 = requests.get(f'{BASE_URL}/time', timeout=2)
        print("✓ Serviço de Agendamento: OK")
    except:
        print("✗ Serviço de Agendamento: OFFLINE")
        return False
    
    try:
        resp2 = requests.get(f'{COORDENADOR_URL}/health', timeout=2)
        print("✓ Serviço Coordenador: OK")
    except:
        print("✗ Serviço Coordenador: OFFLINE")
        return False
    
    return True

def criar_cientista_teste():
    """Cria um cientista para teste"""
    data = {
        'nome': 'Grace Hopper',
        'email': f'grace.hopper.teste.{datetime.now().timestamp()}@test.com',
        'instituicao': 'Yale University',
        'pais': 'Estados Unidos',
        'especialidade': 'Astrofísica Computacional'
    }
    
    response = requests.post(f'{BASE_URL}/cientistas', json=data)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"Erro ao criar cientista: {response.text}")
        return None

def tentar_agendamento(cientista_id, horario_inicio, horario_fim, thread_id):
    """Tenta criar um agendamento"""
    data = {
        'cientista_id': cientista_id,
        'horario_inicio_utc': horario_inicio,
        'horario_fim_utc': horario_fim,
        'objeto_celeste': f'Teste Lock Thread {thread_id}',
        'observacoes': f'Requisição da thread {thread_id}'
    }
    
    try:
        inicio = time.time()
        response = requests.post(f'{BASE_URL}/agendamentos', json=data)
        duracao = time.time() - inicio
        
        status_emoji = "✓" if response.status_code == 201 else "✗"
        print(f"{status_emoji} [Thread {thread_id:02d}] Status: {response.status_code} - Tempo: {duracao:.3f}s")
        
        if response.status_code != 201:
            erro = response.json().get('error', 'Desconhecido')
            print(f"   └─ Motivo: {erro}")
        
        return response.status_code, response.json(), duracao
    except Exception as e:
        print(f"✗ [Thread {thread_id:02d}] Erro: {str(e)}")
        return None, None, 0

def teste_com_lock(num_threads=10):
    """
    Executa teste de concorrência COM LOCK
    """
    print("="*80)
    print("TESTE COM LOCK - ENTREGA 3")
    print("="*80)
    print()
    
    # Verificar serviços
    if not verificar_servicos():
        print("\n⚠ Um ou mais serviços estão offline. Abortando teste.")
        print("\nCertifique-se de que estão rodando:")
        print("   Terminal 1: cd servico-agendamento && python run.py")
        print("   Terminal 2: cd servico-coordenador && npm start")
        return
    
    print(f"\nConfigurando teste com {num_threads} threads simultâneas...\n")
    
    # Criar cientista
    print("1. Criando cientista de teste...")
    cientista_id = criar_cientista_teste()
    if not cientista_id:
        print("Falha ao criar cientista. Abortando teste.")
        return
    print(f"   Cientista criado: ID {cientista_id}\n")
    
    # Definir horário
    agora = datetime.now(timezone.utc)
    inicio = agora + timedelta(hours=25)
    inicio = inicio.replace(minute=(inicio.minute // 5) * 5, second=0, microsecond=0)
    fim = inicio + timedelta(minutes=30)
    
    # Formatar sem info de timezone e adicionar Z para UTC
    horario_inicio_str = inicio.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
    horario_fim_str = fim.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
    
    print(f"2. Horário alvo: {horario_inicio_str} - {horario_fim_str}\n")
    print(f"3. Disparando {num_threads} requisições simultâneas...\n")
    print("-" * 80)
    
    # Criar threads
    threads = []
    resultados = []
    
    for i in range(num_threads):
        def wrapper(tid=i):
            status, response, duracao = tentar_agendamento(
                cientista_id, 
                horario_inicio_str, 
                horario_fim_str, 
                tid
            )
            resultados.append((tid, status, response, duracao))
        
        thread = threading.Thread(target=wrapper)
        threads.append(thread)
    
    # Disparar todas ao mesmo tempo
    inicio_teste = time.time()
    for thread in threads:
        thread.start()
    
    # Aguardar conclusão
    for thread in threads:
        thread.join()
    
    duracao_total = time.time() - inicio_teste
    
    print("-" * 80)
    print("\n" + "="*80)
    print("RESULTADOS")
    print("="*80 + "\n")
    
    # Analisar resultados
    sucessos = [r for r in resultados if r[1] == 201]
    conflitos_409 = [r for r in resultados if r[1] == 409]
    outros_erros = [r for r in resultados if r[1] not in [201, 409] and r[1] is not None]
    falhas_rede = [r for r in resultados if r[1] is None]
    
    print(f"✓ Sucessos (201):         {len(sucessos)}")
    print(f"✗ Recursos ocupados (409): {len(conflitos_409)}")
    print(f"⚠ Outros erros:           {len(outros_erros)}")
    print(f"⚠ Falhas de rede:         {len(falhas_rede)}")
    print(f"\n⏱ Tempo total: {duracao_total:.3f}s")
    
    if resultados:
        tempos = [r[3] for r in resultados if r[3] > 0]
        if tempos:
            print(f"⏱ Tempo médio por requisição: {sum(tempos)/len(tempos):.3f}s")
            print(f"⏱ Tempo mínimo: {min(tempos):.3f}s")
            print(f"⏱ Tempo máximo: {max(tempos):.3f}s")
    
    print("\n" + "-"*80)
    
    if len(sucessos) == 1:
        print("\n🎉 SUCESSO! Apenas 1 agendamento criado (exclusão mútua funcionando!)")
        tid, status, response, duracao = sucessos[0]
        print(f"\nAgendamento vencedor:")
        print(f"   Thread: {tid}")
        print(f"   ID: {response['id']}")
        print(f"   Tempo: {duracao:.3f}s")
    elif len(sucessos) > 1:
        print(f"\n🚨 FALHA! {len(sucessos)} agendamentos criados (lock não está funcionando!)")
        print("\nAgendamentos duplicados:")
        for tid, status, response, duracao in sucessos:
            print(f"   - Thread {tid}: Agendamento ID {response['id']}")
    else:
        print("\n⚠ PROBLEMA! Nenhum agendamento criado")
    
    print("\n" + "="*80)
    print("VERIFICAÇÃO NO BANCO DE DADOS")
    print("="*80 + "\n")
    
    # Aguardar um pouco para garantir consistência
    time.sleep(0.5)
    
    # Consultar agendamentos
    response = requests.get(
        f'{BASE_URL}/agendamentos',
        params={
            'cientista_id': cientista_id,
            'status': 'AGENDADO'
        }
    )
    
    if response.status_code == 200:
        agendamentos = response.json()['agendamentos']
        print(f"Agendamentos no banco: {len(agendamentos)}")
        
        if len(agendamentos) == 1:
            print("\n✓ Banco de dados consistente (1 agendamento)")
        elif len(agendamentos) > 1:
            print(f"\n🚨 Inconsistência no banco ({len(agendamentos)} agendamentos)!")
            print("\nAgendamentos encontrados:")
            for ag in agendamentos:
                print(f"   - ID {ag['id']}: {ag['horario_inicio_utc']}")
    
    print("\n" + "="*80)
    print("ANÁLISE DOS LOGS")
    print("="*80)
    print("\nPara analisar os logs:")
    print("\n1. Serviço de Agendamento (Python):")
    print("   cat servico-agendamento/logs/app.log | grep -E '(Tentando adquirir lock|Lock adquirido|Falha ao adquirir)'")
    print("\n2. Serviço Coordenador (Node.js):")
    print("   (Ver saída do console onde está rodando)")
    print("\n3. Logs de Auditoria:")
    print("   cat servico-agendamento/logs/audit.log | jq '.event_type'")
    print("\n4. Docker Logs (se usando containers):")
    print("   docker-compose logs -f")
    print("="*80 + "\n")

if __name__ == '__main__':
    import sys
    
    num_threads = 10
    if len(sys.argv) > 1:
        try:
            num_threads = int(sys.argv[1])
        except ValueError:
            print("Uso: python test_com_lock.py [num_threads]")
            sys.exit(1)
    
    teste_com_lock(num_threads)
