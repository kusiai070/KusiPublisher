/* ============================================================
   KUSIPUBLISHER - DASHBOARD.JS - Lógica del Dashboard Principal
   ============================================================ */

// Estado del dashboard
let dashboardState = {
  data: {
    metrics: {},
    recentActivity: [],
    quickActions: [
      {
        id: 'create',
        title: 'Create Content',
        description: 'Start creating new content',
        icon: '✨',
        link: 'editor.html'
      },
      {
        id: 'plan',
        title: 'Plan Campaign',
        description: 'Plan your content strategy',
        icon: '📋',
        link: '#'
      },
      {
        id: 'analytics',
        title: 'View Analytics',
        description: 'Check your performance',
        icon: '📊',
        link: '#'
      }
    ]
  },
  isLoading: false,
  lastUpdate: null
};

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
  initializeDashboard();
});

/**
 * Inicializa el dashboard
 */
function initializeDashboard() {
  console.log('Inicializando Dashboard...');
  
  // Renderizar acciones rápidas (estas no dependen de datos externos)
  renderQuickActions();
  
  // Configurar event listeners
  setupDashboardEventListeners();
  
  // Intentar cargar datos reales si el backend está disponible
  loadRealData();
  
  console.log('Dashboard inicializado correctamente');
}

/**
 * Configura event listeners del dashboard
 */
function setupDashboardEventListeners() {
  // Botones de acciones rápidas
  document.querySelectorAll('.quick-action-btn').forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const actionId = this.dataset.action;
      handleQuickAction(actionId);
    });
  });
  
  // Botones de actividad reciente (ver/editar)
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('activity-action-btn')) {
      e.preventDefault();
      const action = e.target.dataset.action;
      const activityId = e.target.dataset.activityId;
      handleActivityAction(action, activityId);
    }
  });
}

/**
 * Renderiza las métricas del dashboard
 */
function renderMetrics() {
  const metricsContainer = document.getElementById('metricsContainer');
  if (!metricsContainer) return;
  
  const { metrics } = dashboardState.data;
  
  const metricsHTML = `
    <div class="metric-card">
      <div class="metric-value">${metrics.totalContent}</div>
      <div class="metric-label">Total Content</div>
      <div class="metric-change positive">+${metrics.totalChange}%</div>
    </div>
    
    <div class="metric-card">
      <div class="metric-value">${metrics.publishedContent}</div>
      <div class="metric-label">Published</div>
      <div class="metric-change positive">+${metrics.publishedChange}%</div>
    </div>
    
    <div class="metric-card">
      <div class="metric-value">${metrics.averageScore}%</div>
      <div class="metric-label">Avg Score</div>
      <div class="metric-change positive">+${metrics.scoreChange}%</div>
    </div>
    
    <div class="metric-card">
      <div class="metric-value">${metrics.thisWeekContent}</div>
      <div class="metric-label">This Week</div>
      <div class="metric-change positive">+${metrics.weekChange}%</div>
    </div>
  `;
  
  metricsContainer.innerHTML = metricsHTML;
  
  // Añadir animaciones de entrada
  setTimeout(() => {
    document.querySelectorAll('.metric-card').forEach((card, index) => {
      setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, index * 100);
    });
  }, 100);
}

/**
 * Renderiza la actividad reciente
 */
function renderRecentActivity() {
  const activityContainer = document.getElementById('recentActivity');
  if (!activityContainer) return;
  
  const { recentActivity } = dashboardState.data;
  
  const activityHTML = recentActivity.map(activity => {
    const platform = PLATFORM_CONFIG[activity.platform];
    const timeAgo = formatTimeAgo(activity.timestamp);
    const statusClass = getStatusClass(activity.status);
    
    return `
      <div class="activity-item">
        <div class="activity-content">
          <div class="activity-title">
            ${platform.icon} ${activity.title}
          </div>
          <div class="activity-meta">
            ${timeAgo} • ${platform.name} • 
            <span class="status ${statusClass}">${activity.status}</span>
          </div>
        </div>
        <div class="activity-score" style="background-color: ${getScoreColor(activity.score)}">
          ${activity.score}
        </div>
        <div class="activity-actions">
          <button class="btn btn-secondary btn-sm activity-action-btn" 
                  data-action="view" data-activity-id="${activity.id}">
            View
          </button>
        </div>
      </div>
    `;
  }).join('');
  
  activityContainer.innerHTML = activityHTML;
}

