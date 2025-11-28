/* ============================================================
   KUSIPUBLISHER - EDITOR.JS - Lógica Principal del Editor
   ============================================================ */

// Estado global de la aplicación
let editorState = {
  title: '',
  content: '',
  platforms: {
    linkedin: null,
    twitter: null,
    instagram: null,
    facebook: null,
    blog: null
  },
  scores: {},
  keywords: [],
  visualIdeas: [],
  isGenerating: false,
  lastGenerated: null
};

// Configuración de plataformas
const PLATFORM_CONFIG = {
  linkedin: {
    name: 'LinkedIn',
    icon: '📘',
    color: '#0077B5',
    description: 'Contenido profesional y networking'
  },
  twitter: {
    name: 'Twitter/X',
    icon: '🐦',
    color: '#1DA1F2',
    description: 'Mensajes concisos y virales'
  },
  instagram: {
    name: 'Instagram',
    icon: '📷',
    color: '#E4405F',
    description: 'Contenido visual y emocional'
  },
  facebook: {
    name: 'Facebook',
    icon: '👥',
    color: '#1877F2',
    description: 'Contenido conversacional'
  },
  blog: {
    name: 'Blog',
    icon: '📝',
    color: '#FF6B35',
    description: 'Contenido largo y detallado'
  }
};

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
  initializeEditor();
});

/**
 * Inicializa el editor y configura todos los event listeners
 */
function initializeEditor() {
  console.log('Inicializando KusiPublisher Editor...');
  
  // Configurar event listeners principales
  setupEventListeners();
  
  // Cargar estado guardado si existe
  loadEditorState();
  
  // Verificar conexión con backend
  checkBackendConnection();
  
  console.log('Editor inicializado correctamente');
}

/**
 * Configura todos los event listeners del editor
 */
function setupEventListeners() {
  // Inputs del editor
  const titleInput = document.getElementById('inputTitle');
  const contentInput = document.getElementById('inputContent');
  
  if (titleInput) {
    titleInput.addEventListener('input', debounce(handleTitleChange, 300));
  }
  
  if (contentInput) {
    contentInput.addEventListener('input', debounce(handleContentChange, 500));
  }
  
  // Botones de acción principales
  const btnGenerate = document.getElementById('btnGenerate');
  const btnQuality = document.getElementById('btnQuality');
  const btnHumanize = document.getElementById('btnHumanize');
  const btnOracle = document.getElementById('btnOracle');
  
  if (btnGenerate) {
    btnGenerate.addEventListener('click', generateAllPlatforms);
  }
  
  if (btnQuality) {
    btnQuality.addEventListener('click', analyzeAllQuality);
  }
  
  if (btnHumanize) {
    btnHumanize.addEventListener('click', humanizeAllContent);
  }
  
  if (btnOracle) {
    btnOracle.addEventListener('click', openOracleModal);
  }
  
  // Botones de copiar en cada preview
  setupCopyButtons();
  
  // Guardar estado al salir de la página
  window.addEventListener('beforeunload', saveEditorState);
}

/**
 * Maneja cambios en el título
 */
function handleTitleChange(event) {
  editorState.title = event.target.value;
  updateGenerateButtonState();
  
  // Auto-guardar
  saveEditorState();
}

/**
 * Maneja cambios en el contenido
 */
function handleContentChange(event) {
  editorState.content = event.target.value;
  updateGenerateButtonState();
  
  // Auto-guardar
  saveEditorState();
  
  // Si hay suficiente contenido, sugerir keywords
  if (editorState.content.length > 50) {
    debounce(suggestKeywords, 1000)();
  }
}

/**
 * Actualiza el estado del botón generar según los inputs
 */
function updateGenerateButtonState() {
  const btnGenerate = document.getElementById('btnGenerate');
  const hasTitle = editorState.title.trim().length > 0;
  const hasContent = editorState.content.trim().length > 0;
  const hasMinContent = editorState.content.trim().length >= 10;
  
  if (btnGenerate) {
    btnGenerate.disabled = !hasTitle || !hasContent || !hasMinContent || editorState.isGenerating;
    
    // Actualizar texto del botón
    if (editorState.isGenerating) {
      btnGenerate.innerHTML = '<span class="spinner"></span> Generando...';
    } else {
      btnGenerate.innerHTML = '✨ Generar Todo';
    }
  }
}

/**
 * Genera contenido para todas las plataformas
 */
