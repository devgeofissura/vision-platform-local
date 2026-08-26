# Crack Vision Pipeline

**Documento:** VP-008  
**Arquivo:** `docs/modules/008-crack-vision-pipeline.md`  
**Versão:** 1.0.0  
**Status:** ESPECIFICAÇÃO OBRIGATÓRIA DE IMPLEMENTAÇÃO

---

# 1. Objetivo

Este documento define o pipeline oficial de visão computacional do módulo de monitoramento de fissuras da Vision Platform.

O objetivo é impedir que os algoritmos de visão computacional analisem elementos existentes fora da etiqueta física instalada sobre a fissura.

A regra principal deste documento é:

> **A imagem completa da câmera NÃO deverá ser utilizada diretamente para detectar marcadores, círculos, linhas ou fissuras.**

O processamento deverá obrigatoriamente seguir uma arquitetura hierárquica:

```text
Imagem completa
      ↓
Localização da etiqueta
      ↓
ROI da etiqueta
      ↓
Validação da ROI
      ↓
Retificação / Homografia
      ↓
Imagem normalizada da etiqueta
      ↓
Detecção dos elementos internos
      ↓
Medições geométricas
      ↓
Detecção da fissura
      ↓
Comparação temporal
      ↓
Classificação / Eventos
```

---

# 2. Problema observado

Em testes iniciais, o algoritmo identificou corretamente algumas das retas existentes na etiqueta, porém também identificou círculos e outros elementos presentes no ambiente externo.

Isso ocorreu porque os detectores estavam recebendo a imagem inteira da câmera.

Exemplo conceitual:

```text
┌───────────────────────────────────────────────┐
│ Ambiente                                      │
│                                               │
│     ○                         ○               │
│                                               │
│              ┌───────────────────────┐        │
│              │                       │        │
│              │       ETIQUETA        │        │
│              │                       │        │
│              └───────────────────────┘        │
│                                               │
│       ○                         ○             │
└───────────────────────────────────────────────┘
```

Os círculos externos não pertencem ao sistema de medição.

Portanto:

```text
círculo externo → IGNORAR
linha externa   → IGNORAR
objeto externo  → IGNORAR
```

---

# 3. Regra absoluta de ROI

Todos os detectores internos deverão operar exclusivamente sobre:

```text
LABEL_ROI
```

São proibidas chamadas como:

```python
detect_markers(full_image)
detect_lines(full_image)
detect_circles(full_image)
detect_crack(full_image)
```

A arquitetura correta será:

```python
label = detect_label(full_image)

roi = extract_label_roi(full_image, label)

normalized = rectify_label(roi)

markers = detect_markers(normalized)

lines = detect_lines(normalized)

crack = detect_crack(normalized)
```

---

# 4. Exceção

Somente o detector responsável por localizar a etiqueta poderá analisar a imagem completa.

Portanto:

```text
Full Image
    ↓
Label Detector
```

é permitido.

Depois disso:

```text
Full Image
    ↓
qualquer outro detector
```

é proibido.

---

# 5. Pipeline oficial

O pipeline completo deverá ser:

```text
STAGE 0
Image Acquisition

        ↓

STAGE 1
Image Quality

        ↓

STAGE 2
Label Detection

        ↓

STAGE 3
ROI Extraction

        ↓

STAGE 4
ROI Validation

        ↓

STAGE 5
Perspective Rectification

        ↓

STAGE 6
Canonical Coordinate System

        ↓

STAGE 7
Internal Element Detection

        ↓

STAGE 8
Geometric Measurement

        ↓

STAGE 9
Crack Detection

        ↓

STAGE 10
Reference Comparison

        ↓

STAGE 11
Temporal Analysis

        ↓

STAGE 12
Classification / Events

        ↓

STAGE 13
Persistence
```

---

# 6. STAGE 0 — Aquisição

Entrada:

```text
Camera
Upload
Mobile
Video Frame
```

Saída:

```text
RawImage
```

Metadados mínimos:

```text
image_id
tenant_id
installation_id
camera_id
captured_at
width
height
format
source
```

---

# 7. STAGE 1 — Qualidade

