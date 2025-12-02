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





console.log('DashboardJS cargado correctamente');