/**
 * Renderiza las acciones rápidas
 */
function renderQuickActions() {
  const actionsContainer = document.getElementById('quickActions');
  if (!actionsContainer) return;
  
  const { quickActions } = dashboardState.data;
  
  const actionsHTML = quickActions.map(action => `
    <button class="btn btn-primary quick-action-btn" 
            data-action="${action.id}" 
            data-link="${action.link}">
      <span style="font-size: 24px; margin-right: 8px;">${action.icon}</span>
      <div>
        <div style="font-weight: 600;">${action.title}</div>
        <div style="font-size: 12px; opacity: 0.8;">${action.description}</div>
      </div>
    </button>
  `).join('');
  
  actionsContainer.innerHTML = actionsHTML;
}

/**
 * Maneja las acciones rápidas
 */
function handleQuickAction(actionId) {
  console.log('Quick action:', actionId);
  
  switch (actionId) {
    case 'create':
      window.location.href = 'editor.html';
      break;
      
    case 'plan':
      showToast('🚧 Función de planificación próximamente disponible', 'info');
      break;
      
    case 'analytics':
      showToast('📊 Analytics dashboard próximamente disponible', 'info');
      break;
      
    default:
      showToast('🔧 Función no implementada aún', 'warning');
  }
}

/**
 * Maneja acciones de actividad reciente
 */
function handleActivityAction(action, activityId) {
  console.log('Activity action:', action, activityId);
  
  const activity = dashboardState.data.recentActivity.find(a => a.id == activityId);
  if (!activity) return;
  
  switch (action) {
    case 'view':
      // Abrir modal o redirigir a vista detallada
      showActivityModal(activity);
      break;
      
    case 'edit':
      // Redirigir al editor con el contenido
      window.location.href = `editor.html?edit=${activityId}`;
      break;
      
    case 'duplicate':
      // Crear copia en el editor
      showToast('📝 Contenido duplicado en el editor', 'success');
      // Redirigir al editor
      setTimeout(() => {
        window.location.href = 'editor.html';
      }, 1000);
      break;
      
    default:
      showToast('🔧 Acción no implementada', 'warning');
  }
}

/**
 * Muestra modal con detalles de actividad
 */
function showActivityModal(activity) {
  const platform = PLATFORM_CONFIG[activity.platform];
  const modal = document.createElement('div');
  modal.className = 'modal-overlay';
  modal.innerHTML = `
    <div class="modal-content">
      <div class="modal-header">
        <h3>${platform.icon} ${activity.title}</h3>
        <button class="modal-close">&times;</button>
      </div>
      <div class="modal-body">
        <div class="activity-detail">
          <p><strong>Platform:</strong> ${platform.name}</p>
          <p><strong>Status:</strong> ${activity.status}</p>
          <p><strong>Score:</strong> ${activity.score}/100</p>
          <p><strong>Created:</strong> ${new Date(activity.timestamp).toLocaleString()}</p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-primary activity-action-btn" 
                  data-action="edit" data-activity-id="${activity.id}">
            Editar
          </button>
          <button class="btn btn-secondary activity-action-btn" 
                  data-action="duplicate" data-activity-id="${activity.id}">
            Duplicar
          </button>
        </div>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  // Event listeners del modal
  modal.querySelector('.modal-close').addEventListener('click', () => {
    document.body.removeChild(modal);
  });
  
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      document.body.removeChild(modal);
    }
  });
  
  // Animar entrada
  setTimeout(() => modal.classList.add('show'), 10);
}

/**
 * Intenta cargar datos reales del backend
 */
async function loadRealData() {
  console.log('DEBUG: loadRealData intentando usar window.KusiAPI:', window.KusiAPI);
  if (dashboardState.isLoading) return;

  dashboardState.isLoading = true;
  console.log('Cargando datos reales del dashboard...');
  showToast('🔄 Cargando datos del dashboard...', 'info');

  try {
    // Verificar si el backend está disponible
    const health = await window.KusiAPI.checkHealth();
    
    if (health && health.status === 'healthy') {
      console.log('Backend disponible, cargando datos reales...');
      
      // Cargar métricas
      const metricsSummary = await window.KusiAPI.getMetricsSummary();
      console.log('Métricas recibidas:', metricsSummary);

      // Mapear métricas del backend a la estructura del frontend
      dashboardState.data.metrics = {
        totalContent: metricsSummary.total_content,
        totalChange: parseInt(metricsSummary.total_content_change.replace('%', '')),
        publishedContent: metricsSummary.published_content,
        publishedChange: parseInt(metricsSummary.published_content_change.replace('%', '')),
        averageScore: metricsSummary.average_quality_score,
        scoreChange: metricsSummary.average_quality_score_change, // Usar el cambio real
        thisWeekContent: metricsSummary.content_this_week,
        weekChange: metricsSummary.content_this_week_change // Usar el cambio real
      };
      renderMetrics(); // Renderizar métricas después de cargar datos reales

      // Cargar actividad reciente
      const recentContent = await window.KusiAPI.getRecentContent();
      console.log('Actividad reciente recibida:', recentContent);
      // Asumiendo que recentContent es un array de objetos con la estructura deseada
      dashboardState.data.recentActivity = recentContent;
      renderRecentActivity(); // Renderizar actividad después de cargar datos reales
      
      dashboardState.lastUpdate = new Date().toISOString();
      showToast('✅ Datos del dashboard sincronizados con el backend', 'success');
    } else {
      console.warn('Backend no disponible, usando datos locales.');
      showToast('⚠️ Backend no disponible. Usando datos locales.', 'warning');
    }
  } catch (error) {
    console.error('❌ Error cargando datos reales del dashboard:', error);
    showToast('❌ Error al cargar datos del dashboard. Usando datos locales.', 'error');
  } finally {
    dashboardState.isLoading = false;
  }
}

/**
 * Formatea tiempo relativo (hace X minutos/horas/días)
 */
function formatTimeAgo(timestamp) {
  const now = new Date();
  const time = new Date(timestamp);
  const diffInSeconds = Math.floor((now - time) / 1000);
  
  if (diffInSeconds < 60) {
    return 'Ahora mismo';
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `Hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `Hace ${hours} hora${hours > 1 ? 's' : ''}`;
  } else {
    const days = Math.floor(diffInSeconds / 86400);
    return `Hace ${days} día${days > 1 ? 's' : ''}`;
  }
}

