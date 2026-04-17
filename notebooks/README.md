# Parasyte Notebooks

## Entrenamiento

### 1. parasyte_lfm_training.ipynb

Fine-tuning de LFM 2.5-1.2B para CDP.

**Pasos:**
1. Clonar repositorio
2. Cargar dataset `cdp_training_v2.json`
3. Descargar modelo base de Liquid AI
4. Aplicar LoRA (rank 16)
5. Entrenar 3 epochs
6. Guardar modelo

**Tiempo estimado:** 2-4 horas (T4/A100)

---

### 2. export_gguf.ipynb

Exportar modelo fine-tuned a formato GGUF.

**Para que sirve:**
- Inference local con llama.cpp
- Sin necesidad de GPU
- Deployment en edge devices

**Tamaños comunes:**
- Q4_K_M: ~1.2GB (recomendado)
- Q5_K_M: ~1.4GB
- Q8_0: ~2.4GB

---

## Dataset

Dataset en `../data/cdp_training_v2.json`:
- 500 ejemplos
- Mapeo semantico instruction -> CDP command
- 8 categorias
- 21 comandos unicos

---

## Requisitos

- Google Colab con GPU (T4 o superior)
- Cuenta de HuggingFace
- 15GB+ espacio en Drive

---

## Flujo completo

```
1. Entrenar (parasyte_lfm_training.ipynb)
   ↓
2. Descargar modelo fine-tuned
   ↓
3. Exportar a GGUF (export_gguf.ipynb)
   ↓
4. Usar con Parasyte
```
