# Módulo de Monitoramento de Fissuras — Especificação para Implementação

**Documento:** VP-007  
**Arquivo sugerido:** `docs/modules/007-crack-monitoring-module.md`  
**Versão:** 1.0.0  
**Status:** ESPECIFICAÇÃO DE IMPLEMENTAÇÃO

---

# 1. Objetivo

Implementar o primeiro módulo especializado de monitoramento de fissuras da Vision Platform.

O módulo deverá analisar fotografias de uma etiqueta física instalada sobre uma fissura estrutural.

A primeira fotografia de uma instalação será cadastrada pelo usuário como **imagem de referência**.

Todas as fotografias posteriores deverão ser comparadas:

1. com a imagem de referência;
2. com a geometria processada da referência;
3. com as medições históricas;
4. com as medições das imagens anteriores.

O objetivo não é simplesmente "detectar uma fissura".

O objetivo é determinar, de forma quantitativa e rastreável, se a fissura apresenta evolução, estabilidade ou alteração geométrica ao longo do tempo.

---

# 2. Importante — não tratar como um simples problema de classificação

NÃO implementar este módulo inicialmente como:

```text
foto -> IA -> ativa/passiva
```

A solução deverá ser híbrida:

```text
Imagem
   ↓
Detecção / Segmentação
   ↓
Localização dos elementos físicos da etiqueta
   ↓
Correção geométrica / perspectiva
   ↓
Sistema de coordenadas normalizado
   ↓
Extração de pontos, linhas, círculos e medidas
   ↓
Comparação com referência
   ↓
Série temporal
   ↓
Índices de alteração
   ↓
Classificação técnica
```

A IA deverá auxiliar a localizar os elementos visuais quando necessário.

As medições geométricas deverão ser calculadas por algoritmos determinísticos sempre que possível.

---

# 3. Elementos existentes na etiqueta

A fotografia de referência fornecida para o desenvolvimento possui os seguintes elementos relevantes:

- etiqueta retangular;
- círculo grande;
- seis círculos pequenos;
- ponto central em cada círculo pequeno;
- duas linhas diagonais;
- região/tarja azul central;
- fissura passando pela região central;
- identificação visual da etiqueta;
- informações de instalação;
- escala geométrica fornecida pela própria etiqueta.

A imagem de referência apresenta seis marcadores distribuídos em três posições de cada lado da região central.

---

# 4. Conceito físico

A etiqueta é colada sobre a fissura.

A região central da etiqueta possui uma faixa azul que atravessa a etiqueta de cima a baixo.

A fissura atravessa essa região.

Os elementos geométricos da etiqueta funcionam como referências para medir alterações da fissura.

A plataforma deverá considerar que:

```text
Etiqueta
    ↓
Sistema de referência físico
    ↓
Fissura
    ↓
Alteração temporal
```

---

# 5. Primeira imagem — referência

A primeira fotografia deverá ser cadastrada explicitamente como:

```text
REFERENCE_IMAGE
```

Essa fotografia será a origem da linha de base.

O sistema deverá armazenar não apenas o arquivo original.

Deverá armazenar também os dados processados da referência.

---

# 6. Dados da referência

A referência deverá possuir, no mínimo:

```text
reference_id
tenant_id
installation_id
image_id
camera_id
captured_at
image_width
image_height

label_corners
homography
coordinate_system

marker_points
circle_geometry
line_AB
line_CD
line_intersection

distances
angles
crack_geometry

processing_version
model_version
algorithm_version

quality_score
```

---

# 7. Workflow para criar uma referência

O usuário deverá conseguir:

```text
Selecionar câmera
        ↓
Visualizar câmera
        ↓
Capturar fotografia
        ↓
Visualizar fotografia
        ↓
Processar
        ↓
Revisar detecções
        ↓
Confirmar
        ↓
Definir como referência
        ↓
Salvar no banco
```

A referência NÃO deverá ser criada automaticamente sem possibilidade de revisão.

