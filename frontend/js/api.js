/* ============================================================
   KUSIPUBLISHER - API.JS - Conexión con Backend FastAPI
   ============================================================ */

const BASE_URL = 'http://localhost:8000';

// Helper para manejar errores de API
function handleApiError(error, endpoint) {
  console.error(`API Error en ${endpoint}:`, error);
  
  let message = 'Error de conexión con el servidor';
  
  if (error.message.includes('Failed to fetch')) {
    message = 'No se pudo conectar con el servidor. Asegúrate de que el backend esté ejecutándose en http://localhost:8000';
  } else if (error.message.includes('404')) {
    message = 'Endpoint no encontrado en el servidor';
  } else if (error.message.includes('500')) {
    message = 'Error interno del servidor';
  }
  
  // Mostrar error al usuario
  if (typeof showToast === 'function') {
    showToast(`❌ ${message}`, 'error');
  }
  
  throw new Error(message);
}

// Helper GET para llamadas a la API
async function apiGet(endpoint) {
  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    handleApiError(error, endpoint);
  }
}

// Helper POST para llamadas a la API
async function apiPost(endpoint, data) {
  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    handleApiError(error, endpoint);
  }
}

// ============================================================
// FUNCIONES ESPECÍFICAS DE LA API
// ============================================================

/**
 * Genera contenido optimizado para una plataforma específica
 * @param {string} platform - Plataforma destino (linkedin, twitter, instagram, facebook, blog)
 * @param {string} title - Título del contenido
 * @param {string} content - Contenido maestro
 * @returns {Promise<Object>} - Contenido generado y metadata
 */
async function generateContent(platform, title, content) {
  return apiPost('/content', {
    campaign_id: 1,
    title: title,
    original_text: content,
    platform: platform
  });
}

/**
 * Analiza la calidad del contenido proporcionado
 * @param {string} content - Contenido a analizar
 * @returns {Promise<Object>} - Score y métricas de calidad
 */
async function analyzeQuality(content) {
  return apiPost('/analyze/quality', {
    content: content
  });
}

/**
 * Analiza el tono y estilo de voz de textos de ejemplo
 * @param {Array<string>} texts - Array de textos para analizar el estilo
 * @returns {Promise<Object>} - Análisis del tono y estilo
 */
async function analyzeVoice(texts) {
  return apiPost('/analyze/voice', {
    texts: texts
  });
}

/**
 * Investiga palabras clave y hashtags para un tema específico
 * @param {string} topic - Tema a investigar
 * @param {string} platform - Plataforma objetivo
 * @returns {Promise<Object>} - Keywords, hashtags y sugerencias
 */
async function researchSEO(topic, platform) {
  return apiPost('/research/seo', {
    topic: topic,
    platform: platform
  });
}

/**
 * Humaniza el contenido para hacerlo más natural
 * @param {string} content - Contenido a humanizar
 * @returns {Promise<Object>} - Contenido humanizado
 */
async function humanizeContent(content) {
  return apiPost('/humanize', {text: content});
}

/**
 * Optimiza contenido para una plataforma específica
 * @param {string} content - Contenido a optimizar
 * @param {string} platform - Plataforma objetivo
 * @returns {Promise<Object>} - Contenido optimizado
 */
async function optimizePlatform(content, platform) {
  return apiPost('/optimize/platform', {
    content: content,
    platform: platform
  });
}

/**
 * Consulta al oráculo para análisis estratégico
 * @param {string} query - Pregunta o consulta estratégica
 * @param {Object} context - Contexto adicional opcional
 * @returns {Promise<Object>} - Análisis y recomendaciones
 */
async function consultOracle(query, context = {}) {
  return apiPost('/oracle/consult', {
    question: query, // Cambiar 'query' a 'question'
    context: context
  });
}

/**
 * Sugiere ideas visuales para el contenido
 * @param {string} content - Contenido base
 * @returns {Promise<Object>} - Ideas visuales con prompts para AI
 */
async function suggestVisuals(content) {
  return apiPost('/visual/suggest', {
    content: content
  });
}

/**
 * Obtiene el historial de versiones de un contenido
 * @param {string|number} id - ID del contenido
 * @returns {Promise<Object>} - Historial de versiones
 */
async function getContentHistory(id) {
  return apiGet(`/content/${id}/history`);
}

/**
 * Inicia una sesión de planificación estratégica
 * @param {string} brief - Descripción inicial del proyecto
 * @returns {Promise<Object>} - Sesión de planificación con preguntas y sugerencias
 */
async function startPlanning(brief) {
  return apiPost('/planning/start', {
    brief: brief
  });
}

/**
 * Obtiene la lista de proveedores LLM disponibles
 * @returns {Promise<Object>} - Lista de proveedores (gemini, openai, anthropic)
 */
async function getLLMProviders() {
  return apiGet('/llm/providers');
}

/**
 * Cambia el proveedor LLM activo
 * @param {string} provider - Nombre del proveedor (gemini, openai, anthropic)
 * @returns {Promise<Object>} - Confirmación del cambio
 */
async function switchLLM(provider) {
  return apiPost('/llm/switch', {
    provider: provider
  });
}

/**
 * Verifica la salud del servidor backend
 * @returns {Promise<Object>} - Estado del servidor
 */
async function checkHealth() {
  try {
    return await apiGet('/api/health');
  } catch (error) {
    return { status: 'error', message: error.message };
  }
}