async function generateAllPlatforms() {
  if (editorState.isGenerating) return;
  
  const title = editorState.title.trim();
  const content = editorState.content.trim();
  
  if (!title || !content || content.length < 10) {
    showToast('⚠️ Por favor ingresa un título y contenido (mínimo 10 caracteres)', 'warning');
    return;
  }
  
  console.log('Iniciando generación para todas las plataformas...');
  
  // Actualizar estado
  editorState.isGenerating = true;
  updateGenerateButtonState();
  
  // Mostrar loading en todas las cards
  showAllLoadingStates(true);
  
  try {
    // Generar contenido para todas las plataformas en paralelo
    const platforms = Object.keys(PLATFORM_CONFIG);
    const generationPromises = platforms.map(platform => 
      generatePlatformContent(platform, title, content)
    );
    
    // Esperar a que todas las generaciones se completen
    const results = await Promise.allSettled(generationPromises);
    
    // Procesar resultados
    let successCount = 0;
    results.forEach((result, index) => {
      const platform = platforms[index];
      if (result.status === 'fulfilled' && result.value) {
        editorState.platforms[platform] = result.value;
        updatePreview(platform, result.value);
        successCount++;
      } else {
        console.error(`Error generando ${platform}:`, result.reason);
        updatePreviewError(platform, result.reason || 'Error de generación');
      }
    });
    
    // Actualizar timestamp de última generación
    editorState.lastGenerated = new Date().toISOString();
    
    // Mostrar resultado
    if (successCount === platforms.length) {
      showToast('✅ Contenido generado exitosamente para todas las plataformas', 'success');
      
      // Analizar calidad automáticamente después de 2 segundos
      setTimeout(() => {
        analyzeAllQuality();
      }, 2000);
      
    } else if (successCount > 0) {
      showToast(`⚠️ Contenido generado para ${successCount} de ${platforms.length} plataformas`, 'warning');
    } else {
      showToast('❌ No se pudo generar contenido para ninguna plataforma', 'error');
    }
    
  } catch (error) {
    console.error('Error en generación:', error);
    showToast('❌ Error al generar contenido: ' + error.message, 'error');
  } finally {
    // Restaurar estado
    editorState.isGenerating = false;
    updateGenerateButtonState();
    showAllLoadingStates(false);
  }
}

/**
 * Genera contenido para una plataforma específica
 */
async function generatePlatformContent(platform, title, content) {
  try {
    console.log(`Generando contenido para ${platform}...`);
    
    const result = await window.KusiAPI.generateContent(platform, title, content);
    
    if (result && typeof result.generated_content === 'string') { // Permitir string vacío
      console.log(`✅ Contenido generado para ${platform}`);
      result.isHumanized = false; // Inicializar como no humanizado
      return result;
    } else {
      throw new Error('Respuesta inválida del servidor');
    }
    
  } catch (error) {
    console.error(`❌ Error generando ${platform}:`, error);
    throw error;
  }
}

/**
 * Analiza la calidad de todos los contenidos generados
 */
async function analyzeAllQuality() {
  console.log('=== INICIO ANÁLISIS CALIDAD ==='); // 1
  const platforms = Object.keys(PLATFORM_CONFIG);
  let analyzedCount = 0;
  
  console.log('Plataformas a analizar:', platforms); // 2
  console.log('Iniciando análisis de calidad...');
  
  for (const platform of platforms) {
    const content = editorState.platforms[platform];
    console.log('Analizando plataforma:', platform, 'Contenido:', content); // 3
    
    if (content && content.generated_content) {
      try {
        console.log('Llamando API con:', content.generated_content); // 4
        const analysis = await window.KusiAPI.analyzeQuality(content.generated_content);
        console.log('Respuesta API:', analysis); // 5
        
        if (analysis && analysis.quality_score !== undefined) {
          editorState.scores[platform] = analysis;
          updateScoreDisplay(platform, analysis.quality_score);
          console.log('✅ Score actualizado:', platform, analysis.quality_score);
          analyzedCount++; // Asegurarse de que esta línea esté bien identada
          console.log(`✅ Calidad analizada para ${platform}: ${analysis.quality_score}%`);
        }
      } catch (error) {
        console.log('ERROR COMPLETO:', error); // 6
        console.error(`❌ Error analizando calidad de ${platform}:`, error);
        updateScoreDisplay(platform, 0);
      }
    }
  }
  
  if (analyzedCount > 0) {
    console.log(`Análisis de calidad completado para ${analyzedCount} plataformas`);
    updateGlobalScore();
  }
}

/**
 * Humaniza todos los contenidos generados
 */