Antes da visão computacional, verificar:

```text
resolution
blur
brightness
contrast
exposure
noise
compression
```

Também verificar se existe imagem válida.

Se a imagem for inválida:

```text
PROCESSING_REJECTED
```

---

# 8. STAGE 2 — Label Detection

Este é o único estágio autorizado a utilizar a imagem completa.

Objetivo:

> Encontrar exclusivamente a etiqueta do fissurômetro.

O detector deverá identificar:

```text
LABEL
```

e, preferencialmente:

```text
P1
P2
P3
P4
```

representando os quatro cantos.

---

# 9. Detector da etiqueta

O primeiro modelo poderá ser:

```text
YOLO pequeno
```

ou outro detector leve apropriado.

Entretanto, o resultado final necessário é geométrico.

Preferência:

```text
detecção da etiqueta
+
quatro keypoints/cantos
```

ou:

```text
bounding box
+
corner estimation
```

---

# 10. Classe única

Se for utilizado object detection, a primeira versão deverá possuir somente uma classe:

```text
crack_monitoring_label
```

Não criar classes como:

```text
circle
line
marker
crack
```

neste primeiro detector.

Esses elementos pertencem a etapas posteriores.

---

# 11. Validação da etiqueta

O sistema deverá validar:

```text
confidence
aspect_ratio
area
position
corner geometry
```

A etiqueta deverá formar um quadrilátero plausível.

---

# 12. Falha na detecção

Se a etiqueta não for encontrada:

```text
LABEL_NOT_FOUND
```

O sistema NÃO deverá continuar procurando círculos ou linhas na imagem completa.

Fluxo:

```text
Label not found
      ↓
STOP
      ↓
INSUFFICIENT_DATA
```

---

# 13. Múltiplas etiquetas

Se mais de uma etiqueta for detectada:

```text
LABEL_1
LABEL_2
LABEL_3
```

o sistema deverá:

1. verificar a instalação/câmera esperada;
2. utilizar contexto da instalação;
3. rejeitar ambiguidade quando não for possível determinar qual etiqueta pertence à instalação.

Não escolher silenciosamente uma etiqueta aleatória.

---

# 14. STAGE 3 — ROI Extraction

Depois da localização:

```text
Full Image
     ↓
P1 P2 P3 P4
     ↓
Crop
     ↓
LABEL_ROI
```

A ROI deverá ser isolada.

---

# 15. Regra de exclusão

Depois da criação da ROI:

```text
pixels outside ROI
```

não deverão participar das etapas:

```text
marker detection
line detection
circle detection
crack detection
```

---

# 16. STAGE 4 — ROI Validation

A ROI deverá ser validada.

Verificar:

```text
label area
label aspect ratio
corners
orientation
visibility
occlusion
```

---

# 17. Máscara de segurança

Além do crop, poderá existir uma máscara:

```text
MASK_LABEL = 1
MASK_OUTSIDE = 0
```

Todos os detectores internos deverão receber a imagem e/ou máscara.

Isso fornece uma segunda barreira contra falsos positivos.

---

# 18. STAGE 5 — Perspective Rectification

A câmera poderá observar a etiqueta inclinada.

Portanto:

```text
ROI original
      ↓
Homography
      ↓
Canonical Label
```

A imagem deverá ser transformada para uma visão frontal.

---

# 19. Homografia

Utilizar:

```text
P1
P2
P3
P4
```

para calcular a transformação.

A ordem dos pontos deverá ser consistente:

```text
P1 = top-left
P2 = top-right
P3 = bottom-right
P4 = bottom-left
```

---

# 20. Tamanho canônico

Definir um tamanho canônico configurável.

Exemplo:

```text
1600 × 1000
```

O valor final deverá ser determinado durante implementação/calibração.

Não codificar dimensões arbitrárias como dimensões físicas reais.

---

# 21. STAGE 6 — Canonical Coordinate System

Após a homografia:

```text
X = horizontal
Y = vertical
```

Todos os elementos deverão possuir coordenadas nesse sistema.

Exemplo:

```text
(0,0) ─────────────────── (W,0)
  │                          │
  │                          │
  │                          │
(0,H) ─────────────────── (W,H)
```

