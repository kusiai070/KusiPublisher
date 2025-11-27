/* ============================================================
   KUSIPUBLISHER - UTILS.JS - Funciones Compartidas y Utilidades
   ============================================================ */

/**
 * Función debounce para limitar la frecuencia de llamadas
 * @param {Function} func - Función a ejecutar
 * @param {number} wait - Tiempo de espera en milisegundos
 * @returns {Function} - Función debounce
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
 * Función throttle para limitar la frecuencia de ejecución
 * @param {Function} func - Función a ejecutar
 * @param {number} limit - Límite de tiempo en milisegundos
 * @returns {Function} - Función throttle
 */
function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * Formatea fecha y hora de manera legible
 * @param {string|Date} date - Fecha a formatear
 * @param {string} format - Formato deseado
 * @returns {string} - Fecha formateada
 */
function formatDate(date, format = 'relative') {
  const d = new Date(date);
  const now = new Date();
  
  if (format === 'relative') {
    const diffInSeconds = Math.floor((now - d) / 1000);
    
    if (diffInSeconds < 60) return 'Justo ahora';
    if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60);
      return `Hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
    }
    if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600);
      return `Hace ${hours} hora${hours > 1 ? 's' : ''}`;
    }
    if (diffInSeconds < 604800) {
      const days = Math.floor(diffInSeconds / 86400);
      return `Hace ${days} día${days > 1 ? 's' : ''}`;
    }
  }
  
  if (format === 'datetime') {
    return d.toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
  
  if (format === 'date') {
    return d.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }
  
  return d.toLocaleString();
}

/**
 * Valida direcciones de email
 * @param {string} email - Email a validar
 * @returns {boolean} - True si es válido
 */
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

/**
 * Valida URLs
 * @param {string} url - URL a validar
 * @returns {boolean} - True si es válida
 */
function validateURL(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

/**
 * Sanitiza texto para prevenir XSS
 * @param {string} text - Texto a sanitizar
 * @returns {string} - Texto sanitizado
 */
function sanitizeText(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Trunca texto a una longitud específica
 * @param {string} text - Texto a truncar
 * @param {number} length - Longitud máxima
 * @param {string} suffix - Sufijo a añadir
 * @returns {string} - Texto truncado
 */
function truncateText(text, length = 100, suffix = '...') {
  if (text.length <= length) return text;
  return text.substring(0, length - suffix.length) + suffix;
}

/**
 * Cuenta palabras en un texto
 * @param {string} text - Texto a analizar
 * @returns {number} - Número de palabras
 */
function countWords(text) {
  return text.trim().split(/\s+/).filter(word => word.length > 0).length;
}

/**
 * Cuenta caracteres en un texto
 * @param {string} text - Texto a analizar
 * @returns {number} - Número de caracteres
 */
function countCharacters(text) {
  return text.length;
}

/**
 * Calcula tiempo de lectura estimado
 * @param {string} text - Texto a analizar
 * @param {number} wpm - Palabras por minuto (por defecto 200)
 * @returns {number} - Minutos de lectura
 */
function calculateReadingTime(text, wpm = 200) {
  const words = countWords(text);
  const minutes = Math.ceil(words / wpm);
  return Math.max(1, minutes);
}

/**
 * Detecta el idioma del texto
 * @param {string} text - Texto a analizar
 * @returns {string} - Código de idioma detectado
 */
function detectLanguage(text) {
  // Implementación básica basada en caracteres comunes
  const spanishChars = /[áéíóúñü]/i;
  const englishChars = /[a-z]/i;
  
  const spanishCount = (text.match(spanishChars) || []).length;
  const englishCount = (text.match(englishChars) || []).length;
  
  if (spanishCount > englishCount * 0.1) return 'es';
  return 'en';
}

/**
 * Genera un ID único
 * @param {string} prefix - Prefijo opcional
 * @returns {string} - ID único
 */
function generateId(prefix = 'id') {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Copia texto al portapapeles
 * @param {string} text - Texto a copiar
 * @returns {Promise<boolean>} - True si se copió exitosamente
 */
async function copyToClipboard(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    } else {
      // Fallback para navegadores antiguos o contextos no seguros
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.top = '0';
      textArea.style.left = '0';
      textArea.style.position = 'fixed';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      return true;
    }
  } catch (error) {
    console.error('Error copiando al portapapeles:', error);
    return false;
  }
}

/**
 * Descarga contenido como archivo
 * @param {string} content - Contenido a descargar
 * @param {string} filename - Nombre del archivo
 * @param {string} mimeType - Tipo MIME
 */
function downloadAsFile(content, filename, mimeType = 'text/plain') {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Lee archivo como texto
 * @param {File} file - Archivo a leer
 * @returns {Promise<string>} - Contenido del archivo
 */
function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = e => resolve(e.target.result);
    reader.onerror = e => reject(e);
    reader.readAsText(file);
  });
}

/**
 * Comprime texto usando LZString (si está disponible)
 * @param {string} text - Texto a comprimir
 * @returns {string} - Texto comprimido
 */
function compressText(text) {
  if (typeof LZString !== 'undefined') {
    return LZString.compressToUTF16(text);
  }
  // Fallback simple
  return btoa(unescape(encodeURIComponent(text)));
}

/**
 * Descomprime texto
 * @param {string} compressed - Texto comprimido
 * @returns {string} - Texto original
 */
function decompressText(compressed) {
  if (typeof LZString !== 'undefined') {
    return LZString.decompressFromUTF16(compressed);
  }
  // Fallback simple
  return decodeURIComponent(escape(atob(compressed)));
}

/**
 * Formatea números con separadores
 * @param {number} num - Número a formatear
 * @returns {string} - Número formateado
 */
function formatNumber(num) {
  return new Intl.NumberFormat('es-ES').format(num);
}

/**
 * Formatea bytes a tamaño legible
 * @param {number} bytes - Bytes a formatear
 * @param {number} decimals - Decimales a mostrar
 * @returns {string} - Tamaño formateado
 */
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Valida JSON
 * @param {string} str - String a validar
 * @returns {boolean} - True si es JSON válido
 */
function isValidJSON(str) {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Mezcla array usando algoritmo Fisher-Yates
 * @param {Array} array - Array a mezclar
 * @returns {Array} - Array mezclado
 */
function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

/**
 * Agrupa elementos de un array
 * @param {Array} array - Array a agrupar
 * @param {Function} keyFn - Función para obtener la clave
 * @returns {Object} - Objeto agrupado
 */
function groupBy(array, keyFn) {
  return array.reduce((groups, item) => {
    const key = keyFn(item);
    (groups[key] = groups[key] || []).push(item);
    return groups;
  }, {});
}

/**
 * Espera un tiempo específico
 * @param {number} ms - Milisegundos a esperar
 * @returns {Promise} - Promise que se resuelve después del tiempo
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Ejecuta función con reintento en caso de error
 * @param {Function} fn - Función a ejecutar
 * @param {number} retries - Número de reintentos
 * @param {number} delay - Retraso entre reintentos
 * @returns {Promise} - Resultado de la función
 */
async function retry(fn, retries = 3, delay = 1000) {
  try {
    return await fn();
  } catch (error) {
    if (retries > 0) {
      await sleep(delay);
      return retry(fn, retries - 1, delay * 2);
    }
    throw error;
  }
}

/**
 * Detecta si el dispositivo es móvil
 * @returns {boolean} - True si es dispositivo móvil
 */
function isMobile() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

/**
 * Detecta si el navegador admite una característica
 * @param {string} feature - Característica a detectar
 * @returns {boolean} - True si está soportada
 */
function supportsFeature(feature) {
  switch (feature) {
    case 'clipboard':
      return navigator.clipboard !== undefined;
    case 'filesystem':
      return 'showOpenFilePicker' in window;
    case 'webp':
      const canvas = document.createElement('canvas');
      canvas.width = 1;
      canvas.height = 1;
      return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    default:
      return false;
  }
}

/**
 * Obtiene parámetros de URL
 * @returns {Object} - Parámetros de URL
 */
function getURLParams() {
  const params = {};
  const urlSearchParams = new URLSearchParams(window.location.search);
  for (const [key, value] of urlSearchParams) {
    params[key] = value;
  }
  return params;
}

/**
 * Actualiza parámetros de URL sin recargar la página
 * @param {Object} params - Parámetros a actualizar
 */
function updateURLParams(params) {
  const url = new URL(window.location);
  Object.entries(params).forEach(([key, value]) => {
    if (value === null || value === undefined) {
      url.searchParams.delete(key);
    } else {
      url.searchParams.set(key, value);
    }
  });
  window.history.replaceState({}, '', url);
}

/**
 * Crea elemento DOM con atributos
 * @param {string} tag - Tag del elemento
 * @param {Object} attributes - Atributos del elemento
 * @param {string} textContent - Contenido de texto
 * @returns {HTMLElement} - Elemento creado
 */
function createElement(tag, attributes = {}, textContent = '') {
  const element = document.createElement(tag);
  
  Object.entries(attributes).forEach(([key, value]) => {
    if (key === 'className') {
      element.className = value;
    } else if (key === 'dataset') {
      Object.entries(value).forEach(([dataKey, dataValue]) => {
        element.dataset[dataKey] = dataValue;
      });
    } else {
      element.setAttribute(key, value);
    }
  });
  
  if (textContent) {
    element.textContent = textContent;
  }
  
  return element;
}

/**
 * Muestra/oculta elemento con animación
 * @param {HTMLElement} element - Elemento a mostrar/ocultar
 * @param {boolean} show - True para mostrar, false para ocultar
 * @param {string} display - Valor display cuando se muestra
 */
function toggleElement(element, show, display = 'block') {
  if (show) {
    element.style.display = display;
    element.style.opacity = '0';
    element.style.transform = 'translateY(10px)';
    
    requestAnimationFrame(() => {
      element.style.transition = 'all 0.3s ease';
      element.style.opacity = '1';
      element.style.transform = 'translateY(0)';
    });
  } else {
    element.style.transition = 'all 0.3s ease';
    element.style.opacity = '0';
    element.style.transform = 'translateY(-10px)';
    
    setTimeout(() => {
      element.style.display = 'none';
    }, 300);
  }
}

/**
 * Logger simple para desarrollo
 */
const Logger = {
  log: (...args) => {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.log('[KusiPublisher]', ...args);
    }
  },
  
  warn: (...args) => {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.warn('[KusiPublisher]', ...args);
    }
  },
  
  error: (...args) => {
    console.error('[KusiPublisher]', ...args);
  },
  
  info: (...args) => {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.info('[KusiPublisher]', ...args);
    }
  }
};

// Hacer utilidades disponibles globalmente
window.KusiUtils = {
  debounce,
  throttle,
  formatDate,
  validateEmail,
  validateURL,
  sanitizeText,
  truncateText,
  countWords,
  countCharacters,
  calculateReadingTime,
  detectLanguage,
  generateId,
  copyToClipboard,
  downloadAsFile,
  readFileAsText,
  compressText,
  decompressText,
  formatNumber,
  formatBytes,
  isValidJSON,
  shuffleArray,
  groupBy,
  sleep,
  retry,
  isMobile,
  supportsFeature,
  getURLParams,
  updateURLParams,
  createElement,
  toggleElement,
  Logger
};

console.log('UtilsJS cargado correctamente');