---

# 8. Seleção da câmera

A interface deverá permitir selecionar uma câmera cadastrada.

Exemplo:

```text
Câmera:
CAM_000001

Local:
Pilar P01

Instalação:
Fissurômetro FIS_000001
```

---

# 9. Captura da fotografia

O sistema deverá permitir:

```text
CAPTURAR FOTO
```

A fotografia deverá ser armazenada no Storage.

O banco deverá armazenar os metadados.

---

# 10. Revisão humana

Antes de confirmar a referência, o usuário deverá visualizar uma sobreposição da detecção.

Exemplo:

```text
Imagem original

+

Cantos da etiqueta

+

Centro dos 6 marcadores

+

Círculo

+

Linha AB

+

Linha CD

+

Interseção

+

Região da fissura
```

O usuário deverá poder corrigir pontos quando a detecção automática estiver incorreta.

---

# 11. Correção de perspectiva

A câmera poderá não estar perfeitamente perpendicular à etiqueta.

Por isso, NÃO comparar diretamente coordenadas de pixels entre fotografias.

Primeiro deverá ser feita a normalização geométrica.

Fluxo:

```text
Imagem original
      ↓
Detecção dos quatro cantos da etiqueta
      ↓
Homografia
      ↓
Imagem retificada
      ↓
Sistema de coordenadas canônico
```

---

# 12. Sistema de coordenadas

Após a retificação, cada imagem deverá possuir um sistema de coordenadas normalizado.

Exemplo:

```text
X → horizontal
Y → vertical
```

A unidade inicial poderá ser:

```text
pixel normalizado
```

Posteriormente deverá ser convertida para:

```text
mm
```

quando a escala física da etiqueta estiver definida.

---

# 13. Escala em milímetros

O sistema deverá suportar calibração física.

Preferência:

```text
distância física conhecida
        ↓
distância em pixels
        ↓
pixels_per_mm
```

Se a etiqueta possuir dimensões físicas conhecidas, elas deverão ser utilizadas.

A conversão deverá ser registrada na referência.

---

# 14. Detecção dos seis marcadores

A IA/algoritmo deverá localizar os seis círculos pequenos.

Cada marcador deverá possuir:

```text
marker_id
center_x
center_y
radius
confidence
```

Identificação lógica:

```text
L1
L2
L3

R1
R2
R3
```

A nomenclatura deverá permanecer consistente entre todas as imagens.

---

# 15. Centro dos marcadores

O ponto central de cada círculo é o ponto de medição.

O sistema deverá trabalhar principalmente com:

```text
L1
L2
L3
R1
R2
R3
```

e não apenas com a borda dos círculos.

---

# 16. Linhas imaginárias dos marcadores

O sistema deverá criar linhas geométricas entre os centros dos marcadores.

Exemplo:

```text
L1 -------- R1
L2 -------- R2
L3 -------- R3
```

Essas linhas deverão ser medidas na referência e nas imagens posteriores.

---

# 17. Medições dos marcadores

Para cada linha deverão ser calculados:

```text
distância
ângulo
inclinação
deslocamento
```

Exemplo:

```text
distance_L1_R1
distance_L2_R2
distance_L3_R3
```

---

# 18. Medições verticais

Também deverão ser calculadas distâncias:

```text
L1-L2
L2-L3
R1-R2
R2-R3
```

Isso permitirá identificar alterações verticais.

---

# 19. Rede geométrica dos seis pontos

O sistema deverá construir uma rede de pontos.

Conceito:

```text
L1 -------- R1
| \        / |
|  \      /  |
L2 -------- R2
|  /      \  |
| /        \ |
L3 -------- R3
```

A geometria real deverá ser determinada pela imagem e pela definição oficial da etiqueta.

Não assumir que as linhas desenhadas acima representam necessariamente todas as medições finais.

---

# 20. Linhas AB e CD