---

# 22. Sistema físico

Quando a dimensão física da etiqueta for conhecida:

```text
pixel
  ↓
mm
```

através da calibração.

Registrar:

```text
pixels_per_mm_x
pixels_per_mm_y
```

quando apropriado.

---

# 23. Não utilizar comparação simples de pixels

É proibido utilizar como principal método:

```text
current_image - reference_image
```

sem normalização geométrica.

A câmera pode ter pequenas diferenças de:

- posição;
- perspectiva;
- escala;
- exposição.

A geometria da etiqueta deverá ser utilizada para estabilizar a comparação.

---

# 24. STAGE 7 — Elementos internos

Somente agora iniciar a análise dos elementos da etiqueta.

Elementos esperados:

```text
1 círculo grande

6 círculos pequenos / marcadores

2 linhas diagonais

região central azul

fissura
```

---

# 25. Conhecimento prévio da etiqueta

A etiqueta possui layout conhecido.

Isso deverá ser utilizado.

O sistema não deverá tratar os elementos como objetos completamente desconhecidos.

Após a retificação, existem regiões esperadas:

```text
L1
L2
L3

R1
R2
R3

AB
CD

CENTER_BAND

LARGE_CIRCLE
```

---

# 26. ROIs internas

Criar sub-ROIs.

Exemplo:

```text
LABEL
│
├── marker_L1_roi
├── marker_L2_roi
├── marker_L3_roi
├── marker_R1_roi
├── marker_R2_roi
├── marker_R3_roi
│
├── line_AB_roi
├── line_CD_roi
│
├── large_circle_roi
│
└── central_crack_roi
```

---

# 27. Marcadores

Os seis marcadores deverão ser tratados como keypoints.

Identificadores:

```text
L1
L2
L3
R1
R2
R3
```

---

# 28. Localização esperada

Cada marcador possui posição aproximada conhecida na etiqueta.

Portanto:

```text
marker detector
+
expected position
+
local ROI
```

deverão ser utilizados em conjunto.

---

# 29. Não procurar seis círculos globalmente

É proibido:

```python
find_all_circles(normalized_image)
```

e simplesmente selecionar os seis primeiros.

A lógica deverá ser:

```text
L1 ROI → localizar L1

L2 ROI → localizar L2

L3 ROI → localizar L3

R1 ROI → localizar R1

R2 ROI → localizar R2

R3 ROI → localizar R3
```

---

# 30. Centro do marcador

O dado principal será:

```text
center_x
center_y
```

O raio do círculo poderá ser armazenado como informação auxiliar.

---

# 31. Confiança

Cada marcador deverá possuir:

```text
confidence
```

Se um marcador não puder ser localizado com segurança:

```text
marker_status = UNCERTAIN
```

Não inventar coordenadas.

---

# 32. Linhas AB e CD

As linhas deverão ser detectadas somente nas regiões correspondentes.

Possíveis técnicas:

```text
Canny
HoughLines
HoughLinesP
LSD
segment detection
```

A escolha deverá ser determinada por benchmark.

---

# 33. Restrição geométrica

As linhas detectadas deverão ser filtradas por:

```text
posição esperada
orientação esperada
comprimento mínimo
proximidade da região esperada
```

---

# 34. Segmento AB

Registrar:

```text
A
B
length_AB
angle_AB
```

---

# 35. Segmento CD

Registrar:

```text
C
D
length_CD
angle_CD
```

---

# 36. Interseção

Calcular:

```text
P = AB ∩ CD
```

Registrar:

```text
P.x
P.y
```

---

# 37. Ângulo AB/CD

Calcular:

```text
angle_AB_CD
```

Manter convenção angular documentada.

---

# 38. Círculo grande

O círculo grande deverá ser localizado somente dentro da ROI da etiqueta.

Nunca executar Hough Circle na imagem original.

---

# 39. Círculo grande como referência

O círculo grande poderá fornecer:

```text
center
radius
```

e auxiliar na validação da homografia e da geometria.

---

# 40. Região azul central

A faixa azul deverá ser identificada como:

```text
CENTER_BAND
```