// ============================================================
// FUNCIONES DE UTILIDAD Y BATCH PROCESSING
// ============================================================

/**
 * Genera contenido para múltiples plataformas en paralelo
 * @param {string} title - Título del contenido
 * @param {string} content - Contenido maestro
 * @param {Array<string>} platforms - Array de plataformas
 * @returns {Promise<Object>} - Resultados de todas las plataformas
 */
async function generateForAllPlatforms(title, content, platforms = ['linkedin', 'twitter', 'instagram', 'facebook', 'blog']) {
  try {
    // Crear array de promesas para generación paralela
    const promises = platforms.map(platform => 
      generateContent(platform, title, content).catch(error => ({
        platform,
        error: error.message,
        generated_content: null
      }))
    );
    
    // Esperar a que todas se completen
    const results = await Promise.all(promises);
    
    // Organizar resultados por plataforma
    const platformResults = {};
    results.forEach((result, index) => {
      const platform = platforms[index];
      platformResults[platform] = result;
    });
    
    return platformResults;
  } catch (error) {
    console.error('Error en generación batch:', error);
    throw error;
  }
}

/**
 * Analiza la calidad de múltiples contenidos en paralelo
 * @param {Object} contents - Objeto con contenidos por plataforma
 * @returns {Promise<Object>} - Scores por plataforma
 */
async function analyzeMultipleQualities(contents) {
  try {
    const promises = Object.entries(contents).map(([platform, content]) => {
      if (!content || content.error) {
        return Promise.resolve({
          platform,
          score: 0,
          error: content?.error || 'Sin contenido'
        });
      }
      
      return analyzeQuality(content.generated_content || content)
        .then(result => ({ platform, ...result }))
        .catch(error => ({
          platform,
          score: 0,
          error: error.message
        }));
    });
    
    const results = await Promise.all(promises);
    
    // Organizar resultados por plataforma
    const qualityResults = {};
    results.forEach(result => {
      qualityResults[result.platform] = result;
    });
    
    return qualityResults;
  } catch (error) {
    console.error('Error en análisis batch:', error);
    throw error;
  }
}

/**
 * Pipeline completo: Genera contenido y analiza calidad
 * @param {string} title - Título del contenido
 * @param {string} content - Contenido maestro
 * @returns {Promise<Object>} - Contenido generado y análisis de calidad
 */
async function fullPipeline(title, content) {
  try {
    console.log('Iniciando pipeline completo...');
    
    // Paso 1: Generar contenido para todas las plataformas
    const generatedContent = await generateForAllPlatforms(title, content);
    
    // Paso 2: Analizar calidad de todo el contenido generado
    const qualityAnalysis = await analyzeMultipleQualities(generatedContent);
    
    // Paso 3: Combinar resultados
    const results = {
      generated: generatedContent,
      quality: qualityAnalysis,
      timestamp: new Date().toISOString()
    };
    
    console.log('Pipeline completado exitosamente');
    return results;
    
  } catch (error) {
    console.error('Error en pipeline completo:', error);
    throw error;
  }
}

// ============================================================
// MANEJO DE CACHÉ Y ALMACENAMIENTO LOCAL
// ============================================================

/**
 * Guarda datos en localStorage con timestamp
 * @param {string} key - Clave de almacenamiento
 * @param {any} data - Datos a guardar
 * @param {number} ttl - Tiempo de vida en minutos (por defecto 60)
 */
function saveToCache(key, data, ttl = 60) {
  const item = {
    data: data,
    timestamp: Date.now(),
    ttl: ttl * 60 * 1000 // Convertir a milisegundos
  };
  localStorage.setItem(`kusi_${key}`, JSON.stringify(item));
}

/**
 * Recupera datos del caché si aún son válidos
 * @param {string} key - Clave de almacenamiento
 * @returns {any|null} - Datos si son válidos, null si expiraron o no existen
 */
function getFromCache(key) {
  const itemStr = localStorage.getItem(`kusi_${key}`);
  if (!itemStr) return null;
  
  try {
    const item = JSON.parse(itemStr);
    const now = Date.now();
    
    // Verificar si el item aún es válido
    if (now - item.timestamp > item.ttl) {
      localStorage.removeItem(`kusi_${key}`);
      return null;
    }
    
    return item.data;
  } catch (error) {
    console.error('Error leyendo caché:', error);
    localStorage.removeItem(`kusi_${key}`);
    return null;
  }
}

/**
 * Limpia todo el caché de la aplicación
 */
function clearCache() {
  const keys = Object.keys(localStorage);
  keys.forEach(key => {
    if (key.startsWith('kusi_')) {
      localStorage.removeItem(key);
    }
  });
}

// ============================================================
// EXPORTAR FUNCIONES PARA USO GLOBAL
// ============================================================

// Hacer funciones disponibles globalmente
window.KusiAPI = {
  // Funciones principales
  generateContent,
  analyzeQuality,
  analyzeVoice,
  researchSEO,
  humanizeContent,
  optimizePlatform,
  consultOracle,
  suggestVisuals,
  getContentHistory,
  startPlanning,
  getLLMProviders,
  switchLLM,
  checkHealth,
  
  // Funciones batch
  generateForAllPlatforms,
  analyzeMultipleQualities,
  fullPipeline,
  
  // Funciones de caché
  saveToCache,
  getFromCache,
  clearCache,
  
  // Constantes
  BASE_URL
};

// Log de inicialización
console.log('KusiAPI inicializado correctamente');