A etiqueta possui duas linhas diagonais que atravessam o círculo maior.

O sistema deverá representar explicitamente:

```text
Segmento AB
Segmento CD
```

Cada segmento deverá possuir:

```text
A = ponto inicial
B = ponto final

C = ponto inicial
D = ponto final
```

---

# 21. Detecção dos pontos A, B, C e D

Os pontos deverão ser obtidos a partir das interseções das linhas com a geometria conhecida do círculo.

Preferência:

```text
círculo
+
linha
=
duas interseções
```

Isso é mais robusto do que tentar detectar quatro pontos arbitrários.

---

# 22. Comprimento dos segmentos

Calcular:

```text
AB
CD
```

em:

```text
pixels
```

e, quando houver calibração:

```text
mm
```

---

# 23. Ângulo entre AB e CD

Calcular:

```text
angle_AB_CD
```

O ângulo deverá ser calculado de forma consistente.

Também registrar:

```text
orientation_AB
orientation_CD
```

---

# 24. Interseção AB × CD

As duas retas deverão possuir um ponto de interseção:

```text
P = AB ∩ CD
```

Registrar:

```text
intersection_x
intersection_y
```

A posição do ponto de interseção deverá ser comparada com a referência.

---

# 25. Alteração do ponto de interseção

Calcular:

```text
ΔX
ΔY
ΔP
```

onde:

```text
ΔP = distância entre a posição da referência e a posição atual
```

---

# 26. Região central da fissura

A região azul deverá ser identificada como região de interesse.

O sistema deverá detectar:

```text
central_band
```

Essa região deverá auxiliar na localização da fissura.

---

# 27. Detecção da fissura

A fissura deverá ser localizada dentro da região de interesse.

Preferência inicial:

```text
image processing
+
edge detection
+
segmentation
+
geometry
```

Se a variabilidade das imagens exigir aprendizado de máquina, adicionar modelo de segmentação.

---

# 28. Não confundir tarja azul com fissura

A tarja azul é um elemento da etiqueta.

A fissura é o elemento estrutural que atravessa essa região.

O modelo deverá aprender/distinguir:

```text
tarja
≠
fissura
```

---

# 29. Geometria da fissura

A fissura detectada deverá ser representada como:

```text
skeleton
```

ou estrutura equivalente.

Calcular:

```text
comprimento
orientação
pontos extremos
curvatura
largura
```

quando tecnicamente possível.

---

# 30. Largura da fissura

A largura deverá ser medida ao longo de múltiplas seções.

Não utilizar somente um ponto.

Exemplo:

```text
w1
w2
w3
w4
w5
...
wn
```

Calcular:

```text
min
max
mean
median
standard deviation
```

---

# 31. Medição temporal

Para cada nova fotografia:

```text
Reference
     ↓
Current
     ↓
Compare
```

e também:

```text
Previous
     ↓
Current
     ↓
Variation
```

---

# 32. Comparação com a referência

Calcular alterações:

```text
Δ marker distances
Δ marker angles
Δ AB
Δ CD
Δ angle AB/CD
Δ intersection
Δ crack width
Δ crack length
Δ crack orientation
```

---

# 33. Comparação temporal

Além da referência, manter série temporal:

```text
T0
T1
T2
T3
...
Tn
```

Cada medição deverá ser armazenada.

---

# 34. Classificação

A plataforma deverá evitar declarar:

```text
ATIVA
```

ou:

```text
PASSIVA
```

baseando-se em uma única medida.

A classificação deverá utilizar múltiplos indicadores.

---

# 35. Estado inicial

A referência deverá possuir:

```text
baseline
```

Não considerar a referência como "ativa" ou "passiva" automaticamente.

Ela representa:

```text
estado inicial conhecido
```

---

# 36. Índice de alteração

Criar um índice quantitativo.

Exemplo conceitual:

```text
change_score
```

Esse índice poderá combinar:

```text
marker displacement
line angle variation
intersection displacement
crack width variation
crack geometry variation
```

Os pesos deverão ser configuráveis.

NÃO definir pesos arbitrários como definitivos sem validação experimental.

---

# 37. Estados

Inicialmente utilizar estados neutros:

```text
STABLE

CHANGED

SIGNIFICANT_CHANGE

INSUFFICIENT_DATA
```

Posteriormente poderão ser mapeados para:

```text
PASSIVE

ACTIVE
```

após validação técnica.

---

# 38. Incerteza

Toda medição deverá possuir indicador de confiança.

Exemplo:

```text
confidence
quality_score
```

---

# 39. Qualidade da imagem

Antes da análise, verificar:

```text
blur
exposure
contrast
resolution
occlusion
perspective
label_visibility
```

---

# 40. Imagem inválida

Se a qualidade estiver abaixo do limite:

```text
PROCESSING_REJECTED
```

ou:

```text
INSUFFICIENT_DATA
```

A plataforma deverá explicar o motivo.

---

# 41. Oclusão

Se parte da etiqueta estiver coberta:

```text
occlusion_detected = true
```

e a confiança deverá ser reduzida.

---

# 42. Câmera

A câmera deverá permanecer, idealmente:

- fixa;
- com posição conhecida;
- com zoom constante;
- com foco estável;
- com exposição razoavelmente estável.

---

# 43. Mudança de câmera

Se a câmera mudar de posição, o sistema deverá detectar possível alteração de geometria da captura.

Não interpretar automaticamente uma mudança de perspectiva como movimentação da fissura.

---

# 44. Registro da câmera

A referência deverá guardar:

```text
camera_id
camera_position
camera_configuration
resolution
```

quando disponível.

---

# 45. Comparação robusta

A comparação deverá utilizar a geometria da etiqueta como referência.

Não utilizar simplesmente:

```text
pixel_current - pixel_reference
```

porque isso produzirá falsos positivos em pequenas mudanças de câmera.

---

# 46. Modelos de IA

A arquitetura deverá permitir múltiplos modelos.

Exemplo:

```text
Label Detector

Marker Detector

Line Detector

Crack Segmentation Model

Quality Model
```

---

# 47. Primeiro modelo

O OpenCode deverá começar pelo menor modelo necessário.

Não iniciar com uma rede neural gigante.

A prioridade é:

```text
OpenCV
+
geometria
+
calibração
```

e adicionar IA onde realmente houver necessidade.

---

# 48. Modelo de detecção

Se for necessário treinar detector:

```text
YOLO pequeno
```

ou arquitetura equivalente leve.

O modelo deverá ser exportável para:

```text
ONNX
```

e executado com:

```text
ONNX Runtime
```

no servidor local.

---

# 49. Treinamento

O treinamento poderá ser realizado em computador com GPU.

O servidor Debian com i5 de segunda geração não deverá ser considerado ambiente ideal para treinamento pesado.

Ele será principalmente:

```text
inference server
```

---

# 50. Dataset

O projeto deverá criar estrutura:

```text
datasets/

    crack_monitoring/

        images/

        annotations/

        train/

        val/

        test/

        reference/

```

---

# 51. Anotações

As imagens deverão possuir anotações para:

- etiqueta;
- seis marcadores;
- círculo;
- linhas;
- região central;
- fissura.

Quando apropriado utilizar pontos/keypoints em vez de bounding boxes.

---

# 52. Ferramenta de anotação

O OpenCode deverá avaliar e configurar uma ferramenta apropriada para anotação.

Preferência:

```text
CVAT
```

ou ferramenta equivalente.

A escolha deverá ser registrada na documentação.

---

# 53. Keypoints

Para os seis marcadores, preferir:

```text
keypoints
```

quando o objetivo principal for localizar o centro.

---

# 54. Segmentação

Para a fissura, preferir:

```text
segmentation
```

quando necessário.

---

# 55. Dataset mínimo