/**
 * Obtiene clase CSS según el estado del contenido
 */
function getStatusClass(status) {
  switch (status) {
    case 'published': return 'published';
    case 'draft': return 'draft';
    case 'scheduled': return 'scheduled';
    default: return '';
  }
}

/**
 * Obtiene color según el score
 */
function getScoreColor(score) {
  if (score >= 85) return 'var(--success)';
  if (score >= 70) return 'var(--primary)';
  if (score >= 50) return 'var(--warning)';
  return 'var(--danger)';
}

/**
 * Muestra notificaciones toast
 */
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = message;
  
  document.body.appendChild(toast);
  
  setTimeout(() => toast.classList.add('show'), 100);
  
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 3000);
}

// CSS adicional para el dashboard
const dashboardStyles = `
<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modal-overlay.show {
  opacity: 1;
}

.modal-content {
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  transform: scale(0.9);
  transition: transform 0.3s ease;
}

.modal-overlay.show .modal-content {
  transform: scale(1);
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--card-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
}

.modal-close {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

.modal-body {
  padding: 24px;
}

.modal-actions {
  margin-top: 24px;
  display: flex;
  gap: 12px;
}

.status {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
}

.status.published {
  background: rgba(16, 185, 129, 0.2);
  color: var(--success);
}

.status.draft {
  background: rgba(245, 158, 11, 0.2);
  color: var(--warning);
}

.status.scheduled {
  background: rgba(124, 104, 238, 0.2);
  color: var(--accent);
}

.metric-card {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s ease;
}

.activity-item {
  opacity: 0;
  transform: translateX(-20px);
  animation: slideIn 0.3s ease forwards;
}

.activity-item:nth-child(1) { animation-delay: 0.1s; }
.activity-item:nth-child(2) { animation-delay: 0.2s; }
.activity-item:nth-child(3) { animation-delay: 0.3s; }
.activity-item:nth-child(4) { animation-delay: 0.4s; }
.activity-item:nth-child(5) { animation-delay: 0.5s; }

@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
`;

// Agregar estilos al documento
if (!document.getElementById('dashboard-styles')) {
  const styleElement = document.createElement('div');
  styleElement.id = 'dashboard-styles';
  styleElement.innerHTML = dashboardStyles;
  document.head.appendChild(styleElement);
}

console.log('DashboardJS cargado correctamente');