Ela deverá ser utilizada como referência para a região onde a fissura atravessa a etiqueta.

---

# 41. Detecção da fissura

Somente depois de:

```text
label detection
ROI
rectification
```

a fissura poderá ser analisada.

---

# 42. ROI da fissura

Criar uma região de interesse específica:

```text
CENTRAL_CRACK_ROI
```

A fissura deverá ser procurada prioritariamente nessa região.

---

# 43. Fissura fora da região esperada

Se houver uma linha escura ou rachadura no fundo da imagem:

```text
IGNORAR
```

Se houver uma linha fora da `CENTRAL_CRACK_ROI`:

```text
IGNORAR
```

---

# 44. Não confundir elementos da etiqueta

O modelo/processamento deverá distinguir:

```text
CENTER_BAND
```

de:

```text
CRACK
```

e:

```text
AB / CD
```

de:

```text
CRACK
```

---

# 45. Estratégia de detecção da fissura

Primeira abordagem:

```text
grayscale
+
contrast normalization
+
denoising
+
edge analysis
+
segmentation
+
morphology
```

Se os resultados forem insuficientes:

```text
segmentation model
```

poderá ser treinado.

---

# 46. Skeleton da fissura

Quando possível:

```text
crack mask
      ↓
skeletonization
      ↓
centerline
```

A centerline será usada para:

```text
length
orientation
geometry
```

---

# 47. Largura

A largura deverá ser calculada perpendicularmente à centerline em vários pontos.

Não utilizar somente um ponto.

---

# 48. Medições dos seis marcadores

Calcular:

```text
L1-R1
L2-R2
L3-R3
```

Além de:

```text
L1-L2
L2-L3

R1-R2
R2-R3
```

---

# 49. Rede geométrica

A rede deverá permitir verificar:

```text
distância
ângulo
inclinação
deformação
```

dos marcadores.

---

# 50. Baseline

A referência deverá gerar:

```text
BASELINE_GEOMETRY
```

contendo:

```text
marker positions
marker distances
marker angles

circle center
circle radius

AB
CD
AB/CD angle
intersection

crack geometry
```

quando disponível.

---

# 51. Processamento de nova imagem

Para uma nova fotografia:

```text
Current Image
     ↓
Label Detection
     ↓
ROI
     ↓
Rectification
     ↓
Internal Detection
     ↓
Measurement
     ↓
Compare with Baseline
```

---

# 52. Comparação

Calcular:

```text
ΔL1-R1
ΔL2-R2
ΔL3-R3

ΔL1-L2
ΔL2-L3

ΔR1-R2
ΔR2-R3

ΔAB
ΔCD
Δangle

Δintersection

Δcrack_width
Δcrack_length
Δcrack_orientation
```

---

# 53. Registro histórico

Cada processamento deverá gerar um registro independente.

Nunca substituir silenciosamente uma medição anterior.

---

# 54. Série temporal

Modelo:

```text
T0 = Reference

T1

T2

T3

...

Tn
```

---

# 55. Comparação dupla

Cada nova medição deverá poder ser comparada:

```text
Current vs Reference
```

e:

```text
Current vs Previous
```

---

# 56. Detecção de alteração

Uma alteração deverá ser baseada em múltiplos indicadores.

Exemplo:

```text
marker displacement
+
line angle variation
+
intersection displacement
+
crack width variation
```

---

# 57. Não classificar por uma única variável

Não utilizar regra simplista:

```text
if crack_width > X:
    ACTIVE
```

como mecanismo definitivo.

A classificação deverá considerar:

```text
múltiplas medidas
qualidade
confiança
histórico
limites configurados
```

---

# 58. Estados

Utilizar inicialmente:

```text
STABLE
CHANGED
SIGNIFICANT_CHANGE
INSUFFICIENT_DATA
```

A tradução para:

```text
PASSIVE
ACTIVE
```

deverá ser uma regra configurável e validada.

---

# 59. Qualidade

Se a imagem tiver baixa qualidade:

```text
INSUFFICIENT_DATA
```

em vez de fabricar uma medição.

---

# 60. Falha de marcador

Se vários marcadores forem perdidos:

```text
measurement_status = INSUFFICIENT_DATA
```

---

# 61. Falha de etiqueta

Se a etiqueta não for detectada:

```text
LABEL_NOT_FOUND
```

O pipeline deverá parar.

---

# 62. Falha de perspectiva

Se a homografia for inválida:

```text
INVALID_GEOMETRY
```

O pipeline deverá parar.

---

# 63. Falha de fissura

Se a fissura não puder ser detectada com confiança:

```text
CRACK_UNCERTAIN
```

Isso não significa automaticamente:

```text
NO_CRACK
```

---

# 64. Arquitetura de software

Estrutura recomendada:

```text
vision/

    acquisition/

    quality/

    label/

        detector.py
        validator.py
        corners.py

    roi/

        extractor.py
        mask.py
        validator.py

    geometry/

        homography.py
        coordinate_system.py
        calibration.py

    markers/

        detector.py
        tracker.py
        measurements.py

    lines/

        detector.py
        measurements.py

    crack/

        detector.py
        segmentation.py
        skeleton.py
        measurements.py

    comparison/

        baseline.py
        temporal.py
        metrics.py

    pipeline/

        orchestrator.py
```

---

# 65. Pipeline Orchestrator

O orchestrator deverá controlar a ordem obrigatória.

Conceito:

```python
image
    ↓
quality
    ↓
label
    ↓
roi
    ↓
rectification
    ↓
markers
    ↓
lines
    ↓
crack
    ↓
measurements
    ↓
comparison
    ↓
result
```

---

# 66. Guard Conditions

Cada etapa deverá verificar se a etapa anterior foi concluída com sucesso.

Exemplo:

```python
if not label_result.success:
    return LABEL_NOT_FOUND
```

---

# 67. Nenhum fallback global

Não implementar:

```python
if marker_not_found_in_roi:
    search_entire_image()
```

Isso é proibido.

Se não encontrou dentro da etiqueta:

```text
MARKER_NOT_FOUND
```

---

# 68. Fallback permitido

Pode haver métodos diferentes dentro da mesma ROI:

```text
Method A
   ↓
falhou
   ↓
Method B
   ↓
falhou
   ↓
UNCERTAIN
```

Mas todos devem operar dentro da ROI correta.

---

# 69. Modelos

O sistema deverá suportar:

```text
label_detector.onnx
marker_detector.onnx
crack_segmenter.onnx
```

quando modelos forem necessários.

---

# 70. Inferência

O ambiente de produção deverá priorizar:

```text
ONNX Runtime
```

quando compatível.

---

# 71. CPU

O servidor alvo possui hardware limitado.

Portanto:

```text
CPU inference
```

deverá ser considerada.

Modelos deverão ser leves.

---

# 72. Treinamento

O treinamento poderá ocorrer em máquina externa com GPU.

Produção:

```text
ONNX
+
ONNX Runtime
```

no servidor local.

---

# 73. Dataset do Label Detector

Criar dataset específico:

```text
datasets/crack_label_detection/
```

Classes:

```text
crack_monitoring_label
```

---

# 74. Dataset dos elementos

Somente depois de estabilizar o Label Detector:

```text
datasets/crack_elements/
```

Poderá conter:

```text
marker
line
crack
```

ou keypoints/segmentação conforme benchmark.

---

# 75. Dataset da fissura

Criar:

```text
datasets/crack_segmentation/
```

com máscaras quando necessário.

---

# 76. Regra para anotação

As anotações deverão refletir o sistema físico.

Não anotar objetos externos como:

```text
circle
marker
line
```

porque não fazem parte da etiqueta.

---

# 77. Data augmentation

Pode utilizar:

```text
brightness
contrast
small rotation
small perspective variation
noise
blur
```

mas não deverá criar transformações que destruam ou alterem artificialmente a geometria que o sistema precisa medir.

---

# 78. Teste obrigatório contra falsos positivos

Criar imagens de teste contendo:

```text
círculos fora da etiqueta
linhas fora da etiqueta
objetos circulares
cabos
lâmpadas
pessoas
estruturas
texturas
```

O sistema deverá ignorá-los.

---

# 79. Teste específico

