# Modelagem de Dados - SCTEC

## Visão Geral

Este documento define as entidades de dados do Sistema de Controle de Telescópio Espacial Compartilhado (SCTEC), seus atributos, relacionamentos e regras de negócio.

---

## 1. Entidade: Cientista

Representa um pesquisador autorizado a usar o telescópio espacial.

### Atributos

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id` | INTEGER | PK, AUTO_INCREMENT | Identificador único do cientista |
| `nome` | STRING(200) | NOT NULL | Nome completo do cientista |
| `email` | STRING(200) | UNIQUE, NOT NULL | Email institucional |
| `instituicao` | STRING(300) | NOT NULL | Universidade ou instituto de pesquisa |
| `pais` | STRING(100) | NOT NULL | País de origem |
| `especialidade` | STRING(200) | NULLABLE | Área de especialização |
| `data_cadastro` | DATETIME | NOT NULL, DEFAULT=NOW | Data e hora do cadastro |
| `ativo` | BOOLEAN | NOT NULL, DEFAULT=TRUE | Status do cientista |

### Regras de Negócio

1. **Email único**: Cada cientista deve ter um email único no sistema
2. **Email válido**: Deve conter '@' e pelo menos um '.'
3. **Nome mínimo**: Nome deve ter no mínimo 3 caracteres
4. **Cientista inativo**: Cientistas com `ativo=FALSE` não podem criar novos agendamentos
5. **Soft delete**: Ao desativar um cientista, seus agendamentos anteriores permanecem no histórico

### Índices

```sql
CREATE INDEX idx_cientistas_email ON cientistas(email);
CREATE INDEX idx_cientistas_ativo ON cientistas(ativo);
```

### Exemplo de Registro

```json
{
  "id": 1,
  "nome": "Marie Curie",
  "email": "marie.curie@sorbonne.fr",
  "instituicao": "Universidade de Paris",
  "pais": "França",
  "especialidade": "Radioastronomia",
  "data_cadastro": "2025-11-09T10:30:00Z",
  "ativo": true
}
```

---

## 2. Entidade: Agendamento

Representa uma reserva de tempo de observação no telescópio.

### Atributos

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id` | INTEGER | PK, AUTO_INCREMENT | Identificador único do agendamento |
| `cientista_id` | INTEGER | FK -> Cientista.id, NOT NULL | Cientista responsável |
| `horario_inicio_utc` | DATETIME | NOT NULL | Início da observação (UTC) |
| `horario_fim_utc` | DATETIME | NOT NULL | Fim da observação (UTC) |
| `objeto_celeste` | STRING(300) | NOT NULL | Alvo da observação |
| `observacoes` | TEXT | NULLABLE | Detalhes da observação |
| `status` | ENUM | NOT NULL, DEFAULT='AGENDADO' | Status do agendamento |
| `data_criacao` | DATETIME | NOT NULL, DEFAULT=NOW | Data de criação do registro |
| `data_cancelamento` | DATETIME | NULLABLE | Data do cancelamento (se aplicável) |
| `motivo_cancelamento` | TEXT | NULLABLE | Justificativa do cancelamento |

### Valores de Status

- `AGENDADO`: Agendamento confirmado e aguardando execução
- `CANCELADO`: Agendamento cancelado pelo cientista ou sistema
- `CONCLUIDO`: Observação realizada com sucesso

### Regras de Negócio

1. **Horário válido**: `horario_fim_utc` deve ser posterior a `horario_inicio_utc`
2. **Duração mínima**: Mínimo de 5 minutos de observação
3. **Duração máxima**: Máximo de 2 horas (120 minutos) por agendamento
4. **Slots de tempo**: Horários devem ser múltiplos de 5 minutos (00, 05, 10, 15, etc.)
5. **Não sobrepor**: Não pode haver sobreposição de horários para agendamentos com status `AGENDADO`
6. **Agendamento futuro**: Não é possível agendar no passado
7. **Antecedência mínima**: Requer 24 horas de antecedência
8. **Limite por cientista**: Cada cientista pode ter no máximo 3 agendamentos ativos (status `AGENDADO`)
9. **Apenas agendados podem ser cancelados**: Só é possível cancelar agendamentos com status `AGENDADO`
10. **Cancelamento com motivo**: Ao cancelar, registrar data e motivo

### Índices

```sql
CREATE INDEX idx_agendamentos_horario_status ON agendamentos(horario_inicio_utc, horario_fim_utc, status);
CREATE INDEX idx_agendamentos_cientista ON agendamentos(cientista_id);
CREATE INDEX idx_agendamentos_status ON agendamentos(status);
```

### Constraints

```sql
ALTER TABLE agendamentos 
  ADD CONSTRAINT check_horarios 
  CHECK (horario_fim_utc > horario_inicio_utc);

ALTER TABLE agendamentos 
  ADD CONSTRAINT check_status 
  CHECK (status IN ('AGENDADO', 'CANCELADO', 'CONCLUIDO'));
```

### Exemplo de Registro