Não iniciar treinamento definitivo com poucas imagens.

O OpenCode deverá criar uma estratégia de coleta e registrar:

```text
quantidade
variações
condições
câmeras
ângulos
iluminação
oclusões
```

---

# 56. Data Augmentation

Avaliar augmentation para:

- pequenas rotações;
- escala;
- iluminação;
- contraste;
- ruído;
- blur controlado;
- pequenas mudanças de perspectiva.

Não aplicar transformações que alterem fisicamente a geometria que está sendo medida sem uma justificativa clara.

---

# 57. Ground Truth

Cada medição deverá possuir possibilidade de validação humana.

A referência deverá ser revisável.

---

# 58. Benchmark

Criar conjunto de imagens de teste que não participe do treinamento.

Medir:

```text
detecção dos marcadores

erro de posição

erro angular

erro de distância

detecção da fissura

erro de largura

estabilidade temporal
```

---

# 59. Métrica principal

Não utilizar somente:

```text
mAP
```

para avaliar o sistema.

Para este projeto, métricas geométricas são essenciais.

---

# 60. Erro de posição

Para cada marcador:

```text
position_error_px
position_error_mm
```

---

# 61. Erro angular

Registrar:

```text
angle_error_deg
```

---

# 62. Erro de distância

Registrar:

```text
distance_error_mm
```

---

# 63. Erro da fissura

Quando houver ground truth:

```text
crack_width_error_mm
crack_length_error_mm
```

---

# 64. Banco de dados

Criar entidades específicas para o módulo.

Conceito:

```text
crack_installations

crack_references

crack_images

crack_measurements

crack_markers

crack_lines

crack_geometry

crack_events
```

Os nomes finais deverão seguir o padrão do banco da Vision Platform.

---

# 65. Installation

Uma instalação representa uma etiqueta/fissurômetro físico instalado em um local.

Exemplo:

```text
installation_id
tenant_id
name
location
camera_id
status
```

---

# 66. Reference

Uma instalação deverá possuir uma referência ativa.

Exemplo:

```text
reference_id
installation_id
image_id
created_at
processing_version
```

---

# 67. Measurements

Cada imagem processada deverá gerar uma medição.

Exemplo:

```text
measurement_id
installation_id
image_id
captured_at
quality_score
change_score
status
```

---

# 68. Marker Measurements

Guardar os seis marcadores.

Exemplo:

```text
L1
L2
L3
R1
R2
R3
```

com:

```text
x
y
confidence
```

---

# 69. Line Measurements

Guardar:

```text
AB
CD
```

com:

```text
length
angle
x1
y1
x2
y2
```

---

# 70. Temporal Comparison

Guardar os deltas em relação à referência.

Exemplo:

```text
delta_marker_distance
delta_marker_angle
delta_AB_length
delta_CD_length
delta_AB_CD_angle
delta_intersection
delta_crack_width
delta_crack_length
```

---

# 71. Visualização

A interface deverá permitir visualizar:

```text
Imagem original

Imagem retificada

Imagem com overlays

Referência

Imagem atual

Diferença geométrica

Gráficos temporais
```

---

# 72. Overlay

O sistema deverá desenhar sobre a imagem:

```text
6 marcadores

AB

CD

interseção

crack

medidas

ângulos

alertas
```

---

# 73. Comparação Visual

Criar visualização:

```text
REFERENCE          CURRENT

   ↓                  ↓

Geometry            Geometry

   ↓                  ↓

       COMPARISON
```

---

# 74. Gráficos

Para cada instalação:

```text
tempo × largura da fissura

tempo × distância L1-R1

tempo × distância L2-R2

tempo × distância L3-R3

tempo × ângulo AB/CD

tempo × deslocamento da interseção
```

---

# 75. Alertas

O sistema deverá permitir configurar limites.

Exemplo:

```text
warning_threshold
critical_threshold
```

Não colocar valores técnicos definitivos no código.