Uma imagem como a imagem de referência deste projeto deverá produzir:

```text
LABEL = detected

EXTERNAL_CIRCLES = ignored

EXTERNAL_LINES = ignored

INTERNAL_MARKERS = detected

INTERNAL_LINES = detected

CRACK_REGION = analyzed
```

---

# 80. Critério de segurança contra falsos positivos

Qualquer elemento localizado fora:

```text
LABEL_ROI
```

deverá receber:

```text
ignored = true
```

ou simplesmente não entrar no resultado.

---

# 81. Overlay de diagnóstico

O sistema deverá gerar uma imagem de debug.

Exemplo:

```text
Original
+
quadrilateral da etiqueta
```

e outra:

```text
Etiqueta retificada
+
L1 L2 L3
+
R1 R2 R3
+
AB
+
CD
+
circle
+
crack
```

---

# 82. Debug obrigatório durante desenvolvimento

O OpenCode deverá salvar imagens intermediárias:

```text
01_original.jpg

02_label_detection.jpg

03_roi.jpg

04_rectified.jpg

05_markers.jpg

06_lines.jpg

07_crack.jpg

08_final_overlay.jpg
```

Isso permitirá descobrir exatamente em qual etapa ocorrerá um erro.

---

# 83. Observabilidade

Cada processamento deverá registrar:

```text
processing_id
stage
duration_ms
success
confidence
error
model_version
algorithm_version
```

---

# 84. Reprodutibilidade

Dado:

```text
image_id
processing_version
model_version
algorithm_version
configuration
```

deverá ser possível reproduzir a análise.

---

# 85. Benchmark

Criar benchmark por estágio:

```text
Label detection accuracy

Corner error

Homography error

Marker position error

Line angle error

Line length error

Crack segmentation quality

Crack width error
```

---

# 86. Métricas geométricas

As métricas principais não serão somente:

```text
mAP
precision
recall
```

Também serão:

```text
pixel error
mm error
degree error
position error
```

---

# 87. Erro de marcador

Registrar:

```text
marker_position_error_px
marker_position_error_mm
```

---

# 88. Erro de linha

Registrar:

```text
line_length_error_mm
line_angle_error_deg
```

---

# 89. Erro de interseção

Registrar:

```text
intersection_error_mm
```

---

# 90. Erro de fissura

Registrar:

```text
crack_width_error_mm
crack_length_error_mm
```

quando ground truth estiver disponível.

---

# 91. Referência

A referência deverá ser criada somente após:

```text
label detection
ROI validation
rectification
marker detection
line detection
geometry validation
```

---

# 92. Aprovação humana

O usuário deverá poder visualizar:

```text
Reference Image
+
Detected Geometry
+
Measurements
```

e então:

```text
CONFIRM REFERENCE
```

---

# 93. Correção manual

O usuário deverá poder corrigir:

```text
label corners
marker centers
line endpoints
crack mask
```

quando necessário.

---

# 94. Armazenamento da referência

Guardar:

```text
original image
rectified image
geometry
measurements
model versions
algorithm versions
calibration
approval
```

---

# 95. Regra de não sobrescrever

Uma nova referência não deverá apagar a referência anterior.

Deverá existir histórico.

---

# 96. API

O pipeline deverá ser integrado à API do módulo.

Exemplo:

```text
POST /api/v1/cracks/installations/{id}/capture

POST /api/v1/cracks/installations/{id}/reference

POST /api/v1/cracks/installations/{id}/process

GET  /api/v1/cracks/installations/{id}/measurements

GET  /api/v1/cracks/installations/{id}/comparison
```

---

# 97. Processamento assíncrono

Se o processamento não puder terminar rapidamente:

```text
POST
 ↓
202 Accepted
 ↓
job_id
 ↓
worker
 ↓
processing
 ↓
result
```

---

# 98. Event Bus

Eventos poderão incluir:

```text
CrackImageCaptured

CrackReferenceCreated

CrackMeasurementCreated

CrackChangeDetected

CrackProcessingFailed
```

---

# 99. Segurança

O processamento deverá respeitar:

```text
tenant_id
installation_id
camera_id
authorization
```