async function humanizeAllContent() {
  console.log('=== INICIO HUMANIZACIÓN ==='); // Similar to 1
  const platforms = Object.keys(PLATFORM_CONFIG);
  let humanizedCount = 0;
  
  console.log('Plataformas a humanizar:', platforms); // Similar to 2
  console.log('Humanizando contenidos...');
  showToast('🔄 Humanizando contenidos...', 'info');
  
  for (const platform of platforms) {
    const content = editorState.platforms[platform];
    console.log('Humanizando plataforma:', platform, 'Contenido:', content); // Similar to 3
    
    if (content && content.generated_content) {
      try {
        console.log('Llamando API con:', content.generated_content); // Similar to 4
        const result = await window.KusiAPI.humanizeContent(content.generated_content);
        console.log('Respuesta API:', result); // Similar to 5
        
        if (result && result.humanized_content) {
          // Actualizar contenido humanizado
          editorState.platforms[platform].generated_content = result.humanized_content;
          editorState.platforms[platform].isHumanized = true; // Marcar como humanizado
          updatePreview(platform, editorState.platforms[platform]);
          humanizedCount++;
          console.log(`✅ Contenido humanizado para ${platform}`);
        }
      } catch (error) {
        console.log('ERROR COMPLETO:', error); // Similar to 6
        console.error(`❌ Error humanizando ${platform}:`, error);
      }
    }
  }
  
  if (humanizedCount > 0) {
    showToast(`✅ ${humanizedCount} contenidos humanizados exitosamente`, 'success');
    
    // Re-analizar calidad después de humanizar
    setTimeout(() => {
      analyzeAllQuality();
    }, 1000);
  } else {
    showToast('⚠️ No se pudo humanizar ningún contenido', 'warning');
  }
}

/**
 * Actualiza la visualización de un preview
 */
function updatePreview(platform, contentData) {
  const card = document.getElementById(`card-${platform}`);
  const contentElement = card?.querySelector('.preview-content');
  const humanizedIndicator = document.getElementById(`humanized-${platform}`); // Obtener el indicador

  console.log(`DEBUG: updatePreview llamado para ${platform}. contentData:`, contentData);
  console.log(`DEBUG: contentElement para ${platform}:`, contentElement);
  console.log(`DEBUG: contentData.generated_content para ${platform}:`, contentData.generated_content);

  if (contentElement && typeof contentData.generated_content === 'string') { // Verificar el tipo para permitir string vacío
    console.log(`DEBUG: *** Actualizando preview con contenido para ${platform} ***`, contentData.generated_content.substring(0, 100) + '...');
    contentElement.textContent = contentData.generated_content;
    
    // Actualizar el indicador de humanización
    if (humanizedIndicator) {
        if (contentData.isHumanized) {
            humanizedIndicator.classList.add('is-humanized');
            humanizedIndicator.title = 'Contenido Humanizado';
        } else {
            humanizedIndicator.classList.remove('is-humanized');
            humanizedIndicator.title = 'Contenido Original';
        }
    }

    // Animar la actualización
    card.style.transform = 'scale(1.02)';
    setTimeout(() => {
      card.style.transform = 'scale(1)';
    }, 200);
  } else {
    console.warn(`WARNING: Condición de updatePreview fallida para ${platform}. contentElement:`, contentElement, ', generated_content type:', typeof contentData.generated_content, ', value:', contentData.generated_content);
  }
}

/**
 * Muestra error en preview
 */
function updatePreviewError(platform, error) {
  const card = document.getElementById(`card-${platform}`);
  const contentElement = card?.querySelector('.preview-content');
  
  if (contentElement) {
    contentElement.innerHTML = `<span style="color: var(--danger);">❌ Error: ${error}</span>`;
  }
}

/**
 * Actualiza la visualización del score
 */
function updateScoreDisplay(platform, score) {
  console.log(`DEBUG: updateScoreDisplay llamado para ${platform}. Recibido score:`, score);
  const card = document.getElementById(`card-${platform}`);
  const scoreBar = card?.querySelector('.score-bar');
  const scoreValue = card?.querySelector('.score-value');
  
  if (scoreBar && scoreValue) {
    scoreBar.style.width = `${score}%`;
    scoreValue.textContent = `${score}%`;
    
    // Actualizar clase según score
    scoreBar.className = 'score-bar';
    if (score >= 85) {
      scoreBar.classList.add('excellent');
    } else if (score >= 70) {
      scoreBar.classList.add('good');
    } else {
      scoreBar.classList.add('warning');
    }
  }
}

/**
 * Calcula y actualiza el score global
 */