---

# 76. Auditoria

Registrar:

```text
quem criou referência

quem alterou referência

quem aprovou medição

quem corrigiu pontos

quando foi processada

qual modelo foi utilizado
```

---

# 77. Versionamento

Cada processamento deverá registrar:

```text
algorithm_version
model_version
processing_version
```

Assim será possível reproduzir uma análise antiga.

---

# 78. Reprocessamento

A plataforma deverá permitir reprocessar uma imagem com versão nova do algoritmo/modelo.

O resultado anterior não deverá ser destruído.

---

# 79. Princípio de Reprodutibilidade

Uma medição histórica deverá poder responder:

```text
Qual imagem?

Qual modelo?

Qual algoritmo?

Qual configuração?

Qual referência?

Qual versão?
```

---

# 80. API do módulo

Criar endpoints compatíveis com a arquitetura geral.

Exemplo:

```text
POST /api/v1/cracks/installations

GET  /api/v1/cracks/installations

GET  /api/v1/cracks/installations/{id}

POST /api/v1/cracks/installations/{id}/capture

POST /api/v1/cracks/installations/{id}/reference

GET  /api/v1/cracks/installations/{id}/measurements

GET  /api/v1/cracks/installations/{id}/comparison
```

Os endpoints finais deverão respeitar o contrato oficial da API.

---

# 81. Definir referência

A operação:

```text
POST /api/v1/cracks/installations/{id}/reference
```

deverá:

1. validar imagem;
2. executar processamento;
3. apresentar/registrar detecções;
4. permitir revisão;
5. salvar geometria;
6. marcar referência;
7. registrar auditoria.

---

# 82. Nova fotografia

Fluxo:

```text
Camera
 ↓
Capture
 ↓
Image
 ↓
Quality
 ↓
Rectification
 ↓
Detection
 ↓
Measurement
 ↓
Comparison
 ↓
Event
```

---

# 83. Foto manual

Também deverá ser possível:

```text
Upload Photo
```

sem câmera.

Isso permitirá utilizar fotos enviadas por celular.

---

# 84. Vídeo

O módulo deverá futuramente permitir extrair frames de vídeos.

Não implementar vídeo antes de estabilizar o processamento de fotografias.

---

# 85. Primeira implementação

A ordem de implementação deverá ser:

```text
1. Cadastro da instalação

2. Cadastro da câmera

3. Captura de fotografia

4. Armazenamento

5. Definição da referência

6. Retificação da imagem

7. Detecção dos 6 marcadores

8. Detecção do círculo

9. Detecção de AB/CD

10. Cálculo geométrico

11. Persistência das medidas

12. Nova fotografia

13. Comparação com referência

14. Série temporal

15. Detecção da fissura

16. Classificação de alteração

17. Treinamento/aperfeiçoamento do modelo
```

---

# 86. Regra importante

NÃO começar treinando uma IA para responder:

```text
"fissura ativa"
```

Primeiro construir um sistema confiável de:

```text
detecção
+
geometria
+
calibração
+
comparação
```

Depois utilizar os dados históricos para treinar classificadores.

---

# 87. Objetivo final

O resultado deverá ser algo semelhante a:

```text
Instalação:
FIS-000001

Referência:
24/08/2026

Última medição:
26/08/2026

Variação da distância:
+0.42 mm

Variação angular:
+0.31°

Variação da interseção:
0.68 mm

Largura da fissura:
0.84 mm

Variação da largura:
+0.18 mm

Qualidade:
94%

Estado:
CHANGED

Confiança:
91%
```

Os valores acima são apenas exemplos de apresentação e NÃO devem ser tratados como valores reais ou limites técnicos.

---

# 88. Regra de engenharia

A Vision Platform deverá separar claramente:

```text
Detecção
```

de:

```text
Medição
```

e:

```text
Interpretação
```

Exemplo:

```text
IA detectou marcador
        ↓
Geometria calculou distância
        ↓
Comparador calculou variação
        ↓
Motor de regras interpretou alteração
```

Isso permitirá auditar o resultado.

---

# 89. Instruções obrigatórias para o OpenCode

Antes de implementar:

1. Ler toda a documentação existente da Vision Platform.
2. Ler `.agent/skills/`.
3. Carregar e respeitar todas as Skills aplicáveis.
4. Não alterar a arquitetura Core.
5. Implementar este módulo como módulo/plugin.
6. Não criar um backend separado.
7. Não criar outro banco.
8. Utilizar o PostgreSQL existente.
9. Utilizar o Storage existente.
10. Utilizar autenticação existente.
11. Utilizar Event Bus existente.
12. Utilizar Camera Service existente.
13. Criar migrations.
14. Criar testes.
15. Criar dataset pipeline.
16. Criar pipeline de anotação.
17. Criar benchmark.
18. Criar documentação.
19. Não assumir valores físicos sem calibração.
20. Não declarar fissura ativa apenas por uma imagem.
21. Não substituir medições geométricas determinísticas por IA sem justificativa.
22. Manter versões de modelos e algoritmos.
23. Permitir revisão humana da referência.
24. Permitir correção manual das detecções.
25. Implementar primeiro a solução geométrica e somente depois treinar modelos onde necessário.

---

# 90. Primeira Sprint

A primeira Sprint específica deste módulo deverá produzir:

```text
[ ] Crack Installation entity

[ ] Camera association

[ ] Capture endpoint

[ ] Image storage

[ ] Reference workflow

[ ] Reference database schema

[ ] Label corner detection

[ ] Perspective correction

[ ] Six marker detection

[ ] Marker coordinate system

[ ] AB/CD detection

[ ] Geometric measurements

[ ] Reference overlay

[ ] Human confirmation UI

[ ] Tests
```

---

# 91. Resultado esperado da primeira Sprint

Ao final, deverá ser possível:

```text
Selecionar câmera

↓

Capturar foto

↓

Visualizar foto

↓

Processar

↓

Detectar etiqueta

↓

Detectar 6 marcadores

↓

Detectar AB/CD

↓

Corrigir perspectiva

↓

Calcular medidas

↓

Revisar

↓

Salvar como referência
```

---

# 92. Resultado esperado da segunda Sprint

Deverá ser possível:

```text
Capturar nova foto

↓

Processar

↓

Comparar com referência

↓

Calcular deltas

↓

Salvar medição

↓

Mostrar comparação

↓

Atualizar histórico
```

---

# 93. Resultado esperado da terceira Sprint

Implementar:

```text
Detecção/segmentação da fissura

↓

Medição de largura

↓

Medição de comprimento

↓

Comparação temporal

↓

Índice de alteração

↓

Alertas
```

---

# 94. Resultado esperado da quarta Sprint

Construir o pipeline de Machine Learning:

```text
Dataset

↓

Annotation

↓

Training

↓

Validation

↓

Benchmark

↓

Export ONNX

↓

Inference

↓

Versioning
```

---

# 95. Critério de sucesso

O módulo será considerado funcional quando uma instalação real puder seguir:

```text
Etiqueta instalada

↓

Câmera cadastrada

↓

Foto inicial

↓

Usuário confirma referência

↓

Sistema calcula baseline

↓

Fotos periódicas

↓

Medições automáticas

↓

Comparação histórica

↓

Identificação de alteração

↓

Registro de evidências
```

---

# 96. Consideração final

Este módulo não deve ser construído como um simples "detector de fissuras".

Ele deve ser construído como um:

**Sistema de medição geométrica temporal de fissuras baseado em visão computacional.**

A IA é um componente do sistema.

A referência física, a calibração, a geometria, as medições e a série temporal são igualmente importantes.

O objetivo final é produzir uma medição tecnicamente rastreável e reproduzível, e não apenas uma classificação visual.

**Fim do Documento**