Não permitir que uma instalação acesse imagens de outra.

---

# 100. Regra Multi-Tenant

Toda imagem, referência e medição deverá estar associada ao Tenant.

Nunca executar consulta global sem isolamento.

---

# 101. Primeira implementação

A primeira implementação NÃO deverá começar pelo treinamento da fissura.

Ordem obrigatória:

```text
1. Label Detector

2. ROI

3. Homography

4. Canonical Coordinates

5. Marker Detection

6. Line Detection

7. Geometry

8. Reference

9. Current Image

10. Comparison

11. Crack Detection

12. ML Optimization
```

---

# 102. Objetivo da primeira prova

Com uma fotografia real:

```text
Imagem completa
```

o sistema deverá conseguir gerar:

```text
Etiqueta detectada
```

e:

```text
Imagem retificada da etiqueta
```

sem analisar objetos externos.

---

# 103. Objetivo da segunda prova

Na etiqueta retificada:

```text
6 marcadores
+
círculo
+
AB
+
CD
```

deverão ser identificados.

---

# 104. Objetivo da terceira prova

Calcular:

```text
distâncias
ângulos
interseção
```

com erro mensurável.

---

# 105. Objetivo da quarta prova

Cadastrar:

```text
T0 = referência
```

e depois:

```text
T1
```

e calcular as diferenças.

---

# 106. Objetivo da quinta prova

Detectar:

```text
fissura
```

e calcular:

```text
largura
comprimento
orientação
```

---

# 107. Regra final para o OpenCode

**NÃO interpretar este módulo como um problema genérico de detecção de objetos.**

Este é um problema de:

```text
VISÃO COMPUTACIONAL CONTROLADA POR GEOMETRIA
```

A ordem é obrigatória:

```text
┌──────────────────────────────┐
│       IMAGEM DA CÂMERA       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      DETECTAR ETIQUETA       │
│       único detector         │
│ permitido na imagem inteira  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        LABEL ROI             │
│     excluir todo exterior    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        HOMOGRAFIA             │
│      RETIFICAÇÃO              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│    ETIQUETA NORMALIZADA      │
└──────────────┬───────────────┘
               │
       ┌───────┼────────┐
       │       │        │
       ▼       ▼        ▼
    6 PONTOS AB/CD   CÍRCULO
       │       │        │
       └───────┼────────┘
               ▼
       GEOMETRIA INTERNA
               │
               ▼
           FISSURA
               │
               ▼
          MEDIÇÕES
               │
               ▼
          REFERÊNCIA
               │
               ▼
       COMPARAÇÃO TEMPORAL
               │
               ▼
            EVENTO
```

**Esta ordem não deverá ser alterada sem atualização deste documento.**

---

# 108. Critério definitivo de implementação

O pipeline somente será considerado correto quando:

1. Objetos externos à etiqueta não forem processados.
2. Círculos externos não gerarem detecções.
3. Linhas externas não gerarem detecções.
4. A etiqueta for localizada primeiro.
5. A ROI for criada antes dos detectores internos.
6. A perspectiva for corrigida antes das medições.
7. Os seis marcadores forem identificados por posição lógica.
8. AB e CD forem identificados somente dentro da etiqueta.
9. A fissura for analisada somente na região apropriada.
10. As medições forem armazenadas.
11. A referência puder ser criada manualmente pelo usuário.
12. Novas imagens puderem ser comparadas com a referência.
13. Cada resultado possuir versão de modelo e algoritmo.
14. O sistema puder produzir imagens intermediárias de diagnóstico.
15. O sistema possuir testes específicos contra falsos positivos externos.

---

# 109. Instrução final ao OpenCode

Antes de implementar qualquer detector adicional, verificar:

```text
"Este detector está recebendo a imagem completa?"
```

Se a resposta for:

```text
SIM
```

e o detector não for o `Label Detector`:

```text
NÃO IMPLEMENTAR.
```

A pergunta obrigatória para cada etapa interna deverá ser:

> **"Qual é a ROI exata onde este elemento pode existir?"**

Se não existir uma ROI definida, a etapa ainda não está pronta para implementação.

**Fim do Documento**