```json
{
  "id": 123,
  "cientista_id": 1,
  "horario_inicio_utc": "2025-12-01T03:00:00Z",
  "horario_fim_utc": "2025-12-01T03:30:00Z",
  "objeto_celeste": "NGC 1300 - Galáxia Espiral Barrada",
  "observacoes": "Estudo da estrutura espiral e formação estelar no núcleo",
  "status": "AGENDADO",
  "data_criacao": "2025-11-09T15:30:45Z",
  "data_cancelamento": null,
  "motivo_cancelamento": null
}
```

---

## 3. Relacionamentos

### Cientista ↔ Agendamento

- **Tipo**: Um para Muitos (1:N)
- **Descrição**: Um cientista pode ter múltiplos agendamentos
- **Chave Estrangeira**: `agendamentos.cientista_id` → `cientistas.id`
- **Cascade**: 
  - ON DELETE: RESTRICT (não permite deletar cientista com agendamentos)
  - ON UPDATE: CASCADE (atualiza referências se ID mudar)

### Diagrama ER (Textual)

```
┌─────────────────┐         1:N         ┌──────────────────┐
│   Cientistas    │◄────────────────────┤  Agendamentos    │
├─────────────────┤                     ├──────────────────┤
│ PK id           │                     │ PK id            │
│    nome         │                     │ FK cientista_id  │
│    email (UK)   │                     │    horario_inicio│
│    instituicao  │                     │    horario_fim   │
│    pais         │                     │    objeto_celeste│
│    especialidade│                     │    observacoes   │
│    data_cadastro│                     │    status        │
│    ativo        │                     │    data_criacao  │
└─────────────────┘                     │    data_cancel.. │
                                        │    motivo_cancel.│
                                        └──────────────────┘
```

---

## 4. Regras de Validação Detalhadas

### Validação de Horários

```python
# Pseudocódigo de validação

def validar_agendamento(dados):
    # 1. Converter para datetime
    inicio = parse_datetime(dados['horario_inicio_utc'])
    fim = parse_datetime(dados['horario_fim_utc'])
    
    # 2. Validar que fim > inicio
    if fim <= inicio:
        raise ValidationError("Horário de fim deve ser posterior ao início")
    
    # 3. Calcular duração
    duracao_minutos = (fim - inicio).total_minutes()
    
    # 4. Validar duração mínima e máxima
    if duracao_minutos < 5:
        raise ValidationError("Duração mínima: 5 minutos")
    if duracao_minutos > 120:
        raise ValidationError("Duração máxima: 120 minutos")
    
    # 5. Validar múltiplos de 5 minutos
    if inicio.minute % 5 != 0 or fim.minute % 5 != 0:
        raise ValidationError("Horários devem ser múltiplos de 5 minutos")
    
    # 6. Validar que não é no passado
    agora = datetime.utcnow()
    if inicio <= agora:
        raise ValidationError("Não é possível agendar no passado")
    
    # 7. Validar antecedência mínima
    antecedencia = inicio - agora
    if antecedencia < timedelta(hours=24):
        raise ValidationError("Antecedência mínima: 24 horas")
    
    # 8. Verificar conflitos
    conflitos = buscar_conflitos(inicio, fim)
    if conflitos:
        raise ValidationError("Conflito de horário detectado")
    
    return True
```

### Detecção de Conflitos

Dois agendamentos têm conflito se:
- Ambos têm status `AGENDADO`
- E há sobreposição de tempo:
  - `inicio_A < fim_B` E `fim_A > inicio_B`

```sql
SELECT * FROM agendamentos
WHERE status = 'AGENDADO'
  AND horario_inicio_utc < :novo_fim
  AND horario_fim_utc > :novo_inicio
```

---

## 5. Configurações do Sistema

### Constantes de Negócio

```python
DURACAO_MINIMA_MINUTOS = 5
DURACAO_MAXIMA_MINUTOS = 120
ANTECEDENCIA_MINIMA_HORAS = 24
MAX_AGENDAMENTOS_ATIVOS_POR_CIENTISTA = 3
NOME_TELESCOPIO = 'Hubble-Acad'
```

---

## 6. Considerações de Performance

1. **Índices compostos**: O índice `idx_agendamentos_horario_status` otimiza a busca de conflitos
2. **Particionamento futuro**: Para escala, considerar particionar por data
3. **Cache**: Agendamentos futuros podem ser cacheados por 5 minutos
4. **Paginação**: Sempre limitar consultas a no máximo 100 registros por página

---

## 7. Migração e Versionamento

### Estratégia de Migração

- Usar migrations do SQLAlchemy (Alembic)
- Versionamento semântico: `YYYYMMDD_HHMMSS_descricao.py`
- Sempre incluir rollback

### Exemplo de Migration

```python
"""create_tables

Revision ID: 20251109_150000
"""

def upgrade():
    op.create_table(
        'cientistas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(200), nullable=False),
        # ... outros campos
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'agendamentos',
        # ...
    )

def downgrade():
    op.drop_table('agendamentos')
    op.drop_table('cientistas')
```

---

## 8. Auditoria e Rastreabilidade

Todos os eventos importantes devem gerar logs de auditoria (ver LOGGING.md):

- Criação de cientista
- Criação de agendamento
- Cancelamento de agendamento
- Tentativas de agendamento com conflito
- Alterações de status

---

*Última atualização: 2025-11-09*
