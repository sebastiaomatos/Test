# Fluxo de WhatsApp automático — Imóveis AQV

> Régua de relacionamento para **acelerar o fechamento** e **recuperar o lead que esfria**.
> Implementável em ManyChat, 360dialog, Z-API, Take Blip, Kommo ou no seu CRM.
> Substitua os campos entre `{{ }}` pelos dados do lead/imóvel.

## Princípios
1. **Responda em até 5 minutos** (idealmente automático no minuto 0). Lead de tráfego pago esfria rápido.
2. **Qualifique cedo:** intenção (morar/investir) + capacidade (financia/à vista).
3. **Sempre ofereça 2 horários fechados** para a visita (facilita o "sim").
4. **Pare a régua** assim que o lead responder e for assumido por um corretor humano.
5. **Reative** quem some, com prova e escassez reais.

---

## Gatilho de entrada
- **Origem A:** clique no anúncio Click-to-WhatsApp → mensagem já chega com contexto.
- **Origem B:** Lead Ads / formulário da landing → dispara a mensagem `M0` automaticamente.

---

## Mensagens da régua

### `M0` — Imediato (0–5 min) · Saudação + qualificação
> Oi, {{nome}}! 👋 Aqui é da Imóveis AQV. Vi que você se interessou pelo *{{imovel}}* ({{metragem}}, {{quartos}} quartos, {{condicao}}).
> Pra já te mostrar o que faz mais sentido: você procura pra **morar** ou pra **investir**?

➡️ **Espera resposta.** Se responder → marca `intencao` e segue para `M1`. Se **não responder em 10 min** → `R1`.

### `M1` — Após resposta de intenção · Capacidade
> Show! E como você pretende comprar: **financiamento** ou **à vista**?
> (Se for financiamento, eu já te ajudo a simular — muita gente usa o **FGTS** na entrada.)

➡️ Marca `pagamento`. Segue para `M2`.

### `M2` — Oferta de visita (2 horários)
> Perfeito, {{nome}}. Esse imóvel costuma sair rápido. Posso te mostrar pessoalmente?
> Fica melhor **amanhã à tarde** ou **sábado de manhã**? 🗓️

➡️ Se aceitar → `M3` (confirmação) + **notifica corretor humano** e **pausa automação**.
➡️ Se não responder em 1 dia → `R2`.

### `M3` — Confirmação de visita
> Combinado! Agendei pra {{data_hora}}. Vou te mandar o endereço e um lembrete no dia. Qualquer coisa, é só chamar aqui. 🙌

---

## Régua de recuperação (quem não responde)

### `R1` — +10 min sem resposta · Prova + leve urgência
> Ah, {{nome}}, só pra você ver o porquê desse imóvel chamar atenção 👇
> [enviar vídeo/foto do {{imovel}}]
> Esse aqui tem saído rápido. Quer que eu segure uma simulação no seu nome?

### `R2` — Dia 2 · Quebra de objeção (preço/financiamento)
> {{nome}}, fiz uma simulação rápida: dá pra deixar a parcela **parecida com um aluguel**, usando o FGTS na entrada. 👀
> Quer que eu te mande os números? É rápido.

### `R3` — Dia 4 · Escassez real
> Passando só pra avisar: a condição da entrada do *{{imovel}}* vai até **{{prazo}}**, e restam **{{unidades}} unidades**.
> Se ainda fizer sentido pra você, me avisa que eu garanto a sua. 🔑

### `R4` — Dia 7 · Última chamada + alternativa (ICP)
> {{nome}}, não quero te encher 🙂 Se o *{{imovel}}* não foi o ideal, tenho **outras 2 opções** no mesmo perfil e faixa de preço.
> Quer que eu te mande? Assim não perde a viagem.

### `R5` — Dia 15 e Dia 30 · Reativação
> Oi, {{nome}}! Surgiu uma **novidade** que combina com o que você procurava: {{novidade}}.
> Vale dar uma olhada? Posso te mandar o vídeo.

---

## Regras de parada e ramificação
| Condição | Ação |
|---|---|
| Lead responde qualquer mensagem | Pausa a régua automática + notifica corretor |
| Lead agenda visita (`M2`/`M3`) | Move no CRM para "Visita agendada" + lembrete D-0 |
| Lead pede "parar"/"sair" | Encerra automação (opt-out) |
| Sem resposta após `R5` (D30) | Move para "Frio" + entra em campanha de reengajamento (Meta BOFU) |
| Lead diz "à vista" / alta renda | Marca prioridade alta → atendimento humano imediato |

## Eventos para o CRM/Pixel (atribuição e otimização)
- `conversa_iniciada` (M0 respondida) → evento de **conversão** para Meta/Google (CAPI).
- `visita_agendada` (M2 aceita) → evento de valor + base de Lookalike.
- `venda` (fechamento no CRM) → evento de valor máximo + Lookalike de compradores.