function updateGlobalScore() {
  const scores = Object.values(editorState.scores);
  
  if (scores.length === 0) return;
  
  const validScores = scores.filter(s => s && s.score > 0);
  
  if (validScores.length === 0) return;
  
  const averageScore = Math.round(
    validScores.reduce((sum, s) => sum + s.score, 0) / validScores.length
  );
  
  const globalScoreBar = document.querySelector('.score-bar-large');
  if (globalScoreBar) {
    globalScoreBar.style.width = `${averageScore}%`;
    globalScoreBar.textContent = `${averageScore}%`;
  }
}

/**
 * Configura los botones de copiar
 */
function setupCopyButtons() {
  document.querySelectorAll('.btn-copy').forEach(button => {
    button.addEventListener('click', function() {
      const platform = this.dataset.platform;
      copyPlatformContent(platform);
    });
  });
}

/**
 * Copia el contenido de una plataforma al portapapeles
 */
async function copyPlatformContent(platform) {
  const content = editorState.platforms[platform];
  
  if (!content || !content.generated_content) {
    showToast('⚠️ No hay contenido para copiar', 'warning');
    return;
  }
  
  try {
    await navigator.clipboard.writeText(content.generated_content);
    showToast(`✅ Contenido de ${PLATFORM_CONFIG[platform].name} copiado`, 'success');
    
    // Efecto visual en el botón
    const button = document.querySelector(`[data-platform="${platform}"]`);
    if (button) {
      const originalText = button.textContent;
      button.textContent = '✓ Copiado';
      button.style.background = 'var(--success)';
      
      setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '';
      }, 2000);
    }
  } catch (error) {
    console.error('Error copiando al portapapeles:', error);
    showToast('❌ Error al copiar contenido', 'error');
  }
}

/**
 * Muestra/oculta estados de loading en todas las cards
 */
function showAllLoadingStates(loading) {
  Object.keys(PLATFORM_CONFIG).forEach(platform => {
    const card = document.getElementById(`card-${platform}`);
    const contentElement = card?.querySelector('.preview-content');
    
    if (card && contentElement) {
      if (loading) {
        card.classList.add('loading');
        contentElement.innerHTML = '<span class="spinner"></span> Generando contenido optimizado...';
      } else {
        card.classList.remove('loading');
      }
    }
  });
}

/**
 * Sugiere keywords basadas en el contenido
 */
async function suggestKeywords() {
  if (!editorState.title && !editorState.content) return;
  
  try {
    const topic = editorState.title || editorState.content.substring(0, 100);
    const result = await window.KusiAPI.researchSEO(topic, 'linkedin');
    
    if (result && result.keywords) {
      editorState.keywords = result.keywords.slice(0, 8); // Limitar a 8 keywords
      updateKeywordsDisplay();
    }
  } catch (error) {
    console.error('Error sugiriendo keywords:', error);
  }
}

/**
 * Actualiza la visualización de keywords
 */
function updateKeywordsDisplay() {
  const keywordsList = document.getElementById('keywordList');
  if (keywordsList && editorState.keywords.length > 0) {
    keywordsList.innerHTML = editorState.keywords
      .map(keyword => `<li>• ${keyword}</li>`)
      .join('');
  }
}

/**
 * Abre modal del oráculo (placeholder)
 */
async function openOracleModal() {
  const userQuestion = prompt('🔮 Ingresa tu pregunta para el Oráculo:');

  if (!userQuestion || userQuestion.trim() === '') {
    showToast('⚠️ La pregunta no puede estar vacía.', 'warning');
    return;
  }

  showToast('🔮 Consultando al Oráculo...', 'info');
  editorState.isGenerating = true; // Usar el estado existente para deshabilitar botones
  updateGenerateButtonState(); // Actualizar el estado de los botones

  try {
    console.log('DEBUG: Llamando a KusiAPI.consultOracle con pregunta:', userQuestion);
    const result = await window.KusiAPI.consultOracle(userQuestion);
    
    if (result && result.consultation) {
      showToast('✅ Consulta al Oráculo exitosa. Revisa la consola para el análisis detallado.', 'success');
      console.log('🔮 Respuesta del Oráculo:', result); // Loguear el objeto completo
      
      // Mostrar la respuesta en el modal
      displayOracleResponseInModal(userQuestion, result);

    } else {
      console.log('DEBUG: Respuesta de KusiAPI.consultOracle (falló la condición):', result); // Log para ver qué llega
      throw new Error('Respuesta inválida del Oráculo: El análisis principal no se encontró.');
    }
  } catch (error) {
    console.error('❌ Error al consultar el Oráculo:', error);
    showToast('❌ Error al consultar el Oráculo: ' + error.message, 'error');
  } finally {
    editorState.isGenerating = false;
    updateGenerateButtonState();
  }
}

/**
 * Guarda el estado del editor en localStorage
 */
function saveEditorState() {
  try {
    const stateToSave = {
      title: editorState.title,
      content: editorState.content,
      lastSaved: new Date().toISOString()
    };
    
    window.KusiAPI.saveToCache('editor_state', stateToSave, 1440); // 24 horas
  } catch (error) {
    console.error('Error guardando estado:', error);
  }
}

/**
 * Carga el estado del editor desde localStorage
 */
function loadEditorState() {
  try {
    const savedState = window.KusiAPI.getFromCache('editor_state');
    
    if (savedState) {
      editorState.title = savedState.title || '';
      editorState.content = savedState.content || '';
      
      // Actualizar UI
      const titleInput = document.getElementById('inputTitle');
      const contentInput = document.getElementById('inputContent');
      
      if (titleInput) titleInput.value = editorState.title;
      if (contentInput) contentInput.value = editorState.content;
      
      updateGenerateButtonState();
      
      console.log('Estado del editor restaurado');
    }
  } catch (error) {
    console.error('Error cargando estado:', error);
  }
}

/**
 * Verifica la conexión con el backend
 */
async function checkBackendConnection() {
  try {
    const health = await window.KusiAPI.checkHealth();
    
    if (health && health.status === 'healthy') {
      console.log('✅ Backend conectado correctamente');
      
      // Mostrar indicador de conexión si existe
      const statusIndicator = document.querySelector('.status-dot');
      if (statusIndicator) {
        statusIndicator.classList.add('connected');
      }
    } else {
      console.warn('⚠️ Backend no disponible');
      showToast('⚠️ Backend no disponible. Algunas funciones pueden no funcionar.', 'warning');
    }
  } catch (error) {
    console.error('❌ Error conectando con backend:', error);
    showToast('❌ No se pudo conectar con el backend', 'error');
  }
}

/**
 * Función debounce para optimizar llamadas frecuentes
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Muestra notificaciones toast
 */
function showToast(message, type = 'info') {
  // Crear elemento toast
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = message;
  
  // Agregar al DOM
  document.body.appendChild(toast);
  
  // Mostrar con animación
  setTimeout(() => toast.classList.add('show'), 100);
  
  // Remover después de 3 segundos
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 3000);
}

// Hacer funciones disponibles globalmente
window.EditorJS = {
  generateAllPlatforms,
  analyzeAllQuality,
  humanizeAllContent,
  copyPlatformContent,
  showToast
};

console.log('EditorJS cargado correctamente');

/**
 * Muestra la respuesta del Oráculo en un modal
 */
function displayOracleResponseInModal(question, response) {
    const oracleModal = document.getElementById('oracleModal');
    const oracleQuestionDiv = document.getElementById('oracleQuestion');
    const oracleResponseDiv = document.getElementById('oracleResponse');
    const copyButton = document.getElementById('copyOracleResponse');

    if (!oracleModal || !oracleQuestionDiv || !oracleResponseDiv) {
        console.error('ERROR: Elementos del modal del Oráculo no encontrados.');
        showToast('❌ Error interno al mostrar la respuesta del Oráculo.', 'error');
        return;
    }

    oracleQuestionDiv.textContent = `Pregunta: "${question}"`;
    oracleResponseDiv.innerHTML = marked.parse(response.consultation); // Renderizar Markdown a HTML

    copyButton.onclick = async () => {
        try {
            await navigator.clipboard.writeText(response.consultation);
            showToast('📋 Respuesta copiada al portapapeles', 'success');
        } catch (err) {
            console.error('Error al copiar la respuesta del Oráculo:', err);
            showToast('❌ Error al copiar al portapapeles', 'error');
        }
    };

    showModal(oracleModal);
}

/**
 * Muestra un modal genérico
 */
function showModal(modalElement) {
    modalElement.style.display = 'block';
    document.getElementById('modalOverlay').style.display = 'block';
}

/**
 * Oculta un modal genérico
 */
function hideModal(modalElement) {
    modalElement.style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
}

// Configurar event listeners para cerrar el modal del Oráculo
document.addEventListener('DOMContentLoaded', () => {
    const oracleModal = document.getElementById('oracleModal');
    if (oracleModal) {
        oracleModal.querySelector('.close-button').onclick = () => hideModal(oracleModal);
        document.getElementById('modalOverlay').onclick = () => hideModal(oracleModal);
        window.onclick = (event) => {
            if (event.target == oracleModal) { hideModal(oracleModal); }
        };
    }
});